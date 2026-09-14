from fastapi import FastAPI

app = FastAPI()

# Api routes


@app.get("/")
def read_root():
    return {"Hello": "World"}
