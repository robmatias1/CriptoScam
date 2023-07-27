# Databricks notebook source
# MAGIC %md
# MAGIC Ingestão da tabela transaction detail na camada bronze

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# COMMAND ----------

blob_folder = "dbfs:/mnt/criptoscamstorage/landing/walletexplorer/*transaction.json"

# Lendo arquivos 
df = spark.read.json(blob_folder)

if not spark.catalog.tableExists("bronze.transactiondetail"):
    # Salve o DataFrame como uma tabela Delta Lake
    df.write.format("delta")\
            .mode("append")\
            .option("path","dbfs:/mnt/criptoscamstorage/bronze/transactiondetail/")\
            .saveAsTable('bronze.transactiondetail')
else:
    df.createOrReplaceTempView("vw_transactiondetail")
    spark.sql(f"""MERGE INTO bronze.transactiondetail AS tr
                  USING vw_transactiondetail AS vw ON vw.hash=tr.hash
                  WHEN NOT MATCHED AND NOT ISNULL(vw.hash) THEN
                  INSERT *"""
             )
    

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bronze.transactiondetail
