import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dados",
    page_icon="🏃🏼",
    layout="wide"
)

st.title("Análise dos dados")

st.write("Este projeto busca entender como o desempenho dos alunos (notas nos testes) é afetado por outras variáveis, como Gênero, Etnia, Nível de Educação dos Pais, Almoço e Curso de Preparação para o Teste.")

st.subheader("Perguntas sobre os dados")
st.write(f"""
    - Qual a correlação entre as Horas de Estudo Semanais e a Nota da Prova Final?
    
    O coeficiente de correlação positivo sugere que, em média, alunos que estudam mais tendem a ter um melhor desempenho.
No entanto, como a correlação não é perfeita (1.0), existem outros fatores que também influenciam a nota final, como qualidade do estudo, frequência às aulas e desempenho passado.
    """)
st.write(f"""
    - Estudantes com maior Nível de Educação Parental tendem a ter melhores Notas nas Provas Finais?
    
    Alunos cujos pais têm ensino superior (Bacharelado/Mestrado) tendem a ter notas mais altas do que aqueles cujos pais possuem apenas ensino médio.
Isso pode ocorrer porque pais com maior nível educacional geralmente têm mais condições de ajudar nos estudos ou incentivar práticas mais eficazes de aprendizado.
    """)

st.write(f"""
    - A participação em Atividades Extracurriculares impacta a Taxa de Aprovação dos Estudantes?
         
    Alunos que participam de atividades extracurriculares têm uma taxa de aprovação ligeiramente maior.
No entanto, a diferença não é muito grande, indicando que as atividades extracurriculares podem contribuir para o sucesso acadêmico, mas não são o fator principal.
    """)

st.subheader("Este conjunto de dados consiste nas notas obtidas pelos alunos em várias disciplinas:")
st.write(" - Gênero: sexo dos alunos → (Masculino/Feminino)")
st.write(" - Raça/Etnia: etnia dos alunos → (Grupo A, B, C, D, E)")
st.write(" - Nível de educação dos pais: nível de educação final dos pais → (Bacharelado, Alguma faculdade, Mestrado, Grau de associado, Ensino médio)")
st.write(" - Almoço: refeição antes do teste → (Padrão ou Gratuito)")



if 'data' not in st.session_state:
    file_path = 'student_performance_dataset.csv'
    st.session_state['data'] = pd.read_csv(file_path)

df = st.session_state["data"]

# Filtragem por tipo de resultado
tipos = ['Todos']
tipos = np.append(tipos, df["Pass_Fail"].unique())
tipo = st.sidebar.selectbox("Tipo de Resultado", tipos)
st.sidebar.markdown("Desenvolvido por Rayara Amaro Figueiredo RM552635")

if tipo == 'Todos':
    df_filtered = df
else:
    df_filtered = df[df["Pass_Fail"] == tipo]

st.dataframe(df_filtered,
             column_config={
                 "Final_Exam_Score": st.column_config.ProgressColumn(
                     "Nota Final", format="%f", min_value=0, max_value=int(df_filtered["Final_Exam_Score"].max()))
             })

st.subheader("Correlação entre as Variáveis")

# Seleção de variáveis numéricas para análise de correlação
variaveis_numericas = ["Study_Hours_per_Week", "Attendance_Rate", "Past_Exam_Scores", "Final_Exam_Score"]
df_corr = df_filtered[variaveis_numericas].corr()

# Exibir a matriz de correlação
st.write("A matriz de correlação abaixo mostra a relação entre as variáveis numéricas. Valores próximos de 1 indicam correlações fortes e positivas, enquanto valores próximos de -1 indicam correlações fortes e negativas.")
st.dataframe(df_corr.style.background_gradient(cmap="coolwarm"))

# Exibir o heatmap de correlação com Seaborn
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(df_corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)



# Cálculo das estatísticas descritivas
stats = {
    "Média": df_filtered[["Study_Hours_per_Week", "Attendance_Rate", "Past_Exam_Scores", "Final_Exam_Score"]].mean(),
    "Mediana": df_filtered[["Study_Hours_per_Week", "Attendance_Rate", "Past_Exam_Scores", "Final_Exam_Score"]].median(),
    "Moda": df_filtered[["Study_Hours_per_Week", "Attendance_Rate", "Past_Exam_Scores", "Final_Exam_Score"]].mode().iloc[0]
}

st.subheader("Distribuição dos Dados:")
st.write("Para horas de estudo por semana, a média e a mediana são próximas, indicando uma distribuição relativamente simétrica. A moda sendo 35 sugere que um número significativo de alunos estuda essa quantidade de horas.")
st.write("A taxa de presença apresenta duas modas, indicando que há dois grupos distintos de alunos com frequências comuns em torno de 84.69% e 91.83%.")
st.write("As notas de exames anteriores são ligeiramente assimétricas, pois a moda é menor que a média e a mediana. Isso pode indicar uma concentração de alunos com notas um pouco mais baixas.")
st.write("A nota do exame final tem moda em 50, que pode sugerir que muitos alunos tiveram notas medianas, possivelmente refletindo dificuldades no exame final.")

# Criar DataFrame das estatísticas
df_stats = pd.DataFrame(stats)

st.subheader("Estatísticas Descritivas")
st.dataframe(df_stats)

st.subheader("Classificação Estatística das Variáveis:")

variaveis = [
    {"Variável": "Gênero", "Tipo": "Qualitativa Nominal"},
    {"Variável": "Horas_Estudo_Semana", "Tipo": "Quantitativa Discreta"},
    {"Variável": "Taxa_Frequencia", "Tipo": "Quantitativa Contínua"},
    {"Variável": "Notas_Provas_Anteriores", "Tipo": "Quantitativa Discreta"},
    {"Variável": "Nivel_Educacao_Parental", "Tipo": "Qualitativa Ordinal"},
    {"Variável": "Acesso_Internet_Casa", "Tipo": "Qualitativa Nominal"},
    {"Variável": "Atividades_Extracurriculares", "Tipo": "Qualitativa Nominal"},
    {"Variável": "Nota_Prova_Final", "Tipo": "Quantitativa Discreta"},
    {"Variável": "Aprovado_Reprovado", "Tipo": "Qualitativa Nominal"}
]
st.dataframe(variaveis)

st.write("""
### Principais Observações:
- A correlação entre **Horas de Estudo por Semana** e **Nota da Prova Final** indica o impacto do tempo de estudo no desempenho acadêmico.
- A **Taxa de Presença** pode influenciar as **Notas de Provas Anteriores** e o **Desempenho Final**.
- As **Notas de Provas Anteriores** geralmente apresentam uma forte correlação com o **Resultado Final**, sugerindo que o histórico acadêmico é um bom preditor de desempenho.
""")