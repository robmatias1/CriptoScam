# Databricks notebook source
# MAGIC %md
# MAGIC #Ingestão da tabela address_fraud_report na camada bronze

# COMMAND ----------

# DBTITLE 1,Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import date


# COMMAND ----------

# DBTITLE 1,Ingestão bronze
blob_folder = "dbfs:/mnt/criptoscamstorage/landing/chainabuse/*_report.json"
data_atual = date.today()

df = spark.read.json(blob_folder)

df = df.withColumn("data_carga",lit(data_atual))

if not spark.catalog.tableExists("bronze.addresfraudreport"):

    df.write.format("delta")\
            .mode("append")\
            .partitionBy("data_carga")\
            .option("path","dbfs:/mnt/criptoscamstorage/bronze/addresfraudreport/")\
            .saveAsTable('bronze.addresfraudreport')
else:
    df.createOrReplaceTempView("vw_addresfraudreport")
    spark.sql(f"""MERGE INTO bronze.addresfraudreport AS tr
                  USING vw_addresfraudreport AS vw ON vw.id=tr.id
                  WHEN NOT MATCHED AND NOT ISNULL(vw.id) THEN
                  INSERT *"""
             )
    
