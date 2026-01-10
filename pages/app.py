import streamlit as st
from textblob import TextBlob
import requests
from infra import ApiHealth

ApiHealth()

def login(password: str, email: str):
    urlAPI = 'https://localhost:8080/api/v1/auth'
    userData = {
        f"email": {email},
        f"nome": {password}
    }
    try:
        response = requests.post(url=urlAPI, json=userData)
        if (response.status_code == 201): #201 status criado
            st.success(f'Login realizado com sucesso. Bem-vindo {name.capitalize()}')
        else:
            st.error(f'Erro ao realizar login {response.status_code}')
            st.write(response.text)
    except Exception as e:
        st.error(f'Ocorreu um erro {e}')


def registerUser(name: str, email:str, password:str):
    urlAPI = 'https://localhost:8080/api/v1/auth'
    newUser = {
        "name": {name},
        "email": {email},
        "password": {password}
    }
    
    try:
        response = requests.post(url=urlAPI, json=newUser)
        if (response.status_code == 201): # TODO: adicionar mais tratamentos de erro para status code
            st.success(f'Usuário criado com sucesso')
        else:
            st.warning(f'Erro ao criar usuário')
    except Exception as e:
        st.warning(f'Ocorreu um erro {e}')



page = st.sidebar.radio("Navegação:", ["Login", "Registrar", "Análise"])
if page == "Login":
    st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    # TODO: cria lógica do login
    login(email=email, password=password)

elif page == "Registrar":
    st.markdown("<h1 style='text-align: center;'>Registrar</h1>", unsafe_allow_html=True)
    name = st.text_input("nome", placeholder="your beatifull name")
    new_email = st.text_input("Novo Email", placeholder="your best email, my Sir")
    new_password = st.text_input("Nova Senha", type="password", placeholder="enter your favorite password")
    # TODO: cria lógica de criar usuário
    registerUser(name=name, email=new_email, password=new_password)

elif page == "Análise":
    st.title('Análise de Sentimentos' , help='https://github.com/ONE-sentiment-analysis/BIA_frontend_python')
    user_input = st.chat_input("Digite sua mensagem para análise:")
    
    st.sidebar.title("Configuração")
    response_type = st.sidebar.checkbox("Mostrar resposta em JSON", value=True)
    model = st.sidebar.selectbox("Modelo", ["TextBlob", "Oracle"])
    user_name = st.sidebar.text_input("Nome do usuário", value="você").capitalize().strip()
    ia_name = "BIA"
    user_icon = st.sidebar.file_uploader("Enviar foto do usuário", type=["jpeg","jpg","png"])
    if user_icon is not None:
        st.sidebar.image(user_icon)    
    
    def responseJson(sentiment, acc):
        return {"previsibilidade": sentiment, "probabilidade": round(acc, 2)}

    def responseAlternative(sentiment, acc):
        if acc > 0:
            st.success(f"{ia_name}: {sentiment} - Probabilidade: {acc:.2f}")
        elif acc < 0:
            st.error(f"{ia_name}: {sentiment} - Probabilidade: {acc:.2f}")
        else:
            st.warning(f"{ia_name}: {sentiment} - Probabilidade: {acc:.2f}")
            
    @st.cache_data
    def analyze(text: str, model: str):
        if model == "TextBlob":
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity  
        else:
            sentiment = 0
            st.warning("Estamos implementando outro modelo")
        
        if sentiment > 0:
            return responseJson("Positivo", sentiment)
        elif sentiment < 0:
            return responseJson("Negativo", sentiment)
        else:
            return responseJson("Neutro", sentiment)

    if "history" not in st.session_state:
        st.session_state.history = []

    if user_input:
        result = analyze(user_input, model)
        st.session_state.history.append((user_name, user_input, result, user_icon))

    for name, text, result, icon in st.session_state.history:
        with st.chat_message("user", avatar=icon if icon is not None else None):
            st.write(f"{name}: {text}")
        with st.chat_message(ia_name, avatar="🤖"):
            if response_type:
                st.json(result)
            else:
                responseAlternative(result["previsibilidade"], result["probabilidade"])

    st.sidebar.subheader("Histórico de análises")
    for name, text, result, icon in st.session_state.history:
        st.sidebar.write(f"{name}: {text}")
        st.sidebar.json(result)