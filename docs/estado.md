# Estado del proyecto

_Última actualización: 2026-11-13_

## 👉 Dónde estamos
**v0.1, pasos 0, 1 y 2 terminados. Lo siguiente es el PASO 3: el motor de reglas.**
Todo está en commits y subido a GitHub (`origin/main`, último commit "Paso 2: clasificación de días..."). En total pasan 24 tests.

## Hecho
- **Paso 0:** repositorio git y GitHub, `.venv`, `requirements.txt` con versiones fijadas, `.gitignore`, `.env.example`, `README.md` y la ruta `GET /` de prueba (`app/main.py`, `tests/test_rutas.py`).
- **Paso 1:** `app/modelos.py`
  - `TipoActividad` (lo que elige el usuario): `partido`, `entreno_fuerte`, `entreno_suave`, `descanso`.
  - `Dia`: `actividad` + `hora` (la hora es obligatoria con actividad y está prohibida en descanso, mediante un `model_validator`).
  - `Semana`: `dias` (exactamente 7; la posición 0 es el lunes) + `peso_kg` (de 30 a 200).
  - 17 tests en `tests/test_modelos.py`.
- **Paso 2:** `app/calendario.py`
  - `TipoDia` (lo que calcula el programa): los 4 tipos de `TipoActividad` + `dia_antes_partido`.
  - `clasificar_semana(semana) -> list[TipoDia]`. Prioridad: partido > día antes de partido > actividad del usuario. El día siguiente se busca con `(i + 1) % 7`, así que el domingo mira al lunes de la misma semana. La hora no se usa.
  - 6 tests en `tests/test_calendario.py`, uno por decisión de diseño.

## Siguiente: PASO 3, motor de reglas (`app/reglas.py`, lo escribe el usuario)
Objetivo: a cada `TipoDia` le corresponden unos objetivos nutricionales, expresados en g/kg y calculados con `peso_kg`.
Antes de programar hay que decidir (y apuntar en `decisiones.md`):
1. **Qué nutrientes** entran en v0.1: hidratos y proteína seguro. ¿Grasa? ¿Hidratación?
2. **Qué fuentes** se citan. Candidata: la posición conjunta ACSM/AND/DC de 2016, *Nutrition and Athletic Performance*. Cada cifra lleva su fuente y la marca "pendiente de validar por un dietista-nutricionista". No se inventan cifras.
3. **La forma del resultado:** probablemente un modelo Pydantic (por ejemplo `ObjetivosDia`) con las cantidades en gramos y un texto con el motivo ("más hidratos porque mañana hay partido"), que necesitará la página final.
4. **Los horarios de las comidas** (el `CLAUDE.md` dice "objetivos y horarios"): si se usan ya en el paso 3 con `Dia.hora` o se dejan para cuando entre la IA.
Para empezar la sesión: Claude plantea el problema y las decisiones; el usuario decide y escribe el código; Claude revisa y escribe los tests restantes.

## Pasos que quedan en v0.1
| # | Paso | Quién |
|---|---|---|
| 3 | Motor de reglas: objetivos por tipo de día (g/kg, con fuentes) | usuario (Claude, tests) |
| 4 | Formulario HTML + ruta POST que muestra los días clasificados y sus objetivos (todavía sin IA). **Aquí se añaden el presupuesto y los gustos a `Semana`**, que se aplazaron en el paso 1 | Claude las plantillas, usuario la conexión |
| 5 | Modelo Pydantic del plan (la salida de la IA), validado con un JSON de ejemplo | juntos |
| 6 | `app/ia.py`: prompt + `client.messages.parse(output_format=...)` con Claude + un reintento si la validación falla (tests con mock) | Claude, explicándolo |
| 7 | `app/planificador.py` (calendario → reglas → IA) + `plan.html` con el plan por día, el motivo de cada ajuste y el aviso visible | usuario el planificador, Claude el HTML |
| 8 | Límites de seguridad: si aparecen alergias o condiciones médicas, mensaje que recomienda acudir a un profesional | juntos |
Al terminar el paso 8 se cierra la v0.1. La v0.2 es la tabla de precios y la verificación del presupuesto en código (ver la hoja de ruta en `CLAUDE.md`).

## Problemas / notas
- Falta rellenar en `app/modelos.py` el comentario de los límites del peso (`# Límites del peso: mínimo ___ porque ___`) y aplicar el estilo PEP 8 (espacios en comas y tipos).
- **Imports:** dentro de `app/` se importa siempre con `app.` (`from app.modelos import ...`). Todo se ejecuta desde la raíz del proyecto (`pytest`, `uvicorn app.main:app --reload`), nunca con el botón ▶ del editor sobre un archivo de `app/`. Esto ya causó errores en el paso 2.
- Conocido: si este lunes hay partido y el de la semana siguiente no, el domingo se clasifica mal (decisión de v0.1, se revisará en v0.5 con Google Calendar).
- Python 3.14.5 (cumple el requisito de 3.11 o superior).
