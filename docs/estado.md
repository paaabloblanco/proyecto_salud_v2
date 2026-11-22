# Estado del proyecto

_Última actualización: 2026-11-14_

## 👉 Dónde estamos
**v0.1, PASO 3 (motor de reglas) a medias.** La investigación está hecha y las decisiones tomadas. `app/reglas.py` tiene `Rango` funcionando y la forma de la regla; faltan las 5 reglas con sus datos y el cálculo con el peso.
- Commits subidos: hasta el paso 2. Commits locales sin `push`: "Metodología: revisión de código…" y "Investigación de nutrición deportiva…".
- Sin commitear: `app/reglas.py` (en curso) y las 3 decisiones nuevas de `docs/decisiones.md`. Se commitean juntos al terminar el paso 3.

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
- **Investigación (paso 3):** `docs/investigacion_nutricion.md` (informe con la tabla por tipo de día) y `docs/investigacion_notas/` (5 notas con las fuentes). Conclusión: solo los hidratos cambian según el día; no hace falta estimar calorías; no existe un "peso ideal" y la app nunca fija un objetivo de peso. El anexo del informe lista citas sin verificar.
- **Decisiones del paso 3** (en `decisiones.md`): objetivos como rangos mín–máx; proteína de 1,6 a 2,2 g/kg todos los días (UEFA 2021); grasa del 20 al 35 % de la energía, que se guarda ahora y se comprueba cuando haya menú.

## Paso 3: qué hay en `app/reglas.py`
- `Rango` ✅ `minimo` y `maximo` con `Field(ge=0)` y un `model_validator` que rechaza `maximo < minimo`. 6–6 es válido. Probado a mano con 6–8, 6–6, 8–6 y -1–5.
- `ObjetivoDiaGporKg`: `tipo_dia`, `rango_hidratos`, `rango_proteina`, `porcentaje_grasa` (los tres son `Rango`) y `motivo: str`.

### Pendiente de pulir (lo escribe el usuario)
- Un comentario que explique por qué se acepta 6–6.
- `motivo` con `Field(min_length=1)`, para que no quede vacío.
- Decidir si se añade un campo `fuente`, o si la fuente va en un comentario encima de cada regla.
- Pensar qué pasa con un porcentaje > 100 (`Rango(minimo=20, maximo=150)`).
- PEP 8:
  - `mode="after"`.
  - Un espacio después de `:` en los campos.
  - Una línea en blanco antes de `@model_validator`.
  - Dos líneas en blanco entre clases.
  - Un salto de línea al final del archivo.

### Siguiente, por orden (lo escribe el usuario)
1. **Las 5 reglas** en un diccionario `TipoDia → regla`, con los motivos escritos por el usuario. Si la clave ya es el `TipoDia`, ¿sobra el campo `tipo_dia` de la regla?
   | Tipo de día | Hidratos (g/kg) | Proteína (g/kg) | Grasa (% de la energía) |
   |---|---|---|---|
   | Partido | 6–8 | 1,6–2,2 | 20–35 |
   | Día antes de partido | 6–8 | 1,6–2,2 | 20–35 |
   | Entreno fuerte | 5–6 | 1,6–2,2 | 20–35 |
   | Entreno suave | 3–5 | 1,6–2,2 | 20–35 |
   | Descanso | 3–5 | 1,6–2,2 | 20–35 |
2. **Una segunda clase** para el objetivo ya calculado, en gramos para una persona. Es distinta de la regla en g/kg, para no mezclar unidades.
3. **Un método de la regla** que recibe `peso_kg` y devuelve esa clase. Los hidratos y la proteína se multiplican por el peso; la grasa no.
4. Tests en `tests/test_reglas.py`: el usuario escribe los suyos y Claude los que falten.
5. Commit del paso 3 junto con las decisiones.

## Pasos que quedan en v0.1
| # | Paso | Quién |
|---|---|---|
| 3 | Motor de reglas (en curso) | usuario (Claude, tests) |
| 4 | Formulario HTML + ruta POST que muestra los días clasificados y sus objetivos (todavía sin IA). **Aquí se añaden el presupuesto y los gustos a `Semana`** | Claude las plantillas, usuario la conexión |
| 5 | Modelo Pydantic del plan (la salida de la IA), validado con un JSON de ejemplo | juntos |
| 6 | `app/ia.py`: prompt + `client.messages.parse(output_format=...)` + un reintento si la validación falla (tests con mock) | Claude, explicándolo |
| 7 | `app/planificador.py` (calendario → reglas → IA) + `plan.html` con el plan, el motivo de cada ajuste y el aviso visible. Aquí se comprueba la grasa (% de la energía del menú) | usuario el planificador, Claude el HTML |
| 8 | Límites de seguridad: alergias o condiciones médicas → recomendar acudir a un profesional | juntos |

## Problemas / notas
- **Guardar antes de probar:** en esta sesión el archivo estaba editado pero sin guardar, y la prueba usaba la versión vieja. En VS Code, un ● en la pestaña significa que hay cambios sin guardar.
- `git commit` está bloqueado para Claude por los permisos: los commits los hace el usuario con `!`, o se da permiso con `/permissions`.
- Falta rellenar en `app/modelos.py` el comentario `# Límites del peso: mínimo ___ porque ___` y aplicar PEP 8.
- **Imports:** dentro de `app/` se importa siempre con `app.`. Todo se ejecuta desde la raíz (`pytest`, `uvicorn app.main:app --reload`), nunca con el botón ▶ del editor.
- Conocido: si este lunes hay partido y el de la semana siguiente no, el domingo se clasifica mal (se revisará en v0.5).
- Python 3.14.5.
