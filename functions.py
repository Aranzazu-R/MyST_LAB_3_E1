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

# 1.0 Estadistica descriptiva

def f_leer_archivo(path,sheet):
    return pd.read_excel(path,sheet)


def f_columnas_tiempos(data):
    for i in range(len(data)):
        data.iloc[i,0]=pd.to_datetime(data.iloc[i,0])
        data.iloc[i,8]=pd.to_datetime(data.iloc[i,8])
        data.loc[i,'Time_change']=data.iloc[i,8]-data.iloc[i,0]
    return data


def f_pip_size(ticker):
    diccionario={'EURUSD':0.00001, 'GBPUSD':0.00001,'EURGBP':0.00001,'USDCAD':0.00001,'USDCHF':0.00001,
                 'GBPJPY':0.001,'USDJPY':0.001,'EURCAD':0.001,'USDCNH':0.00001,'GBPNZD':0.00001,'AUDUSD':0.00001,
                'USDMXN':0.00001,'CADCHF':0.00001,'CADJPY':0.001,'USDNOK':0.00001,'USDSGD':0.00001,'USDPLN':0.00001,
                'USDTRY':0.00001,'EURJPY':0.001,'EURMXN':0.00001,'NZDUSD':0.00001,'GBPCHF':0.00001,'AUDCHF':0.00001,
                'GBPAUD':0.00001}
    return (round(1/diccionario[ticker]))


def f_columnas_pips(data):
    pip = pd.DataFrame(0, index=range(len(data)),columns=['pips'])
    pip['instrument']=data['Symbol']
    for i in range(len(data)):
        if data.loc[i,'Type']=='sell':
            pip.loc[i,'pips']=(data.iloc[i,5]-data.iloc[i,9])*f_pip_size(pip.loc[i,'instrument'])
        else:
            pip.loc[i,'pips']=(data.iloc[i,9]-data.iloc[i,5])*f_pip_size(pip.loc[i,'instrument'])
    pip['pips_acm']=pip['pips'].cumsum()
    pip['profit_acm']=data['Profit'].astype(float).cumsum()
    return pip


def f_estadisticas_ba(data,datapip,df):
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
    df_1.iloc[8,1]=datapip['pips'].median()
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



# 2.0 Metricas de atribucion al desempeño

k=100000
def f_evolucion_capital(data):
    dates=[]
    for i in range(len(data)):
        data.iloc[i,0]=data.iloc[i,0].strftime('%Y-%m-%d')
        dates.append(data.iloc[i,0])
    dates=list(set(dates))
    dates.sort()
    dateslist=pd.date_range(dates[0],dates[-1],freq='d').strftime('%Y-%m-%d')
    evcap=pd.DataFrame({'timestamp':dateslist})
    for i in range(len(dateslist)):
        evcap.loc[i,'profit_d']=data[data['Time']==dateslist[i]]['Profit'].sum()
    evcap.loc[0,'profit_acm_d']=k+evcap.loc[0,'profit_d']
    for i in range(len(dateslist)-1):
        evcap.loc[i+1,'profit_acm_d']=evcap.loc[i,'profit_acm_d']+evcap.loc[i+1,'profit_d']
    return evcap