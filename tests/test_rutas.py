from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_inicio_muestra_el_formulario():
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert "text/html" in respuesta.headers["content-type"]
    # Los 7 días (0..6) y el peso tienen su campo, con los nombres que lee POST /plan
    for i in range(7):
        assert f'name="actividad_{i}"' in respuesta.text
        assert f'name="hora_{i}"' in respuesta.text
    assert 'name="peso_kg"' in respuesta.text


def test_inicio_muestra_el_aviso():
    respuesta = cliente.get("/")
    assert "no sustituye a un dietista-nutricionista" in respuesta.text
