from loguru import logger
from datetime import datetime
from app.database.session import get_db
from fastapi.exceptions import HTTPException
from dateutil.relativedelta import relativedelta
from app.utils.auth import decode_token, check_token
from app.database.repositories.referal import referal_repository
from fastapi import APIRouter, Depends, Response, Request, status


logger.add(
    "logs/users.log",
    format="{time} {level} {message}\n",
    rotation="500MB",
    level="INFO",
    enqueue=True,
)
router = APIRouter()


@router.get(
    "/register_page/{referal_code}",
    summary="Переход на страницу регистрации по реферальной системе",
)
async def create_referal_link(referal_code: str, response: Response):
    try:
        response.set_cookie("code", referal_code)
        logger.info(f"Перешел пользователь по коду {referal_code}")
        return {"status": "ok", "message": "Successful!"}
    except Exception as e:
        logger.error(
            f"Ошибка перехода на страницу регистрации по реферальному коду: {referal_code}\nОшибка: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Iternal server error",
        )


@router.post("/create_code", summary="Создание реферальной ссылки")
async def create_code(
    request: Request,
    code: str,
    session=Depends(get_db),
    token: str = Depends(check_token),
):
    try:
        if await referal_repository.get_code(code, session):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Code already exists"
            )
        email = decode_token(request.cookies.get("users_access_token")).get("email")
        expiration = datetime.now() + relativedelta(months=1)
        await referal_repository.create(code, email, expiration, session)
        logger.info(f"Создан реферальный код: {code}\nПользователь: {email}")
        return {"status": "ok", "message": "Code successfully created!"}
    except Exception as e:
        logger.error(f"Создания реферального кода\n{str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Iternal server error",
        )


@router.get("/get_referals/{referrer_id}", summary="Получить рефералов по id реферера")
async def get_referals(referrer_id: int, session=Depends(get_db)):
    try:
        referals = await referal_repository.get_all_referals(referrer_id, session)
        logger.info(f"Получены рефералы пользователя {referrer_id}")
        return {"status": "ok", "message": referals}
    except Exception as e:
        logger.error(f"Ошибка получения рефералов\n{str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Iternal server error",
        )


@router.post("/get_code_by_email", summary="Получить реферальный код по почте реферера")
async def get_code_by_email(email: str, session=Depends(get_db)):
    try:
        code = await referal_repository.get_by_email(email, session)
        if code:
            logger.info(f"Запрошен код по email: {email}")
            return {"status": "ok", "message": code}

        logger.error(f"Не найден код по email {email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No code found"
        )
    except Exception as e:
        logger.error(f"Ошибка поулчения кода по email\n{str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Iternal server error",
        )
