import streamlit as st
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import pandas as pd
import plotly.express as px

# Configuração da página com título e ícone
st.set_page_config(page_title="Calculadora de Transporte Fácil", page_icon="🚚", layout="centered")

# Estilização CSS para apelo visual e tamanho aproximado de 800x600px
st.markdown("""
    <style>
    .main { max-width: 800px; max-height: 600px; margin: auto; }
    .stButton>button { background-color: #4CAF50; color: white; font-weight: bold; }
    .stNumberInput>label { font-size: 16px; color: #333; }
    .stSuccess { background-color: #e6ffe6; padding: 10px; border-radius: 5px; }
    .stError { background-color: #ffe6e6; padding: 10px; border-radius: 5px; }
    .title { color: #2E7D32; text-align: center; font-size: 32px; }
    .subtitle { color: #555; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# Título e descrição amigáveis
st.markdown('<h1 class="title">Calculadora de Transporte Fácil 🚚</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Descubra a forma mais barata de enviar produtos!</p>', unsafe_allow_html=True)

# Divisão em duas colunas para entrada de dados
col1, col2 = st.columns(2)

# Entrada de custos com dicas (tooltips)
with col1:
    st.subheader("💰 Custos por Rota (€)")
    custo_x12 = st.number_input("Fábrica 1 ➡️ Cidade 2", min_value=0.0, value=4.0, step=0.1, 
                                help="Custo por unidade enviada da Fábrica 1 para a Cidade 2")
    custo_x13 = st.number_input("Fábrica 1 ➡️ Cidade 3", min_value=0.0, value=6.0, step=0.1, 
                                help="Custo por unidade enviada da Fábrica 1 para a Cidade 3")
    custo_x22 = st.number_input("Fábrica 2 ➡️ Cidade 2", min_value=0.0, value=8.0, step=0.1, 
                                help="Custo por unidade enviada da Fábrica 2 para a Cidade 2")
    custo_x23 = st.number_input("Fábrica 2 ➡️ Cidade 3", min_value=0.0, value=3.0, step=0.1, 
                                help="Custo por unidade enviada da Fábrica 2 para a Cidade 3")

# Entrada de oferta e demanda com emojis
with col2:
    st.subheader("📦 Quantidades")
    oferta_o1 = st.number_input("Disponível na Fábrica 1", min_value=0, value=100, step=10, 
                                help="Quantidade total que a Fábrica 1 pode enviar")
    oferta_o2 = st.number_input("Disponível na Fábrica 2", min_value=0, value=150, step=10, 
                                help="Quantidade total que a Fábrica 2 pode enviar")
    demanda_d2 = st.number_input("Necessário na Cidade 2", min_value=0, value=80, step=10, 
                                 help="Quantidade mínima que a Cidade 2 precisa receber")
    demanda_d3 = st.number_input("Necessário na Cidade 3", min_value=0, value=120, step=10, 
                                 help="Quantidade mínima que a Cidade 3 precisa receber")

# Botão estilizado para calcular
if st.button("Calcular Melhor Plano", key="optimize"):
    with st.spinner("Calculando o plano mais econômico..."):  # Animação de carregamento
        # Cria o problema de otimização
        prob = LpProblem("Transporte", LpMinimize)

        # Variáveis de decisão
        x12 = LpVariable("X12", lowBound=0)
        x13 = LpVariable("X13", lowBound=0)
        x22 = LpVariable("X22", lowBound=0)
        x23 = LpVariable("X23", lowBound=0)

        # Custos inseridos pelo usuário
        custos = {'X12': custo_x12, 'X13': custo_x13, 'X22': custo_x22, 'X23': custo_x23}

        # Função objetivo: minimizar custo
        prob += lpSum(custos[var.name] * var for var in [x12, x13, x22, x23])

        # Restrições
        prob += x12 + x13 <= oferta_o1
        prob += x22 + x23 <= oferta_o2
        prob += x12 + x22 >= demanda_d2
        prob += x13 + x23 >= demanda_d3

        # Resolve
        status = prob.solve()

        # Resultados
        if status == 1:  # Solução ótima
            custo_total = value(prob.objective)
            st.markdown('<div class="stSuccess">✅ Plano econômico encontrado!</div>', unsafe_allow_html=True)
            st.write(f"**Custo Total:** €{custo_total:.2f}")

            # Tabela de resultados
            resultados = {
                "Rota": ["Fábrica 1 ➡️ Cidade 2", "Fábrica 1 ➡️ Cidade 3", 
                         "Fábrica 2 ➡️ Cidade 2", "Fábrica 2 ➡️ Cidade 3"],
                "Quantidade": [x12.varValue, x13.varValue, x22.varValue, x23.varValue]
            }
            df = pd.DataFrame(resultados)
            st.table(df.style.format({"Quantidade": "{:.1f}"}))

            # Gráfico interativo com animação
            fig = px.bar(df, x="Rota", y="Quantidade", 
                         title="📊 Quantidade Enviada por Rota", 
                         text=df["Quantidade"].round(1), 
                         color="Rota", 
                         height=350, width=700,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_traces(textposition='auto', marker=dict(line=dict(width=1, color='DarkSlateGrey')))
            fig.update_layout(showlegend=False, transition={'duration': 500})
            st.plotly_chart(fig)

        else:
            st.markdown('<div class="stError">❌ Algo deu errado! Verifique os números.</div>', unsafe_allow_html=True)

# Rodapé com instruções simples
st.markdown("---")
st.write("💡 **Como usar:** Insira os custos e quantidades, clique em 'Calcular' e veja o plano mais barato!")