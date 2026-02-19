from fastapi import FastAPI
from pydantic import BaseModel
from firebase_config import db

app = FastAPI()

# ---------------------
# Models
# ---------------------

class User(BaseModel):
    name: str
    email: str
    password: str
    role: str

class Payment(BaseModel):
    email: str
    service: str
    amount: float
    method: str

# ---------------------
# Routes
# ---------------------

@app.get("/")
def home():
    return {"message": "Santhosh Portfolio Cloud API Running"}

@app.post("/register")
def register(user: User):
    db.collection("users").add(user.dict())
    return {"message": "User Registered Successfully in Cloud"}

@app.post("/login")
def login(user: User):
    return {"message": "Login Successful (Cloud Based)"}

@app.get("/services")
def services():
    return {
        "services": [
            "Resume Editing & ATS Optimization",
            "Bench Sales Marketing",
            "Hotlist Circulation",
            "Vendor Marketing",
            "LinkedIn Branding"
        ]
    }

@app.post("/payment")
def payment(payment: Payment):
    db.collection("payments").add(payment.dict())
    return {"message": "Payment Saved to Cloud"}

