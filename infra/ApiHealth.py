import requests

def health():
    try:
        response = requests.get("http://localhost:8080/actuator/health")
        if(response.status_code == 200):
            print("Connection with Spring boot")
            print(response.content)
    except Exception as e:
        print("Ocorreu um erro ao tentar conectar com API", e)