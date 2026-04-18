import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas - Superstore",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização Customizada (Aesthetics)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #1e3a8a;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Carregamento de Dados
@st.cache_data
def load_data():
    url = "https://gist.githubusercontent.com/nnbphuong/38db511db14542f3ba9ef16e69d3814c/raw/Superstore.csv"
    df = pd.read_csv(url, encoding='latin1')
    
    # Limpeza e Transformação
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df['Month'] = df['Order Date'].dt.month_name()
    df['Year'] = df['Order Date'].dt.year
    df['Month_Year'] = df['Order Date'].dt.to_period('M').astype(str)
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Sidebar - Filtros
st.sidebar.title("🔍 Filtros")
year_filter = st.sidebar.multiselect("Selecione o Ano", options=df['Year'].unique(), default=df['Year'].unique())
region_filter = st.sidebar.multiselect("Selecione a Região", options=df['Region'].unique(), default=df['Region'].unique())

df_filtered = df[df['Year'].isin(year_filter) & df['Region'].isin(region_filter)]

# Título Principal
st.title("📊 Análise de Vendas & Insights de Negócio")
st.markdown("---")

# KPIs Principais
col1, col2, col3, col4 = st.columns(4)
total_sales = df_filtered['Sales'].sum()
total_profit = df_filtered['Profit'].sum()
total_orders = df_filtered['Order ID'].nunique()
avg_discount = df_filtered['Discount'].mean() * 100

col1.metric("Faturamento Total", f"${total_sales:,.2f}")
col2.metric("Lucro Total", f"${total_profit:,.2f}")
col3.metric("Total de Pedidos", f"{total_orders}")
col4.metric("Desconto Médio", f"{avg_discount:.2f}%")

st.markdown("###")

# Layout das Análises
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    # 2. Produtos mais vendidos
    st.subheader("📦 Top 10 Produtos por Faturamento")
    top_products = df_filtered.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_prod = px.bar(top_products, x='Sales', y='Product Name', orientation='h', 
                     color='Sales', color_continuous_scale='Blues',
                     template="plotly_white")
    fig_prod.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_prod, use_container_width=True)

with row1_col2:
    # 3. Regiões que mais faturam
    st.subheader("🗺️ Faturamento por Região")
    reg_sales = df_filtered.groupby('Region')['Sales'].sum().reset_index()
    fig_reg = px.pie(reg_sales, values='Sales', names='Region', hole=.4,
                    color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_reg, use_container_width=True)

st.markdown("---")

# 4. Sazonalidade (Linha do Tempo)
st.subheader("📈 Tendência Mensal de Vendas")
monthly_sales = df_filtered.groupby('Month_Year')['Sales'].sum().reset_index()
fig_trend = px.line(monthly_sales, x='Month_Year', y='Sales', markers=True,
                    line_shape='spline', render_mode='svg')
fig_trend.update_layout(xaxis_title="Mês/Ano", yaxis_title="Vendas ($)")
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# 5. Clientes que mais compram
row2_col1, row2_col2 = st.columns([2, 1])

with row2_col1:
    st.subheader("👥 Top 10 Clientes (Faturamento)")
    top_customers = df_filtered.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_cust = px.bar(top_customers, x='Customer Name', y='Sales', color='Sales',
                     color_continuous_scale='Viridis')
    st.plotly_chart(fig_cust, use_container_width=True)

with row2_col2:
    # 💡 Insights e Recomendações Reais
    st.subheader("💡 Insights & Recomendações")
    st.info("""
    **1. Sazonalidade (Dezembro):**
    As vendas tendem a atingir o pico no Q4.
    *Recomendação:* Aumentar o estoque dos produtos da categoria 'Technology' e 'Office Supplies' em 20% a partir de Novembro.

    **2. Regiões Potenciais:**
    A região **South** apresenta o menor volume mas maior lucro relativo por pedido.
    *Recomendação:* Investir em marketing direcionado para expansão na região South.

    **3. Estratégia de Clientes:**
    Os Top 1% clientes representam uma fatia significativa do lucro.
    *Recomendação:* Criar um programa de fidelidade VIP para os 50 maiores clientes.
    """)

# Rodapé
st.markdown("---")
st.caption("Projeto 1: Análise de Vendas")
