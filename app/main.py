"""Punto de entrada de la aplicación web.

Arranque en local:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI

app = FastAPI(title="Planificador de comidas para futsal")


@app.get("/")
def inicio() -> dict[str, str]:
    """Ruta de prueba: confirma que el servidor está funcionando."""
    return {"mensaje": "Hola, el servidor funciona"}
