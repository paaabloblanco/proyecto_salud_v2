from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_inicio_responde():
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"mensaje": "Hola, el servidor funciona"}
