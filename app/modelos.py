from pydantic import BaseModel, model_validator,Field
from enum import StrEnum
from datetime import time

class TipoActividad(StrEnum):
    PARTIDO = "partido"
    ENTRENO_FUERTE = "entreno_fuerte"
    ENTRENO_SUAVE  = "entreno_suave"
    DESCANSO = "descanso"

class Dia(BaseModel):
    hora:time|None = None
    actividad:TipoActividad

    @model_validator(mode="after")
    def comprobar_hora(self):
        if self.actividad in {TipoActividad.ENTRENO_FUERTE , 
                              TipoActividad.ENTRENO_SUAVE,
                                TipoActividad.PARTIDO} and self.hora is None : 
            raise ValueError(f"{self.actividad} necesita una hora")
        
        elif self.actividad is TipoActividad.DESCANSO and self.hora is not None : 
            raise ValueError("Descanso no puede llevar hora")
        return self

class Semana(BaseModel):
    dias: list[Dia] = Field(min_length=7, max_length=7)
    # Límites del peso: mínimo ___ porque ___; máximo ___ porque ___
    peso_kg: float = Field(ge=30, le=200)
