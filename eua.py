import plotly.graph_objects as go
import pandas as pd
import streamlit as st 


st.set_page_config(page_title="EUA- Eleições 2024",  page_icon="📈", layout="wide")

st.title('📈 Análise das eleições presidenciais dos EUA em 2024')

# https://projects.fivethirtyeight.com/polls/president-general/2024/national/
st.markdown('Fonte: [FiveThirtyEight](https://projects.fivethirtyeight.com/polls/president-general/2024/national/)')

# Carrega os dados de estimativas de votos direto do site do FiveThirtyEight
df = pd.read_json('https://projects.fivethirtyeight.com/polls/president-general/2024/national/polling-average.json')
# Filtrar os dados de interesse removendo Kennedy e criando uma cópia
# df = df[df["candidate"] != "Kennedy" ] .copy()

# Pivotar o DataFrame
df_pivot = df.pivot(index='date', columns='candidate', values='pct_estimate').reset_index()
df_pivot['Difference'] = df_pivot['Harris'] - df_pivot['Trump']

# Pivotar 'hi' e 'lo' e mesclar
hi_pivot = df.pivot(index='date', columns='candidate', values='hi').reset_index()
lo_pivot = df.pivot(index='date', columns='candidate', values='lo').reset_index()
df_pivot = df_pivot.merge(hi_pivot, on='date', suffixes=('', '_hi'))
df_pivot = df_pivot.merge(lo_pivot, on='date', suffixes=('', '_lo'))

# Criar o gráfico
fig = go.Figure()

# Harris
fig.add_trace(go.Scatter(
    x=df_pivot['date'],
    y=df_pivot['Harris'],
    mode='lines+markers+text',
    name='Harris',
    legendgroup='Harris', # agrupar as legendas

    text=df_pivot['Harris'].round(1),  # Texto a ser exibido (valores arredondados)
    textposition='top center',  # Posição do texto
    textfont=dict(size=9),

    line=dict(color='red'),
    hovertemplate=(
        '<b>Harris</b><br>' +
        'Data: %{x|%d-%m-%Y}<br>' +
        'Estimativa: %{y:.1f}%<br>' +
        'Diferença (Harris - Trump): %{customdata:.1f}%<extra></extra>'
    ),
    customdata=df_pivot['Difference']
))

fig.add_trace(go.Scatter(
    x=pd.concat([df_pivot['date'], df_pivot['date'][::-1]]),
    y=pd.concat([df_pivot['Harris_hi'], df_pivot['Harris_lo'][::-1]]),
    fill='toself',
    fillcolor='rgba(255, 0, 0, 0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo='skip',
    showlegend=False,
    legendgroup='Harris'
))

# Trump
fig.add_trace(go.Scatter(
    x=df_pivot['date'],
    y=df_pivot['Trump'],
    mode='lines+markers+text',
    name='Trump',
    legendgroup='Trump',
    text=df_pivot['Trump'].round(1),  # Texto a ser exibido (valores arredondados)
    textposition='top center',  # Posição do texto
    textfont=dict(size=9),    
    line=dict(color='blue'),
    hovertemplate=(
        '<b>Trump</b><br>' +
        'Data: %{x|%d-%m-%Y}<br>' +
        'Estimativa: %{y:.1f}%<br>' +
        'Diferença (Harris - Trump): %{customdata:.1f}%<extra></extra>'
    ),
    customdata=df_pivot['Difference']
))

fig.add_trace(go.Scatter(
    x=pd.concat([df_pivot['date'], df_pivot['date'][::-1]]),
    y=pd.concat([df_pivot['Trump_hi'], df_pivot['Trump_lo'][::-1]]),
    fill='toself',
    fillcolor='rgba(0, 0, 255, 0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo='skip',
    showlegend=False,
    legendgroup='Trump' 
))



# Kennedy
# fig.add_trace(go.Scatter(
#     x=df_pivot['date'],
#     y=df_pivot['Kennedy'],
#     mode='lines+markers+text',
#     name='Kennedy',
#     legendgroup='Kennedy',
#     text=df_pivot['Kennedy'].round(1),  # Texto a ser exibido (valores arredondados)
#     textposition='top center',  # Posição do texto
#     textfont=dict(size=9),    
#     line=dict(color='orange'),
#     hovertemplate=(
#         '<b>Kennedy</b><br>' +
#         'Data: %{x|%d-%m-%Y}<br>' +
#         'Estimativa: %{y:.2f}%<br>' +
#         'Diferença (Harris - Kennedy): %{customdata:.2f}%<extra></extra>'
#     ),
#     customdata=df_pivot['Difference']
# ))

# fig.add_trace(go.Scatter(
#     x=pd.concat([df_pivot['date'], df_pivot['date'][::-1]]),
#     y=pd.concat([df_pivot['Kennedy_hi'], df_pivot['Kennedy_lo'][::-1]]),
#     fill='toself',
#     fillcolor='rgba(0, 0, 255, 0.1)',
#     line=dict(color='rgba(255,255,255,0)'),
#     hoverinfo='skip',
#     showlegend=False,
#     legendgroup='Kennedy' 
# ))


# Layout
fig.update_layout(
    title='Estimativas com Diferença entre Harris e Trump',
    xaxis_title='Data',
    yaxis_title='Estimativa (%)',
    template='plotly_white',
    hovermode='x',
)



col = st.container()
with col:
    st.plotly_chart(fig, use_container_width=False)