from enum import StrEnum
from app.modelos import Semana, TipoActividad

class TipoDia(StrEnum):
    PARTIDO = "partido"
    DIA_ANTES_PARTIDO = "dia_antes_partido"
    ENTRENO_FUERTE =  "entreno_fuerte"
    ENTRENO_SUAVE = "entreno_suave"
    DESCANSO = "descanso"


DE_ACTIVIDAD_A_TIPO_DIA = {
    TipoActividad.PARTIDO: TipoDia.PARTIDO,
    TipoActividad.ENTRENO_FUERTE: TipoDia.ENTRENO_FUERTE,
    TipoActividad.ENTRENO_SUAVE: TipoDia.ENTRENO_SUAVE,
    TipoActividad.DESCANSO: TipoDia.DESCANSO,
}


def clasificar_semana(semana: Semana) -> list[TipoDia]:
    dias = semana.dias
    resultado:list[TipoDia] = []

    for i, dia in enumerate(dias):
        
        manana_hay_partido =   dias[(i +1) % 7].actividad is TipoActividad.PARTIDO
           
        if dia.actividad is not TipoActividad.PARTIDO and manana_hay_partido:
            resultado.append(TipoDia.DIA_ANTES_PARTIDO)
        else:
            resultado.append(DE_ACTIVIDAD_A_TIPO_DIA[dia.actividad])
        
    return resultado

        
        
