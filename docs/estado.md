# Estado del proyecto

_Última actualización: 2026-11-12_

## Versión en curso
v0.1: formulario semanal → plan de comidas por día (ver `CLAUDE.md`).

## Hecho
- `CLAUDE.md` (renombrado a mayúsculas) con la visión, el stack, los límites y la metodología. Se añade el peso corporal al formulario de v0.1.
- Estructura, dependencias y orden de pasos de v0.1 aprobados (ver `docs/decisiones.md`).
- **Paso 0:** repositorio git, `.venv`, `requirements.txt` con versiones fijadas, `.gitignore`, `.env.example`, `README.md` y la ruta `GET /` de prueba con su test (`tests/test_rutas.py`). pytest: 1 test pasa.
- **Paso 1:** `app/modelos.py` (`TipoActividad`, `Dia` con un validador de la hora, `Semana` con 7 días y `peso_kg`) y 17 tests en `tests/test_modelos.py`. Commit hecho y subido a GitHub.

## Siguiente
- **Paso 2 (en curso):** `TipoDia` y `clasificar_semana` en `app/calendario.py`. `tests/test_calendario.py` tiene 6 tests, uno por decisión de diseño. Fallan 5 por un error de lógica en `clasificar_semana` (mira la actividad de hoy en vez de la de mañana y no aplica `% 7`). Lo arregla el usuario.

## Problemas / preguntas abiertas
- Pendiente dentro de v0.1: añadir el presupuesto y los gustos al modelo `Semana` (aplazados en el paso 1).
- Falta elegir qué fuentes publicadas usarán las reglas nutricionales (candidata: la posición conjunta ACSM/AND/DC de 2016). Se decide en el paso 3.
- Python instalado: 3.14.5 (cumple el requisito de 3.11 o superior).
