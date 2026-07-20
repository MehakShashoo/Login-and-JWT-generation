from fastapi import APIRouter, HTTPException
from database import supabase
from models.user_models import LoginRequest, TokenResponse
from security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=TokenResponse)
def login(user: LoginRequest):

    email = user.email.strip().lower()
    password = user.password

    try:
        response = (
            supabase.table("users")
            .select("id,email,password_hash,is_active")
            .eq("email", email)
            .execute()
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

    if not response.data:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    db_user = response.data[0]

    if not verify_password(password, db_user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    if not db_user["is_active"]:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    try:
        token = create_access_token(str(db_user["id"]))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }