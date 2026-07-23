from fastapi import FastAPI

from app.middleware import logging_middleware

app = FastAPI()

app.middleware("http")(logging_middleware)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/error")
def error():
    raise Exception("Test exception")