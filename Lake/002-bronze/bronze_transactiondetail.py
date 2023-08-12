# Databricks notebook source
# MAGIC %md
# MAGIC #Ingestão da tabela transaction detail na camada bronze

# COMMAND ----------

# DBTITLE 1,Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import date


# COMMAND ----------

# DBTITLE 1,Ingestão bronze
blob_folder = "dbfs:/mnt/criptoscamstorage/landing/walletexplorer/*transaction.json"
data_atual = date.today()

df = spark.read.json(blob_folder)

df = df.withColumn("data_carga",lit(data_atual))

if not spark.catalog.tableExists("bronze.transactiondetail"):

    df.write.format("delta")\
            .mode("append")\
            .partitionBy("data_carga")\
            .option("path","dbfs:/mnt/criptoscamstorage/bronze/transactiondetail/")\
            .saveAsTable('bronze.transactiondetail')
else:
    df.createOrReplaceTempView("vw_transactiondetail")
    spark.sql(f"""MERGE INTO bronze.transactiondetail AS tr
                  USING vw_transactiondetail AS vw ON vw.hash=tr.hash
                  WHEN NOT MATCHED AND NOT ISNULL(vw.hash) THEN
                  INSERT *"""
             )
    
