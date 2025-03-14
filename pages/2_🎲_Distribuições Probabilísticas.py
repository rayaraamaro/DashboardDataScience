import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotnine import *

# Configuração da página
st.set_page_config(page_title="DataLife Insights", layout="wide")


# Adicionando o logo
st.logo("logo.png")

# Adicionando o logo
st.image("logo.png", width=150)

df = pd.read_csv("student_performance_dataset.csv")

# Criando as sub-abas (pages)
pages = st.sidebar.selectbox("Escolha a Distribuição:", [
    "Distribuição de Bernoulli",
    "Distribuição Binomial",
    "Distribuição de Poisson",
    "Distribuição Normal",
    "Analise seus Dados"
])

st.sidebar.markdown("Desenvolvido por Rayara Amaro Figueiredo RM552635")


# Função para exibir gráfico Plotly
def plot_distribution(x, y, title, xlabel, ylabel):
    fig = go.Figure(data=[go.Bar(x=x, y=y)])
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
    st.plotly_chart(fig)

if pages == "Distribuição de Bernoulli":
    st.header("Distribuição de Bernoulli")
    st.write("A distribuição de Bernoulli modela experimentos com duas possibilidades: sucesso (1) ou fracasso (0). No seu caso, 'Passar' ou 'Reprovar'.")
    st.write("Eu escolhi essa função para ter um bom parâmetro sobre se a rotina e histórico do aluno realmente influenciou no seu resultado final!")
    
    st.latex(r"P(X = x) = p^x (1 - p)^{1-x}, \quad x \in \{0,1\}")
    
    p = df['Pass_Fail'].value_counts(normalize=True)['Pass']
    valores = [0, 1]
    probabilidades = [1 - p, p]
    df_bernoulli = pd.DataFrame({"X": valores, "P(X)": probabilidades}).set_index("X")
    
    col1, col2 = st.columns([0.25, 0.75])

    col1.write("Tabela de Probabilidades:")
    col1.write(df_bernoulli)
    col1.write("A tabela de probabilidades mostra as chances de um aluno passar ou reprovar.")
    

    col2.write("Distribuição de Probabilidades")
    plot_distribution(valores, probabilidades, "Distribuição de Bernoulli", "Resultado", "Probabilidade")

    st.subheader("Conclusão sobre a Distribuição de Bernoulli")
    
    st.write(f"""
        A distribuição de Bernoulli foi aplicada para modelar o desempenho dos alunos no exame final, considerando duas possíveis saídas: 
        **sucesso (aprovação)** ou **fracasso (reprovação)**. 

        Com base nos dados analisados, a probabilidade estimada de um aluno ser aprovado no exame final é **{p:.2f}**, enquanto a 
        probabilidade de reprovação é **{1 - p:.2f}**.  

        O resultado indica que, dentro do conjunto de dados, aproximadamente **{p * 100:.2f}% dos alunos foram aprovados**, enquanto 
        **{(1 - p) * 100:.2f}% foram reprovados**. Isso significa que a taxa de aprovação/reprovação está diretamente relacionada às 
        variáveis analisadas, como tempo de estudo, presença e nível de educação dos pais.  

        Essa análise permite avaliar o impacto das variáveis estudadas no desempenho dos alunos e pode ser útil para identificar fatores 
        críticos que influenciam o sucesso acadêmico.
    """)

# Definir a página de Distribuição Binomial
elif pages == "Distribuição Binomial":
    st.header("Distribuição Binomial")
    st.write("A distribuição binomial modela o número de sucessos em n tentativas independentes.")


    p = df['Pass_Fail'].value_counts(normalize=True)['Pass']
    
    st.latex(r"P(X = k) = \binom{n}{k} p^k (1 - p)^{n-k}")
    st.divider()

    col1, col2 = st.columns([0.5, 0.5])
    
    # Inputs de usuário para o número de tentativas e sucessos
    n_max = col1.number_input("Número máximo de tentativas", value=50)
    n = col1.slider("Número de tentativas (n):", min_value=1, max_value=n_max, value=10, step=1)
    k = col2.slider("Número de sucessos (k):", min_value=0, max_value=n, value=5, step=1)
    p = col2.slider("Probabilidade de sucesso (p):", min_value=0.0, max_value=1.0, value=p, step=0.01)
    
    # Calcular a distribuição binomial
    x = np.arange(0, n + 1)
    y = stats.binom.pmf(x, n, p)
    
    # Tabela de probabilidades
    df_binomial = pd.DataFrame({"X": x, "P(X)": y, "P(X ≤ k) (Acumulado)": np.cumsum(y)}).set_index("X")
    st.write("Tabela de probabilidades:")
    st.write(df_binomial)
    
    # Exibir gráfico da distribuição binomial
    plot_distribution(x, y, "Distribuição Binomial", "Número de sucessos", "Probabilidade")

    st.subheader("Conclusão sobre a Distribuição Binomial")
    prob_acumulada = np.cumsum(y)[k]
    st.write(f"""
        A distribuição binomial foi aplicada para modelar o número de aprovações entre um total de {n} tentativas, 
        considerando uma probabilidade de sucesso (aprovação) de {p:.2f}. 

        Com base nos parâmetros escolhidos, a probabilidade de obter exatamente {k} sucessos é **{y[k]:.4f}**, enquanto 
        a probabilidade acumulada de obter até {k} sucessos (P(X ≤ k)) é **{prob_acumulada:.4f}**.

        Isso significa que, dado o cenário definido, há aproximadamente {prob_acumulada * 100:.2f}% de chance de que **no máximo {k}** 
        alunos sejam aprovados. Essa análise ajuda a entender o desempenho acadêmico dos estudantes e pode ser usada 
        para prever resultados em diferentes contextos educacionais.
    """)

