# Planificador de comidas para jugadores de futsal

## Qué es
App web que genera un plan semanal de comidas para jugadores de futsal según su calendario de entrenos y partidos, sus gustos y su presupuesto. Público: jugadores que no pueden pagar un nutricionista.

Es sobre todo un **proyecto de aprendizaje** (Python, APIs, IA, cloud). Primero será una app web; la versión móvil vendrá más adelante.

## Regla principal de arquitectura: la IA propone y el código verifica
1. **Calendario** → cada día se clasifica: partido, día antes de partido, entreno fuerte, entreno suave o descanso.
2. **Motor de reglas** (Python) → cada tipo de día tiene sus objetivos nutricionales y horarios.
3. **IA** → propone recetas que cumplan esos objetivos, los gustos y el presupuesto. Devuelve JSON.
4. **Código** → comprueba que el plan cumple los objetivos y el presupuesto. Si no, se lo devuelve a la IA para que lo ajuste.

La IA nunca decide los objetivos nutricionales ni calcula precios. Eso lo hace siempre el código.

## Stack
- Backend: Python 3.11+ con FastAPI
- Frontend (v0): HTML con plantillas Jinja2 y el mínimo JavaScript posible
- IA: API de Claude, con la respuesta JSON validada con Pydantic
- Tests: pytest
- Más adelante: Supabase (Postgres y login), despliegue en la nube, Google Calendar y versión móvil

## Límites de seguridad (no negociables)
- No da consejos para enfermedades, alergias ni condiciones médicas: en esos casos recomienda acudir a un profesional.
- No genera dietas agresivas de pérdida de peso ni restricciones calóricas.
- Las reglas nutricionales se basan en guías publicadas de nutrición deportiva, con la fuente citada en el código, y se marcan como "pendiente de validar por un dietista-nutricionista". No se inventan cifras.
- La app muestra un aviso visible: es orientación general y no sustituye a un profesional.

## Metodología de trabajo
Soy estudiante y estoy aprendiendo Python. El objetivo es que entienda cada pieza del proyecto.
- Antes de escribir código, propón un plan corto y espera mi OK.
- Trabaja en pasos pequeños: un cambio que se pueda probar cada vez.
- Explica el porqué de cada decisión técnica, no solo el qué.
- **La lógica central la escribo yo:** clasificación de días, motor de reglas y verificación del presupuesto. Tú me planteas el problema, me das pistas y revisas mi código. No me des la solución salvo que te la pida.
- Lo repetitivo (configuración, plantillas HTML, boilerplate) lo puedes escribir tú, explicándome qué hace.
- Los nombres de funciones de librería dímelos directamente; no hace falta que los busque yo.
- Cada función con lógica lleva su test en pytest.
- Commits pequeños, con mensajes claros en español.
- Nunca subas secretos: las claves van en `.env`, que está en `.gitignore`.

### Revisión de código (entrenar el criterio)
- Cuando Claude escribe código con algo que aprender (no HTML trivial ni configuración), lo entrega marcado como `🔍 REVISIÓN` y yo lo reviso antes de aceptarlo.
- Mi revisión responde siempre: 1) ¿qué hace, en una frase? 2) ¿qué pasa con una entrada rara? 3) ¿qué cambiarías y por qué? 4) ¿lo aceptas: sí o no?
- Claude corrige mi revisión: qué vi bien y qué se me escapó.
- Fallos puestos a propósito: en más o menos 1 de cada 3 revisiones, Claude mete un fallo sutil sin avisar. Solo en bloques `🔍 REVISIÓN`, nunca en la lógica que escribo yo.
- Regla de seguridad: el código de una revisión no se commitea hasta que Claude revela si había fallo puesto. La revelación se hace siempre en la misma sesión, justo después de mi veredicto.

## Contexto entre sesiones
- `docs/estado.md`: qué está hecho, qué es lo siguiente y qué problemas hay abiertos. Léelo al empezar cada sesión y actualízalo al terminar.
- `docs/decisiones.md`: registro breve de cada decisión de diseño y su porqué.

## Versión actual: v0.1
**Objetivo:** una página web donde introduzco mi semana a mano y recibo un plan de comidas por día.
- Formulario: para cada día de la semana, el tipo de actividad (partido, entreno fuerte, entreno suave o descanso) y la hora; peso corporal en kg (las reglas se expresan en g/kg); presupuesto semanal; alimentos que me gustan y que no.
- El backend clasifica los días (incluido "día antes de partido") y aplica las reglas.
- La IA genera el plan y el código valida que el JSON tiene el formato correcto.
- La página muestra el plan por día, con el motivo de cada ajuste (por ejemplo, "más hidratos hoy porque mañana hay partido").

**Fuera de alcance en v0.1:** login, base de datos, precios reales, Google Calendar, despliegue y móvil.

## Hoja de ruta
- v0.2: tabla de precios propia (unos 50 productos) y verificación del presupuesto en código
- v0.3: Supabase para guardar los planes, los gustos y el login
- v0.4: despliegue en la nube
- v0.5: integración con Google Calendar
- v1.0: PWA o app móvil