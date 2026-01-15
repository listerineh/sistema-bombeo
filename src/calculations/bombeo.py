"""
Módulo de cálculos específicos para bombeo
"""
import math
from typing import Dict, List, Tuple
from ..models import SistemaTuberias
from .hidraulica import CalculadoraHidraulica

class CalculadoraBombeo:
    """Clase para realizar cálculos específicos de bombeo"""
    
    def __init__(self, sistema: SistemaTuberias):
        self.sistema = sistema
        self.hidraulica = CalculadoraHidraulica(sistema)
    
    def calcular_potencia_hidraulica(self, Ht: float) -> float:
        """Calcula la potencia hidráulica requerida"""
        Q = self.sistema.caudal
        rho = self.sistema.fluido.densidad
        g = self.hidraulica.G
        
        Wh = Q * rho * g * Ht
        return Wh
    
    def calcular_potencia_bomba(self, Wh: float) -> float:
        """Calcula la potencia que debe suministrar la bomba"""
        eta = self.sistema.eficiencia_bomba
        return Wh / eta
    
    def calcular_NPSHa(self, longitud_sucursal: float, elevacion_fluido_sucursal: float) -> float:
        """
        Calcula el NPSH disponible (NPSHa)
        
        Args:
            longitud_sucursal: Longitud de la línea de succión (m)
            elevacion_fluido_sucursal: Elevación del fluido respecto a la bomba (m)
        """
        rho = self.sistema.fluido.densidad
        g = self.hidraulica.G
        P1 = self.sistema.presion_punto1
        Pvap = self.sistema.fluido.presion_vapor
        
        # Calcular pérdidas en la línea de succión
        perdidas_sucursal = self._calcular_perdidas_sucursal(longitud_sucursal)
        
        # Cálculo de NPSHa
        h_presion_inicial = P1 / (rho * g)
        h_presion_vapor = Pvap / (rho * g)
        
        NPSHa = h_presion_inicial - h_presion_vapor + elevacion_fluido_sucursal - perdidas_sucursal
        
        return NPSHa
    
    def _calcular_perdidas_sucursal(self, longitud_sucursal: float) -> float:
        """Calcula pérdidas en la línea de succión"""
        if not self.sistema.tramos:
            return 0.0
        
        # Usar el primer diámetro
        diametro = self.sistema.tramos[0].diametro
        velocidad = self.hidraulica.calcular_velocidad(self.sistema.caudal, diametro)
        Re = self.hidraulica.calcular_numero_reynolds(velocidad, diametro)
        f = self.hidraulica.calcular_factor_friccion(Re)
        
        # Pérdidas mayores en succión
        hv = self.hidraulica.calcular_altura_velocidad(velocidad)
        hf_major_suc = f * (longitud_sucursal / diametro) * hv
        
        # Pérdidas menores en succión (accesorios típicos de succión)
        accesorios_sucursal = [
            "entrada_tanque", "codo_90_radio_largo", "codo_90_radio_corto", 
            "codo_45", "tee_flujo_directo", "tee_flujo_ramal", 
            "valvula_compuerta_abierta", "filtro_y"
        ]
        
        K_suc_total = 0.0
        for accesorio in self.sistema.accesorios:
            if accesorio.tipo.value in accesorios_sucursal:
                K_suc_total += accesorio.K_total
        
        hf_minor_suc = K_suc_total * hv
        hf_total_suc = hf_major_suc + hf_minor_suc
        
        return hf_total_suc
    
    def calcular_alturas_sucursal_descarga(self) -> Tuple[float, float]:
        """Calcula las alturas de succión y descarga"""
        rho = self.sistema.fluido.densidad
        g = self.hidraulica.G
        
        H_suc = self.sistema.elevacion_punto1 + (self.sistema.presion_punto1 / (rho * g))
        H_desc = self.sistema.elevacion_punto2 + (self.sistema.presion_punto2 / (rho * g))
        
        return H_suc, H_desc
    
    def obtener_resultados_completos(self, longitud_sucursal: float = 5.0, 
                                   elevacion_fluido_sucursal: float = 1.0) -> Dict[str, float]:
        """
        Obtiene todos los resultados del cálculo de bombeo
        
        Args:
            longitud_sucursal: Longitud de la línea de succión (m)
            elevacion_fluido_sucursal: Elevación del fluido respecto a la bomba (m)
        """
        # Parámetros del flujo
        parametros_flujo = self.hidraulica.obtener_parametros_flujo()
        
        # Pérdidas
        hf_major, hf_minor, hf_total = self.hidraulica.calcular_perdidas_totales()
        
        # Alturas
        h_elev = self.hidraulica.calcular_altura_elevacion()
        h_presion = self.hidraulica.calcular_altura_presion()
        Ht = self.hidraulica.calcular_carga_total_bomba()
        
        # Alturas de succión y descarga
        H_suc, H_desc = self.calcular_alturas_sucursal_descarga()
        
        # NPSHa
        NPSHa = self.calcular_NPSHa(longitud_sucursal, elevacion_fluido_sucursal)
        
        # Potencias
        Wh = self.calcular_potencia_hidraulica(Ht)
        Wb = self.calcular_potencia_bomba(Wh)
        
        # Presiones de referencia
        h_presion_inicial = self.sistema.presion_punto1 / (self.sistema.fluido.densidad * self.hidraulica.G)
        h_presion_vapor = self.sistema.fluido.presion_vapor / (self.sistema.fluido.densidad * self.hidraulica.G)
        
        return {
            # Parámetros del flujo
            'velocidad': parametros_flujo.get('velocidad', 0),
            'numero_reynolds': parametros_flujo.get('numero_reynolds', 0),
            'factor_friccion': parametros_flujo.get('factor_friccion', 0),
            
            # Pérdidas
            'perdidas_mayores': hf_major,
            'perdidas_menores': hf_minor,
            'perdidas_totales': hf_total,
            
            # Alturas
            'altura_elevacion': h_elev,
            'altura_presion': h_presion,
            'carga_total_bomba': Ht,
            'altura_sucursal': H_suc,
            'altura_descarga': H_desc,
            
            # NPSH
            'NPSHa': NPSHa,
            'presion_inicial_m': h_presion_inicial,
            'presion_vapor_m': h_presion_vapor,
            'elevacion_fluido_sucursal': elevacion_fluido_sucursal,
            'perdidas_sucursal': self._calcular_perdidas_sucursal(longitud_sucursal),
            
            # Potencias
            'potencia_hidraulica_W': Wh,
            'potencia_bomba_W': Wb,
            'potencia_hidraulica_kW': Wh / 1000,
            'potencia_bomba_kW': Wb / 1000
        }
