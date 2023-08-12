# Databricks notebook source
# MAGIC %md
# MAGIC #Ingestão das tabelas transactiondetail,transactiondetailinput e transactiondetailoutput na camada silver

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# COMMAND ----------

df = spark.table("bronze.transactiondetail")\
          .withColumn("fee",col("fee")/100000000)\
          .select(col("fee").cast('float'),
                  col("block_height"),
                  col("block_index"),
                  col("double_spend").cast('float'),
                  col("hash").alias("id_transacao"),
                  col("lock_time"),
                  col("relayed_by"),
                  col("size").cast('int').alias("tamanho"),
                  col("time"),
                  col("tx_index").alias("tx_index_transacao"),
                  col("ver").cast('int').alias("versao"),
                  col("vin_sz").cast('int').alias("nr_enderecos_in"),
                  col("vout_sz").cast('int').alias("nr_enderecos_out"),
                  col("weight"),
                  col("data_carga"))
          
if not spark.catalog.tableExists("silver.transactiondetail"):
    # Salve o DataFrame como uma tabela Delta Lake
    df.write.format("delta")\
            .mode("append")\
            .partitionBy("data_carga")\
            .option("path","dbfs:/mnt/criptoscamstorage/silver/transactiondetail/")\
            .saveAsTable('silver.transactiondetail')
else:
    df.createOrReplaceTempView("vw_transactiondetail")
    spark.sql(f"""MERGE INTO silver.transactiondetail AS tr
                  USING vw_transactiondetail AS vw ON vw.id_transacao=tr.id_transacao
                  WHEN NOT MATCHED THEN
                  INSERT *"""
             )



# COMMAND ----------

# DBTITLE 1,Inputs da transação

df = spark.table("bronze.transactiondetail")\
          .withColumn("input",explode("inputs") )\
          .withColumn("valor",col("input").getItem('prev_out').getField('value')/100000000 )\
          .select(col("hash").alias("id_transacao"),
                  col("input").getItem('prev_out').getField('spent').alias("spent"),
                  col("input").getItem('prev_out').getField('addr').alias("endereco_input"),
                  col("valor").cast("float").alias("valor_input"),
                  col("input").getItem('prev_out').getField('tx_index').alias("tx_index_transacao_anterior"),
                  col("input").getItem('prev_out').getItem('spending_outpoints').getField('tx_index')[0].alias("tx_index_transacao"),
                  col("data_carga")
                  )
if not spark.catalog.tableExists("silver.transactiondetailinput"):
    # Salve o DataFrame como uma tabela Delta Lake
    df.write.format("delta")\
            .mode("append")\
            .partitionBy("data_carga")\
            .option("path","dbfs:/mnt/criptoscamstorage/silver/transactiondetailinput/")\
            .saveAsTable('silver.transactiondetailinput')
else:
    df.createOrReplaceTempView("vw_transactiondetailinput")
    spark.sql(f"""MERGE INTO silver.transactiondetailinput AS tr
                  USING vw_transactiondetailinput AS vw ON vw.id_transacao=tr.id_transacao
                  WHEN NOT MATCHED THEN
                  INSERT *"""
             )
    

# COMMAND ----------


df = spark.table("bronze.transactiondetail")\
          .withColumn("out",explode("out") )\
          .withColumn("valor",col("out").getField('value')/100000000 )\
          .select(col("hash").alias("id_transacao"),
                  col("out").getField('spent').alias("spent"),
                  col("out").getField('addr').alias("endereco_out"),
                  col("valor").cast("float").alias("valor_out"),
                  col("out").getField('tx_index').alias("tx_index_transacao"),
                  col("out").getItem('spending_outpoints').getField('tx_index')[0].alias("tx_index_transacao_posterior"),
                  col("data_carga")
                  )
if not spark.catalog.tableExists("silver.transactiondetailoutput"):
    # Salve o DataFrame como uma tabela Delta Lake
    df.write.format("delta")\
            .mode("append")\
            .partitionBy("data_carga")\
            .option("path","dbfs:/mnt/criptoscamstorage/silver/transactiondetailoutput/")\
            .saveAsTable('silver.transactiondetailoutput')
else:
    df.createOrReplaceTempView("vw_transactiondetailoutput")
    spark.sql(f"""MERGE INTO silver.transactiondetailoutput AS tr
                  USING vw_transactiondetailoutput AS vw ON vw.id_transacao=tr.id_transacao
                  WHEN NOT MATCHED THEN
                  INSERT *"""
             )
    
