# Databricks notebook source
# MAGIC %md
# MAGIC Ingestão da tabela transactions na camada bronze

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# COMMAND ----------

blob_folder = "dbfs:/mnt/criptoscamstorage/landing/walletexplorer/*_transact_inputs.csv"

# Leia os arquivos CSVs na pasta e armazene-os em um DataFrame
df = spark.read.csv(blob_folder, header=True, inferSchema=True)

df = df.withColumn("data_carga", current_date())


# Salve o DataFrame como uma tabela Delta Lake
df.write.format("delta")\
        .mode("append")\
        .partitionBy('data_carga')\
        .saveAsTable('bronze.transactions_inputs')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bronze.transactions_inputs
