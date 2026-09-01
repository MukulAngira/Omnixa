from fastapi import FastAPI , status , Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings 
from app.core.database import connect_to_mongo , close_mongo_connection



@asynccontextmanager 
async def lifespan(app : FastAPI):

    await connect_to_mongo()
    print("DATABASE Connected")

    yield

    await close_mongo_connection()
    print("Database Disconnected")


app = FastAPI(
    title="Omnixa API",
    version="1.0.0",
    lifespan=lifespan
)

origins =  [
        "http://localhost:5173",   
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

app.add_middleware(

    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


'''
--DEAR RIYA,

Here , Command for python Run -> "python -m app.main"
AAGR UVICORN per Run KERNA h to -> "uvicorn app.main:app"
And Command for requirement.txt -> "pip install -r requrirements.txt"

Thank You!!!

'''
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=3000,
        reload=True
    )