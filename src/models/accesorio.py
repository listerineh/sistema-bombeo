"""
Modelo para representar accesorios de tuberías
"""
from dataclasses import dataclass
from enum import Enum

class TipoAccesorio(Enum):
    """Enumeración de tipos de accesorios"""
    ENTRADA_TANQUE = "entrada_tanque"
    SALIDA_TANQUE = "salida_tanque"
    CODO_90_RADIO_LARGO = "codo_90_radio_largo"
    CODO_90_RADIO_CORTO = "codo_90_radio_corto"
    CODO_45 = "codo_45"
    TEE_FLUJO_DIRECTO = "tee_flujo_directo"
    TEE_FLUJO_RAMAL = "tee_flujo_ramal"
    VALVULA_COMPUERTA_ABIERTA = "valvula_compuerta_abierta"
    VALVULA_GLOBO_ABIERTA = "valvula_globo_abierta"
    VALVULA_RETENCION_BOLA = "valvula_retencion_bola"
    VALVULA_RETENCION_BISAGRA = "valvula_retencion_bisagra"
    FILTRO_Y = "filtro_y"
    REDUCCION_BRUSCA = "reduccion_brusca"
    EXPANSION_BRUSCA = "expansion_brusca"

@dataclass
class Accesorio:
    """Clase que representa un accesorio de tubería"""
    tipo: TipoAccesorio
    coeficiente_K: float
    longitud_equivalente: float  # metros (Leq)
    norma: str  # ASTM, ISO, etc.
    fabricante: str
    cantidad: int = 1
    
    def __post_init__(self):
        if self.coeficiente_K < 0:
            raise ValueError("El coeficiente K no puede ser negativo")
        if self.longitud_equivalente < 0:
            raise ValueError("La longitud equivalente no puede ser negativa")
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
    
    @property
    def K_total(self):
        """Retorna el coeficiente K total considerando la cantidad"""
        return self.coeficiente_K * self.cantidad
    
    @property
    def Leq_total(self):
        """Retorna la longitud equivalente total considerando la cantidad"""
        return self.longitud_equivalente * self.cantidad
