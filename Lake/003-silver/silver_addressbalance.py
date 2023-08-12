# Databricks notebook source
# MAGIC %md
# MAGIC #Ingestão da tabela address balance na camada silver

# COMMAND ----------

# DBTITLE 1,Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import date


# COMMAND ----------

# DBTITLE 1,Ingestão silver

df = spark.table("bronze.addressbalance")\
          .withColumn("saldo_atual",col("final_balance")/100000000)\
          .withColumn("total_recebido",col("total_received")/100000000)\
          .withColumn("total_enviado",col("total_sent")/100000000)\
          .select(
                  col("address").alias("endereco"),
                  col("saldo_atual").cast('float'),
                  col("total_recebido").cast('float'),
                  col("total_enviado").cast('float'),
                  col("data_carga"))

if not spark.catalog.tableExists("silver.addressbalance"):
    # Salve o DataFrame como uma tabela Delta Lake
    df.write.format("delta")\
            .mode("append")\
            .partitionBy("data_carga")\
            .option("path","dbfs:/mnt/criptoscamstorage/silver/addressbalance/")\
            .saveAsTable('silver.addressbalance')
else:
    df.createOrReplaceTempView("vw_addressbalance")
    spark.sql(f"""MERGE INTO silver.addressbalance AS tr
                  USING vw_addressbalance AS vw ON vw.data_carga=tr.data_carga
                  WHEN NOT MATCHED THEN
                  INSERT *"""
             )
    
    
