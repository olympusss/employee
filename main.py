from fastapi import FastAPI

app = FastAPI()

@app.get("/api/home")
def get_home():
    return "Hello World!!!"