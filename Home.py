import streamlit as st
import pandas as pd

dados = pd.read_json('dados/dados.json')

st.set_page_config(layout= 'centered')

headerSection = st.container()
homeSection = st.container()
loginSection = st.container()
logoutSection = st.container()

def login_page():
    with loginSection:        
        if st.session_state['loggedIn'] == False:
            userName = nome()
            password = senha()
            LoginButtonClicked = st.button('Login')
            if LoginButtonClicked:
                if login(userName, password):
                    st.session_state['loggedIn'] = True
                else:
                    st.session_state['loggendIn'] = False
                    st.error('Senha ou usuário inválidos!')
# @st.cache_data    
def Usuario(key):
    if 'user' in st.session_state:
            user =  dados['Alunos'][st.session_state[key]]['nome']
            return user
    else:
        st.error('Sem usuário')

def loggedOut_Clicked():
    st.session_state['loggedIn'] = False

def logout_page():
    loginSection.empty()
    with logoutSection:
        st.button('Log Out', key='logout', on_click=loggedOut_Clicked)

def loggedIn_Clicked(userName, password):
    if login(userName,password):
        st.session_state['loggendIn'] = True
    else:
        st.session_state['loggendIn'] = False
        st.error('Senha ou usuário inválidos!')

def login(usuario: str, senha: str) -> bool:
    if usuario in dados['Alunos'] and senha == dados['Alunos'][usuario]['senha']:
        return True
    else:
        return False

def nome():
    userName = st.text_input(label='', value='', placeholder='Entrar com usuário', key='user')
    return userName
def senha():
    password = st.text_input(label='', value='', placeholder='Entrar com a senha', type='password', key='password')
    return password

def save_value(key):
    st.session_state[key] = st.session_state["_"+key]

def get_value(key):
    st.session_state["_"+key] = st.session_state[key]
    return st.session_state[key]

def home_page():
    with homeSection:       
        aba1, aba2 = st.tabs(['Home', 'Meus Treinos'])
        get_value('user')
        save_value('user')
        usuario = st.session_state['user']
        aluno = dados['Alunos'][usuario]
        with aba1:
            col1, col2 = st.columns(2)    
            with col1:
                col1.metric('Nome', value=aluno['nome'] )
                col1.metric('Nome Completo', aluno['nome_completo'])
                col1.metric('Altura', aluno['altura'])
            with col2:
                col2.metric('Idade', aluno['idade'])
                col2.metric('Peso', aluno['peso'])
                col2.metric('IMC', aluno['IMC'])

        with aba2:        
            treinos_disponiveis = []
            for tipo_treino in dados['Treinos'][usuario].keys():
                treinos_disponiveis.append(tipo_treino)

            page = st.radio('Treinos Disponíveis', treinos_disponiveis, horizontal=True)

            st.subheader(f'Esse é o seu treino: {page}')
            st.write('Exercícios: ')

            treino = dados['Treinos'][usuario]

            n = 1
            for exercicio in treino[page]:
                if n == 1:
                    ordem_ex = 'Primeiro'
                elif n == 2:
                    ordem_ex = 'Segundo'
                elif n == 3:
                    ordem_ex = 'Terceiro'
                elif n == 4:
                    ordem_ex = 'Quarto'
                elif n == 5:
                    ordem_ex = 'Quinto'
                elif n == 6:
                    ordem_ex = 'Sexto'
                elif n == 7:
                    ordem_ex = 'Sétimo'
                elif n == 8:
                    ordem_ex = 'Oitavo'
                elif n == 9:
                    ordem_ex = 'Nono'
                else:
                    ordem_ex = '...'

                with st.expander(f'{ordem_ex}'):
                    coluna1, coluna2, coluna3, coluna4  = st.columns([3,1,1,1])
                    
                    coluna1.metric('Exercício', treino[page][exercicio]['exercicio'])
                    coluna2.metric(f'Séries', treino[page][exercicio]['series'])
                    coluna3.metric(f'Repetições', treino[page][exercicio]['repeticoes'])
                    coluna4.metric(f'Carga', treino[page][exercicio]['carga'])
                            
                    n += 1
                    
with headerSection:
    st.title('Personal')
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        login_page()
    else:
        if st.session_state['loggedIn']:
            logout_page()
            home_page()            
        else:
            login_page()