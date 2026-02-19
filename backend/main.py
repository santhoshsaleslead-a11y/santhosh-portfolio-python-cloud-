from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from firebase_config import db
from auth import create_token, verify_token

app = FastAPI()

# ---------------- MODELS ----------------

class Login(BaseModel):
    email: str
    password: str

class Service(BaseModel):
    name: str
    price: float

class Payment(BaseModel):
    email: str
    service: str
    amount: float
    method: str

# ---------------- DEFAULT SERVICES ----------------

DEFAULT_SERVICES = [
    {"name": "IT Consulting", "price": 500},
    {"name": "HR Consulting", "price": 400},
    {"name": "Healthcare Consulting", "price": 600},
    {"name": "Marketing Consulting", "price": 450},
    {"name": "Resume Writing", "price": 150},
    {"name": "Social Media Marketing", "price": 300},
    {"name": "Content Strategy", "price": 350},
    {"name": "Leadership Development", "price": 550},
    {"name": "Negotiation", "price": 250},
    {"name": "Team Building", "price": 380},
]

# ---------------- INIT SERVICES ----------------

@app.on_event("startup")
def init_services():
    services_ref = db.collection("services")
    if not services_ref.stream():
        for service in DEFAULT_SERVICES:
            services_ref.add(service)

# ---------------- LOGIN (Admin Only) ----------------

@app.post("/admin/login")
def admin_login(login: Login):
    if login.email == "admin@santhosh.com" and login.password == "admin123":
        token = create_token({"role": "admin"})
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# ---------------- GET SERVICES ----------------

@app.get("/services")
def get_services():
    services = db.collection("services").stream()
    return [service.to_dict() | {"id": service.id} for service in services]

# ---------------- UPDATE PRICE (ADMIN ONLY) ----------------

@app.put("/admin/update/{service_id}")
def update_price(service_id: str, service: Service, token: str):
    decoded = verify_token(token)
    if decoded["role"] != "admin":
        raise HTTPException(status_code=403)

    db.collection("services").document(service_id).update({
        "name": service.name,
        "price": service.price
    })

    return {"message": "Service Updated Successfully"}

# ---------------- PAYMENT ----------------

@app.post("/payment")
def make_payment(payment: Payment):
    db.collection("payments").add(payment.dict())
    return {"message": "Payment Recorded"}
