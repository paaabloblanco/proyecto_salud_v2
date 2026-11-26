# ✈️ Plan de estudio para el vuelo (≈ 4 horas, sin ordenador)

_Preparado el 2026-11-26. Punto de partida: `docs/estado.md` → estamos en el **paso 4** (las plantillas ya están hechas; te falta la ruta `POST /plan`)._

## Cómo usar este documento
- Necesitas solo la tablet y algo para escribir (papel o una app de notas). **No hace falta internet ni Python.**
- Cada bloque tiene: **explicación → ejercicios → pistas**. Las **soluciones están al final del todo**. Intenta cada ejercicio de verdad antes de mirarlas: lo que no te cueste, no se te queda.
- Si te atascas más de 5 minutos: lee la pista 1, luego la pista 2, y solo después la solución.
- Al aterrizar, lo que hayas escrito en papel lo pasamos al código juntos (paso a paso, con tests).

## Horario

| Bloque | Tema | Tiempo | Acumulado |
|---|---|---|---|
| 1 | Repaso: tu propio código (modelos, calendario, reglas) | 35 min | 0:35 |
| 2 | Cómo viaja un formulario por HTTP | 45 min | 1:20 |
| 3 | Diseñar y escribir la ruta `POST /plan` (paso 4) | 60 min | 2:20 |
| ☕ | Descanso: levántate, agua, mira por la ventana | 10 min | 2:30 |
| 4 | Preparar el paso 5: el modelo del plan de la IA | 40 min | 3:10 |
| 5 | Revisión de código: entrena el criterio | 30 min | 3:40 |
| 6 | Pendientes pequeños y decisiones | 15 min | 3:55 |
| 7 | Cierre: lista para cuando aterrices | 5 min | 4:00 |

Si el vuelo se alarga, repasa los ejercicios que peor te salieron. Si se acorta, el bloque 6 es el más prescindible.

---

## Bloque 1 · Repaso de tu código (35 min)

**Objetivo:** que puedas explicar sin mirar qué hace cada pieza que ya existe, porque la ruta del paso 4 las conecta todas.

### 1.1 El flujo completo (lee, 5 min)

```
Formulario HTML ──► Semana (app/modelos.py)          valida: 7 días, hora sí/no, peso 30–200
                      │
                      ▼
               clasificar_semana (app/calendario.py)  ──► list[TipoDia] (7 elementos)
                      │
                      ▼
     REGLAS_POR_DIA[tipo].calcular_gramos(peso, tipo)  (app/reglas.py)
                      │
                      ▼
               list[ObjetivoDiaGramos] ──► resultados.html
```

La regla de oro del proyecto: **la IA propone y el código verifica.** Todo lo de este diagrama es código determinista: misma entrada → misma salida, siempre. Por eso se puede testear.

### 1.2 Tu código, para tenerlo delante

`app/modelos.py` (resumido):
```python
class TipoActividad(StrEnum):
    PARTIDO = "partido"
    ENTRENO_FUERTE = "entreno_fuerte"
    ENTRENO_SUAVE  = "entreno_suave"
    DESCANSO = "descanso"

class Dia(BaseModel):
    hora: time | None = None
    actividad: TipoActividad
    # model_validator: con actividad → hora obligatoria; en descanso → hora prohibida

class Semana(BaseModel):
    dias: list[Dia] = Field(min_length=7, max_length=7)
    peso_kg: float = Field(ge=30, le=200)
```

`app/calendario.py`:
```python
def clasificar_semana(semana: Semana) -> list[TipoDia]:
    dias = semana.dias
    resultado: list[TipoDia] = []
    for i, dia in enumerate(dias):
        manana_hay_partido = dias[(i + 1) % 7].actividad is TipoActividad.PARTIDO
        if dia.actividad is not TipoActividad.PARTIDO and manana_hay_partido:
            resultado.append(TipoDia.DIA_ANTES_PARTIDO)
        else:
            resultado.append(DE_ACTIVIDAD_A_TIPO_DIA[dia.actividad])
    return resultado
```

`app/reglas.py` (las cifras en g/kg):

| Tipo de día | Hidratos (g/kg) | Proteína (g/kg) | Grasa (% energía) |
|---|---|---|---|
| partido | 6–8 | 1,6–2,2 | 20–35 |
| dia_antes_partido | 6–8 | 1,6–2,2 | 20–35 |
| entreno_fuerte | 5–6 | 1,6–2,2 | 20–35 |
| entreno_suave | 3–5 | 1,6–2,2 | 20–35 |
| descanso | 3–5 | 1,6–2,2 | 20–35 |

### Ejercicios del bloque 1 (30 min)

**E1.1** Clasifica a mano esta semana (escribe los 7 `TipoDia`):
L entreno fuerte · M descanso · X entreno suave · J entreno fuerte · V entreno suave · S partido · D descanso

**E1.2** Igual, pero ahora hay partido el **sábado y el domingo**. ¿Qué cambia?

**E1.3** Igual que E1.1, pero el **lunes** es partido en vez de entreno fuerte. ¿Qué le pasa al domingo? ¿Por qué? (Pista: busca `% 7`.) ¿Es correcto en la vida real? (Lee la decisión del 2026-11-12 en `decisiones.md` si la recuerdas.)

