# Databricks notebook source
# MAGIC %md
# MAGIC #Ingestão das tabelas transactiondetail,transactiondetailinput e transactiondetailoutput na camada silver

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# COMMAND ----------

# DBTITLE 1,Inputs da transação

df = spark.table("bronze.addresfraudreport")\
          .withColumn("add",explode("addresses") )\
          .select(col("id").alias("id_fraud_report"),
                  col("add").getField('address').alias("endereco_fraude"),
                  col("add").getField('chain').alias("moeda"),
                  col("add").getField('domain').alias("dominio"),
                  col("checked").alias("checado"),
                  col("createdAt").alias("data_report"),
                  col("scamCategory").alias("categoria"),
                  col("trusted").alias("validado"),
                  col("data_carga")
                  )
if not spark.catalog.tableExists("silver.addresfraudreport"):
    # Salve o DataFrame como uma tabela Delta Lake
    df.write.format("delta")\
            .mode("append")\
            .partitionBy("data_carga")\
            .option("path","dbfs:/mnt/criptoscamstorage/silver/addresfraudreport/")\
            .saveAsTable('silver.addresfraudreport')
else:
    df.createOrReplaceTempView("vw_addresfraudreport")
    spark.sql(f"""MERGE INTO silver.addresfraudreport AS tr
                  USING vw_addresfraudreport AS vw ON vw.id_fraud_report=tr.id_fraud_report
                  WHEN NOT MATCHED THEN
                  INSERT *"""
             )
    
