from pydantic import BaseModel, model_validator, Field
from app.calendario import TipoDia

class Rango(BaseModel):
    minimo: float = Field(ge=0)
    maximo: float = Field(ge=0)
    @model_validator(mode = "after")
    def comprobar_rango(self):
        if self.maximo < self.minimo:
            raise ValueError("El minimo no puede ser mayor que el maximo")
        
        return self

class ObjetivoDiaGporKg(BaseModel):
    tipo_dia: TipoDia
    rango_hidratos: Rango
    rango_proteina: Rango
    porcentaje_grasa: Rango
    motivo: str = Field(min_length=1)