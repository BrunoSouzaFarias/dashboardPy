import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração inicial do Streamlit
st.set_page_config(
    page_title="Dashboard de Chamados",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': 'Dashboard de análise de chamados'
    }
)
st.title("Dashboard de Chamados")

# Upload de arquivo Excel
st.sidebar.header("Carregar Arquivo Excel")
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])

@st.cache_data
def load_data(uploaded_file):
    return pd.read_excel(uploaded_file)

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {str(e)}")
        st.stop()

    # Exibir as colunas do arquivo Excel
    st.write("Colunas encontradas no arquivo Excel:", df.columns)

    # Filtros interativos
    st.sidebar.header("Filtros")
    unidade_filter = st.sidebar.multiselect("Selecione as Unidades", options=df["Unidade"].unique(), default=df["Unidade"].unique())
    chave_filter = st.sidebar.multiselect("Selecione as Chaves", options=df["Chave"].unique(), default=df["Chave"].unique())

    # Se houver coluna de data
    if 'data' in df.columns:
        date_filter = st.sidebar.date_input(
            "Selecione o período",
            [pd.to_datetime(df['Entrada do chamado']).min(), 
             pd.to_datetime(df['Entrada do chamado']).max()]
        )

    # Aplicar filtros
    filtered_data = df[(df["Unidade"].isin(unidade_filter)) & (df["Chave"].isin(chave_filter))]

    # Verificar se as colunas esperadas estão no arquivo
    expected_columns = ["Chave", "Status", "Unidade"]  # Exemplo com menos colunas

    # Mostrar os dados filtrados
    st.dataframe(filtered_data)

    # KPIs
    st.header("KPIs")
    st.metric("Total de Chamados", len(filtered_data))
    st.metric("Chamados Concluídos", len(filtered_data[filtered_data["Status"] == "CONCLUÍDO"]))

    # Gráficos principais
    st.header("Análises e Gráficos")

    # Organizar gráficos de pizza lado a lado
    col1, col2 = st.columns(2)

    with col1:
        # 1. Distribuição de Chamados (Concluídos vs Pendentes)
        status_count = filtered_data["Status"].value_counts().reset_index()
        status_count.columns = ["Status", "Quantidade"]
        status_fig = px.pie(status_count, names="Status", values="Quantidade", title="Distribuição de Chamados (Concluídos vs Pendentes)")
        status_fig.update_traces(textinfo="percent+label+value")  # Adiciona quantidade e porcentagem
        st.plotly_chart(status_fig)

    with col2:
        # 2. Chamados Escalonados
        escalonado_data = filtered_data["Escalonado"].value_counts().reset_index()
        escalonado_data.columns = ["Status", "Quantidade"]
        
        # Ajustar os rótulos para melhor visualização
        escalonado_data["Status"] = escalonado_data["Status"].replace({
            "Sim": "N1 para N2",
            "N2 - Operações": "N2 Operações",
            "NOC": "NOC",
            "Não": "Não Escalonados"
        })
        
        escalonado_pie_fig = px.pie(
            escalonado_data, 
            names="Status", 
            values="Quantidade", 
            title="Distribuição de Chamados Escalonados",
            color="Status",
            color_discrete_map={
                "N1 para N2": "#EF553B",
                "N2 Operações": "#FFA15A",
                "NOC": "#FF6692",
                "Não Escalonados": "#636EFA"
            }
        )
        escalonado_pie_fig.update_traces(textinfo="percent+label+value")
        st.plotly_chart(escalonado_pie_fig)

    # Adicionar mais gráficos de pizza se necessário

    # Organizar os outros gráficos abaixo
    st.subheader("Análises por Técnico e Categoria")

    # 3. Chamados por Técnico N1 Responsável
    tecnico_status = filtered_data.groupby(['Técnico N1 Responsável', 'Status']).size().reset_index(name='Quantidade')
    tecnico_fig = px.bar(tecnico_status, x='Técnico N1 Responsável', y='Quantidade', color='Status', 
                         title="Chamados por Técnico N1 Responsável", barmode='stack')
    tecnico_fig.update_traces(text=tecnico_status['Quantidade'], textposition='inside')  # Adiciona quantidade dentro das barras
    st.plotly_chart(tecnico_fig)

    # 4. Chamados por Categoria - N1
    categoria_count = filtered_data["Categoria - N1"].value_counts().reset_index()
    categoria_count.columns = ["Categoria - N1", "Quantidade"]
    categoria_fig = px.bar(categoria_count, x="Categoria - N1", y="Quantidade", title="Distribuição de Chamados por Categoria")
    categoria_fig.update_traces(text=categoria_count['Quantidade'], textposition='inside')  # Adiciona quantidade dentro das barras
    st.plotly_chart(categoria_fig)

    # 6. Chamados por Entrada do Chamado (sem a divisão por Unidade)
    entrada_count = filtered_data.groupby('Entrada do chamado').size().reset_index(name='Quantidade')

    # Gráfico de Barra (sem a divisão por Unidade)
    entrada_fig = px.bar(entrada_count, x='Entrada do chamado', y='Quantidade', 
                        title="Quantidade Total de Chamados por Entrada do Chamado")
    entrada_fig.update_traces(text=entrada_count['Quantidade'], textposition='inside')  # Adiciona quantidade dentro das barras
    st.plotly_chart(entrada_fig)

    # 7. Gráfico de linha temporal mostrando tendência de chamados
    st.subheader("Tendência de Chamados ao Longo do Tempo")
    timeline_data = filtered_data.groupby(['Entrada do chamado', 'Status']).size().reset_index(name='Quantidade')
    timeline_fig = px.line(timeline_data, x='Entrada do chamado', y='Quantidade', color='Status',
                          title="Tendência de Chamados por Status ao Longo do Tempo")
    st.plotly_chart(timeline_fig)

    # 8. Top 5 categorias com mais chamados
    st.subheader("Top 5 Categorias Mais Frequentes")
    top_categorias = filtered_data["Categoria - N1"].value_counts().head(5).reset_index()
    top_categorias.columns = ["Categoria", "Quantidade"]
    top_cat_fig = px.bar(top_categorias, x="Categoria", y="Quantidade",
                         title="Top 5 Categorias com Mais Chamados")
    top_cat_fig.update_traces(text=top_categorias['Quantidade'], textposition='inside')
    st.plotly_chart(top_cat_fig)

    # 9. Tempo médio de resolução por categoria (se houver data de conclusão)
    if 'Data de conclusão' in filtered_data.columns and 'Entrada do chamado' in filtered_data.columns:
        filtered_data['Tempo de Resolução'] = pd.to_datetime(filtered_data['Data de conclusão']) - pd.to_datetime(filtered_data['Entrada do chamado'])
        tempo_medio = filtered_data.groupby('Categoria - N1')['Tempo de Resolução'].mean().reset_index()
        tempo_fig = px.bar(tempo_medio, x='Categoria - N1', y='Tempo de Resolução',
                          title="Tempo Médio de Resolução por Categoria")
        st.plotly_chart(tempo_fig)

    # 10. Distribuição de chamados por hora do dia
    if 'Criado' in filtered_data.columns:
        try:
            # Converter para datetime uma única vez e armazenar
            filtered_data['Data_Criacao'] = pd.to_datetime(
                filtered_data['Criado'],
                dayfirst=True,
                errors='coerce'
            )
            
            # Distribuição por hora
            filtered_data['Hora'] = filtered_data['Data_Criacao'].dt.hour
            hora_data = filtered_data.dropna(subset=['Hora'])
            
            if not hora_data.empty:
                # Gráfico por hora
                hora_count = hora_data.groupby('Hora').size().reset_index(name='Quantidade')
                hora_fig = px.bar(hora_count, x='Hora', y='Quantidade',
                                title="Distribuição de Chamados por Hora do Dia")
                hora_fig.update_traces(text=hora_count['Quantidade'], textposition='inside')
                st.plotly_chart(hora_fig)
                
                # Gráfico por mês
                filtered_data['Mes'] = filtered_data['Data_Criacao'].dt.strftime('%Y-%m')
                mes_count = filtered_data.groupby('Mes').size().reset_index(name='Quantidade')
                mes_fig = px.bar(mes_count, x='Mes', y='Quantidade',
                               title="Distribuição de Chamados por Mês")
                mes_fig.update_traces(text=mes_count['Quantidade'], textposition='inside')
                st.plotly_chart(mes_fig)
            else:
                st.error("Não foi possível extrair as datas da coluna 'Criado'")
                st.write("Verifique se a coluna contém datas válidas")
        except Exception as e:
            st.error(f"Erro ao processar as datas: {str(e)}")
    else:
        st.error("Coluna 'Criado' não encontrada no arquivo")

    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(filtered_data)
    st.download_button(
        "Download dos dados filtrados",
        csv,
        "dados_filtrados.csv",
        "text/csv"
    )

else:
    st.info("Carregue um arquivo Excel para iniciar a análise.")
