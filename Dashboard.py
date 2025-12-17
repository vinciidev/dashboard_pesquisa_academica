import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Estatístico",
    layout="wide"
)

with st.sidebar:
    st.image("assets/3.jpg", width=180)
    st.markdown("## Pesquisa de Probabilidade e Estatística")
    st.markdown("**Discente:** Pedro Vinicius Barbosa Araújo")
    st.markdown("**Professor:** Jailson de Araujo Rodrigues")
    st.markdown("**Instituição:** Instituto Federal da Bahia")
    st.markdown("---")
    st.markdown("Análise estatística desenvolvida com Pandas e Streamlit - Projeto fictício")
    st.markdown("Matéria: Probabilidade e Estatística")


# Carregar CSV
df = pd.read_csv("dados_pesquisa_ia.csv")

st.title("📊 Dashboard Estatístico")

st.write("Pesquisa fictícia sobre o uso de Assistentes de IA no ambito acadêmico e profissional.")

# ======================
# TABELA DE DADOS
# ======================
st.subheader("Dados simulados da pesquisa")
st.dataframe(df)

# ======================
# MEDIDAS ESTATÍSTICAS
# ======================

# Seleção das variáveis quantitativas
colunas_quant = ["Idade", "Horas_IA_Dia", "Frequencia_Semanal"]

# Estatísticas básicas
stats = df[colunas_quant].describe().T

# Adiciona a moda
stats["Moda"] = df[colunas_quant].mode().iloc[0]

stats = stats.drop(columns=["25%", "75%"])

# Renomeia colunas para português
stats = stats.rename(columns={
    "count": "Quantidade",
    "mean": "Média",
    "std": "Desvio Padrão",
    "min": "Mínimo",
    "50%": "Mediana",
    "max": "Máximo"
})

st.subheader("Medidas Estatísticas das Variáveis Quantitativas")
st.dataframe(stats.round(2), use_container_width=True)

st.markdown("""
**Justificativa:**  
As medidas de tendência central (média, mediana e moda) permitem identificar valores típicos do grupo analisado, 
enquanto o desvio padrão indica o grau de dispersão dos dados. Essas técnicas são apropriadas para compreender 
o comportamento geral do público em relação ao uso de assistentes de IA.
""")

# ======================
# GRÁFICOS
# ======================
st.subheader("📈 Análises Gráficas")

col1, col2 = st.columns(2)

with col1:
    faixas = pd.cut(
        df["Idade"],
        bins=[18, 25, 30, 35, 40, 50],
        labels=["18-25", "26-30", "31-35", "36-40", "40+"]
    )

    idade_faixa = faixas.value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(idade_faixa.index, idade_faixa.values)
    ax.set_xlabel("Faixa Etária")
    ax.set_ylabel("Quantidade de pessoas")
    ax.set_title("Distribuição por Faixa Etária")

    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df["Horas_IA_Dia"], bins=[0,1,2,3,4,5,6], edgecolor="black")
    ax.set_xlabel("Horas por dia")
    ax.set_ylabel("Quantidade de pessoas")
    ax.set_title("Quantidade de Usuários por Tempo Diário de Uso")

    st.pyplot(fig)

# Gráfico de linha para Frequência Semanal
col5, col6 = st.columns(2)

with col5:
    # Agrupa e conta frequências
    freq_count = df["Frequencia_Semanal"].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(freq_count.index, freq_count.values, marker='o', linewidth=2, markersize=8)
    ax.set_xlabel("Dias por semana")
    ax.set_ylabel("Quantidade de pessoas")
    ax.set_title("Frequência de Uso Semanal")
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

with col6:
    # Gráfico de uso por nível de experiência
    uso_por_nivel = df.groupby("Nivel_Experiencia")["Horas_IA_Dia"].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.barh(uso_por_nivel.index, uso_por_nivel.values, color=['#0b1c2d', '#123c5a', '#1f77b4', '#7fd3f7'])
    ax.set_xlabel("Média de Horas por Dia")
    ax.set_ylabel("Nível de Experiência")
    ax.set_title("Uso Médio Diário por Senioridade")
    
    # Adiciona valores nas barras
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}h', 
                ha='left', va='center', fontsize=9, fontweight='bold')
    
    st.pyplot(fig)

# ======================
# VARIÁVEIS QUALITATIVAS
# ======================
st.subheader("📊 Variáveis Qualitativas")

col3, col4 = st.columns(2)

with col3:
    sexo_count = df["Sexo"].value_counts().reset_index()
    sexo_count.columns = ["Sexo", "Quantidade"]

    fig = px.pie(
        sexo_count,
        names="Sexo",
        values="Quantidade",
        hole=0.5,
        color="Sexo",
        color_discrete_map={
            "Masculino": "#1f77b4",  # azul
            "Feminino": "#ff69b4"    # rosa
        }
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}",
        textinfo="none"  # remove texto fixo
    )

    fig.update_layout(
        title="Distribuição por Sexo",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:
    nivel_count = df["Nivel_Experiencia"].value_counts().reset_index()
    nivel_count.columns = ["Nivel_Experiencia", "Quantidade"]

    cores = {
        "Sênior": "#0b1c2d",     # azul marinho
        "Pleno": "#123c5a",      # azul médio escuro
        "Júnior": "#1f77b4",     # azul padrão
        "Estudante": "#7fd3f7"   # azul claro / ciano
    }

    fig = px.pie(
        nivel_count,
        names="Nivel_Experiencia",
        values="Quantidade",
        hole=0.5,
        color="Nivel_Experiencia",
        color_discrete_map=cores
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Quantidade: %{value}<br>"
            "Percentual: %{percent}"
        ),
        textinfo="none"  # remove texto fixo
    )

    fig.update_layout(
        title="Nível de Experiência dos participantes",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# ANÁLISE DESCRITIVA
# ======================
st.subheader("Análise dos Resultados")

st.markdown("""
Os resultados indicam que a maior parte dos participantes simulados utilizam assistentes de IA de forma recorrente ao longo da semana, 
com tempo diário médio significativo. No caso observado existe um equilibrio nas faixas etárias, com predominância de jovens e adultos,
o que é compatível com o perfil do público-alvo da área de tecnologia.

O nível de experiência mostra predominância de estudantes e profissionais em início de carreira, sugerindo que 
a IA é utilizada como ferramenta de apoio ao aprendizado e à produtividade. O gráfico de uso por senioridade 
revela padrões interessantes sobre quais grupos utilizam mais intensamente as ferramentas de IA no seu dia a dia.
""")