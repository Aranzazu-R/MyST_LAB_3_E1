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
import functions as fn

# Estadistica descriptiva

## Importacion de datos
mtf=fn.f_leer_archivo('MyST_LAB2_FMHL.xlsx','Historico MT5')
mtm=fn.f_leer_archivo('MyST_LAB2_MMM.xlsx','Historico MT5')
mtp=fn.f_leer_archivo('MyST_LAB2_PHMC.xlsx','Historico MT5')
mta=fn.f_leer_archivo('MyST_LAB2_ARG.xlsx','Historico MT5')


## time change
tcf=fn.f_columnas_tiempos(mtf)
tcm=fn.f_columnas_tiempos(mtm)
tcp=fn.f_columnas_tiempos(mtp)
tca=fn.f_columnas_tiempos(mta)

## pips
pf=fn.f_columnas_pips(mtf)
pm=fn.f_columnas_pips(mtm)
pp=fn.f_columnas_pips(mtp)
pa=fn.f_columnas_pips(mta)

## estadisticas_tabla
e_bat_f=fn.f_estadisticas_ba(mtf,f_columnas_pips(mtf),'tabla')
e_bat_m=fn.f_estadisticas_ba(mtm,f_columnas_pips(mtm),'tabla')
e_bat_p=fn.f_estadisticas_ba(mtp,f_columnas_pips(mtp),'tabla')
e_bat_a=fn.f_estadisticas_ba(mta,f_columnas_pips(mta),'tabla')

## estadisticas_ranking
e_bar_f=fn.f_estadisticas_ba(mtf,f_columnas_pips(mtf),'ranking').head()
e_bar_m=fn.f_estadisticas_ba(mtm,f_columnas_pips(mtm),'ranking').head()
e_bar_p=fn.f_estadisticas_ba(mtp,f_columnas_pips(mtp),'ranking').head()
e_bar_a=fn.f_estadisticas_ba(mta,f_columnas_pips(mta),'ranking').head()


# Metricas de Atribucion al desempeño
evcap_f=fn.f_evolucion_capital(mtf)
evcap_m=fn.f_evolucion_capital(mtm)
evcap_p=fn.f_evolucion_capital(mtp)
evcap_a=fn.f_evolucion_capital(mta)
