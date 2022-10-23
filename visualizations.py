import numpy as np
import functions as fn
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd


def grafica_1(data):
    data=fn.f_estadisticas_ba(data,'ranking')
    lista=np.zeros(len(data))
    lista[data['rank %'].idxmax()]=0.2
    fig = go.Figure(data=[go.Pie(labels=data['Symbol'], values=data['rank %'], pull=lista)])
    return fig.show()

def grafica_2(data):
    data_profit=fn.f_evolucion_capital(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_profit['timestamp'], y=data_profit['profit_acm_d'],
                    mode='lines',name='Profit Acum',line=dict(color='black')))
    #dd
    dd=data_profit['profit_acm_d'].min()
    ix_dd=data_profit[data_profit['profit_acm_d']==dd].index.min()
    ix_dd=1 if ix_dd==0 else ix_dd
    dd_dates=[data_profit.iloc[[ix_dd-1]]['timestamp'].min().strftime('%Y-%m-%d'),data_profit.iloc[[ix_dd]]['timestamp'].min().strftime('%Y-%m-%d')]
    dd_prof=[int(data_profit.iloc[[ix_dd-1]]['profit_acm_d']),int(data_profit.iloc[[ix_dd]]['profit_acm_d'])]
    fig.add_trace(go.Scatter(x=dd_dates, y=dd_prof,
                    mode='lines',name='DrawDown',line=dict(color='red',width=4,dash='dash')))
    #du
    du=data_profit['profit_acm_d'].max()
    ix_du=data_profit[data_profit['profit_acm_d']==du].index.min()
    ix_du=1 if ix_du==0 else ix_du
    du_dates=[data_profit.iloc[[ix_du-1]]['timestamp'].min().strftime('%Y-%m-%d'),data_profit.iloc[[ix_du]]['timestamp'].min().strftime('%Y-%m-%d')]
    du_prof=[int(data_profit.iloc[[ix_du-1]]['profit_acm_d']),int(data_profit.iloc[[ix_du]]['profit_acm_d'])]
    fig.add_trace(go.Scatter(x=du_dates, y=du_prof,
                    mode='lines',name='DrawUp',line=dict(color='green',width=4,dash='dash')))
    return fig.show()

def graph_tab(data:'datos a graficar en gráfica de tablas', ejex:'nombre de el eje x', ejey:'nombre de el eje y', titulo:'titulo de la grafica'):
    plt.style.use('ggplot')
    data.plot(kind='bar')
    plt.xlabel(ejex)
    plt.ylabel(ejey)
    plt.title(titulo)
    return plt.show()

def grafica_3(data_disp):
    data_disp = pd.DataFrame({'efecto':['status_quo', 'aversion_perdida', 'sensibilidad_decreciente'],'ocurrencias':[data_disp.iloc[0,0],0,0]})
    fig = px.bar(data_disp, x='efecto', y='ocurrencias')
    fig.update_layout(title = 'Disposition Effect',yaxis_title='Disposition',xaxis_title='Effect')
    return fig.show()