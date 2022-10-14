import functions as fun

#%% 1
mtf1 = fun.f_leer_archivo('MyST_LAB2_FMHL.xlsx','Historico MT5')

mtf = fun.f_columnas_tiempos(mtf1)

col_pipsf = fun.f_columnas_pips(mtf)

estsf = fun.f_estadisticas_ba(mtf,'tabla')
ranf = fun.f_estadisticas_ba(mtf,'ranking')

#%% 2
profsf = fun.f_evolucion_capital(mtf).reset_index()

benchmarkf = fun.get_adj_closes('SPY', start_date=profsf.iloc[0,0], end_date=profsf.iloc[-1,0])

mad = fun.f_estadisticas_mad(fun.f_no_habiles(profsf),benchmarkf)