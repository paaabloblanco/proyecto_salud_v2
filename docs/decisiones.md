# Registro de decisiones

Formato: fecha, decisión, porqué. Las decisiones se añaden al final y no se borran; si una cambia, se añade una nueva que la sustituye.

---

## 2026-11-12. Stack base (definido en CLAUDE.md)
**Decisión:** Python 3.11+, FastAPI, Jinja2 para el HTML, la API de Claude con validación Pydantic y pytest.
**Porqué:** el objetivo es aprender Python, APIs, IA y cloud. FastAPI usa Pydantic de forma nativa, así que la misma herramienta valida tanto los datos del formulario como el JSON de la IA. Con Jinja2 se evita tener un frontend separado mientras el foco está en el backend.

## 2026-11-12. La IA propone y el código verifica
**Decisión:** los objetivos nutricionales y los precios los calcula siempre el código. La IA solo propone recetas en JSON.
**Porqué:** el código es determinista y se puede testear; la IA no. Así las cifras con impacto en la salud son trazables a una fuente y no dependen de lo que "invente" el modelo.

## 2026-11-12. Estructura de carpetas de v0.1
**Decisión:** paquete `app/` con un archivo por pieza de la arquitectura (`calendario.py`, `reglas.py`, `ia.py`, `planificador.py`, `modelos.py`, `main.py`, `config.py`), plantillas en `app/templates/` y tests en `tests/`.
**Porqué:** cada responsabilidad está en su sitio. `calendario.py` y `reglas.py` son funciones puras, sin FastAPI ni IA, así que se testean rápido y sin internet. Las rutas solo reciben datos y pintan resultados; el planificador se podrá reutilizar en la versión móvil.

## 2026-11-12. Dependencias y entorno
**Decisión:** `venv` + `pip` + `requirements.txt`. Paquetes: fastapi, uvicorn[standard], jinja2, python-multipart, anthropic, pydantic-settings, pytest y httpx.
**Porqué:** `venv` viene con Python y no añade herramientas que aprender. `python-multipart` hace falta para leer formularios HTML; `httpx`, para el `TestClient`; `pydantic-settings` valida el `.env` al arrancar. El SDK `anthropic` trae `messages.parse(output_format=ModeloPydantic)`, que devuelve el JSON ya validado.

## 2026-11-12. Modelo de IA configurable
**Decisión:** `claude-opus-5-5` por defecto, definido en `.env` (`MODELO_IA`).
**Porqué:** se puede cambiar a uno más barato durante las pruebas sin tocar el código.

## 2026-11-12. Orden de construcción: de dentro hacia fuera
**Decisión:** primero los modelos de entrada, la clasificación y las reglas; después la web sin IA; después el esquema del plan; y al final la llamada a la IA.
**Porqué:** la lógica determinista es la base de "el código verifica". La IA cuesta dinero, es lenta y no es determinista, así que se integra cuando todo lo demás ya está probado. Definir el esquema antes que el prompt hace que la IA se adapte a nuestro contrato.

## 2026-11-12. Pedir el peso corporal en el formulario
**Decisión:** el formulario pide el peso en kg y las reglas se expresan en g/kg, como en las guías publicadas (p. ej., la posición conjunta ACSM/AND/DC de 2016, *Nutrition and Athletic Performance*). La altura no se pide.
**Porqué:** las cifras de las guías van en g/kg; sin el peso habría que inventar cantidades absolutas, y eso está prohibido. La altura no hace falta para estas reglas. Además, no pedirla evita cálculos tipo IMC que acercarían la app a consejos de peso, que están fuera de sus límites. El peso se introduce en el formulario y no se guarda en el código.

## 2026-11-12. Renombrar claude.md a CLAUDE.md
**Porqué:** es la convención que reconoce Claude Code en cualquier sistema operativo (en Linux y Mac importan las mayúsculas).

## 2026-11-12. Presupuesto y gustos se aplazan dentro de v0.1
**Decisión:** el paso 1 modela solo los días, la actividad, la hora y el peso. El presupuesto y los gustos se añadirán más adelante.
**Porqué:** se avanza con lo mínimo que necesitan la clasificación (paso 2) y las reglas (paso 3). El `CLAUDE.md` los sigue listando en v0.1, así que habrá que añadirlos antes de cerrar la versión.

## 2026-11-12. Los días se identifican del 1 (lunes) al 7 (domingo)
**Decisión:** el número no es un campo; lo da la **posición** en `Semana.dias`. En el código, `dias[0]` es el lunes y `dias[6]` el domingo; el 1–7 solo se usa al mostrar los días al usuario.
**Porqué:** es más sencillo. Como no hay un campo de número, no puede haber días repetidos y no hace falta validarlo. Coste: hay que recordar que Python empieza a contar desde 0.

## 2026-11-12. Prioridad al clasificar los días
**Decisión:** si se cumplen dos tipos a la vez, manda este orden: **partido > día antes de partido > la actividad elegida por el usuario**.
- Un entreno el día antes de un partido se clasifica como "día antes de partido".
- Con dos partidos seguidos, los dos días son "partido".
**Porqué:** si hay entreno el día antes de un partido, será muy suave, así que lo que importa para la nutrición es preparar el partido. Y un día con partido es siempre día de partido, aunque al día siguiente haya otro.

## 2026-11-12. La hora no se usa para clasificar los días (v0.1)
**Decisión:** la clasificación solo mira la actividad de cada día y la del siguiente.
**Porqué:** simplifica el paso 2. La hora se usará más adelante para colocar las comidas alrededor de las sesiones.

## 2026-11-12. Después del domingo viene el lunes de la misma semana (v0.1)
**Decisión:** para clasificar el domingo se mira el lunes de *esta* semana, como si la semana se repitiera. En el código: el día siguiente al de la posición `i` es el de la posición `(i + 1) % 7`.
**Porqué:** las semanas de entreno suelen ser iguales y así no hay que pedir nada más al usuario. Limitación conocida: si este lunes hay partido y el siguiente no, el domingo se clasifica como "día antes de partido" sin serlo. Es poco probable, porque los partidos suelen ser en fin de semana. Se revisará en v0.5, cuando Google Calendar dé las fechas reales.

## 2026-11-14. Revisión de código con fallos puestos a propósito
**Decisión:** el código que escribe Claude y tiene algo que aprender se entrega como `🔍 REVISIÓN`. Yo lo reviso con 4 preguntas fijas y Claude corrige mi revisión. En más o menos 1 de cada 3 revisiones hay un fallo sutil puesto a propósito, que se revela justo después de mi veredicto y siempre antes del commit.
**Porqué:** leer y juzgar código ajeno (también el de una IA) es una habilidad clave, y así no acepto nada a ciegas. Las preguntas fijas evitan el "parece bien" sin mirar. El fallo aleatorio obliga a revisar de verdad. Que no se pueda commitear sin la revelación garantiza que ningún fallo puesto se quede en el proyecto.
