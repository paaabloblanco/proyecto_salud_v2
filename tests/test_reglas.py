import pytest
from pydantic import ValidationError

from app.calendario import TipoDia
from app.reglas import REGLAS_POR_DIA, Rango


# --- Rango ---

def test_rango_valido():
    rango = Rango(minimo=6, maximo=8)
    assert rango.minimo == 6
    assert rango.maximo == 8


def test_rango_con_minimo_igual_al_maximo_es_valido():
    rango = Rango(minimo=6, maximo=6)
    assert rango.minimo == rango.maximo


def test_rango_con_minimo_mayor_que_maximo_da_error():
    with pytest.raises(ValidationError):
        Rango(minimo=8, maximo=6)


def test_rango_negativo_da_error():
    with pytest.raises(ValidationError):
        Rango(minimo=-1, maximo=5)


# --- REGLAS_POR_DIA ---

def test_hay_una_regla_para_cada_tipo_de_dia():
    for tipo in TipoDia:
        assert tipo in REGLAS_POR_DIA


def test_ninguna_regla_tiene_el_motivo_vacio():
    for regla in REGLAS_POR_DIA.values():
        assert regla.motivo.strip() != ""


# --- Cálculo en gramos ---

def calcular(tipo: TipoDia, peso: float):
    """Atajo: busca la regla del tipo de día y la calcula para ese peso."""
    return REGLAS_POR_DIA[tipo].calcular_gramos(peso, tipo)


def test_partido_70_kg_hidratos_en_gramos():
    objetivo = calcular(TipoDia.PARTIDO, 70)
    assert objetivo.rango_hidratos_g.minimo == pytest.approx(420)
    assert objetivo.rango_hidratos_g.maximo == pytest.approx(560)


def test_partido_70_kg_proteina_en_gramos():
    objetivo = calcular(TipoDia.PARTIDO, 70)
    assert objetivo.rango_proteina_g.minimo == pytest.approx(112)
    assert objetivo.rango_proteina_g.maximo == pytest.approx(154)


def test_descanso_60_kg_hidratos_en_gramos():
    objetivo = calcular(TipoDia.DESCANSO, 60)
    assert objetivo.rango_hidratos_g.minimo == pytest.approx(180)
    assert objetivo.rango_hidratos_g.maximo == pytest.approx(300)


def test_la_grasa_no_cambia_con_el_peso():
    ligero = calcular(TipoDia.PARTIDO, 50)
    pesado = calcular(TipoDia.PARTIDO, 100)
    assert ligero.porcentaje_grasa == pesado.porcentaje_grasa
    assert ligero.porcentaje_grasa.minimo == 20
    assert ligero.porcentaje_grasa.maximo == 35


def test_el_resultado_lleva_el_tipo_de_dia_y_el_motivo_de_la_regla():
    objetivo = calcular(TipoDia.ENTRENO_FUERTE, 70)
    assert objetivo.tipo_dia == TipoDia.ENTRENO_FUERTE
    assert objetivo.motivo == REGLAS_POR_DIA[TipoDia.ENTRENO_FUERTE].motivo


def test_modificar_el_resultado_no_cambia_la_regla():
    objetivo = calcular(TipoDia.PARTIDO, 70)
    objetivo.porcentaje_grasa.maximo = 999
    assert REGLAS_POR_DIA[TipoDia.PARTIDO].porcentaje_grasa.maximo == 35


def test_peso_negativo_da_error():
    with pytest.raises(ValidationError):
        calcular(TipoDia.PARTIDO, -70)


def test_peso_cero_da_cero_gramos():
    # Documenta el comportamiento: el método no rechaza el 0.
    # En la app no llega nunca porque Semana limita el peso entre 30 y 200 kg.
    objetivo = calcular(TipoDia.PARTIDO, 0)
    assert objetivo.rango_hidratos_g.minimo == 0
    assert objetivo.rango_hidratos_g.maximo == 0
