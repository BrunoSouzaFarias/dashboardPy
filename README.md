# 📊 Dashboard de Análise de Chamados

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0.0+-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-green.svg)
![Pandas](https://img.shields.io/badge/Pandas-1.0+-yellow.svg)

## 🎯 Sobre o Projeto

Dashboard interativo para análise de chamados de suporte técnico, desenvolvido com Python e Streamlit. Oferece visualizações detalhadas e insights importantes sobre o fluxo de atendimento.

## ✨ Funcionalidades

- 📈 **Análises Visuais**:
  - Distribuição de chamados por status
  - Análise de escalonamentos
  - Desempenho por técnico
  - Categorização de chamados
  - Tendências temporais

- 🔍 **Filtros Dinâmicos**:
  - Por unidade
  - Por categoria
  - Por período
  - Por status

- 📊 **Métricas Principais**:
  - Total de chamados
  - Taxa de resolução
  - Tempo médio de atendimento
  - Distribuição por horário

## 🚀 Como Usar

1. **Instalação das Dependências**:
 bash
pip install -r requirements.txt


2. **Executando o Dashboard**:
bash
streamlit run dashboard.py


3. **Carregando os Dados**:
   - Faça upload de um arquivo Excel (.xlsx)
   - Os dados serão automaticamente processados e visualizados

## 📋 Requisitos do Arquivo Excel

O arquivo deve conter as seguintes colunas:
- Tipo de item
- Chave
- Categoria - N1
- Status
- Criado
- Técnico N1 Responsável
- Unidade
- Escalonado

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)

## 📈 Screenshots

[Aqui você pode adicionar algumas screenshots do seu dashboard em ação]

## 🤝 Contribuições

Contribuições são sempre bem-vindas! Sinta-se à vontade para:
- 🐛 Reportar bugs
- 💡 Sugerir novas funcionalidades
- 📖 Melhorar a documentação

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

Bruno Souza Farias

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/bruno-souza-farias/)](https://www.linkedin.com/in/bruno-souza-farias/)
[![GitHub](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=Github&logoColor=white&link=https://github.com/BrunoSouzaFarias)](https://github.com/BrunoSouzaFarias)

---

⭐️ Se este projeto te ajudou, considere dar uma estrela!