elif pages == "Distribuição de Poisson":
    st.header("Distribuição de Poisson")

    st.subheader("Fórmula da Distribuição de Poisson")
    st.latex(r"P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}")

    col1, col2 = st.columns([0.3,0.7])
    
    # Usar a média da Taxa de Presença (Attendance Rate) como a taxa λ
    lambd = df['Attendance_Rate'].mean()
    x_max = col1.number_input("Número de eventos desejado",min_value=0, step=1,value=20)
    
    # Cálculo da distribuição de Poisson
    x = np.arange(0, x_max)  
    y = stats.poisson.pmf(x, lambd)
    
    # Criar dataframe para exibição
    df_poisson = pd.DataFrame({"X": x, "P(X)": y, "P(X ≤ k) (Acumulado)": np.cumsum(y),
                               "P(X > k) (Acumulado Cauda Direita)": 1-np.cumsum(y)}).set_index("X")
    
    # Exibição da tabela de probabilidades
    col2.write("Tabela de probabilidades:")
    col2.write(df_poisson)
    
    # Exibir gráfico da distribuição de Poisson
    plot_distribution(x, y, "Distribuição de Poisson", "Número de eventos", "Probabilidade")

    st.subheader("Conclusão sobre a Distribuição de Poisson")
    
    st.write(f"""
        A distribuição de Poisson é usada para modelar o número de ocorrências de um evento dentro de um intervalo fixo, 
        dado que os eventos ocorrem de forma independente e a uma taxa constante **λ**. 

        Neste caso, utilizamos a **média da Taxa de Presença dos alunos ({lambd:.2f})** como o valor de **λ**, representando 
        a frequência esperada de presenças em um determinado período.

        Com base nos cálculos, podemos observar que a probabilidade de que exatamente **k** eventos ocorram segue a função 
        de probabilidade de massa de Poisson. Além disso, a tabela apresenta a **probabilidade acumulada** de ocorrer até **k** eventos 
        (P(X ≤ k)), assim como a **probabilidade de exceder k eventos** (P(X > k)).

        Os resultados indicam que a distribuição da presença dos alunos pode ser modelada por Poisson, sugerindo que a 
        frequência de comparecimento segue um padrão previsível. Isso pode ser útil para prever o comportamento dos alunos 
        em função de suas rotinas e hábitos escolares.
    """)

