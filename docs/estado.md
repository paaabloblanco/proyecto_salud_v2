# Estado del proyecto

_Última actualización: 2026-11-12_

## Versión en curso
v0.1: formulario semanal → plan de comidas por día (ver `CLAUDE.md`).

## Hecho
- `CLAUDE.md` (renombrado a mayúsculas) con la visión, el stack, los límites y la metodología. Se añade el peso corporal al formulario de v0.1.
- Estructura, dependencias y orden de pasos de v0.1 aprobados (ver `docs/decisiones.md`).
- **Paso 0:** repositorio git, `.venv`, `requirements.txt` con versiones fijadas, `.gitignore`, `.env.example`, `README.md` y la ruta `GET /` de prueba con su test (`tests/test_rutas.py`). pytest: 1 test pasa.

## Siguiente
- **Paso 1:** modelos Pydantic de entrada en `app/modelos.py` (`TipoActividad`, `Dia`, `Semana`, incluido el peso) y `tests/test_modelos.py`.
- Después, el paso 2: la clasificación de días (la escribe el usuario).

## Problemas / preguntas abiertas
- Falta elegir qué fuentes publicadas usarán las reglas nutricionales (candidata: la posición conjunta ACSM/AND/DC de 2016). Se decide en el paso 3.
- Python instalado: 3.14.5 (cumple el requisito de 3.11 o superior).
