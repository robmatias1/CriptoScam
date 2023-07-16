# Databricks notebook source
# Importe as bibliotecas necessárias
from pyspark.sql import SparkSession

# Crie uma sessão do Spark
spark = SparkSession.builder \
    .appName("Exemplo de Leitura de Arquivo Delta Lake") \
    .getOrCreate()

# Leia o arquivo Delta Lake
df = spark.read.json("dbfs:/mnt/criptoscamstorage/landing/output-onlineyamltools.json")

# Mostre o DataFrame
df.display()



# COMMAND ----------

# MAGIC %fs
# MAGIC
# MAGIC ls mnt/
