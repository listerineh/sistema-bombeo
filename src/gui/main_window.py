"""
Ventana principal de la aplicación de cálculo de bombeo.

Este módulo contiene la clase MainWindow que sirve como contenedor principal
de la aplicación, gestionando la interfaz de usuario y la coordinación
entre los diferentes componentes del sistema de cálculo.
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
    QHBoxLayout, QWidget, QLabel, QPushButton, QMessageBox,
    QStatusBar, QMenuBar, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

from .input_panel import InputPanel
from .results_panel import ResultsPanel
from .system_viewer import SystemViewer
from .styles import apply_modern_style


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación Sistema de Cálculo de Bombeo.
    
    Esta clase gestiona la interfaz principal, incluyendo:
    - Layout general con splitter (60% input, 40% resultados)
    - Coordinación entre paneles de entrada, resultados y visualización
    - Gestión de menús y barra de estado
    - Control del flujo de cálculo y actualización de datos
    """
    
    def __init__(self):
        super().__init__()
        self.sistema = None
        self.resultados = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario principal."""
        self.setWindowTitle("Sistema de Cálculo de Bombeo - Nayehi Gonzaga")
        self.setGeometry(50, 50, 1400, 900)
        
        # Pantalla completa por defecto
        self.showMaximized()
        
        # Aplicar estilo moderno
        apply_modern_style(self)
        
        # Crear menú
        self.create_menu()
        
        # Crear widgets principales
        self.create_central_widget()
        
        # Crear barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo para calcular sistema de bombeo")
        
        # Conectar señales
        self.connect_signals()
    
    def create_menu(self):
        """Crea la barra de menú con las opciones principales."""
        menubar = self.menuBar()
        
        # Menú Archivo
        archivo_menu = menubar.addMenu('Archivo')
        
        nuevo_action = archivo_menu.addAction('Nuevo Sistema')
        nuevo_action.triggered.connect(self.nuevo_sistema)
        
        guardar_action = archivo_menu.addAction('Guardar Resultados')
        guardar_action.triggered.connect(self.guardar_resultados)
        
        archivo_menu.addSeparator()
        
        salir_action = archivo_menu.addAction('Salir')
        salir_action.triggered.connect(self.close)
        
        # Menú Herramientas
        herramientas_menu = menubar.addMenu('Herramientas')
        
        calcular_action = herramientas_menu.addAction('Calcular Sistema')
        calcular_action.triggered.connect(self.calcular_sistema)
        
        # Menú Ayuda
        ayuda_menu = menubar.addMenu('Ayuda')
        
        about_action = ayuda_menu.addAction('Acerca de')
        about_action.triggered.connect(self.show_about)
    
    def create_central_widget(self):
        """Crea el widget central con layout splitter para paneles principales."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Crear splitter para dividir izquierda/derecha
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo: Entrada de datos
        self.input_panel = InputPanel()
        splitter.addWidget(self.input_panel)
        
        # Panel derecho: Resultados y visualización
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Pestañas para resultados y visualización
        self.tab_widget = QTabWidget()
        
        # Pestaña de resultados
        self.results_panel = ResultsPanel()
        self.tab_widget.addTab(self.results_panel, "Resultados")
        
        # Pestaña de visualización del sistema
        self.system_viewer = SystemViewer()
        self.tab_widget.addTab(self.system_viewer, "Visualización")
        
        right_layout.addWidget(self.tab_widget)
        splitter.addWidget(right_widget)
        
        # Configurar splitter (60% izquierda, 40% derecha)
        splitter.setSizes([840, 560])
        
        main_layout.addWidget(splitter)
    
    def connect_signals(self):
        """Conecta las señales entre widgets para coordinación."""
        # Señal del panel de entrada cuando se completa
        self.input_panel.data_ready.connect(self.on_data_ready)
        
        # Señal del panel de entrada para calcular
        self.input_panel.calculate_requested.connect(self.calcular_sistema)
    
    def on_data_ready(self, sistema):
        """Se ejecuta cuando los datos del sistema están configurados.
        
        Args:
            sistema: Objeto SistemaTuberias con la configuración completa
        """
        self.sistema = sistema
        self.status_bar.showMessage("Sistema configurado. Listo para calcular.")
        
        # Actualizar visualización
        self.system_viewer.update_system(sistema)
    
    def calcular_sistema(self):
        """Realiza los cálculos hidráulicos del sistema configurado.
        
        Ejecuta los cálculos de bombeo y actualiza los paneles de resultados
        y visualización con los nuevos valores calculados.
        """
        if not self.sistema:
            QMessageBox.warning(self, "Advertencia", 
                              "Primero configure el sistema de tuberías.")
            return
        
        try:
            self.status_bar.showMessage("Calculando sistema...")
            
            # Importar aquí para evitar importación circular
            from ..calculations import CalculadoraBombeo
            
            # Realizar cálculos
            calc = CalculadoraBombeo(self.sistema)
            self.resultados = calc.obtener_resultados_completos()
            
            # Actualizar panel de resultados
            self.results_panel.update_results(self.resultados)
            
            # Cambiar a pestaña de resultados
            self.tab_widget.setCurrentIndex(0)
            
            self.status_bar.showMessage("Cálculo completado exitosamente")
            
        except Exception as e:
            QMessageBox.critical(self, "Error de Cálculo", 
                              f"Error al calcular el sistema: {str(e)}")
            self.status_bar.showMessage("Error en el cálculo")
    
    def nuevo_sistema(self):
        """Crea un nuevo sistema limpiando todos los datos actuales."""
        self.sistema = None
        self.resultados = None
        self.input_panel.clear_data()
        self.results_panel.clear_results()
        self.system_viewer.clear_system()
        self.status_bar.showMessage("Nuevo sistema creado")
    
    def guardar_resultados(self):
        """Guarda los resultados del cálculo en formato PDF/Excel.
        
        TODO: Implementar funcionalidad de exportación de resultados.
        """
        if not self.resultados:
            QMessageBox.warning(self, "Advertencia", 
                              "No hay resultados para guardar.")
            return
        
        # TODO: Implementar guardado a PDF/Excel
        QMessageBox.information(self, "Información", 
                              "Función de guardado en desarrollo.")
    
    def show_about(self):
        """Muestra el diálogo Acerca de con información de la aplicación."""
        QMessageBox.about(self, "Acerca de",
                          "Sistema de Cálculo de Bombeo\n"
                          "Proyecto Nay - Versión 1.0\n\n"
                          "Aplicación para calcular parámetros de bombeo\n"
                          "en sistemas de tuberías sin lecho poroso.\n\n"
                          "Desarrollado con ❤️ para Nayehi")

def main():
    """Función principal para ejecutar la aplicación GUI.
    
    Returns:
        int: Código de salida de la aplicación
    """
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    return app.exec()
