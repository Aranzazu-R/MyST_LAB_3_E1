"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Laboratorio 1. Inversión Pasiva y Activa                                                   -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: FridaHernandezL                                                                             -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/FridaHernandezL/Laboratorio1_MyST                                    -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np 

def f_leer_archivo(path,sheet):
    return pd.read_excel(path,sheet)


def f_columnas_tiempos(data,col1,col2):
    for i in range(len(data)):
        data[col1]=pd.to_datetime(data.iloc[i,0])
        data[col2]=pd.to_datetime(data.iloc[i,8])
        data['Time_change']=mtf[col1]-mtf[col2]
    return data


def f_pip_size(ticker):
    diccionario={'EURUSD':0.00001, 'GBPUSD':0.00001,'EURGBP':0.00001,'USDCAD':0.00001,'USDCHF':0.00001,
                 'GBPJPY':0.001,'USDJPY':0.001,'EURCAD':0.001}
    return (round(1/diccionario[ticker]))


def f_columnas_pips(data):
    pip = pd.DataFrame(0, index=range(len(mtf)),columns=['pips'])
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
    df_1.iloc[2,1]=len(mtf[(mtf['Profit']>0) & (mtf['Type']=='buy')])
    df_1.iloc[3,1]=len(mtf[(mtf['Profit']>0) & (mtf['Type']=='sell')])
    df_1.iloc[4,1]=len(data[data['Profit']<0])
    df_1.iloc[5,1]=len(mtf[(mtf['Profit']<0) & (mtf['Type']=='buy')])
    df_1.iloc[6,1]=len(mtf[(mtf['Profit']<0) & (mtf['Type']=='sell')])
    df_1.iloc[7,1]=data['Profit'].median()
    df_1.iloc[8,1]=datapip['pips'].median()
    df_1.iloc[9,1]=df_1.iloc[1,1]/df_1.iloc[0,1]
    df_1.iloc[10,1]=df_1.iloc[1,1]/df_1.iloc[5,1]
    df_1.iloc[11,1]=df_1.iloc[3,1]/df_1.iloc[1,1]
    df_1.iloc[10,1]=df_1.iloc[4,1]/df_1.iloc[1,1]
    df_1['valor']=round(df_1['valor'],2)
    
    uniques=mtf['Symbol'].unique()
    rank=[]
    for i in uniques:
        rank.append(round(len(data[(data['Profit']>0) & (data['Symbol']==i)])/len(data[data['Symbol']==i])*100,2))
    df_2_ranking=pd.DataFrame({'Symbol':uniques,'rank %':rank})
    
    diccionario={'tabla':df_1,'ranking':df_2_ranking}
    return diccionario[df]