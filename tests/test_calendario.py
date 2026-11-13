from app.calendario import TipoDia, clasificar_semana
from app.modelos import Semana

# Abreviaturas para que las semanas de los tests se lean de un vistazo.
P = "partido"
F = "entreno_fuerte"
S = "entreno_suave"
D = "descanso"


def crear_semana(actividades: list[str]) -> Semana:
    """Crea una Semana a partir de 7 actividades (de lunes a domingo).
    Pone una hora cualquiera a las que la necesitan: en la clasificación no se usa."""
    dias = []
    for actividad in actividades:
        if actividad == D:
            dias.append({"actividad": actividad})
        else:
            dias.append({"actividad": actividad, "hora": "19:00"})
    return Semana(dias=dias, peso_kg=70)


def test_semana_sin_partidos_cada_dia_es_su_actividad():
    #                        L  M  X  J  V  S  D
    semana = crear_semana([F, D, S, F, D, S, D])
    assert clasificar_semana(semana) == [
        TipoDia.ENTRENO_FUERTE,
        TipoDia.DESCANSO,
        TipoDia.ENTRENO_SUAVE,
        TipoDia.ENTRENO_FUERTE,
        TipoDia.DESCANSO,
        TipoDia.ENTRENO_SUAVE,
        TipoDia.DESCANSO,
    ]


def test_descanso_antes_de_partido_es_dia_antes():
    #                        L  M  X  J  V  S  D
    semana = crear_semana([F, D, P, F, D, S, D])
    assert clasificar_semana(semana) == [
        TipoDia.ENTRENO_FUERTE,
        TipoDia.DIA_ANTES_PARTIDO,  # martes: mañana hay partido
        TipoDia.PARTIDO,
        TipoDia.ENTRENO_FUERTE,
        TipoDia.DESCANSO,
        TipoDia.ENTRENO_SUAVE,
        TipoDia.DESCANSO,
    ]


def test_entreno_antes_de_partido_es_dia_antes():
    """Decisión: el día antes de partido manda sobre el entreno."""
    #                        L  M  X  J  V  S  D
    semana = crear_semana([F, D, S, D, F, P, D])
    assert clasificar_semana(semana) == [
        TipoDia.ENTRENO_FUERTE,
        TipoDia.DESCANSO,
        TipoDia.ENTRENO_SUAVE,
        TipoDia.DESCANSO,
        TipoDia.DIA_ANTES_PARTIDO,  # viernes: tenía entreno fuerte, pero mañana hay partido
        TipoDia.PARTIDO,
        TipoDia.DESCANSO,
    ]


def test_dos_partidos_seguidos_son_dos_dias_de_partido():
    """Decisión: el partido manda sobre el día antes de partido."""
    #                        L  M  X  J  V  S  D
    semana = crear_semana([F, D, S, D, D, P, P])
    assert clasificar_semana(semana) == [
        TipoDia.ENTRENO_FUERTE,
        TipoDia.DESCANSO,
        TipoDia.ENTRENO_SUAVE,
        TipoDia.DESCANSO,
        TipoDia.DIA_ANTES_PARTIDO,
        TipoDia.PARTIDO,  # sábado: aunque el domingo haya otro partido, sigue siendo partido
        TipoDia.PARTIDO,
    ]


def test_partido_el_lunes_hace_del_domingo_dia_antes():
    """Decisión: después del domingo viene el lunes de la misma semana."""
    #                        L  M  X  J  V  S  D
    semana = crear_semana([P, D, F, D, S, D, D])
    assert clasificar_semana(semana) == [
        TipoDia.PARTIDO,
        TipoDia.DESCANSO,
        TipoDia.ENTRENO_FUERTE,
        TipoDia.DESCANSO,
        TipoDia.ENTRENO_SUAVE,
        TipoDia.DESCANSO,
        TipoDia.DIA_ANTES_PARTIDO,  # domingo: el "día siguiente" es el lunes
    ]


def test_partido_el_domingo_no_afecta_al_lunes():
    """El lunes es el día SIGUIENTE al domingo, no el anterior: no cambia."""
    #                        L  M  X  J  V  S  D
    semana = crear_semana([F, D, S, D, F, D, P])
    assert clasificar_semana(semana) == [
        TipoDia.ENTRENO_FUERTE,
        TipoDia.DESCANSO,
        TipoDia.ENTRENO_SUAVE,
        TipoDia.DESCANSO,
        TipoDia.ENTRENO_FUERTE,
        TipoDia.DIA_ANTES_PARTIDO,
        TipoDia.PARTIDO,
    ]
