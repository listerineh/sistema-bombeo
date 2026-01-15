"""
Módulo de cálculos hidráulicos para sistemas de tuberías
"""
import math
from typing import Dict, List, Tuple
from ..models import SistemaTuberias, TramoTuberia

class CalculadoraHidraulica:
    """Clase para realizar cálculos hidráulicos en sistemas de tuberías"""
    
    def __init__(self, sistema: SistemaTuberias):
        self.sistema = sistema
        self.constantes = self._cargar_constantes()
    
    def _cargar_constantes(self) -> Dict[str, float]:
        """Carga constantes físicas necesarias"""
        from .data_loader import DataLoader
        loader = DataLoader()
        return loader.cargar_constantes()
    
    @property
    def G(self) -> float:
        """Aceleración gravitacional"""
        return self.constantes.get('gravedad', 9.81)
    
    @property
    def PATM(self) -> float:
        """Presión atmosférica estándar"""
        return self.constantes.get('presion_atmosferica', 101325.0)
    
    def calcular_area_seccion(self, diametro: float) -> float:
        """Calcula el área de la sección transversal de la tubería"""
        return math.pi * (diametro ** 2) / 4.0
    
    def calcular_velocidad(self, caudal: float, diametro: float) -> float:
        """Calcula la velocidad del fluido en la tubería"""
        area = self.calcular_area_seccion(diametro)
        return caudal / area
    
    def calcular_numero_reynolds(self, velocidad: float, diametro: float) -> float:
        """Calcula el número de Reynolds"""
        rho = self.sistema.fluido.densidad
        mu = self.sistema.fluido.viscosidad
        return (rho * velocidad * diametro) / mu
    
    def calcular_factor_friccion(self, Re: float) -> float:
        """Calcula el factor de fricción de Darcy-Weisbach"""
        if Re < 2000:
            # Flujo laminar
            return 64.0 / Re
        else:
            # Flujo turbulento - Correlación de Blasius
            return 0.3164 * (Re ** -0.25)
    
    def calcular_altura_velocidad(self, velocidad: float) -> float:
        """Calcula la altura de velocidad (energía cinética por unidad de peso)"""
        return (velocidad ** 2) / (2 * self.G)
    
    def calcular_perdidas_mayores_tramo(self, tramo: TramoTuberia, velocidad: float, f: float) -> float:
        """Calcula pérdidas mayores (fricción en tubería) para un tramo específico"""
        hv = self.calcular_altura_velocidad(velocidad)
        return f * (tramo.longitud / tramo.diametro) * hv
    
    def calcular_perdidas_menores_totales(self, velocidad: float) -> float:
        """Calcula pérdidas menores totales (accesorios)"""
        hv = self.calcular_altura_velocidad(velocidad)
        K_total = sum(acc.K_total for acc in self.sistema.accesorios)
        return K_total * hv
    
    def calcular_perdidas_totales(self) -> Tuple[float, float, float]:
        """
        Calcula todas las pérdidas del sistema
        Returns: (perdidas_mayores, perdidas_menores, perdidas_totales)
        """
        if not self.sistema.tramos:
            return 0.0, 0.0, 0.0
        
        # Usar el primer diámetro (asumimos diámetro constante)
        diametro = self.sistema.tramos[0].diametro
        velocidad = self.calcular_velocidad(self.sistema.caudal, diametro)
        Re = self.calcular_numero_reynolds(velocidad, diametro)
        f = self.calcular_factor_friccion(Re)
        
        # Calcular pérdidas mayores por cada tramo
        perdidas_mayores = sum(
            self.calcular_perdidas_mayores_tramo(tramo, velocidad, f) 
            for tramo in self.sistema.tramos
        )
        
        # Calcular pérdidas menores
        perdidas_menores = self.calcular_perdidas_menores_totales(velocidad)
        
        perdidas_totales = perdidas_mayores + perdidas_menores
        
        return perdidas_mayores, perdidas_menores, perdidas_totales
    
    def calcular_altura_presion(self) -> float:
        """Calcula la altura de presión (diferencia de presiones)"""
        rho = self.sistema.fluido.densidad
        P2 = self.sistema.presion_punto2
        P1 = self.sistema.presion_punto1
        return (P2 - P1) / (rho * self.G)
    
    def calcular_altura_elevacion(self) -> float:
        """Calcula la altura de elevación"""
        return self.sistema.elevacion_punto2 - self.sistema.elevacion_punto1
    
    def calcular_carga_total_bomba(self) -> float:
        """Calcula la carga total que debe proporcionar la bomba (Ht)"""
        h_elev = self.calcular_altura_elevacion()
        h_presion = self.calcular_altura_presion()
        _, _, h_perdidas = self.calcular_perdidas_totales()
        
        Ht = h_elev + h_presion + h_perdidas
        return Ht
    
    def obtener_parametros_flujo(self) -> Dict[str, float]:
        """Retorna parámetros básicos del flujo"""
        if not self.sistema.tramos:
            return {}
        
        diametro = self.sistema.tramos[0].diametro
        velocidad = self.calcular_velocidad(self.sistema.caudal, diametro)
        Re = self.calcular_numero_reynolds(velocidad, diametro)
        f = self.calcular_factor_friccion(Re)
        
        return {
            'velocidad': velocidad,
            'numero_reynolds': Re,
            'factor_friccion': f,
            'area_seccion': self.calcular_area_seccion(diametro)
        }
