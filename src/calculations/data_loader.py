"""
Módulo para cargar datos desde archivos CSV
"""
import csv
import os
import sys
from typing import Dict, List
from ..models.accesorio import Accesorio, TipoAccesorio
from ..models.fluido import Fluido

class DataLoader:
    """Clase para cargar datos desde archivos CSV"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # Detectar si estamos en un ejecutable PyInstaller
            if getattr(sys, 'frozen', False):
                # Estamos en un ejecutable empaquetado
                base_path = sys._MEIPASS
                self.data_dir = os.path.join(base_path, 'data')
            else:
                # Estamos en desarrollo normal
                self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        else:
            self.data_dir = data_dir
    
    def cargar_constantes(self) -> Dict[str, float]:
        """Carga constantes físicas desde CSV"""
        constantes = {}
        filepath = os.path.join(self.data_dir, 'constantes.csv')
        
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                constantes[row['constante']] = float(row['valor'])
        
        return constantes
    
    def cargar_accesorios(self) -> Dict[str, Accesorio]:
        """Carga accesorios desde CSV"""
        accesorios = {}
        filepath = os.path.join(self.data_dir, 'accesorios.csv')
        
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convertir longitud equivalente de mm a metros
                leq_m = float(row['longitud_equivalente_mm']) / 1000.0
                
                accesorio = Accesorio(
                    tipo=TipoAccesorio(row['tipo_accesorio']),
                    coeficiente_K=float(row['coeficiente_K']),
                    longitud_equivalente=leq_m,
                    norma=row['norma'],
                    fabricante=row['fabricante']
                )
                accesorios[row['tipo_accesorio']] = accesorio
        
        return accesorios
    
    def cargar_fluidos(self) -> Dict[str, Fluido]:
        """Carga fluidos desde CSV"""
        fluidos = {}
        filepath = os.path.join(self.data_dir, 'fluidos.csv')
        
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                fluido = Fluido(
                    nombre=row['nombre'],
                    densidad=float(row['densidad']),
                    viscosidad=float(row['viscosidad']),
                    presion_vapor=float(row['presion_vapor'])
                )
                fluidos[row['nombre']] = fluido
        
        return fluidos
    
    def obtener_fluido_por_nombre(self, nombre: str) -> Fluido:
        """Obtiene un fluido específico por nombre"""
        fluidos = self.cargar_fluidos()
        if nombre not in fluidos:
            raise ValueError(f"Fluido '{nombre}' no encontrado en la base de datos")
        return fluidos[nombre]
    
    def obtener_accesorio_por_tipo(self, tipo: str) -> Accesorio:
        """Obtiene un accesorio específico por tipo"""
        accesorios = self.cargar_accesorios()
        if tipo not in accesorios:
            raise ValueError(f"Accesorio '{tipo}' no encontrado en la base de datos")
        return accesorios[tipo]
