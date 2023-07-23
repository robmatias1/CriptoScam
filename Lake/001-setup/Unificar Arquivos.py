# Databricks notebook source
import pandas as pd
from glob import glob

# COMMAND ----------

arquivos = sorted(glob(r'dbfs:/mnt/criptoscamstorage/walletexplorer/*_transactions.csv'))

# COMMAND ----------

arquivos
