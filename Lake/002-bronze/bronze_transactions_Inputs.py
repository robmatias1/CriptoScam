# Databricks notebook source
# MAGIC %md
# MAGIC Ingestão da tabela transactions na camada bronze

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# COMMAND ----------

blob_folder = "dbfs:/mnt/criptoscamstorage/landing/walletexplorer/*_transactions.csv"

# Lendo arquivos 
df = spark.read.csv(blob_folder, header=True, inferSchema=True)

if not spark.catalog.tableExists("bronze.transactions"):
    # Salve o DataFrame como uma tabela Delta Lake
    df.write.format("delta")\
            .mode("append")\
            .option("path","dbfs:/mnt/criptoscamstorage/bronze/")\
            .saveAsTable('bronze.transactions')
else:
    df.createOrReplaceTempView("vw_transaction")
    spark.sql(f"""MERGE INTO bronze.transactions AS tr
                  USING vw_transaction AS vw ON vw.transaction=tr.transaction
                  WHEN NOT MATCHED AND NOT ISNULL(vw.transaction) THEN
                  INSERT *"""
             )
    

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bronze.transactions
