import requests
import streamlit as st

def registerUser(name: str, email:str, password:str):
    urlAPI = 'http:localhost:8080/api/v1/auth'
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
