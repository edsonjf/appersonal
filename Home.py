import streamlit as st
import pandas as pd

st.set_page_config(layout= 'centered')

st.title('Personal :man-lifting-weights:')

dados = pd.read_json('dados/dados.json')

def creds_entered():
    if st.session_state['user'].strip() in dados['Alunos'] and st.session_state['passwd'].strip() == dados['Alunos'][st.session_state['user']]['senha']:
        st.session_state['autenticado'] = True
    else:
        st.session_state['autenticado'] = False
        if not st.session_state["passwd"]:
            st.warning("Entrar com a senha!")
        elif not st.session_state["user"]:
            st.warning("Entrar com o usuário!")
        else:
            st.error('Senha ou Usuário invlido')

def autenticacao_usuario():
    if "autenticado" not in st.session_state:
        st.text_input(label="Username :", value="", key="user", on_change=creds_entered)
        st.text_input(label="Password :", value="", key="passwd", type="password", on_change=creds_entered)
        return False
    else:
        if st.session_state['autenticado']:
        
            return True
        else:
            st.text_input(label="Username :", value="", key="user", on_change=creds_entered)
            st.text_input(label="Password :", value="", key="passwd", type="password", on_change=creds_entered)
            return False

if autenticacao_usuario():
    
    aba1, aba2 = st.tabs(['Home', 'Meus Treinos'])
    usuario = st.session_state['user']
    #usuario = st.session_state['user']
    aluno = dados['Alunos'][usuario]
    with aba1:
        col1, col2 = st.columns([2,1])
        with col1:
            col1.metric('Nome', value=aluno['nome'] )
            col1.metric('Nome Completo', aluno['nome_completo'])
            col1.metric('Altura', aluno['altura'])
        with col2:
            col2.metric('Idade', aluno['idade'])
            col2.metric('Peso', aluno['peso'])
            col2.metric('IMC'), aluno['IMC']

    with aba2:
        
        treinos_disponiveis = []
        for tipo_treino in dados['Treinos'][usuario].keys():
            treinos_disponiveis.append(tipo_treino)
        
        page = st.radio('Treinos Disponíveis', treinos_disponiveis, horizontal=True)
        st.subheader('Esse é o seu treino:')
        #st.write('Page retorna: ', treinos_disponiveis)
        treino = dados['Treinos'][usuario]

        coluna1, coluna2, coluna3, coluna4  = st.columns([4,1,1,1])
        with coluna1:
            for i in treino[page]:
                coluna1.metric(i, treino[page][i]['exercicio'])
                coluna2.metric('Séries', treino[page][i]['series'])
                coluna3.metric('Repetições', treino[page][i]['repeticoes']) 
                coluna4.metric('Carga', treino[page][i]['carga'])