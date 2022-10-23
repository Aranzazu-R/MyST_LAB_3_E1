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
import functions as fn
from datetime import datetime, date, timedelta

k=100000

## Importacion de datos
mtf=fn.f_leer_archivo('files/MyST_LAB2_FMHL.xlsx','Historico MT5')
mtm=fn.f_leer_archivo('files/MyST_LAB2_MMM.xlsx','Historico MT5')
mtp=fn.f_leer_archivo('files/MyST_LAB2_PHMC.xlsx','Historico MT5')
mta=fn.f_leer_archivo('files/MyST_LAB2_ARG.xlsx','Historico MT5')

## Benchmark
end_f=pd.to_datetime(mtf.iloc[-1,0])+timedelta(days=1)
benchmark_f=fn.get_adj_closes(tickers='SPY',start_date=pd.to_datetime(mtf.iloc[0,0]).strftime('%Y-%m-%d'),end_date=end_f.strftime('%Y-%m-%d'))
end_m=pd.to_datetime(mtm.iloc[-1,0])+timedelta(days=1)
benchmark_m=fn.get_adj_closes(tickers='SPY',start_date=pd.to_datetime(mtm.iloc[0,0]).strftime('%Y-%m-%d'),end_date=end_m.strftime('%Y-%m-%d'))
end_p=pd.to_datetime(mtm.iloc[-1,0])+timedelta(days=1)
benchmark_p=fn.get_adj_closes(tickers='SPY',start_date=pd.to_datetime(mtp.iloc[0,0]).strftime('%Y-%m-%d'),end_date=end_p.strftime('%Y-%m-%d'))
end_a=pd.to_datetime(mtm.iloc[-1,0])+timedelta(days=1)
benchmark_a=fn.get_adj_closes(tickers='SPY',start_date=pd.to_datetime(mta.iloc[0,0]).strftime('%Y-%m-%d'),end_date=end_a.strftime('%Y-%m-%d'))


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

data_pips0 = pd.read_csv("files/instruments_pips.csv")
data_pips = data_pips0.set_index("Instrument")
