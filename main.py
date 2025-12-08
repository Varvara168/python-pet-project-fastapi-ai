from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from ai_client import *
from db import Base, engine, get_user_requests, add_request_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    #metadata - данные про всех детей 
    print("Таблицы созданы")
    yield  #

app = FastAPI(
    title="AI чат",
    lifespan=lifespan
    )


@app.get("/api/requests")
def get_my_requests(request: Request):
    user_ip_address = request.client.host
    user_requests = get_user_requests(ip_address=user_ip_address)
    return user_requests

@app.post("/api/requests")
def answer_ai(
    request: Request,
    promt: str = Body(embed=True),
    ):
    answer = answer_script(promt)
    user_ip_address = request.client.host
    add_request_data(
        ip_address=user_ip_address, 
        promt=promt,
        response=answer,
    )
    return {"answer": answer}


app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
