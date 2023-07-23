# Databricks notebook source
from pyspark.sql import SparkSession



# COMMAND ----------

blob_folder_path = "dbfs:/mnt/criptoscamstorage/landing/walletexplorer/*_transactions.csv"

# Leia os arquivos CSVs na pasta e armazene-os em um DataFrame
df = spark.read.csv(blob_folder_path, header=True, inferSchema=True)

# Exiba o DataFrame
df.show()

delta_table_path = "dbfs:/mnt/criptoscamstorage/bronze/transactions/transactions"

# Salve o DataFrame como uma tabela Delta Lake
df.write.format("delta").mode("overwrite").saveAsTable('bronze.transactions')
