from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI(title="Hello API")

# Persistencia en memoria: una lista normal de Python.
# Se pierde al reiniciar el servidor, y para este ejercicio es lo deseado.
nombres_recibidos: list[str] = []


class HelloRequest(BaseModel):
    """Define cómo debe ser el JSON de entrada."""
    name: str  # obligatorio: no tiene valor por defecto

    @field_validator("name")
    @classmethod
    def name_no_vacio(cls, valor: str) -> str:
        valor = valor.strip()  # quita espacios al principio y final
        if not valor:
            raise ValueError("name no puede estar vacío")
        return valor


class HelloResponse(BaseModel):
    """Define cómo es el JSON de salida."""
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/hello", response_model=HelloResponse)
def hello(datos: HelloRequest):
    nombres_recibidos.append(datos.name)
    return {"message": f"Hello {datos.name}"}