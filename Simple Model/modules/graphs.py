from plotly import graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def cmap():
    """

    :return: list colour map for change periods
    """

    return ['#00789c', '#d1495b', '#edae49', '#66a182', '#2e4057', '#8d96a3']


def counter_actual(df_plot, s_d, e_d):
    """

    :return:
    """

    fig = go.Figure()

    df_plot.reset_index(inplace=True)

    fig.add_trace(go.Scatter(x=df_plot['ds'],
                             y=df_plot['z'],
                             line=dict(color="#DEDEDE"),
                             name='Predicted Min'))

    fig.add_trace(go.Scatter(x=df_plot['ds'],
                             y=df_plot['y'],
                             line=dict(color="#DEDEDE"),
                             mode='lines',
                             name='Predicted Max'
                             ))

    fig.add_trace(go.Scatter(x=df_plot['ds'],
                             y=df_plot['x'],
                             name='Predicted Mean'),
                  )

    fig.add_trace(go.Scatter(x=df_plot['ds'],
                             y=df_plot['q'].rolling(7).mean(),
                             name='Actual',
                             line=dict(color="#44546A")))

    for i in range(0, len(s_d)):
        fig.add_vrect(x0=s_d[i],
                      x1=e_d[i],
                      line_width=0,
                      fillcolor=cmap()[i],
                      opacity=0.35,
                      annotation_text='Change Period ' + str(i + 1))

    fig.update_layout(height=600,
                      margin=dict(r=1, l=1, t=1, b=1),
                      xaxis_title='ds',
                      yaxis_title='n',
                      template='seaborn',
                      showlegend=False
                      )

    return fig


def point_effect(df, s_d, e_d):
    """

    :return:
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['ds'].dt.strftime("%d/%m/%Y"),
                             y=df['q'] - df['z'],
                             fill=None,
                             line=dict(color="#DEDEDE"),
                             name='Point Effect Lower'))

    fig.add_trace(go.Scatter(x=df['ds'].dt.strftime("%d/%m/%Y"),
                             y=df['q'] - df['y'],
                             fill='tonexty',
                             line=dict(color="#DEDEDE"),
                             mode='lines',
                             name='Point Effect Upper'))

    fig.add_trace(go.Scatter(x=df['ds'].dt.strftime("%d/%m/%Y"),
                             y=df['q'] - df['x'],
                             name='Point Effect'))

    fig.add_trace(go.Scatter(x=df.ds.dt.strftime("%d/%m/%Y"), \
                             y=np.zeros(len(df)), \
                             mode='lines', line=dict(color="#C00000"), showlegend=False))

    fig.update_xaxes(type='category')

    for i in range(0, len(s_d)):
        fig.add_vrect(x0=s_d[i].strftime("%d/%m/%Y"),
                      x1=e_d[i].strftime("%d/%m/%Y"),
                      line_width=0,
                      fillcolor=cmap()[i],
                      opacity=0.35,
                      annotation_text='Change Period ' + str(i + 1))

    fig.update_layout(height=600,
                      margin=dict(r=1, l=1, t=1, b=1),
                      xaxis_title='ds',
                      yaxis_title='n',
                      template='seaborn',
                      showlegend=False
                      )

    # fig.add_hrect(y0=0,
    #               y1=0,
    #               line_width=1)

    return fig


def cumulative_pointwise(df, s_d, e_d):
    """

    :param pointwise_df:
    :param s_d:
    :return:
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['ds'].dt.strftime("%d/%m/%Y"),
                             y=np.cumsum(df['q']) - np.cumsum(df['z']),
                             fill=None,
                             line=dict(color="#DEDEDE"),
                             name='Cumulative Point Effect Lower'))

    fig.add_trace(go.Scatter(x=df['ds'].dt.strftime("%d/%m/%Y"),
                             y=np.cumsum(df['q']) - np.cumsum(df['y']),
                             fill='tonexty',
                             line=dict(color="#DEDEDE"),
                             mode='lines',
                             name='Cumulative Point Effect Upper'))

    fig.add_trace(go.Scatter(x=df['ds'].dt.strftime("%d/%m/%Y"),
                             y=np.cumsum(df['q']) - np.cumsum(df['x']),
                             name='Cumulative Point Effect'))

    fig.add_trace(go.Scatter(x=df.ds.dt.strftime("%d/%m/%Y"), \
                             y=np.zeros(len(df)), \
                             mode='lines', line=dict(color="#C00000"), showlegend=False))

    fig.update_xaxes(type='category')

    for i in range(0, len(s_d)):
        fig.add_vrect(x0=s_d[i].strftime("%d/%m/%Y"),
                      x1=e_d[i].strftime("%d/%m/%Y"),
                      line_width=0,
                      fillcolor=cmap()[i],
                      opacity=0.35,
                      annotation_text='Change Period ' + str(i + 1))

    fig.add_hrect(y0=0,
                  y1=0,
                  line_width=1)

    fig.update_layout(height=600,
                      margin=dict(r=1, l=1, t=1, b=1),
                      xaxis_title='ds',
                      yaxis_title='n',
                      template='seaborn',
                      showlegend=False)

    return fig
