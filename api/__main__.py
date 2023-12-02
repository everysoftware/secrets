from fastapi import FastAPI

app = FastAPI(title="Secrets")


@app.get("/")
async def hello():
    return {"message": "Hello World"}
