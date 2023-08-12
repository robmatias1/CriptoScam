# Databricks notebook source
# MAGIC %md
# MAGIC #Ingestão da tabela transaction by address na camada bronze

# COMMAND ----------

# DBTITLE 1,Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import date


# COMMAND ----------

# DBTITLE 1,Ingestão bronze
blob_folder = "dbfs:/mnt/criptoscamstorage/landing/walletexplorer/*_transactions.csv"
data_atual = date.today()

df = spark.read.csv(blob_folder, header=True, inferSchema=True)

df = df.withColumn("data_carga",lit(data_atual))

if not spark.catalog.tableExists("bronze.transactionbyaddress"):

    df.write.format("delta")\
            .mode("append")\
            .partitionBy("data_carga")\
            .option("path","dbfs:/mnt/criptoscamstorage/bronze/transactionbyaddress/")\
            .saveAsTable('bronze.transactionbyaddress')
else:
    df.createOrReplaceTempView("vw_transactionbyaddress")
    spark.sql(f"""MERGE INTO bronze.transactionbyaddress AS tr
                  USING vw_transactionbyaddress AS vw ON vw.transaction=tr.transaction
                  WHEN NOT MATCHED AND NOT ISNULL(vw.transaction) THEN
                  INSERT *"""
             )
    
