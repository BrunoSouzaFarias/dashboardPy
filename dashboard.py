import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração inicial do Streamlit
st.set_page_config(page_title="Dashboard de Chamados", layout="wide")
st.title("Dashboard de Chamados")

# Upload de arquivo Excel
st.sidebar.header("Carregar Arquivo Excel")
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Carregar dados do Excel em um DataFrame
    df = pd.read_excel(uploaded_file)

    # Exibir as colunas do arquivo Excel
    st.write("Colunas encontradas no arquivo Excel:", df.columns)

    # Filtros interativos
    st.sidebar.header("Filtros")
    unidade_filter = st.sidebar.multiselect("Selecione as Unidades", options=df["Unidade"].unique(), default=df["Unidade"].unique())
    chave_filter = st.sidebar.multiselect("Selecione as Chaves", options=df["Chave"].unique(), default=df["Chave"].unique())

    # Aplicar filtros
    filtered_data = df[(df["Unidade"].isin(unidade_filter)) & (df["Chave"].isin(chave_filter))]

    # Verificar se as colunas esperadas estão no arquivo
    expected_columns = ["Tipo de item", "Chave", "Categoria - N1", "Criador", "Resumo", "Status", "Unidade", "Tipo", "Escalonado", "Entrada do chamado"]
    if all(col in df.columns for col in expected_columns):
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
            escalonado_count = filtered_data[filtered_data["Status"] == "Escalonado"].shape[0]
            total_count = len(filtered_data)
            escalonado_data = pd.DataFrame({
                "Status": ["Escalonado", "Outros"],
                "Quantidade": [escalonado_count, total_count - escalonado_count]
            })
            escalonado_pie_fig = px.pie(escalonado_data, names="Status", values="Quantidade", title="Distribuição de Chamados Escalonados")
            escalonado_pie_fig.update_traces(textinfo="percent+label+value")  # Adiciona quantidade e porcentagem
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

        # 5. Chamados Concluídos (não Escalonados)
        concluidos_nao_escalonados_count = filtered_data[(filtered_data["Status"] == "CONCLUÍDO") & (filtered_data["Status"] != "Escalonado")].shape[0]
        concluidos_nao_escalonados_data = pd.DataFrame({
            "Status": ["Concluídos Não Escalonados", "Outros"],
            "Quantidade": [concluidos_nao_escalonados_count, total_count - concluidos_nao_escalonados_count]
        })
        concluidos_nao_escalonados_pie_fig = px.pie(concluidos_nao_escalonados_data, names="Status", values="Quantidade", title="Distribuição de Chamados Concluídos (Não Escalonados)")
        concluidos_nao_escalonados_pie_fig.update_traces(textinfo="percent+label+value")  # Adiciona quantidade e porcentagem
        st.plotly_chart(concluidos_nao_escalonados_pie_fig)

        # 6. Chamados por Entrada do Chamado (sem a divisão por Unidade)
        entrada_count = filtered_data.groupby('Entrada do chamado').size().reset_index(name='Quantidade')

        # Gráfico de Barra (sem a divisão por Unidade)
        entrada_fig = px.bar(entrada_count, x='Entrada do chamado', y='Quantidade', 
                     title="Quantidade Total de Chamados por Entrada do Chamado")
        entrada_fig.update_traces(text=entrada_count['Quantidade'], textposition='inside')  # Adiciona quantidade dentro das barras
        st.plotly_chart(entrada_fig)

    else:
        st.error("O arquivo Excel não contém as colunas esperadas. Verifique a estrutura do arquivo.")
else:
    st.info("Carregue um arquivo Excel para iniciar a análise.")
