from fastapi import FastAPI

app = FastAPI()
#prices developer bogdan = 100000000$
#prices developer 1 = 100000$
#prices developer 2 = 1000$

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
