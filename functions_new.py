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
import pandas_datareader.data as web
import statistics as st

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
    diccionario={'EURUSD':0.00001, 'GBPUSD':0.00001,'EURGBP':0.00001,'USDCAD':0.00001,'USDCHF':0.00001,
                 'GBPJPY':0.001,'USDJPY':0.001,'EURCAD':0.001,'USDCNH':0.00001,'GBPNZD':0.00001,'AUDUSD':0.00001,
                'USDMXN':0.00001,'CADCHF':0.00001,'CADJPY':0.001,'USDNOK':0.00001,'USDSGD':0.00001,'USDPLN':0.00001,
                'USDTRY':0.00001,'EURJPY':0.001,'EURMXN':0.00001,'NZDUSD':0.00001,'GBPCHF':0.00001,'AUDCHF':0.00001,
                'GBPAUD':0.00001}
    return (round(1/diccionario[ticker]))


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
    df_1=pd.DataFrame({'medida':['Ops totales','Ganadoras','Ganadoras_c','Ganadoras_v','Perdedoras','Perdedoras_c',
                             'Perdedoras_v','Mediana (profit)','Mediana (pips)','r_efectividad','r_proporcion',
                             'r_efectividad_c', 'r_efectividad_v'],
                   'valor':np.zeros(13),
                  'descripcion':['Operaciones totales','Operaciones ganadoras','Operaciones ganadoras de compra',
                                'Operaciones ganadoras de venta','Operaciones perdedoras','Operaciones perdedoras de compra',
                                'Operaciones perdedoras de venta','Mediana de profit de operaciones',
                                 'Mediana de pips de operaciones','Ganadoras totales/ Operaciones totales',
                                'Ganadoras totales/ Perdedoras totales','Ganadoras compras/ Operaciones totales',
                                 'Ganadoras ventas/ Operaciones totales']})
    df_1.iloc[0,1]=len(data)
    df_1.iloc[1,1]=len(data[data['Profit']>0])
    df_1.iloc[2,1]=len(data[(data['Profit']>0) & (data['Type']=='buy')])
    df_1.iloc[3,1]=len(data[(data['Profit']>0) & (data['Type']=='sell')])
    df_1.iloc[4,1]=len(data[data['Profit']<0])
    df_1.iloc[5,1]=len(data[(data['Profit']<0) & (data['Type']=='buy')])
    df_1.iloc[6,1]=len(data[(data['Profit']<0) & (data['Type']=='sell')])
    df_1.iloc[7,1]=data['Profit'].median()
    df_1.iloc[8,1]=data['pips'].median()
    df_1.iloc[9,1]=df_1.iloc[1,1]/df_1.iloc[0,1]
    df_1.iloc[10,1]=df_1.iloc[1,1]/df_1.iloc[5,1]
    df_1.iloc[11,1]=df_1.iloc[3,1]/df_1.iloc[1,1]
    df_1.iloc[10,1]=df_1.iloc[4,1]/df_1.iloc[1,1]
    df_1['valor']=round(df_1['valor'],2)
    
    uniques=data['Symbol'].unique()
    rank=[]
    for i in uniques:
        rank.append(round(len(data[(data['Profit']>0) & (data['Symbol']==i)])/len(data[data['Symbol']==i])*100,2))
    df_2_ranking=pd.DataFrame({'Symbol':uniques,'rank %':rank})
    
    diccionario={'tabla':df_1,'ranking':df_2_ranking}
    return diccionario[df]



#%% 2.0 Metricas de atribucion al desempeño

def f_evolucion_capital(data):
    prof = data[["Time","Profit"]]
    prof['timestamp'] = pd.to_datetime(data["Time"])
    prof.set_index('timestamp',inplace=True)
    prof = prof.resample("D").sum()
    prof['profit_acm_d'] = 100000 + prof['Profit'].astype(float).cumsum()
    return prof

def f_no_habiles(data):
    data = data[(data.timestamp != '2022-09-24') & (data.timestamp != '2022-09-25') & (data.timestamp != '2022-09-16') & (data.timestamp != '2022-09-17') & (data.timestamp != '2022-09-18')]
    return data

def get_adj_closes(tickers, start_date=None, end_date=None):
    closes = web.DataReader(name=tickers, data_source='yahoo', start=start_date, end=end_date)
    closes = closes['Adj Close']
    closes.sort_index(inplace=True)
    return closes

def f_estadisticas_mad(data,benchmark):
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
        min_max = data['profit_acm_d'].idxmin()
        fecha_min = data['timestamp'][min_max]
        #DrawUp (Capital):
        draw_up = data['profit_acm_d'].max()
        plus_max = data['profit_acm_d'].idxmax()
        fecha_max = data['timestamp'][plus_max]
        est_mad=pd.DataFrame({'metrica':['sharpe_original','sharpe_actualizado','drawdown_capi','drawdown_capi',
                                         'drawdown_capi','drawup_capi','drawup_capi','drawup_capi'],
                             'valor':[sharp_o, sharp_a, fecha_min, fecha_max ,draw_down, fecha_min, fecha_max ,draw_up],
                             'descripcion':['Sharpe Ratio Fórmula Original','Sharpe Ratio Fórmula Ajustada',
                                            'Fecha inicial del DrawDown de Capital', 'Fecha final del DrawDown de Capital',
                                            'Máxima pérdida flotante registrada', 'Fecha inicial del DrawUp de Capital', 
                                            'Fecha final del DrawUp de Capital','Máxima ganancia flotante registrada']})
        return est_mad