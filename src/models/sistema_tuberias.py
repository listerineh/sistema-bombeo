"""
Modelo para representar un sistema de tuberías
"""
from dataclasses import dataclass, field
from typing import List, Literal
from .fluido import Fluido
from .accesorio import Accesorio

@dataclass
class TramoTuberia:
    """Clase que representa un tramo de tubería"""
    longitud: float  # metros
    orientacion: Literal['horizontal', 'vertical']
    diametro: float  # metros
    material: str = "acero"  # por defecto
    
    def __post_init__(self):
        if self.longitud <= 0:
            raise ValueError("La longitud debe ser positiva")
        if self.diametro <= 0:
            raise ValueError("El diámetro debe ser positivo")
        if self.orientacion not in ['horizontal', 'vertical']:
            raise ValueError("La orientación debe ser 'horizontal' o 'vertical'")

@dataclass
class SistemaTuberias:
    """Clase que representa un sistema completo de tuberías"""
    tramos: List[TramoTuberia] = field(default_factory=list)
    accesorios: List[Accesorio] = field(default_factory=list)
    fluido: Fluido = None
    caudal: float = 0.0  # m³/s
    eficiencia_bomba: float = 0.70  # decimal
    
    # Puntos del sistema
    elevacion_punto1: float = 0.0  # metros
    elevacion_punto2: float = 0.0  # metros
    presion_punto1: float = 101325.0  # Pa (atmosférica por defecto)
    presion_punto2: float = 101325.0  # Pa (atmosférica por defecto)
    
    def __post_init__(self):
        if self.caudal <= 0:
            raise ValueError("El caudal debe ser positivo")
        if not 0 < self.eficiencia_bomba <= 1:
            raise ValueError("La eficiencia debe estar entre 0 y 1")
    
    @property
    def longitud_total(self):
        """Calcula la longitud total de tubería"""
        return sum(tramo.longitud for tramo in self.tramos)
    
    @property
    def diametro_constante(self):
        """Verifica si todos los tramos tienen el mismo diámetro"""
        if not self.tramos:
            return True
        primer_diametro = self.tramos[0].diametro
        return all(tramo.diametro == primer_diametro for tramo in self.tramos)
    
    def agregar_tramo(self, longitud: float, orientacion: str, diametro: float, material: str = "acero"):
        """Agrega un tramo al sistema"""
        tramo = TramoTuberia(longitud, orientacion, diametro, material)
        self.tramos.append(tramo)
    
    def agregar_accesorio(self, accesorio: Accesorio):
        """Agrega un accesorio al sistema"""
        self.accesorios.append(accesorio)
    
    def obtener_tramos_verticales(self):
        """Retorna los tramos verticales"""
        return [tramo for tramo in self.tramos if tramo.orientacion == 'vertical']
    
    def obtener_tramos_horizontales(self):
        """Retorna los tramos horizontales"""
        return [tramo for tramo in self.tramos if tramo.orientacion == 'horizontal']
