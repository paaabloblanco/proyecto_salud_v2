from pydantic import BaseModel, Field, model_validator

from app.calendario import TipoDia


class Rango(BaseModel):
    minimo: float = Field(ge=0)
    maximo: float = Field(ge=0)

    @model_validator(mode="after")
    def comprobar_rango(self):
        if self.maximo < self.minimo:
            raise ValueError("El minimo no puede ser mayor que el maximo")
        return self


class ObjetivoDiaGramos(BaseModel):
    tipo_dia: TipoDia
    rango_hidratos_g: Rango
    rango_proteina_g: Rango
    porcentaje_grasa: Rango
    motivo: str = Field(min_length=1)


class ObjetivoDiaGporKg(BaseModel):
    rango_hidratos: Rango
    rango_proteina: Rango
    porcentaje_grasa: Rango
    motivo: str = Field(min_length=1)

    def calcular_gramos(self, peso_kg: float, tipo_dia: TipoDia) -> ObjetivoDiaGramos:
        return ObjetivoDiaGramos(
            tipo_dia=tipo_dia,
            rango_hidratos_g=Rango(
                minimo=self.rango_hidratos.minimo * peso_kg,
                maximo=self.rango_hidratos.maximo * peso_kg,
            ),
            rango_proteina_g=Rango(
                minimo=self.rango_proteina.minimo * peso_kg,
                maximo=self.rango_proteina.maximo * peso_kg,
            ),
            porcentaje_grasa=self.porcentaje_grasa.model_copy(),
            motivo=self.motivo,
        )


# Objetivos diarios por tipo de día, en g/kg de peso corporal (la grasa, en % de la energía).
# Fuentes (detalle en docs/investigacion_nutricion.md):
#   - Hidratos: UEFA 2021 (Collins et al., BJSM 55:416) y ACSM 2016 (Thomas et al.).
#     Descanso (3-5) es una inferencia a partir del rango "ligero" de ACSM: hay poca evidencia.
#   - Proteína 1,6-2,2 g/kg: UEFA 2021.
#   - Grasa 20-35 % de la energía: ACSM 2016.
# PENDIENTE DE VALIDAR POR UN DIETISTA-NUTRICIONISTA.
REGLAS_POR_DIA = {
    TipoDia.PARTIDO: ObjetivoDiaGporKg(
        rango_hidratos=Rango(minimo=6, maximo=8),
        rango_proteina=Rango(minimo=1.6, maximo=2.2),
        porcentaje_grasa=Rango(minimo=20, maximo=35),
        motivo="Día de partido: hidratos altos para tener energía durante el partido y recuperarte después.",
    ),
    TipoDia.DIA_ANTES_PARTIDO: ObjetivoDiaGporKg(
        rango_hidratos=Rango(minimo=6, maximo=8),
        rango_proteina=Rango(minimo=1.6, maximo=2.2),
        porcentaje_grasa=Rango(minimo=20, maximo=35),
        motivo="Más hidratos hoy porque mañana hay partido: así llegas con las reservas de energía llenas.",
    ),
    TipoDia.ENTRENO_FUERTE: ObjetivoDiaGporKg(
        rango_hidratos=Rango(minimo=5, maximo=6),
        rango_proteina=Rango(minimo=1.6, maximo=2.2),
        porcentaje_grasa=Rango(minimo=20, maximo=35),
        motivo="Entreno fuerte: hidratos moderados-altos para rendir y recuperar la energía gastada.",
    ),
    TipoDia.ENTRENO_SUAVE: ObjetivoDiaGporKg(
        rango_hidratos=Rango(minimo=3, maximo=5),
        rango_proteina=Rango(minimo=1.6, maximo=2.2),
        porcentaje_grasa=Rango(minimo=20, maximo=35),
        motivo="Entreno suave: menos hidratos que en un día fuerte porque el gasto es menor.",
    ),
    TipoDia.DESCANSO: ObjetivoDiaGporKg(
        rango_hidratos=Rango(minimo=3, maximo=5),
        rango_proteina=Rango(minimo=1.6, maximo=2.2),
        porcentaje_grasa=Rango(minimo=20, maximo=35),
        motivo="Día de descanso: hidratos más bajos porque no entrenas; la proteína se mantiene para recuperar.",
    ),
}
