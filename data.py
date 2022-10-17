"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 3. Behavioral Finance                                                          -- #
# -- script: functions.py : python script for data collection                                            -- #
# -- author: FridaHernandezL                                                                             -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/FridaHernandezL/MyST_LAB_3_E1                                        -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import statistics as st
pd.options.mode.chained_assignment = None  # default='warn'
import yfinance as yf
from datetime import datetime, date, timedelta
import MetaTrader5 as mt5
import pytz
import functions as fn

k=100000

## Importacion de datos
mtf=fn.f_leer_archivo('MyST_LAB2_FMHL.xlsx','Historico MT5')
mtm=fn.f_leer_archivo('MyST_LAB2_MMM.xlsx','Historico MT5')
mtp=fn.f_leer_archivo('MyST_LAB2_PHMC.xlsx','Historico MT5')
mta=fn.f_leer_archivo('MyST_LAB2_ARG.xlsx','Historico MT5')

#data for import closes
end_f=pd.to_datetime(mtf.iloc[-1,0])+timedelta(days=1)
end_m=pd.to_datetime(mtm.iloc[-1,0])+timedelta(days=1)
end_p=pd.to_datetime(mtp.iloc[-1,0])+timedelta(days=1)
end_a=pd.to_datetime(mta.iloc[-1,0])+timedelta(days=1)

#fn.f_be_de(mtf).to_csv(r"rates_f.csv")
#fn.f_be_de(mtm).to_csv(r"rates_m.csv")
#fn.f_be_de(mtp).to_csv(r"rates_p.csv")
#fn.f_be_de(mta).to_csv(r"rates_a.csv")

rates_f=pd.read_csv('rates_f.csv')
rates_m=pd.read_csv('rates_m.csv')
rates_p=pd.read_csv('rates_p.csv')
rates_a=pd.read_csv('rates_a.csv')