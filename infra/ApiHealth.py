import requests

def health():
    response = requests.get("http://localhost:8080/actuator/health")
    print(response.status_code)
    print(response.content)