"""
Modelo para representar propiedades de fluidos
"""
from dataclasses import dataclass

@dataclass
class Fluido:
    """Clase que representa las propiedades de un fluido"""
    nombre: str
    densidad: float  # kg/m³
    viscosidad: float  # Pa·s
    presion_vapor: float  # Pa
    
    def __post_init__(self):
        if self.densidad <= 0:
            raise ValueError("La densidad debe ser positiva")
        if self.viscosidad <= 0:
            raise ValueError("La viscosidad debe ser positiva")
        if self.presion_vapor < 0:
            raise ValueError("La presión de vapor no puede ser negativa")
