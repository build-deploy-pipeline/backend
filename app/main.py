from fastapi import FastAPI
from api import webapp


app = FastAPI()
app.include_router(webapp.router)


@app.get("/ping")
def health_check():
    return {"ping": "pong"}
