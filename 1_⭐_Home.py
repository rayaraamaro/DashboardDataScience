import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo

if "data" not in st.session_state:
    df = pd.read_csv("student_performance_dataset.csv", index_col="Student_ID")
    print(df.columns)
    df = df.sort_values(by="Final_Exam_Score", ascending=False)
    st.session_state["data"] = df


# Configuração da página
st.set_page_config(page_title="DataLife Insights", layout="wide")
st.sidebar.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/rayaraamaro/)")
st.sidebar.markdown("Desenvolvido por Rayara Amaro Figueiredo RM552635")

# Adicionando logo com streamlit-extras
# add_logo("logo.jpeg")

# Adicionando o logo
st.logo("logo.png")

# Adicionando o logo no body
# st.image("logo.png", width=150)

import streamlit as st

col1, col2 = st.columns([1, 3])

with col1:
    st.image("ray.png", width=250)

with col2:
    st.title("Statistics by Rayara Amaro")
    st.write("Olá! Meu nome é Rayara Amaro, tenho 22 anos e estudo Engenharia de Software. Trabalho como estagiária na IBM, na área de Inteligência Artificial, desenvolvendo projetos para parceiros. Minhas melhores linguagens e skills é Python e Watsonx Assistant - Assistente com IA da IBM. Uma softskill que possuo e gosto muito é ser extrovertida e saber conversar! Além de ser uma boa ouvinte e saber receber feedbacks.")
    st.write("Sempre tive interesse em entender como estudar de um jeito mais eficiente, o que me levou a pesquisar sobre aprendizado e otimização do estudo. Isso me ajudou a conseguir uma bolsa de 100% na FIAP e hoje continuo explorando esse tema. Nesse momento, vamos analisar um banco de dados sobre rotinas e hábitos de estudantes de alta performance para entender o que realmente faz diferença no dia a dia.")
   
st.write("Fora do mundo da tecnologia e dos estudos, sou apaixonada por gatos, curto tudo relacionado a beleza e cosméticos, gosto de treinar na academia, jogar League of Legends e acompanhar animes – Spy x Family está entre os meus favoritos.")

st.write("No fim, estou sempre buscando aprender e melhorar, seja no trabalho, nos estudos ou nas coisas que gosto de fazer no tempo livre.")

st.write(":star: Um bom lofi é essencial para bons estudos! :star:")

st.video("https://www.youtube.com/watch?v=r5lLHzCZ8IE")