elif pages == "Distribuição Normal":
    st.header("Distribuição Normal")

    st.markdown('''A distribuição normal, também conhecida como distribuição de Gauss, é uma das mais importantes na estatística e na ciência de dados. Ela descreve fenômenos naturais e sociais em que os valores se concentram ao redor de uma média, formando um gráfico em forma de sino. Esse comportamento é comum em diversas situações do dia a dia, como alturas de pessoas, notas em provas e erros de medição em experimentos.''')
    
    # Exibindo a fórmula da distribuição normal
    st.subheader("Fórmula da Distribuição Normal")
    st.latex(r"f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{(x - \mu)^2}{2\sigma^2}}")
    
    # Usando a coluna 'Final_Exam_Score' para calcular a média e desvio padrão
    mu = df['Final_Exam_Score'].mean()
    sigma = df['Final_Exam_Score'].std()
    
    # Gerando os dados da distribuição normal
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
    y = stats.norm.pdf(x, mu, sigma)
    y_cdf = stats.norm.cdf(x, mu, sigma)

    # Exibindo o gráfico da distribuição normal (PDF)
    col1, col2 = st.columns(2)  
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='PDF'))
    fig.update_layout(title="Distribuição Normal", xaxis_title="Notas", yaxis_title="Densidade de Probabilidade")
    col1.plotly_chart(fig)

    # Exibindo o gráfico da distribuição normal acumulada (CDF)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x, y=y_cdf, mode='lines', name='CDF'))
    fig2.update_layout(title="Distribuição Normal Acumulada", xaxis_title="Notas", yaxis_title="Probabilidade Acumulada")
    col2.plotly_chart(fig2)

    # Opção para adicionar uma segunda curva normal
    curva2 = st.checkbox("Adicionar uma segunda curva normal")
    if curva2:
        mu_2 = st.number_input("Média 2 (μ):", value=2.0)
        sigma_2 = st.number_input("Desvio Padrão 2 (σ):", value=1.0, min_value=0.1)
        x_2 = np.linspace(mu_2 - 4*sigma_2, mu_2 + 4*sigma_2, 100)
        y_2 = stats.norm.pdf(x_2, mu_2, sigma_2)
        y_2_cdf = stats.norm.cdf(x_2, mu_2, sigma_2)

        # Gráfico com a segunda curva normal
        fig.add_trace(go.Scatter(x=x_2, y=y_2, mode='lines', name='Curva Normal 2'))
        col1.plotly_chart(fig)

        # Gráfico com a segunda curva acumulada
        fig2.add_trace(go.Scatter(x=x_2, y=y_2_cdf, mode='lines', name='Curva Normal 2 Acumulada'))
        col2.plotly_chart(fig2)

        st.subheader("Conclusão sobre a Distribuição Normal")

    st.write(f"""
        A **distribuição normal** é uma das mais utilizadas na estatística e modelagem de dados, pois muitos fenômenos naturais seguem esse padrão. 
        Ela é caracterizada pela sua forma de sino, com a maioria dos valores concentrados em torno da média.

        Neste caso, analisamos a distribuição das **notas finais dos alunos**, onde:
        - **Média (μ)**: {mu:.2f}
        - **Desvio Padrão (σ)**: {sigma:.2f}

        A distribuição gerada nos gráficos mostra como as notas estão distribuídas, permitindo analisar a dispersão e a concentração dos valores. 
        A curva acumulada (CDF) ajuda a entender a **probabilidade de um aluno obter uma nota até um certo limite**.

        Se a distribuição das notas for aproximadamente normal, podemos inferir que a maioria dos alunos obteve notas próximas à média, 
        com poucos alunos nas extremidades (notas muito baixas ou muito altas). Esse comportamento pode indicar um ensino uniforme e uma avaliação equilibrada.

        Caso a distribuição seja muito assimétrica ou achatada, pode ser necessário revisar fatores como dificuldade da prova, 
        variação no desempenho dos alunos ou até mesmo impactos externos na avaliação.
    """)
        