**E1.4** Un jugador de **70 kg** en día de partido. Calcula a mano el rango de hidratos y de proteína en gramos. ¿Y en descanso?

**E1.5** Explica con tus palabras (2–3 frases cada una):
- a) ¿Por qué `calcular_gramos` **crea** un objeto nuevo en vez de modificar la regla?
- b) ¿Por qué la grasa no se convierte a gramos en el motor de reglas?
- c) ¿Qué pasa si creo `Dia(actividad="descanso", hora="18:00")`? ¿Y `Dia(actividad="partido")`?
- d) ¿Qué pasa con `Semana(dias=[...6 días...], peso_kg=70)`?

**E1.6** En `clasificar_semana` se usa `is` para comparar enums. ¿Funcionaría con `==`? ¿Y si comparas `dia.actividad == "partido"` (un texto)? Piensa en qué es un `StrEnum`.

> Pista E1.6: un `StrEnum` **es** un `str` (hereda de él). ¿Qué devuelve `"partido" == TipoActividad.PARTIDO`?

---

## Bloque 2 · Cómo viaja un formulario por HTTP (45 min)

**Objetivo:** entender exactamente qué datos le llegan a tu ruta, para no llevarte sorpresas al escribirla.

### 2.1 Petición y respuesta (lee, 10 min)

HTTP es una conversación de **una pregunta y una respuesta**, y no tiene memoria: cada petición llega sola, sin saber nada de las anteriores (por eso los rechazados del paso 6b viajarán en campos ocultos).

