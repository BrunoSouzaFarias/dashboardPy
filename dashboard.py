import pandas as pd
import streamlit as st
import plotly.express as px

# Cria o aplicativo Streamlit
st.set_page_config(page_title="Dashboard de Chamados", layout="wide")
st.title("Dashboard de Chamados")

# Upload de arquivo Excel
st.sidebar.header("Carregar Arquivo Excel")
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Carrega os dados do Excel para um DataFrame
    df = pd.read_excel(uploaded_file)

    # Exibe as colunas do arquivo Excel para ajudar na verificação
    st.write("Colunas encontradas no arquivo Excel:", df.columns)

    # Filtros interativos
    st.sidebar.header("Filtros")
    unidade_filter = st.sidebar.multiselect("Selecione as Unidades", options=df["Unidade"].unique(), default=df["Unidade"].unique())
    chave_filter = st.sidebar.multiselect("Selecione as Chaves", options=df["Chave"].unique(), default=df["Chave"].unique())

    # Filtra os dados com base nos filtros selecionados
    filtered_data = df[(df["Unidade"].isin(unidade_filter)) & (df["Chave"].isin(chave_filter))]

    # Verifica se o arquivo tem as colunas esperadas
    expected_columns = ["Tipo de item", "Chave", "Categoria - N1", "Criador", "Resumo", "Status", "Unidade", "Tipo", "Entrada do chamado"]
    if all(col in df.columns for col in expected_columns):
        # Mostra os dados filtrados
        st.dataframe(filtered_data)

        # KPIs
        st.header("KPIs")
        st.metric("Total de Chamados", len(filtered_data))
        st.metric("Chamados Concluídos", len(filtered_data[filtered_data["Status"] == "CONCLUÍDO"]))

        # Gráficos

        # 1. Porcentagem de Chamados Concluídos vs Pendentes
        status_count = filtered_data["Status"].value_counts().reset_index()
        status_count.columns = ["Status", "Quantidade"]
        status_fig = px.pie(status_count, names="Status", values="Quantidade", title="Distribuição de Chamados (Concluídos vs Pendentes)")
        st.plotly_chart(status_fig)

        # 2. Chamados por Técnico N1 Responsável (Concluídos vs Pendentes)
        tecnico_status = filtered_data.groupby(['Criador', 'Status']).size().reset_index(name='Quantidade')
        tecnico_fig = px.bar(tecnico_status, x='Criador', y='Quantidade', color='Status', 
                             title="Chamados por Técnico N1 Responsável (Concluídos vs Pendentes)", 
                             barmode='stack')
        st.plotly_chart(tecnico_fig)

        # 3. Chamados por Categoria - N1
        categoria_count = filtered_data["Categoria - N1"].value_counts().reset_index()
        categoria_count.columns = ["Categoria - N1", "Quantidade"]
        categoria_fig = px.bar(categoria_count, x="Categoria - N1", y="Quantidade", title="Distribuição de Chamados por Categoria")
        st.plotly_chart(categoria_fig)

        # 4. Chamados Concluídos por Unidade
        concluded_by_unidade = filtered_data[filtered_data["Status"] == "CONCLUÍDO"]["Unidade"].value_counts().reset_index()
        concluded_by_unidade.columns = ["Unidade", "Quantidade"]
        concluded_by_unidade_fig = px.bar(concluded_by_unidade, x="Unidade", y="Quantidade", title="Chamados Concluídos por Unidade")
        st.plotly_chart(concluded_by_unidade_fig)

        # 5. Chamados por Chave
        chave_count = filtered_data["Chave"].value_counts().reset_index()
        chave_count.columns = ["Chave", "Quantidade"]
        chave_fig = px.bar(chave_count, x="Chave", y="Quantidade", title="Chamados por Chave")
        st.plotly_chart(chave_fig)

        # 6. Chamados por Tipo
        tipo_count = filtered_data["Tipo"].value_counts().reset_index()
        tipo_count.columns = ["Tipo", "Quantidade"]
        tipo_fig = px.bar(tipo_count, x="Tipo", y="Quantidade", title="Distribuição de Chamados por Tipo")
        st.plotly_chart(tipo_fig)
        
    else:
        st.error("O arquivo Excel não contém as colunas esperadas. Verifique a estrutura do arquivo.")
else:
    st.info("Carregue um arquivo Excel para iniciar a análise.")
