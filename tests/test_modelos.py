import pytest
from pydantic import ValidationError
from app.modelos import Dia, Semana, TipoActividad

def semana_valida() -> dict:
    """Devuelve los datos de una semana correcta.
    Cada test copia esto y cambia solo lo que quiere romper."""
    return {
        "dias": [
            {"actividad": "entreno_fuerte", "hora": "19:00"},  # lunes
            {"actividad": "descanso"},                               # martes
            {"actividad": "entreno_suave", "hora": "19:00"},   # miércoles
            {"actividad": "descanso"},                               # jueves
            {"actividad": "entreno_fuerte", "hora": "19:00"},  # viernes
            {"actividad": "partido", "hora": "11:00"},               # sábado
            {"actividad": "descanso"},                               # domingo
        ],
        "peso_kg": 70,
    }

   

def test_semana_valida_se_crea():
    datos = semana_valida()                    # preparar
    semana = Semana(**datos)                   # actuar
    assert len(semana.dias) == 7               # comprobar
    assert semana.dias[5].actividad == TipoActividad.PARTIDO

def test_actividad_inventada_falla():
    datos = semana_valida()
    datos["dias"][0]["actividad"] = "siesta"     # rompemos solo el lunes
    with pytest.raises(ValidationError):
        Semana(**datos)

def test_semana_6_dias():
    datos = semana_valida()
    datos["dias"].pop()
    with pytest.raises(ValidationError):
        Semana(**datos)

def test_semana_8_dias():
    datos = semana_valida()
    datos["dias"].append({"actividad": "descanso"})
    with pytest.raises(ValidationError):
            Semana(**datos)


# --- Peso ---------------------------------------------------------------
# parametrize ejecuta el mismo test una vez por cada valor de la lista.

@pytest.mark.parametrize("peso", [29.9, 0, -5, 200.1])
def test_peso_fuera_de_limites_falla(peso):
    datos = semana_valida()
    datos["peso_kg"] = peso
    with pytest.raises(ValidationError):
        Semana(**datos)


@pytest.mark.parametrize("peso", [30, 200])
def test_peso_justo_en_el_limite_pasa(peso):
    datos = semana_valida()
    datos["peso_kg"] = peso
    semana = Semana(**datos)
    assert semana.peso_kg == peso


# --- Regla de la hora (validador de Dia) ---------------------------------

@pytest.mark.parametrize("actividad", ["entreno_fuerte", "entreno_suave", "partido"])
def test_actividad_sin_hora_falla(actividad):
    with pytest.raises(ValidationError, match="necesita una hora"):
        Dia(actividad=actividad)


def test_descanso_con_hora_falla():
    with pytest.raises(ValidationError, match="Descanso no puede llevar hora"):
        Dia(actividad="descanso", hora="10:00")


def test_descanso_sin_hora_pasa():
    dia = Dia(actividad="descanso")
    assert dia.hora is None


def test_partido_con_hora_pasa():
    dia = Dia(actividad="partido", hora="18:00")
    assert dia.actividad == TipoActividad.PARTIDO
    assert dia.hora.hour == 18     # Pydantic ha convertido "18:00" en un objeto time


def test_semana_con_entreno_sin_hora_falla():
    """Comprueba que el error de un Dia también hace fallar la Semana."""
    datos = semana_valida()
    del datos["dias"][0]["hora"]   # el lunes es entreno: sin hora no vale
    with pytest.raises(ValidationError, match="necesita una hora"):
        Semana(**datos)
