from fastapi import FastAPI

app = FastAPI(
    title="PyKids Academy API",
    version="0.1"
)


@app.get("/")
def inicio():
    return {
        "mensaje": "🐍 PyKids Academy funcionando",
        "version": "0.1"
    }


@app.get("/saludo/{nombre}")
def saludo(nombre:str):
    return {
        "mensaje": f"Hola {nombre}, bienvenida a PyKids Academy"
    }
