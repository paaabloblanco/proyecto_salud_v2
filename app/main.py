"""Punto de entrada de la aplicación web.

Arranque en local:  uvicorn app.main:app --reload
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Planificador de comidas para futsal")

# Ruta absoluta a app/templates, calculada desde este archivo: así funciona
# aunque uvicorn o pytest se lancen desde otra carpeta.
CARPETA_PLANTILLAS = Path(__file__).parent / "templates"
plantillas = Jinja2Templates(directory=CARPETA_PLANTILLAS)


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    """Muestra el formulario de la semana."""
    return plantillas.TemplateResponse(request, "formulario.html")


# TODO (usuario): ruta POST /plan
#   formulario -> Semana -> clasificar_semana -> calcular_gramos para cada día
#   y devolver plantillas.TemplateResponse(request, "resultados.html", {"semana": ..., "objetivos": ...})
