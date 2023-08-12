# Databricks notebook source
# MAGIC %md
# MAGIC #Ingestão da tabela transaction by address na camada silver

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# COMMAND ----------


df = spark.table("bronze.transactionbyaddress")\
          .filter(col("date") != 'Element')\
          .withColumn("tipo_transacao",when(substring(col("received/sent"),1,1)=='+','Recebida')\
                                      .when(substring(col("received/sent"),1,1)=='-','Enviada'))\
          .withColumn("dh_transacao",to_timestamp("date", "yyyy-MM-dd HH:mm:ss"))\
          .withColumn("dt_transacao",to_date("date", "yyyy-MM-dd HH:mm:ss"))\
          .select(col("dh_transacao"),
                  col("dt_transacao"),
                  col("transaction").alias("id_transacao"),
                  col("address").alias("endereco_transacao"),
                  col("tipo_transacao"),
                  col("received/sent").cast('float').alias("valor_transacao"),
                  col("balance").cast('float').alias("saldo"),
                  col("data_carga"))

if not spark.catalog.tableExists("silver.transactionbyaddress"):
    # Salve o DataFrame como uma tabela Delta Lake
    df.write.format("delta")\
            .mode("append")\
            .partitionBy("data_carga")\
            .option("path","dbfs:/mnt/criptoscamstorage/silver/transactionbyaddress/")\
            .saveAsTable('silver.transactionbyaddress')
else:
    df.createOrReplaceTempView("vw_transactionbyaddress")
    spark.sql(f"""MERGE INTO silver.transactionbyaddress AS tr
                  USING vw_transactionbyaddress AS vw ON vw.data_carga=tr.data_carga
                  WHEN NOT MATCHED THEN
                  INSERT *"""
             )
    