elif pages == "Analise seus Dados":
    st.header("Análise de Dados")
    st.write("Faça upload do seu arquivo Excel para analisar a distribuição de uma variável numérica.")
    uploaded_file = st.file_uploader("Carregue seu arquivo Excel", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("Amostra dos dados:")
        st.write(df.head())
        
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        if colunas_numericas:
            coluna_escolhida = st.selectbox("Escolha uma coluna numérica:", colunas_numericas)
            
            if coluna_escolhida:
                st.write("Distribuição dos dados:")
                st.write(df[coluna_escolhida].describe())
                
                dist = st.selectbox("Escolha a distribuição para análise:", ["Poisson", "Normal", "Binomial"])
                
                if dist == "Poisson":
                    
                    col1, col2 = st.columns([0.3,0.7])
                    
                    lambda_est = df[coluna_escolhida].mean()

                    x_min = col1.number_input("Número mínimo de eventos",value=0)
                    x_max = col1.number_input("Número máximo de eventos desejado",value=2*lambda_est)
                    
                    x = np.arange(x_min, x_max)
                    y = stats.poisson.pmf(x, lambda_est)
                    y_cdf = stats.poisson.cdf(x,lambda_est)

                    df_poisson = pd.DataFrame({"X": x, "P(X)": y, "P(X ≤ k) (Acumulado)": np.cumsum(y),"P(X > k) (Acumulado Cauda Direita)": 1-np.cumsum(y)}).set_index("X")

                    col2.write("Tabela de probabilidades:")
                    col2.write(df_poisson)
                    
                    st.subheader(f"Estimativa de λ (Taxa média de Ocorrência): {lambda_est:.2f}")
                    prob_acum = st.toggle("Probabilidade Acumulada")
                    if prob_acum:
                        st.write("Probabilidades 'somadas' desde a origem!")
                        y_selec = y_cdf
                        fig = go.Figure(data=[go.Line(x=x, y=y_selec)])
                        fig.update_layout(title="Distribuição de Poisson Acumulada", xaxis_title="Número de eventos", yaxis_title="Probabilidade Acumulada")
                        st.plotly_chart(fig)
                    else:
                        y_selec = y
                        plot_distribution(x, y_selec, "Distribuição de Poisson", "Número de eventos", "Probabilidade")
                    


                    
                elif dist == "Normal":
                    
                    n = df[coluna_escolhida].count()
                    mu_est = df[coluna_escolhida].mean()
                    sigma_est = df[coluna_escolhida].std()
                    st.subheader(f"Estimativa de μ: {mu_est:.2f}, σ: {sigma_est:.2f}")


                    # Create distplot with custom bin_size
                    #colunas_categoricas = df.select_dtypes(include=[np.character]).#columns.tolist()
                    
                    #st.selectbox("Escolha uma variável qualitativa",colunas_categoricas)


                    hist_data = [df[coluna_escolhida].dropna().tolist()]
                    group_labels=['distplot']
                    b_size = st.number_input("Largura de Classe - Histograma",min_value=0.1,value=5.0)

                    fig = ff.create_distplot(
                        hist_data, group_labels, bin_size=b_size)
                    
                    teorica = st.checkbox("Curva teórica")
                    if teorica:

                        # Adicionando a curva da distribuição normal teórica com média e desvio padrão da amostra
                        x = np.linspace(mu_est - 4*sigma_est, mu_est + 4*sigma_est, 100)
                        y = stats.norm.pdf(x, mu_est, sigma_est)

                        # Criando um trace da curva normal
                        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Curva Normal', line=dict(color='red')))
                    
                    st.plotly_chart(fig)

                    p = ggplot(df, aes(sample=coluna_escolhida)) + geom_qq(size=3,colour='red',alpha=0.7) + geom_qq_line()+theme_bw()+labs(x="Quantis Teóricos",y = "Quantis Amostrais", title="Gráfico QQPlot")
                    st.pyplot(ggplot.draw(p))





                
                elif dist in ["Binomial"]:
                    threshold = st.number_input("Defina o limiar para True/False:")
                    p_est = (df[coluna_escolhida] > threshold).mean()
                    k = st.slider("Número de sucessos (k):", min_value=0, max_value=50, value=5, step=1)
                    st.write(f"Estimativa de p: {p_est:.2f}")
                    valores = np.arange(0, k + 1)
                    probabilidades = stats.binom.pmf(valores, k, p_est)
                    plot_distribution(valores, probabilidades, f"Distribuição {dist}", "Resultado", "Probabilidade")
                    df_binomial = pd.DataFrame({"X": valores, "P(X)": probabilidades})
                    st.write("Tabela de probabilidades:")
                    st.write(df_binomial)

                    st.subheader("Conclusão sobre a Análise de Dados")

                    st.write(f"""
                        A funcionalidade de **Análise de Dados** permite ao usuário carregar um arquivo Excel e explorar a distribuição de uma variável numérica. Dependendo da natureza dos dados, diferentes distribuições estatísticas podem ser aplicadas:

                        - **Distribuição de Poisson**: Indicada para modelar eventos que ocorrem em um intervalo fixo, como a frequência de presenças ou ocorrências em um determinado período.  
                        - Estimativa da taxa média de ocorrência (λ): **{lambda_est:.2f}**  
                        - O gráfico mostra a probabilidade de diferentes contagens de eventos ocorrerem dentro do intervalo especificado.

                        - **Distribuição Normal**: Aplicada a variáveis contínuas que seguem uma distribuição simétrica em torno da média, como notas de exames.  
                        - Média estimada (μ): **{mu_est:.2f}**  
                        - Desvio padrão estimado (σ): **{sigma_est:.2f}**  
                        - O histograma apresenta a distribuição empírica dos dados, enquanto a curva teórica ajuda a verificar se os dados seguem uma normalidade.

                        - **Distribuição Binomial**: Usada para modelar o número de sucessos em um conjunto fixo de tentativas independentes, como a probabilidade de um aluno atingir uma determinada nota mínima.  
                        - Probabilidade estimada de sucesso (p): **{p_est:.2f}**  
                        - A tabela e o gráfico mostram a distribuição dos sucessos para diferentes cenários.

                        Essa análise permite visualizar padrões nos dados, identificar tendências e verificar se uma variável segue uma determinada distribuição teórica. Com isso, podemos tomar decisões mais informadas e entender melhor o comportamento dos dados carregados.
                    """)