from fastapi import FastAPI

app = FastAPI()

@app.get("/api/home")
def get_home():
    s = int()
    for i in range(1, 10):
        s = s + i
    return s