- **GET /** → "dame la página". Tu ruta `inicio` devuelve `formulario.html`.
- **POST /plan** → "toma estos datos y haz algo con ellos". El navegador la envía al pulsar el botón, porque el formulario dice `<form method="post" action="/plan">`.

La respuesta lleva un **código de estado**:
| Código | Significa | Cuándo lo verás |
|---|---|---|
| 200 | OK | todo bien |
| 404 | no existe esa ruta | escribes mal la URL |
| 405 | método no permitido | haces GET a una ruta que solo acepta POST |
| 422 | datos que no se pueden procesar | FastAPI/Pydantic rechazan lo que enviaste |
| 500 | error en el servidor | tu código lanza una excepción que nadie captura |

### 2.2 Qué envía exactamente el navegador (lee, 10 min)

Tu `formulario.html` tiene, para cada día `i` de 0 a 6, un `<select name="actividad_i">` y un `<input type="time" name="hora_i">`, y además `<input type="number" name="peso_kg">`.

Al enviar, el navegador manda el cuerpo de la petición así (formato `application/x-www-form-urlencoded`):

```
actividad_0=entreno_fuerte&hora_0=19%3A30&actividad_1=descanso&hora_1=&...&peso_kg=70.5
```

Tres cosas **muy importantes**:
1. **Todo llega como texto (`str`)**. `"70.5"` no es un `float`, `"19:30"` no es un `time`. Alguien tiene que convertirlo → Pydantic lo hace por ti cuando creas el modelo (modo "lax": acepta `"70.5"` para un `float` y `"19:30"` para un `time`).
2. **Un `input` vacío NO desaparece: llega como texto vacío `""`**. Fíjate en `hora_1=`. Y `""` no es `None`. Tu `Dia` dice "en descanso, la hora debe ser `None`" → si le pasas `""`, ¿qué pasa? (Lo verás en E2.3.)
3. **El `required` y el `min="30"` del HTML no te protegen.** Son una ayuda del navegador; cualquiera puede mandar una petición sin pasar por tu formulario (con `curl`, con un script…). Por eso validamos en el servidor con `Semana`. Regla: **nunca confíes en lo que llega del cliente.**

`%3A` es `:` codificado (la URL no puede llevar ciertos caracteres tal cual). FastAPI lo descodifica solo; tú recibes `"19:30"`.

### 2.3 Cómo se leen esos datos en FastAPI (lee, 10 min)

Hay dos formas. Te recomiendo la segunda para este caso:

**Forma A: un parámetro por campo, con `Form`:**
```python
from fastapi import Form

@app.post("/plan")
def plan(request: Request, actividad_0: str = Form(), hora_0: str = Form(""), ...):
```
Con 7 días son 15 parámetros escritos a mano. Mucho texto repetido → fácil equivocarse.

**Forma B: leer el formulario entero con `await request.form()`:**
```python
@app.post("/plan", response_class=HTMLResponse)
async def plan(request: Request):
    formulario = await request.form()
    actividad_lunes = formulario.get("actividad_0")   # → "entreno_fuerte" (str) o None si no vino
```
- `request.form()` devuelve algo parecido a un diccionario. `.get(clave)` devuelve `None` si la clave no está.
- **¿Por qué `async` y `await`?** Leer el cuerpo de la petición es esperar datos que llegan por la red. `await` significa "espera a que esto termine, y mientras tanto deja al servidor atender a otros". Regla práctica: **si usas `await` dentro, la función tiene que ser `async def`**. No hace falta entender más por ahora.
- Con la forma B puedes usar un **bucle** `for i in range(7)` y construir `f"actividad_{i}"`. Es la ventaja clave.

Nombres de librería que vas a necesitar (te los doy directamente):
- `await request.form()` → leer el formulario
- `from pydantic import ValidationError` → la excepción que lanza Pydantic si los datos no valen
- `plantillas.TemplateResponse(request, "plantilla.html", {"clave": valor}, status_code=...)` → pintar una plantilla
- En tests: `cliente.post("/plan", data={...})` → enviar un formulario desde el `TestClient`

### Ejercicios del bloque 2 (15 min)

**E2.1** Escribe la línea de cuerpo que enviaría el navegador para: lunes partido a las 18:00, el resto descanso, peso 68. (No hace falta codificar `:` como `%3A`.)

**E2.2** ¿Qué código de estado esperas en cada caso? a) GET a `/plan` cuando solo existe la ruta POST. b) POST a `/plan` antes de haberla escrito. c) Tu ruta lanza un `ValidationError` y no lo capturas.

**E2.3** El martes es descanso y la hora llega como `""`. Si haces `Dia(actividad="descanso", hora="")`:
- a) ¿Qué crees que pasa? (Piensa: ¿Pydantic puede convertir `""` en un `time`?)
- b) Escribe **una línea** que convierta `""` en `None` y deje `"19:30"` como está.

> Pista E2.3b: en Python, `""` es "falso" en un `if`. ¿Qué devuelve `"" or None`? ¿Y `"19:30" or None`?

**E2.4** Un usuario malicioso envía `peso_kg=-5` saltándose el formulario. ¿Qué parte de tu código lo para? ¿En qué momento exacto?

---

## Bloque 3 · La ruta `POST /plan` (60 min) ⭐ el bloque principal

**Objetivo:** salir del avión con la ruta del paso 4 escrita en papel, para pasarla al ordenador en 10 minutos. Esta parte es **tuya** (la lógica central la escribes tú). Las pistas van graduadas.

### 3.1 Qué tiene que hacer la ruta (lee, 5 min)

Lo dice el `TODO` de `app/main.py`:
```python
# TODO (usuario): ruta POST /plan
#   formulario -> Semana -> clasificar_semana -> calcular_gramos para cada día
#   y devolver plantillas.TemplateResponse(request, "resultados.html", {"semana": ..., "objetivos": ...})
```
Y `resultados.html` espera:
- `semana`: un objeto `Semana` (usa `semana.peso_kg` y `semana.dias[i].hora`)
- `objetivos`: una `list[ObjetivoDiaGramos]` de 7 elementos, **en el mismo orden** (0 = lunes)

### 3.2 Ejercicio guiado en micropasos (40 min)

Escribe cada paso en papel. Son 1–3 líneas cada uno.

**P1. La cabecera.** Escribe el decorador y la definición de la función. Debe responder a POST en `/plan`, devolver HTML y poder usar `await`.
> Pista: copia la de `inicio` y cambia tres cosas.

**P2. Leer el formulario.** Una línea que guarde el formulario en una variable.

**P3. Construir los 7 `Dia`.** Crea una lista vacía `dias` y un bucle de 0 a 6. En cada vuelta: saca la actividad y la hora del formulario, convierte la hora vacía en `None` (E2.3b) y añade un `Dia(...)` a la lista.
> Ejemplo análogo (no es la solución):
> ```python
> notas = []
> for i in range(3):
>     texto = datos.get(f"nota_{i}")
>     notas.append(Nota(valor=texto))
> ```

**P4. Construir la `Semana`.** Una línea, con `dias` y el peso del formulario.

**P5. ¿Y si los datos no valen?** P3 y P4 pueden lanzar `ValidationError` (descanso con hora, partido sin hora, peso fuera de rango…). Si no lo capturas, el usuario ve un error 500. Rodea P3 y P4 con `try / except ValidationError`. Dentro del `except`, devuelve otra vez `formulario.html` con un mensaje de error y `status_code=422`.
> Ejemplo análogo:
> ```python
> try:
>     edad = int(texto)
> except ValueError:
>     return "Eso no es un número"
> ```
> Pregunta para pensar: ¿por qué es mejor **no** meter en el `try` el resto de la función (clasificar y calcular)? (Pista: si ahí hay un fallo, ¿es culpa del usuario o tuya?)

**P6. Clasificar.** Una línea: `tipos = ...`

**P7. Calcular los objetivos.** Para cada `tipo` de `tipos`, busca su regla en `REGLAS_POR_DIA` y llama a `calcular_gramos(peso, tipo)`. Hazlo primero con un `for` y `append`. Si te sobra tiempo, reescríbelo como *list comprehension* (`[... for tipo in tipos]`).

**P8. Responder.** Devuelve `resultados.html` con `semana` y `objetivos`.

**P9. Imports.** ¿Qué tienes que importar arriba de `main.py`? Haz la lista (son 4 nombres, de 3 módulos distintos). Recuerda: dentro de `app/` se importa siempre con `app.` delante.

**P10. El mensaje de error en la plantilla.** `formulario.html` todavía no muestra ningún error. Escribe las 3 líneas de Jinja2 que mostrarían `error` solo si existe.
> Pista: `{% if ... %} ... {% endif %}` y `{{ variable }}`.

### 3.3 Tests de la ruta (15 min)

Cada función con lógica lleva su test. Diseña en papel (nombre + qué envías + qué compruebas) estos 4 tests para `tests/test_rutas.py`:

1. Una semana válida devuelve 200 y aparece "Día antes de partido" donde toca.
2. Un jugador de 70 kg en día de partido ve los hidratos `420–560` (usa tu cálculo de E1.4).
3. Descanso **con** hora → 422.
4. Peso fuera de rango (p. ej. `"20"`) → 422.

> Pista: prepara una función auxiliar que devuelva un diccionario con una semana válida (todo descanso, horas `""`, peso `"70"`), y en cada test cambia solo lo que necesites. Así cada test se lee en 3 líneas.
> `cliente.post("/plan", data=datos)` → `respuesta.status_code`, `respuesta.text`.
> Para cada test pregúntate: **¿qué cambio en la ruta haría fallar este test?** Si no se te ocurre ninguno, el test no sirve (lección de la sesión del 2026-11-22).

---

## ☕ Descanso (10 min)

En serio: levántate, estira las piernas, bebe agua. La cabeza consolida lo aprendido cuando paras.

---

## Bloque 4 · Preparar el paso 5: el modelo del plan de la IA (40 min)

**Objetivo:** llegar al paso 5 con una propuesta de diseño propia. El paso 5 se hace **juntos**, así que aquí no hay una única respuesta correcta: hay buenas razones.

### 4.1 El problema (lee, 10 min)

En el paso 6 la IA devolverá un JSON con el plan. Antes de escribir el prompt definimos el **contrato**: un modelo Pydantic que diga exactamente qué forma tiene ese JSON. Si la IA devuelve algo que no encaja, Pydantic lanza `ValidationError` y le pedimos que lo corrija (un reintento).

Después el código **verifica** el plan: suma los gramos de cada día y comprueba que caen dentro de los rangos de `ObjetivoDiaGramos`. Y comprueba la grasa así:

```
energía (kcal) = hidratos_g × 4 + proteína_g × 4 + grasa_g × 9
% grasa        = (grasa_g × 9) / energía × 100
```

Ejemplo de JSON que podría devolver la IA para **un** día:
```json
{
  "comidas": [
    {
      "nombre": "Desayuno",
      "alimentos": [
        {"nombre": "Avena", "cantidad_g": 80, "hidratos_g": 48, "proteina_g": 10, "grasa_g": 5},
        {"nombre": "Plátano", "cantidad_g": 120, "hidratos_g": 27, "proteina_g": 1, "grasa_g": 0}
      ]
    }
  ]
}
```

### Ejercicios del bloque 4 (30 min)

**E4.1** Diseña las clases Pydantic (solo nombres de clase, campos y tipos, en papel) para el plan de una semana. Piensa de dentro hacia fuera: `Alimento` → `Comida` → `PlanDia` → `PlanSemana`. Para cada campo decide: ¿tipo?, ¿límites con `Field` (p. ej. `ge=0`)?, ¿lista con longitud fija?

**E4.2** Preguntas de diseño (respóndelas con 1–2 frases y tu porqué; luego irán a `decisiones.md`):
- a) ¿El `PlanDia` debe llevar el `tipo_dia`, o lo sabemos ya por la posición? (Recuerda la decisión "una sola fuente de verdad" del 2026-11-22.)
- b) ¿Quién calcula los **totales** del día: la IA (un campo `total_hidratos_g` en el JSON) o el código (sumando)? ¿Por qué?
- c) ¿Usarías `extra="forbid"` en estos modelos? ¿Qué ganas y qué arriesgas?
- d) Pregunta difícil: los gramos de hidratos **de cada alimento** también los escribe la IA. ¿No es eso "la IA calculando cifras nutricionales"? ¿Cómo lo resolverías más adelante? (Pista: piensa en qué hará la v0.2 con los precios.)

**E4.3** Calcula a mano la energía y el % de grasa, y di si cumple el rango 20–35 %:
- a) 450 g hidratos, 130 g proteína, 80 g grasa
- b) 300 g hidratos, 120 g proteína, 120 g grasa

**E4.4** Escribe en papel la función `porcentaje_grasa(hidratos_g, proteina_g, grasa_g) -> float`. ¿Qué pasa si los tres valen 0? ¿Qué debería pasar? Escribe también los nombres de 3 tests que le harías.

---

## Bloque 5 · Revisión de código: entrena el criterio (30 min)

Tres fragmentos. **Alguno puede estar bien y alguno puede tener un fallo.** Para cada uno responde las 4 preguntas de siempre:
1. ¿Qué hace, en una frase?
2. ¿Qué pasa con una entrada rara?
3. ¿Qué cambiarías y por qué?
4. ¿Lo aceptas: sí o no?

**R1.** Conversión de la hora en la ruta:
```python
for i in range(7):
    hora = formulario.get(f"hora_{i}")
    if hora == "":
        hora = None
    dias.append(Dia(actividad=formulario.get(f"actividad_{i}"), hora=hora))
```

**R2.** Porcentaje de grasa:
```python
def porcentaje_grasa(hidratos_g: float, proteina_g: float, grasa_g: float) -> float:
    energia = hidratos_g * 4 + proteina_g * 4 + grasa_g * 4
    return grasa_g * 9 / energia * 100


def test_porcentaje_grasa_dentro_de_rango():
    resultado = porcentaje_grasa(450, 130, 80)
    assert 20 <= resultado <= 35
```

**R3.** Una versión "simplificada" de la clasificación:
```python
def clasificar_semana(semana: Semana) -> list[TipoDia]:
    dias = semana.dias
    resultado = []
    for i in range(6):
        if dias[i].actividad is not TipoActividad.PARTIDO and dias[i + 1].actividad is TipoActividad.PARTIDO:
            resultado.append(TipoDia.DIA_ANTES_PARTIDO)
        else:
            resultado.append(DE_ACTIVIDAD_A_TIPO_DIA[dias[i].actividad])
    return resultado
```
> Pregunta extra para R3: ¿alguno de tus 6 tests de `test_calendario.py` lo detectaría? ¿Cuál? Si no lo sabes, apúntalo para mirarlo al aterrizar.

---

## Bloque 6 · Pendientes pequeños (15 min)

De `docs/estado.md`. Escribe tu respuesta en papel; al aterrizar la pasamos al código o a `decisiones.md`.

**E6.1** Rellena el comentario de `app/modelos.py`:
`# Límites del peso: mínimo ___ porque ___; máximo ___ porque ___`
(Pista: ¿quién usa la app? ¿qué protege cada límite: errores de tecleo, unidades equivocadas como libras o gramos…?)

**E6.2** Escribe el comentario para `Rango` que explique por qué se acepta `Rango(minimo=6, maximo=6)`.

**E6.3** Hoy `Rango(minimo=20, maximo=150)` se acepta para la grasa, y un porcentaje de 150 no tiene sentido. Propón **dos** soluciones distintas y elige una con su porqué. (Pista: una toca `Rango`; la otra crea algo nuevo solo para porcentajes.)

**E6.4** Decide sobre `extra="forbid"`: ¿en las reglas?, ¿en el plan de la IA?, ¿en ninguno? Escribe la entrada para `decisiones.md` con el formato de siempre (fecha, decisión, porqué).

---

## Bloque 7 · Cierre (5 min)

Al aterrizar, en este orden:
1. [ ] Pasar la ruta del bloque 3 a `app/main.py` y guardar (¡ojo al ● de la pestaña!).
2. [ ] Añadir el `{% if error %}` a `formulario.html`.
3. [ ] Escribir los 4 tests del bloque 3.3 y lanzar `pytest` **desde la raíz y con el `.venv` activado**.
4. [ ] Probar a mano: `uvicorn app.main:app --reload` y abrir `http://127.0.0.1:8000`.
5. [ ] Contarme tus respuestas de los bloques 4, 5 y 6 para revisarlas juntos.
6. [ ] Commit pequeño: "Paso 4: ruta POST /plan con validación y tests".

Autoevaluación rápida (de 1 a 5): ¿sabría explicar a un compañero… (a) qué llega en un POST de formulario? (b) por qué `""` no es `None`? (c) por qué se captura `ValidationError` solo alrededor de la entrada? (d) cómo se calcula el % de grasa?

---
---
---

# 🔑 SOLUCIONES

> ⚠️ Para aquí si no has intentado el ejercicio. Mirar la solución antes de pelearte con el problema te da la sensación de entenderlo, pero no el aprendizaje.

<br><br><br><br><br><br>

## Soluciones del bloque 1

**E1.1** L `entreno_fuerte` · M `descanso` · X `entreno_suave` · J `entreno_fuerte` · V `dia_antes_partido` · S `partido` · D `descanso`.
El domingo mira al lunes (`(6 + 1) % 7 = 0`), que es entreno fuerte, así que el domingo es descanso.

**E1.2** V `dia_antes_partido` · S `partido` · D `partido`. El sábado tiene partido mañana, pero **partido gana** (prioridad partido > día antes > actividad). El resto igual que E1.1.

**E1.3** El domingo pasa a `dia_antes_partido` porque `(6 + 1) % 7 = 0` → mira el lunes **de esta misma semana**. En la vida real solo es correcto si el lunes siguiente también hay partido. Es la limitación conocida que se revisará en v0.5 con Google Calendar. La semana completa queda: L `partido` · M `descanso` · X `entreno_suave` · J `entreno_fuerte` · V `dia_antes_partido` · S `partido` · D `dia_antes_partido`.

**E1.4** 70 kg, partido: hidratos 6×70 = **420** a 8×70 = **560 g**; proteína 1,6×70 = **112** a 2,2×70 = **154 g**.
Descanso: hidratos 3×70 = **210** a 5×70 = **350 g**; proteína igual, 112–154 g.

**E1.5**
- a) Si modificara la regla, como `REGLAS_POR_DIA` es compartida por todos, el siguiente jugador recibiría cifras ya multiplicadas (el `=` no copia, pone otra etiqueta al mismo objeto). Además, al crear un objeto nuevo Pydantic lo **valida** (un peso negativo da `minimo < 0` → error), mientras que cambiar un campo después no se valida.
- b) Porque el % de grasa depende de la energía total del menú, y el menú todavía no existe: lo propone la IA después. Se verifica cuando llega el plan.
- c) `Dia(actividad="descanso", hora="18:00")` → `ValidationError` ("Descanso no puede llevar hora"). `Dia(actividad="partido")` → `ValidationError` ("partido necesita una hora"), porque `hora` vale `None` por defecto.
- d) `ValidationError`: `min_length=7` en `dias`.

**E1.6** Sí funcionaría con `==`, e incluso `dia.actividad == "partido"` da `True`, porque un `StrEnum` hereda de `str`. Se usa `is` porque cada miembro de un enum es un objeto único (es más estricto: `"partido" is TipoActividad.PARTIDO` es `False`). Comparar con el texto `"partido"` funciona, pero si un día te equivocas y escribes `"partdio"`, no salta ningún error: simplemente nunca es igual. Con `TipoActividad.PARTDIO` Python lanza `AttributeError` en el acto. Por eso se compara con el enum.

## Soluciones del bloque 2

**E2.1**
```
actividad_0=partido&hora_0=18:00&actividad_1=descanso&hora_1=&actividad_2=descanso&hora_2=&actividad_3=descanso&hora_3=&actividad_4=descanso&hora_4=&actividad_5=descanso&hora_5=&actividad_6=descanso&hora_6=&peso_kg=68
```
Fíjate en que las horas vacías **sí aparecen** (`hora_1=`).

**E2.2** a) **405**: la URL existe, pero no para GET. b) **404**: hoy `/plan` no existe para ningún método. (La diferencia: 404 = no hay nada en esa URL; 405 = hay algo, pero no con ese método.) c) **500**: excepción no capturada.

**E2.3**
- a) Pydantic intenta convertir `""` en un `time`, no puede y lanza `ValidationError` (algo como "Input should be in a valid time format"). Así que un descanso perfectamente válido daría error. Por eso hay que convertir antes.
- b) `hora = formulario.get(f"hora_{i}") or None`
  `"" or None` → `None` (porque `""` es falso, `or` devuelve lo segundo). `"19:30" or None` → `"19:30"`. Y si la clave no viene, `.get` ya da `None`, y `None or None` → `None`.

**E2.4** El `Field(ge=30, le=200)` de `Semana.peso_kg`. Salta **en el momento de crear** `Semana(...)`, con un `ValidationError`. Pydantic valida al crear el objeto.

## Soluciones del bloque 3

### La ruta completa (`app/main.py`)

```python
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.calendario import clasificar_semana
from app.modelos import Dia, Semana
from app.reglas import REGLAS_POR_DIA

# ... (app, CARPETA_PLANTILLAS, plantillas e inicio se quedan igual) ...


@app.post("/plan", response_class=HTMLResponse)
async def plan(request: Request):
    """Recibe la semana del formulario y muestra los objetivos de cada día."""
    formulario = await request.form()

    # 1) Entrada: convertir el formulario en una Semana. Solo aquí puede fallar
    #    por culpa del usuario, así que solo esto va dentro del try.
    try:
        dias = []
        for i in range(7):
            dias.append(
                Dia(
                    actividad=formulario.get(f"actividad_{i}"),
                    hora=formulario.get(f"hora_{i}") or None,  # "" (vacío) -> None
                )
            )
        semana = Semana(dias=dias, peso_kg=formulario.get("peso_kg"))
    except ValidationError as error:
        return plantillas.TemplateResponse(
            request,
            "formulario.html",
            {"error": str(error)},
            status_code=422,
        )

    # 2) Lógica: clasificar y calcular (aquí un fallo sería un bug nuestro, no del usuario).
    tipos = clasificar_semana(semana)
    objetivos = [REGLAS_POR_DIA[tipo].calcular_gramos(semana.peso_kg, tipo) for tipo in tipos]

    # 3) Salida
    return plantillas.TemplateResponse(
        request,
        "resultados.html",
        {"semana": semana, "objetivos": objetivos},
    )
```

P7 con `for` (equivalente a la comprehension):
```python
objetivos = []
for tipo in tipos:
    regla = REGLAS_POR_DIA[tipo]
    objetivos.append(regla.calcular_gramos(semana.peso_kg, tipo))
```

**Por qué el `try` solo rodea la entrada (P5):** un `ValidationError` al crear `Dia`/`Semana` significa "el usuario mandó datos malos" → le enseñamos el formulario con el error (422). Si clasificar o calcular fallara, sería un **bug nuestro**; si lo metiéramos en el mismo `try`, se lo enseñaríamos al usuario como si fuera culpa suya y no nos enteraríamos. Mejor que salte el 500 y lo veamos.

**P9 imports:** `ValidationError` (de `pydantic`), `clasificar_semana` (de `app.calendario`), `Dia` y `Semana` (de `app.modelos`), `REGLAS_POR_DIA` (de `app.reglas`).

**P10, en `formulario.html`** (dentro del `{% block contenido %}`, antes del `<form>`):
```html
{% if error %}
<p class="error">Revisa los datos: {{ error }}</p>
{% endif %}
```
Mejora para más adelante: `str(error)` es un texto técnico en inglés. Se puede recorrer `error.errors()` para mostrar mensajes más amables. No hace falta en el paso 4.

### Los tests (`tests/test_rutas.py`)

```python
def semana_valida():
    """Una semana de 7 descansos, 70 kg. Cada test cambia solo lo que necesita."""
    datos = {"peso_kg": "70"}
    for i in range(7):
        datos[f"actividad_{i}"] = "descanso"
        datos[f"hora_{i}"] = ""
    return datos


def test_plan_semana_valida_marca_dia_antes_de_partido():
    datos = semana_valida()
    datos["actividad_5"] = "partido"  # sábado
    datos["hora_5"] = "18:00"
    respuesta = cliente.post("/plan", data=datos)
    assert respuesta.status_code == 200
    assert "Día antes de partido" in respuesta.text


def test_plan_calcula_hidratos_de_partido_con_el_peso():
    datos = semana_valida()
    datos["actividad_5"] = "partido"
    datos["hora_5"] = "18:00"
    respuesta = cliente.post("/plan", data=datos)
    assert "420–560" in respuesta.text  # 6–8 g/kg × 70 kg (ojo: es una raya "–", no un guion "-")


def test_plan_descanso_con_hora_da_422():
    datos = semana_valida()
    datos["hora_2"] = "10:00"  # miércoles, descanso con hora
    respuesta = cliente.post("/plan", data=datos)
    assert respuesta.status_code == 422


def test_plan_peso_fuera_de_rango_da_422():
    datos = semana_valida()
    datos["peso_kg"] = "20"
    respuesta = cliente.post("/plan", data=datos)
    assert respuesta.status_code == 422
```

**¿Qué cambio haría fallar cada test?**
1. Olvidar el `% 7`, no llamar a `clasificar_semana`, o equivocarse de posición.
2. Pasar un peso incorrecto a `calcular_gramos` (p. ej. un número fijo) o usar la regla de otro tipo de día.
3. Quitar el `try/except` (daría 500) o olvidar `status_code=422` (daría 200).
4. Lo mismo que el 3, pero por el lado del peso. Aunque el `min="30"` del HTML exista, el test envía directamente: demuestra que el servidor se defiende solo.

Test extra si quieres: una semana de 7 descansos con todas las horas `""` → 200. Este test **fallaría si olvidas el `or None`**. Es probablemente el más valioso de todos.

## Soluciones del bloque 4

**E4.1** Una propuesta (no la única):
```python
class Alimento(BaseModel):
    nombre: str = Field(min_length=1)
    cantidad_g: float = Field(gt=0)
    hidratos_g: float = Field(ge=0)
    proteina_g: float = Field(ge=0)
    grasa_g: float = Field(ge=0)


class Comida(BaseModel):
    nombre: str = Field(min_length=1)          # "Desayuno", "Comida", "Merienda"…
    alimentos: list[Alimento] = Field(min_length=1)


class PlanDia(BaseModel):
    comidas: list[Comida] = Field(min_length=1)


class PlanSemana(BaseModel):
    dias: list[PlanDia] = Field(min_length=7, max_length=7)  # posición 0 = lunes, como Semana
```

**E4.2**
- a) Por posición, igual que `Semana`: el tipo de día ya lo sabe el código (`clasificar_semana`). Si la IA también lo escribiera, podrían contradecirse (una sola fuente de verdad). Coste: hay que confiar en que la IA respete el orden, y `min_length=7, max_length=7` lo vigila a medias.
- b) **El código suma.** Si la IA diera los totales, podría equivocarse al sumar (los modelos de lenguaje fallan en aritmética) y la verificación compararía un número inventado. "La IA propone y el código verifica": el código suma los alimentos y compara con los rangos.
- c) A favor: si la IA añade campos raros o escribe mal un nombre (`"proteinas_g"` en vez de `"proteina_g"`), con `extra="forbid"` salta el error y se reintenta, en vez de perder el dato en silencio. En contra: más reintentos (más coste y tiempo). Para el plan de la IA, **tiene mucho sentido**, porque ahí un campo mal escrito es justo el fallo típico. Con `messages.parse(output_format=...)` además el esquema ya guía a la IA.
- d) Sí, es la zona gris del diseño. En v0.1 se acepta porque el código al menos verifica la coherencia (sumas y rangos), pero las cifras por alimento siguen siendo de la IA. Solución futura, como con los precios en v0.2: una **tabla propia de composición de alimentos** (p. ej. BEDCA o USDA), donde la IA solo elige alimento y cantidad y el código calcula los macros. Merece una entrada en `decisiones.md` y una nota en `estado.md`.

**E4.3**
- a) 450×4 + 130×4 + 80×9 = 1800 + 520 + 720 = **3040 kcal**. Grasa: 720 / 3040 × 100 = **23,7 %** → cumple.
- b) 300×4 + 120×4 + 120×9 = 1200 + 480 + 1080 = **2760 kcal**. Grasa: 1080 / 2760 × 100 = **39,1 %** → **no cumple** (pasa de 35).

**E4.4**
```python
def porcentaje_grasa(hidratos_g: float, proteina_g: float, grasa_g: float) -> float:
    energia = hidratos_g * 4 + proteina_g * 4 + grasa_g * 9
    if energia == 0:
        raise ValueError("Un menú sin energía no tiene porcentaje de grasa")
    return grasa_g * 9 / energia * 100
```
Con los tres a 0 la versión sin el `if` lanza `ZeroDivisionError`. Lanzar un error con un mensaje claro es mejor que devolver 0 (que "cumpliría" sin sentido o fallaría en silencio). Aunque en la práctica `PlanDia` exige al menos una comida con un alimento, la función no debe depender de eso.
Tests: `test_porcentaje_grasa_ejemplo_a_da_23_7` (con `pytest.approx(23.68, abs=0.01)`), `test_porcentaje_grasa_solo_grasa_da_100`, `test_porcentaje_grasa_sin_energia_lanza_error` (con `pytest.raises(ValueError)`).
El test "solo grasa" es muy bueno: con 0, 0, 10 el resultado tiene que ser exactamente 100. Un fallo en los multiplicadores lo rompe.

## Soluciones del bloque 5

**R1: está bien. ✅** Hace lo mismo que `or None`, solo que más largo.
- Qué hace: convierte la hora vacía en `None` antes de crear cada `Dia`.
- Entrada rara: si `hora_i` no viene, `.get` devuelve `None`, que no es `""`, y se queda en `None`: bien. Si viene `"  "` (espacios), no es `""` → Pydantic falla con 422; aceptable.
- Qué cambiaría: podría ser `or None` en una línea, pero es cuestión de gusto; la versión larga es incluso más legible para quien empieza.
- Veredicto: **sí**. Si buscaste un fallo y no lo había, bien: aceptar código correcto también es criterio. No hay que inventar fallos.

**R2: tiene un fallo. ❌** La energía multiplica la grasa por **4** en vez de por **9**.
- Con 450/130/80: energía = 1800 + 520 + 320 = 2640 → 720 / 2640 = **27,3 %** (el correcto es 23,7 %).
- **Lo traicionero:** el test pasa igual, porque 27,3 también está entre 20 y 35. Un test que solo comprueba "está en el rango" no detecta el fallo. Hay que comparar con el **valor exacto** calculado a mano (`pytest.approx(23.68, abs=0.01)`), o usar el caso "solo grasa" (0, 0, 10): con el fallo daría 225 % en vez de 100 %.
- Entrada rara: todo a 0 → `ZeroDivisionError`.
- Veredicto: **no**. Es la misma lección que el 2026-11-22: un test tiene que poder fallar.

**R3: tiene un fallo. ❌** `range(6)` solo recorre lunes a sábado: **el domingo desaparece**, y la lista tiene 6 elementos en vez de 7. Además el sábado mira a `dias[6]` (domingo), pero el domingo nunca mira al lunes: se perdió el `% 7`.
- Si en vez de `range(6)` pusieras `range(7)`, `dias[i + 1]` con `i = 6` daría `IndexError`. Por eso existía el `% 7`: el "arreglo" de `range(6)` esconde el error en lugar de resolverlo.
- Consecuencia en la ruta: `objetivos` tendría 6 elementos y `resultados.html` mostraría solo 6 filas, **sin dar ningún error**. Los fallos que no hacen ruido son los peores.
- Lo detectaría cualquier test que compruebe `len(resultado) == 7` o que mire el domingo (p. ej. "partido el lunes → domingo es día antes de partido"). Al aterrizar, mira si tus tests de `test_calendario.py` cubren eso.
- Veredicto: **no**.

## Soluciones del bloque 6

**E6.1** Ejemplo: `# Límites del peso: mínimo 30 porque por debajo es casi seguro un error de tecleo (o un niño, fuera del público de la app); máximo 200 porque por encima probablemente se escribió en libras o es otro error.` Lo importante es que **tú** expliques qué protege cada límite: no son cifras médicas, sino una barrera contra datos imposibles.

**E6.2** Ejemplo: `# Se acepta minimo == maximo (p. ej. 6–6): es un objetivo exacto, un caso límite válido. Solo se rechaza maximo < minimo, que es imposible.`

**E6.3** Opción 1: añadir `le=100` a `Rango`. Problema: los gramos también son `Rango` y sí pueden pasar de 100 (420–560 g), así que **rompería** los hidratos. Opción 2: crear `RangoPorcentaje(Rango)`, una subclase con `maximo: float = Field(ge=0, le=100)`, y usarla en `porcentaje_grasa`. Es la buena: el tipo dice qué es, como hiciste al separar g/kg de gramos. (Opción 3 válida: un `model_validator` en las clases de objetivo que compruebe solo la grasa.)

**E6.4** Ejemplo de entrada:
> **2026-11-XX. `extra="forbid"` en el plan de la IA, no en las reglas (v0.1)**
> **Decisión:** el modelo del plan (paso 5) usa `model_config = ConfigDict(extra="forbid")`. Las reglas no.
> **Porqué:** la IA puede escribir mal un nombre de campo y, con el valor por defecto (`extra="ignore"`), el dato se perdería en silencio; así salta el error y se reintenta. Las reglas las escribimos nosotros y tienen tests; añadirlo ahí sería también razonable para detectar erratas, pero es menos urgente.

(Cualquier respuesta con un porqué sólido vale; esta es solo un ejemplo.)

---

_¡Buen vuelo! 🛫 Al aterrizar, abre `docs/estado.md` y sigue la lista del bloque 7._
