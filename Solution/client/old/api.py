import requests
from requests.auth import HTTPBasicAuth
from config import API_URL

def login(user, password):
    auth = HTTPBasicAuth(user, password)
    r = requests.get(f"{API_URL}/livres", auth=auth)
    if r.status_code == 200:
        return auth
    return None

def get_livres(auth):
    r = requests.get(f"{API_URL}/livres", auth=auth)
    r.raise_for_status()
    return r.json()
