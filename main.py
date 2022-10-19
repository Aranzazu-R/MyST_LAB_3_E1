"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 3. Behavioral Finance                                                          -- #
# -- script: main.py : python script for main code                                           -- #
# -- author: FridaHernandezL                                                                             -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/FridaHernandezL/MyST_LAB_3_E1                                        -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
import functions as fn
import data as dta
from visualizations import grafica_1, grafica_2

# Estadistica descriptiva

## time change
tcf=fn.f_columnas_tiempos(dta.mtf)
tcm=fn.f_columnas_tiempos(dta.mtm)
tcp=fn.f_columnas_tiempos(dta.mtp)
tca=fn.f_columnas_tiempos(dta.mta)

## pips
pf=fn.f_columnas_pips(dta.mtf)
pm=fn.f_columnas_pips(dta.mtm)
pp=fn.f_columnas_pips(dta.mtp)
pa=fn.f_columnas_pips(dta.mta)

## estadisticas_tabla
e_bat_f=fn.f_estadisticas_ba(dta.mtf,'tabla')
e_bat_m=fn.f_estadisticas_ba(dta.mtm,'tabla')
e_bat_p=fn.f_estadisticas_ba(dta.mtp,'tabla')
e_bat_a=fn.f_estadisticas_ba(dta.mta,'tabla')

## estadisticas_ranking
e_bar_f=fn.f_estadisticas_ba(dta.mtf,'ranking').head()
e_bar_m=fn.f_estadisticas_ba(dta.mtm,'ranking').head()
e_bar_p=fn.f_estadisticas_ba(dta.mtp,'ranking').head()
e_bar_a=fn.f_estadisticas_ba(dta.mta,'ranking').head()


# Metricas de Atribucion al desempeño
k=dta.k
evcap_f=fn.f_evolucion_capital(dta.mtf)
evcap_m=fn.f_evolucion_capital(dta.mtm)
evcap_p=fn.f_evolucion_capital(dta.mtp)
evcap_a=fn.f_evolucion_capital(dta.mta)

## SPY closes
benchmark_f=fn.get_adj_closes(tickers='SPY',start_date=pd.to_datetime(dta.mtf.iloc[0,0]).strftime('%Y-%m-%d'),end_date=dta.end_f.strftime('%Y-%m-%d'))
benchmark_m=fn.get_adj_closes(tickers='SPY',start_date=pd.to_datetime(dta.mtm.iloc[0,0]).strftime('%Y-%m-%d'),end_date=dta.end_m.strftime('%Y-%m-%d'))
benchmark_p=fn.get_adj_closes(tickers='SPY',start_date=pd.to_datetime(dta.mtp.iloc[0,0]).strftime('%Y-%m-%d'),end_date=dta.end_p.strftime('%Y-%m-%d'))
benchmark_a=fn.get_adj_closes(tickers='SPY',start_date=pd.to_datetime(dta.mta.iloc[0,0]).strftime('%Y-%m-%d'),end_date=dta.end_a.strftime('%Y-%m-%d'))

## estadisticas mad

est_f=fn.f_estadisticas_mad(dta.mtf,benchmark_f)
est_m=fn.f_estadisticas_mad(dta.mtm,benchmark_m)
est_p=fn.f_estadisticas_mad(dta.mtp,benchmark_p)
est_a=fn.f_estadisticas_mad(dta.mta,benchmark_a)

# Behavioral finance

## rates


# Visualizations

## grafica 1
grafica_1(dta.mtf)
grafica_1(dta.mtm)
grafica_1(dta.mtp)
grafica_1(dta.mta)


## grafica 2
grafica_2(dta.mtf)
grafica_2(dta.mtm)
grafica_2(dta.mtp)
grafica_2(dta.mta)


