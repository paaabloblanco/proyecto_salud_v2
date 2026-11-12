# Planificador de comidas para jugadores de futsal

Proyecto de aprendizaje. Ver `CLAUDE.md` para la visión y `docs/estado.md` para el estado actual.

> Orientación general. No sustituye a un dietista-nutricionista.

## Puesta en marcha (Windows)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # y pon tu clave en .env
uvicorn app.main:app --reload
```

Abre http://127.0.0.1:8000. Para los tests: `pytest`.
