import requests
import streamlit as st

def registerUser(name: str, email:str, password:str):
    urlAPI = 'http://localhost:8080/api/v1/auth/register'

    newUser = {
        "name": name,
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url=urlAPI, json=newUser)
        if response.status_code == 201:
            st.success('Usuário criado com sucesso')
        elif response.status_code == 400:
            st.warning(f'Erro de validação: {response.text}')
        else:
            st.warning(f'Erro ao criar usuário: {response.status_code}')
    except Exception as e:
        st.warning(f'Ocorreu um erro de conexão: {e}')
