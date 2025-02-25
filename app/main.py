from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1.auth import router as auth_router
from app.routers.v1.users import router as user_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhots", "127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(user_router, prefix="/api/v1", tags=["user"])
