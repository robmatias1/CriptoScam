# Databricks notebook source
# MAGIC %md
# MAGIC CONEXÃO COM ADLS
# MAGIC

# COMMAND ----------

# DBTITLE 1,variaveis de conexão
storage_account_name ="criptoscamstorage"
client_id = "b78e3824-a8b9-4729-816f-7bd3e72edf23"
tenant_id = "ba61204e-44c0-42e4-b4fc-790645eef591"
client_secret = "o6U8Q~ntLcfEQ-7qOSgpKa4KykFOUBBUNXcX7blV"


# COMMAND ----------

# DBTITLE 1,variavel de configuração
config = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type":"org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id":f"{client_id}",
          "fs.azure.account.oauth2.client.secret":f"{client_secret}",
          "fs.azure.account.oauth2.client.endpoint":f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
}

# COMMAND ----------

def mount(container):
    dbutils.fs.mount(
        source = f"abfss://{container}@{storage_account_name}.dfs.core.windows.net/",
        mount_point = f"/mnt/{storage_account_name}/{container}",
        extra_configs = config
    )

# COMMAND ----------

mount("landing")
mount("bronze")
mount("silver")
mount("gold")

# COMMAND ----------


dbutils.fs.ls("mnt/criptoscamstorage/landing") 

# COMMAND ----------


