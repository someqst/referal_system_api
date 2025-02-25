from loguru import logger
from app.database.session import get_db
from app.schemas.user import UserSchema
from fastapi.exceptions import HTTPException
from app.database.repositories import user_repository
from fastapi import APIRouter, Depends, Response, status, Request
from app.utils.auth import get_password_hash, authenticate_user, create_access_token


logger.add(
    "logs/auth.log",
    format="{time} {level} {message}\n",
    rotation="500MB",
    level="INFO",
    enqueue=True,
)
router = APIRouter()


@router.post("/register")
async def register_user(
    user_data: UserSchema, response: Request, session=Depends(get_db)
):
    try:
        user = await user_repository.get_by_email(user_data.email, session)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )
        await user_repository.create(
            user_data.email,
            get_password_hash(user_data.password),
            response.cookies.get("code"),
            session,
        )
        logger.info(f"Зарегистрирован пользователь: {user_data.email}")
        return {"status": "ok", "message": "You have successfully registered!"}
    except Exception as e:
        logger.error(f"Ошибка регистрации\n{str(e)}")


@router.post("/login")
async def auth_user(response: Response, user_data: UserSchema, session=Depends(get_db)):
    try:
        user = await user_repository.get_by_email(user_data.email, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User doesn't exists"
            )

        check = await authenticate_user(
            password=user_data.password, hashed_password=user.password
        )
        if not check:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong password or username",
            )
        access_token = create_access_token({"email": user.email})
        response.set_cookie(key="users_access_token", value=access_token, httponly=True)
        logger.info(f"Вошел пользователь: {user_data.email}")
        return {"status": "ok", "message": "You have successfully logged in!"}
    except Exception as e:
        logger.error(f"Ошибка входа\n{str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Iternal server error",
        )


@router.post("/logout")
async def logout_user(response: Response):
    try:
        response.delete_cookie(key="users_access_token")
        return {"status": "ok", "message": "You are successfully logged out!"}
    except Exception as e:
        logger.error(f"Ошибка выхода:\n{str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Iternal server error",
        )
