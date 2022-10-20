"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 3. Behavioral Finance                                                  -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: FridaHernandezL                                                                             -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/FridaHernandezL/MyST_LAB_3_E1                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
import statistics as st
pd.options.mode.chained_assignment = None  # default='warn'
import yfinance as yf
from datetime import datetime, date, timedelta
import MetaTrader5 as mt5
import pytz
import plotly.graph_objects as go
import data as dta

# 1.0 Estadistica descriptiva

def f_leer_archivo(path,sheet):
    return pd.read_excel(path,sheet)


def f_columnas_tiempos(data):
    col1=pd.to_datetime(data.iloc[:,0])
    col2=pd.to_datetime(data.iloc[:,8])
    data['Time_change']=col2-col1 
    for i in range(len(data)):
        data['Time_change'][i] = data['Time_change'][i].total_seconds() 
    return data


def f_pip_size(ticker):
    size=pd.read_csv('files/instruments_pips.csv')
    pip=size[size['Instrument']==ticker]['TickSize']
    return (int(1/pip))


def f_columnas_pips(data):
    for i in range(len(data)):
        if data.loc[i,'Type']=='sell':
            data.loc[i,'pips']=(data.iloc[i,5]-data.iloc[i,9])*f_pip_size(data.loc[i,'Symbol'])
        else:
            data.loc[i,'pips']=(data.iloc[i,9]-data.iloc[i,5])*f_pip_size(data.loc[i,'Symbol'])
    data['pips_acm']=data['pips'].cumsum()
    data['profit_acm']=data['Profit'].astype(float).cumsum()
    return data


def f_estadisticas_ba(data,df):
    df_1_tabla=pd.DataFrame({'medida':['Ops totales','Ganadoras','Ganadoras_c','Ganadoras_v','Perdedoras','Perdedoras_c',
                             'Perdedoras_v','Mediana (profit)','Mediana (pips)','r_efectividad','r_proporcion',
                             'r_efectividad_c', 'r_efectividad_v'],
                   'valor':np.zeros(13),
                  'descripcion':['Operaciones totales','Operaciones ganadoras','Operaciones ganadoras de compra',
                                'Operaciones ganadoras de venta','Operaciones perdedoras','Operaciones perdedoras de compra',
                                'Operaciones perdedoras de venta','Mediana de profit de operaciones',
                                 'Mediana de pips de operaciones','Ganadoras totales/ Operaciones totales',
                                'Ganadoras totales/ Perdedoras totales','Ganadoras compras/ Operaciones totales',
                                 'Ganadoras ventas/ Operaciones totales']})
    df_1_tabla.iloc[0,1]=len(data)
    df_1_tabla.iloc[1,1]=len(data[data['Profit']>0])
    df_1_tabla.iloc[2,1]=len(data[(data['Profit']>0) & (data['Type']=='buy')])
    df_1_tabla.iloc[3,1]=len(data[(data['Profit']>0) & (data['Type']=='sell')])
    df_1_tabla.iloc[4,1]=len(data[data['Profit']<0])
    df_1_tabla.iloc[5,1]=len(data[(data['Profit']<0) & (data['Type']=='buy')])
    df_1_tabla.iloc[6,1]=len(data[(data['Profit']<0) & (data['Type']=='sell')])
    df_1_tabla.iloc[7,1]=data['Profit'].median()
    df_1_tabla.iloc[8,1]=f_columnas_pips(data)['pips'].median()
    df_1_tabla.iloc[9,1]=df_1_tabla.iloc[1,1]/df_1_tabla.iloc[0,1]
    df_1_tabla.iloc[10,1]=df_1_tabla.iloc[1,1]/df_1_tabla.iloc[5,1]
    df_1_tabla.iloc[11,1]=df_1_tabla.iloc[3,1]/df_1_tabla.iloc[1,1]
    df_1_tabla.iloc[10,1]=df_1_tabla.iloc[4,1]/df_1_tabla.iloc[1,1]
    df_1_tabla['valor']=round(df_1_tabla['valor'],2)
    
    uniques=data['Symbol'].unique()
    rank=[]
    for i in uniques:
        rank.append(round(len(data[(data['Profit']>0) & (data['Symbol']==i)])/len(data[data['Symbol']==i])*100,2))
    df_2_ranking=pd.DataFrame({'Symbol':uniques,'rank %':rank})
    
    diccionario={'tabla':df_1_tabla,'ranking':df_2_ranking}
    return diccionario[df]


#%% 2.0 Metricas de atribucion al desempeño

def f_evolucion_capital(data):
    prof = data[["Time","Profit"]]
    prof['timestamp'] = pd.to_datetime(data["Time"])
    prof.set_index('timestamp',inplace=True)
    prof = prof.resample("D").sum()
    prof['profit_acm_d'] = 100000 + prof['Profit'].astype(float).cumsum()
    prof=prof.reset_index()
    prof=prof[(prof['timestamp']!='2022-09-17')&(prof['timestamp']!='2022-09-24')]
    prof=prof.reset_index(drop=True)
    return prof

def get_adj_closes(tickers, start_date=None, end_date=None):
    # Descargamos DataFrame con todos los datos
    closes = yf.download(tickers, start_date, end_date)
    # Solo necesitamos los precios ajustados en el cierre
    closes = closes['Adj Close']
    # Se ordenan los índices de manera ascendente
    closes.sort_index(inplace=True)
    return closes

def f_estadisticas_mad(data,benchmark):
        data=f_evolucion_capital(data)
        #Sharpe Ratio Original:
        rp = np.mean(np.log(data['profit_acm_d'] / data['profit_acm_d'].shift()).dropna())
        sdp = np.log(data['profit_acm_d'] / data['profit_acm_d'].shift()).dropna().std()
        rf = 0.05/365
        sharp_o = (rp - rf) / sdp
        #Sharpe Ratio Actualizado:
        r_trader = np.log(data['profit_acm_d'] / data['profit_acm_d'].shift()).dropna()
        r_benchmark = np.log(benchmark / benchmark.shift()).dropna()
        rtr = r_trader.tolist()
        rbm = r_benchmark.tolist()
        product = list(map(lambda x,y: x-y ,rtr,rbm))
        sdp2 = st.pstdev(product) 
        sharp_a = (np.mean(r_trader) - np.mean(r_benchmark)) / sdp2
        #DrawDown (Capital):
        draw_down = data['profit_acm_d'].min()
        idx_fecha_in_dd = data[data['profit_acm_d']==draw_down].index
        fecha_min_dd = data.loc[idx_fecha_in_dd,'timestamp']-timedelta(days=1)
        fecha_min_dd=fecha_min_dd.min().strftime('%Y-%m-%d')
        fecha_max_dd = data[data['profit_acm_d']==draw_down]['timestamp'].max().strftime('%Y-%m-%d')
        #DrawUp (Capital):
        draw_up = data['profit_acm_d'].max()
        idx_fecha_in_du = data[data['profit_acm_d']==draw_up].index
        fecha_min_du = data.loc[idx_fecha_in_du,'timestamp']-timedelta(days=1)
        fecha_min_du=fecha_min_du.min().strftime('%Y-%m-%d')
        fecha_max_du = data[data['profit_acm_d']==draw_up]['timestamp'].max().strftime('%Y-%m-%d')
        est_mad=pd.DataFrame({'metrica':['sharpe_original','sharpe_actualizado','drawdown_capi','drawdown_capi',
                                         'drawdown_capi','drawup_capi','drawup_capi','drawup_capi'],
                             'valor':[sharp_o, sharp_a, fecha_min_dd, fecha_max_dd ,draw_down, fecha_min_du, fecha_max_du ,draw_up],
                             'descripcion':['Sharpe Ratio Fórmula Original','Sharpe Ratio Fórmula Ajustada',
                                            'Fecha inicial del DrawDown de Capital', 'Fecha final del DrawDown de Capital',
                                            'Máxima pérdida flotante registrada', 'Fecha inicial del DrawUp de Capital', 
                                            'Fecha final del DrawUp de Capital','Máxima ganancia flotante registrada']})
        return est_mad

#%% 3.0 Behavioral Finance

def f_be_de(data):
    year1=int(data['Time'].min()[0:4])
    year2=int(data['Time'].max()[0:4])
    
    month1=int(data['Time'].min()[6])
    month2=int(data['Time'].max()[6])
    
    day1=int(data['Time'].min()[8:10])
    day2=int(data['Time'].max()[8:10])
    # import the 'pandas' module for displaying data obtained in the tabular form
    import pandas as pd
    pd.set_option('display.max_columns', 500) # number of columns to be displayed
    pd.set_option('display.width', 1500)      # max table width to display

    # establish connection to MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime(year1,month1,day1, tzinfo=timezone)
    utc_to = datetime(year2,month2,day2, hour = 23, tzinfo=timezone)
    # get bars from USDJPY M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
    symbols=data['Symbol'].unique()
    rate_df=[]
    for symbol in symbols:
        rates= pd.DataFrame(mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5, utc_from, utc_to))
        rates['Symbol']=symbol
        rate_df.append(rates)
    rates = pd.concat(rate_df)

    # shut down connection to the MetaTrader 5 terminal
    mt5.shutdown()
    
    # convert time in seconds into the 'datetime' format
    rates['time']=pd.to_datetime(rates['time'], unit='s')

    # display data
    return rates


def disp_effect(data,rates):
    param_data=data[data['Profit']>0].reset_index(drop=True)
    idx=param_data.index
    otidx=[]
    prices_ancla=[]
    for i in range(len(idx)):
        n_param_data=param_data.drop([i]).reset_index(drop=True)
        for j in range(len(n_param_data)):
            limit_inf=pd.to_datetime(n_param_data.iloc[[idx[j]]]['Time'])
            limit_sup=pd.to_datetime(n_param_data.iloc[[idx[j]]]['Time.1'])
            closetime_ancla=pd.to_datetime(param_data.iloc[[idx[i]]]['Time.1'])
            if closetime_ancla.values<limit_sup.values and closetime_ancla.values>limit_inf.values:
                otidx.append(n_param_data.iloc[[idx[j]]])
                prices_ancla.append(param_data.iloc[[idx[i]]])
    otidx_n=pd.concat(otidx).drop_duplicates().reset_index(drop=True)
    prices_ancla_n=pd.concat(prices_ancla).drop_duplicates().reset_index(drop=True)
    if len(otidx_n)!=0:
        symbolquotes=[]
        wanted_time=[]
        symbols=otidx_n['Symbol'].values
        vol=otidx_n['Volume'].values
        pip=[]
        for i in range(len(prices_ancla_n)):
            wanted_time.append(rates['time'].where(pd.to_datetime(rates['time']) > pd.to_datetime(prices_ancla_n.loc[i,'Time.1'])).dropna().min())
            symbolquotes.append(float(rates[(rates['time']==wanted_time[i])&(rates['Symbol']==symbols[i])]['close'].values))
        for symbol in symbols:
            pip.append(f_pip_size(symbol))
        symbolprofit=(otidx_n['Price'].values-symbolquotes)*pip*vol
        disp_effect=[]
        for i in range(len(symbolprofit)):
            if symbolprofit[i]<0:
                disp_effect.append(symbolprofit[i])
    return disp_effect