import streamlit as st
import requests

def login(password: str, email: str):
    urlAPI = 'http://localhost:8080/api/v1/auth/login'
    userData = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(url=urlAPI, json=userData)

        if response.status_code == 200:
            data = response.json()
            token = data.get("token")

            st.session_state['token'] = token
            st.session_state['logado'] = True

            st.success('Login realizado com sucesso.')
            st.rerun()
        elif response.status_code == 403 or response.status_code == 401:
            st.error('Email ou senha incorretos.')
        else:
            st.error(f'Erro ao realizar login: {response.status_code} - {response.text}')

    except Exception as e:
        st.error(f'Ocorreu um erro de conexão: {e}')
