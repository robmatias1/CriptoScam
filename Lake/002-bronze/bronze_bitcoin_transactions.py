# Databricks notebook source
from pyspark.sql import SparkSession



blob_folder_path = "dbfs:/mnt/criptoscamstorage/landing/walletexplorer/14fwd64XGE3HgHCknbLVuqWBkL1Lfa1KCw_transactions.csv"

# Leia os arquivos CSVs na pasta e armazene-os em um DataFrame
df = spark.read.csv(blob_folder_path, header=True, inferSchema=True)

# Exiba o DataFrame
df.show()

delta_table_path = "dbfs:/mnt/criptoscamstorage/bronze/transactions/transactions"

# Salve o DataFrame como uma tabela Delta Lake
df.write.format("delta").mode("overwrite").saveAsTable('bronze.transactions')


# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE bronze
