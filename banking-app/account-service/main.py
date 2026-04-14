from fastapi import FastAPI, Depends, HTTPException, Header
import uvicorn

app = FastAPI()

fake_db = {
    "alice": {"balance": 150000, "status": "active", "account_type": "premium"},
    "bob": {"balance": 250, "status": "active", "account_type": "standard"}
}

@app.get("/account/{username}")
def get_account(username: str, x_user: str = Header(None)):
    # Simulating simple auth boundary or trust verification
    if x_user != username and x_user != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized lateral movement or invalid user context.")
    
    if username not in fake_db:
        raise HTTPException(status_code=404, detail="Account not found.")
        
    return fake_db[username]
    
@app.get("/health")
def healthz():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
