# Databricks notebook source


# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# COMMAND ----------

blob_folder = "dbfs:/mnt/criptoscamstorage/landing/walletexplorer/*_transactions.csv"

# Leia os arquivos CSVs na pasta e armazene-os em um DataFrame
df = spark.read.csv(blob_folder, header=True, inferSchema=True)

df = df.withColumn("data_carga", current_date())

df_with_timestamp.display()
# Salve o DataFrame como uma tabela Delta Lake
df.write.format("delta")\
        .mode("append")\
        .partitionBy('data_carga')\
        .saveAsTable('bronze.transactions')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bronze.transactions
