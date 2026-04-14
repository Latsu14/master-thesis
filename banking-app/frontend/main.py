import os
import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

AUTH_URL = os.environ.get("AUTH_URL", "http://auth-service:8001")
ACCOUNT_URL = os.environ.get("ACCOUNT_URL", "http://account-service:8000")

HTML_TEMPLATE = """
<html>
    <head><title>ZTA Banking Frontend</title></head>
    <body style="font-family: Arial; padding: 2rem;">
        <h1>Zero Trust Bank</h1>
        <p>Login to view your account details.</p>
        <form action="/login" method="post">
            Username: <input type="text" name="username"><Br><Br>
            Password: <input type="password" name="password"><Br><Br>
            <input type="submit" value="Login">
        </form>
        <div style="margin-top:20px; color: red;">{error}</div>
        <div style="margin-top:20px; color: green;">{data}</div>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def index(error="", data=""):
    return HTML_TEMPLATE.format(error=error, data=data)

@app.post("/login", response_class=HTMLResponse)
def login(username: str = Form(...), password: str = Form(...)):
    # 1. Contact Auth Service
    try:
        resp = requests.post(f"{AUTH_URL}/login", json={"username": username, "password": password})
        if resp.status_code != 200:
            return HTML_TEMPLATE.format(error="Invalid Credentials", data="")
        
        # 2. If valid, contact Account Service with headers
        account_resp = requests.get(f"{ACCOUNT_URL}/account/{username}", headers={"x-user": username})
        if account_resp.status_code != 200:
            return HTML_TEMPLATE.format(error=f"Account Service Error: {account_resp.text}", data="")
            
        data = account_resp.json()
        return HTML_TEMPLATE.format(
            error="", 
            data=f"Success! Confirmed Balance for {username}: ${data['balance']}"
        )
    except Exception as e:
        return HTML_TEMPLATE.format(error=f"Connection Error: {e}", data="")

@app.get("/health")
def healthz():
    return {"status": "ok"}
