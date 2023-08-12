-- Databricks notebook source
create OR REPLACE TEMP VIEW vw_graph as 
select distinct
       endereco_input     as ID,
       endereco_input     as ID_PAI,
       '#0000FF'          as COR_ORIGEM,
       '#FF0000'          as COR_DO_NO,
       'Nivel 1'          as NIVEL,
       tx_index_transacao
from silver.transactiondetailinput 
where endereco_input in (
select distinct endereco_fraude
from silver.addresfraudreport) 

-- COMMAND ----------

create OR REPLACE TEMP VIEW vw_graph2 as 
select distinct
       output.endereco_out AS ID,
       graph.ID            AS ID_PAI,
       '#060A5F'           as COR_ORIGEM,
       '#5F090A'           as COR_DO_NO,
       'Nivel 2'           as NIVEL,
       output.tx_index_transacao_posterior as tx_index_transacao
from silver.transactiondetailoutput output
inner join vw_graph as graph on output.tx_index_transacao =graph.tx_index_transacao


-- COMMAND ----------

create OR REPLACE TEMP VIEW vw_graph3 as 
select distinct
       output.endereco_out AS ID,
       graph.ID            AS ID_PAI,
       '#1B5F0D'           as COR_ORIGEM,
       '#5F5118'           as COR_DO_NO,
       'Nivel 3'           as NIVEL,
       output.tx_index_transacao_posterior as tx_index_transacao
from silver.transactiondetailoutput output
inner join vw_graph2 as graph on output.tx_index_transacao =graph.tx_index_transacao

-- COMMAND ----------

create OR REPLACE TEMP VIEW vw_graph4 as 
select distinct
       output.endereco_out AS ID,
       graph.ID            AS ID_PAI,
       '#1B5F0D'           as COR_ORIGEM,
       '#5F5118'           as COR_DO_NO,
       'Nivel 4'           as NIVEL,
       output.tx_index_transacao_posterior as tx_index_transacao
from silver.transactiondetailoutput output
inner join vw_graph3 as graph on output.tx_index_transacao =graph.tx_index_transacao

-- COMMAND ----------

create or replace table gold.graph as
select * 
from vw_graph union
select * 
from vw_graph2 union
select * 
from vw_graph3 union
select * 
from vw_graph4
