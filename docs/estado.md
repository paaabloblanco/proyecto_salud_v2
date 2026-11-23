# Estado del proyecto

_Última actualización: 2026-11-23_

## 👉 Dónde estamos
**v0.1: el PASO 3 (motor de reglas) está terminado.** Lo siguiente es el **paso 4** (formulario HTML + ruta POST, todavía sin IA).
- 2026-11-23: el presupuesto pasa a v0.2 y los gustos se recogen por rechazo sobre el plan (ver `decisiones.md`).

## Hecho
- **Paso 0:** repositorio git y GitHub, `.venv`, `requirements.txt` con versiones fijadas, `.gitignore`, `.env.example`, `README.md` y la ruta `GET /` de prueba (`app/main.py`, `tests/test_rutas.py`).
- **Paso 1:** `app/modelos.py`
  - `TipoActividad`: `partido`, `entreno_fuerte`, `entreno_suave`, `descanso`.
  - `Dia`: `actividad` + `hora` (la hora es obligatoria con actividad y está prohibida en descanso, mediante un `model_validator`).
  - `Semana`: `dias` (exactamente 7; la posición 0 es el lunes) + `peso_kg` (de 30 a 200).
  - 17 tests en `tests/test_modelos.py`.
- **Paso 2:** `app/calendario.py`
  - `TipoDia`: los 4 de `TipoActividad` + `dia_antes_partido`.
  - `clasificar_semana(semana) -> list[TipoDia]`. Prioridad: partido > día antes de partido > actividad. El día siguiente es `(i + 1) % 7`.
  - 6 tests en `tests/test_calendario.py`.
- **Investigación (paso 3):** `docs/investigacion_nutricion.md` y `docs/investigacion_notas/`. Solo los hidratos cambian según el día; no se estiman calorías; la app nunca fija un objetivo de peso.
- **Paso 3:** `app/reglas.py`
  - `Rango`: `minimo` y `maximo` (`ge=0`); un `model_validator` rechaza `maximo < minimo`.
  - `ObjetivoDiaGramos`: `tipo_dia`, `rango_hidratos_g`, `rango_proteina_g`, `porcentaje_grasa`, `motivo`. Es el objetivo ya calculado para una persona.
  - `ObjetivoDiaGporKg` (la regla): `rango_hidratos`, `rango_proteina`, `porcentaje_grasa`, `motivo`. Método `calcular_gramos(peso_kg, tipo_dia) -> ObjetivoDiaGramos`: crea un objeto nuevo (no modifica nada), multiplica hidratos y proteína por el peso y copia la grasa con `model_copy()`.
  - `REGLAS_POR_DIA`: diccionario `TipoDia → ObjetivoDiaGporKg` con las 5 reglas, sus motivos y el comentario de fuentes ("PENDIENTE DE VALIDAR POR UN DIETISTA-NUTRICIONISTA").
  - 14 tests en `tests/test_reglas.py`. **Total: 38 tests pasando.**

## Siguiente: paso 4
`Semana` no cambia.
1. Claude escribe las plantillas Jinja2: el formulario (7 días + peso) y la página de resultados.
2. El usuario escribe la ruta `POST` en `app/main.py`: formulario → `Semana` → `clasificar_semana` → `calcular_gramos` para cada día.

## Pendientes pequeños
- **`extra="forbid"`** (`model_config = ConfigDict(extra="forbid")`): Pydantic ignora en silencio los campos de más. Decidir si se usa en las reglas (para detectar erratas) y en el modelo del plan de la IA (paso 5). Apuntarlo en `decisiones.md`.
- Un comentario en `Rango` que explique por qué se acepta 6–6 (lo escribe el usuario).
- Qué pasa con un porcentaje > 100 (`Rango(minimo=20, maximo=150)`): hoy se acepta.
- En `app/modelos.py`: rellenar el comentario `# Límites del peso: mínimo ___ porque ___` y aplicar PEP 8.

## Pasos que quedan en v0.1
| # | Paso | Quién |
|---|---|---|
| 4 | Formulario HTML + ruta POST que muestra los días clasificados y sus objetivos (todavía sin IA) | Claude las plantillas, usuario la conexión |
| 5 | Modelo Pydantic del plan (la salida de la IA), validado con un JSON de ejemplo | juntos |
| 6 | `app/ia.py`: prompt + `client.messages.parse(output_format=...)` + un reintento si la validación falla (tests con mock) | Claude, explicándolo |
| 6b | Gustos por rechazo: modelo de los rechazados (p. ej. `list[str]`), campos ocultos en la página del plan, ruta para regenerar y su hueco en el prompt | juntos |
| 7 | `app/planificador.py` (calendario → reglas → IA) + `plan.html` con el plan, el motivo de cada ajuste y el aviso visible. Aquí se comprueba la grasa (% de la energía del menú) | usuario el planificador, Claude el HTML |
| 8 | Límites de seguridad: alergias o condiciones médicas → recomendar acudir a un profesional | juntos |

## Lecciones de esta sesión (2026-11-22)
- **Revisión:** el fallo puesto (un test que recorría `REGLAS_POR_DIA` en vez de `TipoDia`, así que no podía fallar) se escapó. "Todo ok" no basta: responder las 4 preguntas. Para cada test, preguntarse qué cambio del código lo haría fallar.
- `=` con objetos no copia: pone otra etiqueta al mismo objeto. Para copiar un modelo de Pydantic, `model_copy()`.
- Pydantic valida al **crear** el objeto, no al cambiar un campo después. Por eso conviene crear objetos nuevos en lugar de modificarlos.
- Pydantic ignora por defecto los campos de más (`extra="ignore"`).
- Comparar decimales en los tests con `pytest.approx`.

## Problemas / notas
- **Guardar antes de probar:** un ● en la pestaña de VS Code significa que hay cambios sin guardar (pasó otra vez en esta sesión).
- **Usar el `.venv`:** con el Python del sistema no está `pytest`.
- En la consola de Windows las tildes salen como `D�a`; el archivo está bien.
- `git commit` está bloqueado para Claude por los permisos: los commits los hace el usuario con `!`, o se da permiso con `/permissions`.
- **Imports:** dentro de `app/` se importa siempre con `app.`. Todo se ejecuta desde la raíz (`pytest`, `uvicorn app.main:app --reload`), nunca con el botón ▶ del editor.
- Conocido: si este lunes hay partido y el de la semana siguiente no, el domingo se clasifica mal (se revisará en v0.5).
- Python 3.14.5.
