import streamlit as st
import requests

def login(password: str, email: str):
    urlAPI = 'http://localhost:8080/api/v1/auth'
    userData = {
        f"email": {email},
        f"nome": {password}
    }
    
    try:
        response = requests.post(url=urlAPI, json=userData)
        if (response.status_code == 201): #201 status criado
            # st.success(f'Login realizado com sucesso. Bem-vindo {name.capitalize()}')
            st.success(f'Login realizado com sucesso.')
        else:
            st.error(f'Erro ao realizar login {response.status_code}')
            st.write(response.text)
    except Exception as e:
        st.error(f'Ocorreu um erro {e}')
