from fastapi import FastAPI, HTTPException, status
from models import LoginRequest
from utils import create_access_token

app = FastAPI()



MOCK_USER = {
    "id": "user_1",
    "email": "test@example.com",
    "password": "12345678",
}


@app.get("/")
def root() -> dict[str, str]:
    return {"hello": "world"}


@app.post("/login")
async def login(payload: LoginRequest) -> dict:
    if (
        payload.email.lower() != MOCK_USER["email"]
        or payload.password != MOCK_USER["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    access_token  = create_access_token(
        user_id=MOCK_USER["id"],
        email=MOCK_USER["email"],
    )

    return {
        "message": "Login successful",
        "user": {
            "id": MOCK_USER["id"],
            "email": MOCK_USER["email"],
        },
        "token": {
            "access_token": access_token ,
            "token_type": "bearer",
        },
    }
