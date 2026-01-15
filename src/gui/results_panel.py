"""
Panel de resultados del sistema de bombeo.

Este módulo contiene la clase ResultsPanel que se encarga de mostrar
los resultados de los cálculos hidráulicos de manera organizada y
fácil de leer para el usuario.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QTableWidget, QHeaderView, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class ResultsPanel(QWidget):
    """Panel para mostrar los resultados del cálculo del sistema de bombeo.
    
    Este widget se divide en dos secciones principales:
    - Resultados principales: Los 6 valores más importantes (Ht, NPSHa, Potencia, etc.)
    - Resultados detallados: Tabla completa con todos los parámetros calculados
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario del panel de resultados."""
        layout = QVBoxLayout(self)
        
        # Título y descripción
        title = QLabel("Resultados del Cálculo")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        desc = QLabel("Resultados del análisis hidráulico del sistema")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #666; font-size: 11px; margin-bottom: 8px;")
        layout.addWidget(desc)
        
        # Splitter vertical para resultados principales y detallados
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Panel de resultados principales
        main_results = self.create_main_results_panel()
        splitter.addWidget(main_results)
        
        # Panel de resultados detallados
        detailed_results = self.create_detailed_results_panel()
        splitter.addWidget(detailed_results)
        
        # Configurar splitter (50% principales, 50% detallados)
        splitter.setSizes([350, 350])
        
        layout.addWidget(splitter)
    
    def create_main_results_panel(self):
        """Crea el panel con los resultados principales más importantes.
        
        Returns:
            QGroupBox: Widget contenedor con los 6 resultados principales
                      organizados en dos columnas (3 por columna).
        """
        group = QGroupBox("Resultados Principales")
        layout = QVBoxLayout(group)
        
        # Grid para resultados importantes
        results_grid = QWidget()
        grid_layout = QHBoxLayout(results_grid)
        grid_layout.setSpacing(30)
        
        # Columna izquierda
        left_column = QVBoxLayout()
        left_column.setSpacing(15)
        
        # Carga total de bomba
        self.ht_label = QLabel("Ht: -- m")
        self.ht_label.setProperty("class", "result")
        left_column.addWidget(QLabel("Carga Total de Bomba:"))
        left_column.addWidget(self.ht_label)
        
        # NPSH disponible
        self.npsh_label = QLabel("NPSHa: -- m")
        self.npsh_label.setProperty("class", "result")
        left_column.addWidget(QLabel("NPSH Disponible:"))
        left_column.addWidget(self.npsh_label)
        
        # Potencia requerida
        self.power_label = QLabel("Potencia: -- kW")
        self.power_label.setProperty("class", "result")
        left_column.addWidget(QLabel("Potencia Requerida:"))
        left_column.addWidget(self.power_label)
        
        left_column.addStretch()
        grid_layout.addLayout(left_column)
        
        # Columna derecha
        right_column = QVBoxLayout()
        right_column.setSpacing(15)
        
        # Velocidad
        self.velocity_label = QLabel("Velocidad: -- m/s")
        right_column.addWidget(QLabel("Velocidad del Fluido:"))
        right_column.addWidget(self.velocity_label)
        
        # Número de Reynolds
        self.reynolds_label = QLabel("Re: --")
        right_column.addWidget(QLabel("Número de Reynolds:"))
        right_column.addWidget(self.reynolds_label)
        
        # Factor de fricción
        self.friction_label = QLabel("f: --")
        right_column.addWidget(QLabel("Factor de Fricción:"))
        right_column.addWidget(self.friction_label)
        
        right_column.addStretch()
        grid_layout.addLayout(right_column)
        
        layout.addWidget(results_grid)
        
        return group
    
    def create_detailed_results_panel(self):
        """Crea el panel con la tabla de resultados detallados.
        
        Returns:
            QGroupBox: Widget contenedor con tabla completa de resultados
                      organizados por categorías (flujo, alturas, potencia).
        """
        group = QGroupBox("Resultados Detallados")
        layout = QVBoxLayout(group)
        
        # Tabla de resultados
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Parámetro", "Valor"])
        
        # Configurar tabla
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Aumentar altura de filas para mejor legibilidad
        self.results_table.verticalHeader().setDefaultSectionSize(25)
        self.results_table.verticalHeader().setMinimumSectionSize(25)
        
        layout.addWidget(self.results_table)
        
        return group
    
    def update_results(self, resultados):
        """Actualiza todos los resultados mostrados con los valores calculados.
        
        Args:
            resultados (dict): Diccionario con todos los resultados del cálculo
                            incluyendo parámetros del flujo, alturas, potencia, etc.
        """
        if not resultados:
            return
        
        # Actualizar resultados principales
        self.ht_label.setText(f"Ht: {resultados['carga_total_bomba']:.3f} m")
        self.npsh_label.setText(f"NPSHa: {resultados['NPSHa']:.3f} m")
        self.power_label.setText(f"Potencia: {resultados['potencia_bomba_kW']:.2f} kW")
        
        self.velocity_label.setText(f"Velocidad: {resultados['velocidad']:.2f} m/s")
        self.reynolds_label.setText(f"Re: {resultados['numero_reynolds']:.0f}")
        self.friction_label.setText(f"f: {resultados['factor_friccion']:.4f}")
        
        # Actualizar tabla detallada
        self.populate_results_table(resultados)
    
    def populate_results_table(self, resultados):
        """Llena la tabla detallada con todos los resultados organizados.
        
        Args:
            resultados (dict): Diccionario con todos los resultados del cálculo
        """
        # Organizar resultados por categorías
        categories = {
            "Parámetros del Flujo": [
                ("Velocidad", f"{resultados['velocidad']:.2f} m/s"),
                ("Número de Reynolds", f"{resultados['numero_reynolds']:.0f}"),
                ("Factor de Fricción", f"{resultados['factor_friccion']:.4f}")
            ],
            "Alturas del Sistema": [
                ("Altura de Elevación", f"{resultados['altura_elevacion']:.3f} m"),
                ("Pérdidas Mayores", f"{resultados['perdidas_mayores']:.3f} m"),
                ("Pérdidas Menores", f"{resultados['perdidas_menores']:.3f} m"),
                ("Carga Total de Bomba (Ht)", f"{resultados['carga_total_bomba']:.3f} m")
            ],
            "Potencia": [
                ("Potencia Hidráulica", f"{resultados['potencia_hidraulica_kW']:.2f} kW"),
                ("Potencia Requerida", f"{resultados['potencia_bomba_kW']:.2f} kW")
            ]
        }
        
        # Contar total de filas
        total_rows = sum(len(items) for items in categories.values())
        self.results_table.setRowCount(total_rows)
        
        # Llenar tabla
        row = 0
        for category, items in categories.items():
            # Agregar fila de categoría
            self.results_table.setItem(row, 0, self.create_table_item(category, is_category=True))
            self.results_table.setItem(row, 1, self.create_table_item("", is_category=True))
            row += 1
            
            # Agregar items de la categoría
            for param, value in items:
                self.results_table.setItem(row, 0, self.create_table_item(param))
                self.results_table.setItem(row, 1, self.create_table_item(value))
                row += 1
    
    def create_table_item(self, text, is_category=False):
        """Crea un item para la tabla con formato apropiado.
        
        Args:
            text (str): Texto del item
            is_category (bool): True si es una fila de categoría
            
        Returns:
            QTableWidgetItem: Item configurado para la tabla
        """
        from PyQt6.QtWidgets import QTableWidgetItem
        
        item = QTableWidgetItem(text)
        
        if is_category:
            # Formato para categorías (negrita y fondo)
            item.setBackground(QColor(60, 60, 60))
            item.setForeground(QColor(255, 255, 255))
            font = item.font()
            font.setBold(True)
            item.setFont(font)
        else:
            # Formato para datos regulares
            item.setBackground(QColor(45, 45, 45))
            item.setForeground(QColor(220, 220, 220))
        
        return item
    
    def clear_results(self):
        """Limpia todos los resultados mostrados."""
        self.ht_label.setText("Ht: -- m")
        self.npsh_label.setText("NPSHa: -- m")
        self.power_label.setText("Potencia: -- kW")
        self.velocity_label.setText("Velocidad: -- m/s")
        self.reynolds_label.setText("Re: --")
        self.friction_label.setText("f: --")
        self.results_table.setRowCount(0)
