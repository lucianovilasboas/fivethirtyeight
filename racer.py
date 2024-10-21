import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import time
import requests

# Obter os dados da API e convertê-los para um DataFrame
polling_average = requests.get('https://projects.fivethirtyeight.com/polls/president-general/2024/national/polling-average.json').json()
df_polling_average = pd.DataFrame(polling_average)

# Converter a coluna 'date' para formato datetime
df_polling_average['date'] = pd.to_datetime(df_polling_average['date'])

# Configuração do layout do Streamlit
st.title('Polling Average Race Chart - Eleição 2024')

# Definir um filtro para o partido (opcional)
partidos_selecionados = st.multiselect('Selecione os partidos para exibir:', df_polling_average['party'].unique(), default=['REP', 'DEM'])

# Filtrar os dados pelos partidos selecionados
df_filtered = df_polling_average[df_polling_average['party'].isin(partidos_selecionados)]

df_filtered.sort_values(by='date', ascending=True, inplace=True)

# Placeholder para o gráfico
chart_placeholder = st.empty()

# Função para criar o gráfico com base na etapa atual
def update_chart(step):
    fig = go.Figure()

    # Pegar apenas as datas até o ponto atual da animação
    data_atual = df_filtered[df_filtered['date'] <= df_filtered['date'].unique()[step]]

    # Adicionar trace para cada candidato
    for candidate in data_atual['candidate'].unique():
        df_candidate = data_atual[data_atual['candidate'] == candidate]
        fig.add_trace(go.Scatter(x=df_candidate['date'], y=df_candidate['pct_estimate'], mode='lines+markers', name=candidate))
    
    fig.update_layout(
        xaxis=dict(title="Data"),
        yaxis=dict(title="Porcentagem de Votos Estimada"),
        title="Evolução das Estimativas ao longo do tempo",
        showlegend=True
    )
    
    # Atualizar o gráfico no placeholder
    chart_placeholder.plotly_chart(fig, use_container_width=True)

# Laço de controle da animação
start_button = st.button('Iniciar Animação')

if start_button:
    for i in range(len(df_filtered['date'].unique())):
        update_chart(i)
        time.sleep(.2)  # Pausa de 1 segundo entre as atualizações
