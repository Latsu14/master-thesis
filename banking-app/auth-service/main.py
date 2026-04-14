from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

# Simulating a database of users
USERS = {"alice": "password123", "bob": "secret"}

@app.post("/login")
def login(req: LoginRequest):
    if req.username in USERS and USERS[req.username] == req.password:
        return {"token": f"fake-jwt-{req.username}", "user": req.username}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/health")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
