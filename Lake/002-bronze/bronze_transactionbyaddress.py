# Databricks notebook source
# MAGIC %md
# MAGIC Ingestão da tabela transaction by address na camada bronze

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# COMMAND ----------

blob_folder = "dbfs:/mnt/criptoscamstorage/landing/walletexplorer/*_transactions.csv"

# Lendo arquivos 
df = spark.read.csv(blob_folder, header=True, inferSchema=True)
# df.withColumnRenamed("Column1","address")\
#     .withColumnRenamed("Column2","send")\
#         .withColumnRenamed("Column3","txid_ant").display()
if not spark.catalog.tableExists("bronze.transactionbyaddress"):
    # Salve o DataFrame como uma tabela Delta Lake
    df.write.format("delta")\
            .mode("append")\
            .option("path","dbfs:/mnt/criptoscamstorage/bronze/transactionbyaddress/")\
            .saveAsTable('bronze.transactionbyaddress')
else:
    df.createOrReplaceTempView("vw_transactionbyaddress")
    spark.sql(f"""MERGE INTO bronze.transactionbyaddress AS tr
                  USING vw_transactionbyaddress AS vw ON vw.txid=tr.txid
                  WHEN NOT MATCHED AND NOT ISNULL(vw.txid) THEN
                  INSERT *"""
             )
    

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bronze.transactionbyaddress
