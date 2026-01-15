"""
Panel de entrada de datos del sistema de bombeo.

Este módulo contiene la clase InputPanel que proporciona la interfaz
para que el usuario configure todos los parámetros del sistema de tuberías,
incluyendo fluidos, tramos, accesorios y puntos del sistema.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox, QPushButton,
    QCheckBox, QScrollArea, QFormLayout, QGridLayout, QButtonGroup
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..models import SistemaTuberias
from ..calculations import DataLoader


class InputPanel(QWidget):
    """Panel para la entrada de datos del sistema de bombeo.
    
    Este widget gestiona la configuración completa del sistema incluyendo:
    - Datos básicos (fluido, caudal, eficiencia)
    - Tramos de tubería (longitud, orientación, diámetro)
    - Accesorios (tipos y cantidades)
    - Puntos del sistema (elevaciones y presiones)
    
    Señales:
        data_ready: Emitida cuando el sistema está configurado
        calculate_requested: Emitida cuando se solicita cálculo
    """
    
    # Señales
    data_ready = pyqtSignal(object)
    calculate_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.loader = DataLoader()
        self.accesorios_data = self.loader.cargar_accesorios()
        self.fluidos_data = self.loader.cargar_fluidos()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del panel de entrada."""
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Configuración del Sistema")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Descripción
        desc = QLabel("Configure los parámetros del sistema de tuberías")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #666; font-size: 11px; margin-bottom: 8px;")
        layout.addWidget(desc)
        
        # Área scrollable
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Sección de datos básicos
        self.create_basic_data_section(scroll_layout)
        
        # Sección de tramos de tubería
        self.create_pipes_section(scroll_layout)
        
        # Sección de accesorios
        self.create_fittings_section(scroll_layout)
        
        # Sección de puntos del sistema
        self.create_points_section(scroll_layout)
        
        # Botones de acción
        self.create_action_buttons(scroll_layout)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
    
    def create_basic_data_section(self, layout):
        """Crea la sección de datos básicos"""
        group = QGroupBox("Datos Básicos del Sistema")
        group_layout = QFormLayout(group)
        
        # Selector de fluido
        self.fluid_combo = QComboBox()
        fluid_names = list(self.fluidos_data.keys())
        self.fluid_combo.addItems(fluid_names)
        self.fluid_combo.currentTextChanged.connect(self.on_fluid_changed)
        group_layout.addRow("Fluido:", self.fluid_combo)
        
        # Caudal
        self.caudal_input = QDoubleSpinBox()
        self.caudal_input.setRange(0.001, 1000.0)
        self.caudal_input.setDecimals(3)
        self.caudal_input.setSuffix(" L/s")
        self.caudal_input.setValue(10.0)
        group_layout.addRow("Caudal:", self.caudal_input)
        
        # Eficiencia de bomba
        self.eficiencia_input = QDoubleSpinBox()
        self.eficiencia_input.setRange(0.1, 1.0)
        self.eficiencia_input.setDecimals(2)
        self.eficiencia_input.setSuffix(" %")
        self.eficiencia_input.setValue(0.70)
        self.eficiencia_input.setSingleStep(0.05)
        group_layout.addRow("Eficiencia Bomba:", self.eficiencia_input)
        
        layout.addWidget(group)
    
    def create_pipes_section(self, layout):
        """Crea la sección de tramos de tubería"""
        group = QGroupBox("Tramos de Tubería")
        group_layout = QVBoxLayout(group)
        
        # Instrucciones
        instructions = QLabel("Agregue los tramos con sus longitudes y orientaciones")
        instructions.setStyleSheet("color: #666; font-size: 10px; margin-bottom: 4px;")
        group_layout.addWidget(instructions)
        
        # Contenedor para tramos
        self.pipes_container = QWidget()
        self.pipes_layout = QVBoxLayout(self.pipes_container)
        
        # Agregar primer tramo por defecto
        self.add_pipe_section()
        
        # Botón para agregar tramo
        add_pipe_btn = QPushButton("Agregar Tramo")
        add_pipe_btn.clicked.connect(self.add_pipe_section)
        add_pipe_btn.setMinimumHeight(35)
        group_layout.addWidget(self.pipes_container)
        group_layout.addWidget(add_pipe_btn)
        
        layout.addWidget(group)
    
    def add_pipe_section(self):
        """Agrega una sección para un tramo de tubería"""
        pipe_widget = QWidget()
        pipe_layout = QHBoxLayout(pipe_widget)
        
        # Longitud
        longitud_input = QDoubleSpinBox()
        longitud_input.setRange(0.1, 1000.0)
        longitud_input.setDecimals(1)
        longitud_input.setSuffix(" m")
        longitud_input.setValue(10.0)
        
        # Orientación
        orient_combo = QComboBox()
        orient_combo.addItems(["horizontal", "vertical"])
        
        # Diámetro
        diametro_input = QDoubleSpinBox()
        diametro_input.setRange(0.01, 2.0)
        diametro_input.setDecimals(3)
        diametro_input.setSuffix(" m")
        diametro_input.setValue(0.100)
        
        # Botón de eliminar
        remove_btn = QPushButton("X")
        remove_btn.setProperty("class", "danger")
        remove_btn.setMaximumWidth(30)
        remove_btn.setMinimumHeight(25)
        remove_btn.clicked.connect(lambda: self.remove_pipe_section(pipe_widget))
        
        pipe_layout.addWidget(QLabel("Longitud:"))
        pipe_layout.addWidget(longitud_input)
        pipe_layout.addWidget(QLabel("Orientación:"))
        pipe_layout.addWidget(orient_combo)
        pipe_layout.addWidget(QLabel("Diámetro:"))
        pipe_layout.addWidget(diametro_input)
        pipe_layout.addWidget(remove_btn)
        pipe_layout.addStretch()
        
        # Guardar referencias
        pipe_widget.longitud_input = longitud_input
        pipe_widget.orient_combo = orient_combo
        pipe_widget.diametro_input = diametro_input
        
        self.pipes_layout.addWidget(pipe_widget)
    
    def remove_pipe_section(self, widget):
        """Elimina una sección de tramo"""
        self.pipes_layout.removeWidget(widget)
        widget.deleteLater()
    
    def create_fittings_section(self, layout):
        """Crea la sección de accesorios"""
        group = QGroupBox("Accesorios")
        group_layout = QVBoxLayout(group)
        
        # Instrucciones
        instructions = QLabel("Seleccione los accesorios y especifique las cantidades")
        instructions.setStyleSheet("color: #666; font-size: 10px; margin-bottom: 4px;")
        group_layout.addWidget(instructions)
        
        # Contenedor para accesorios
        self.fittings_container = QWidget()
        fittings_layout = QGridLayout(self.fittings_container)
        
        # Crear checkboxes para cada accesorio
        self.fitting_checkboxes = {}
        self.fitting_spinboxes = {}
        
        row, col = 0, 0
        for accesorio_name, accesorio in self.accesorios_data.items():
            # Checkbox
            checkbox = QCheckBox(accesorio.tipo.value.replace('_', ' ').title())
            checkbox.stateChanged.connect(self.on_fitting_changed)
            
            # Spinbox para cantidad
            spinbox = QSpinBox()
            spinbox.setRange(0, 100)
            spinbox.setValue(0)
            spinbox.setEnabled(False)
            spinbox.setMaximumWidth(60)
            
            # Guardar referencias
            self.fitting_checkboxes[accesorio_name] = checkbox
            self.fitting_spinboxes[accesorio_name] = spinbox
            
            fittings_layout.addWidget(checkbox, row, col)
            fittings_layout.addWidget(spinbox, row, col + 1)
            
            col += 2
            if col >= 4:
                col = 0
                row += 1
        
        group_layout.addWidget(self.fittings_container)
        layout.addWidget(group)
    
    def on_fitting_changed(self, state):
        """Habilita/deshabilita spinbox cuando cambia el checkbox"""
        sender = self.sender()
        for accesorio_name, checkbox in self.fitting_checkboxes.items():
            if checkbox == sender:
                self.fitting_spinboxes[accesorio_name].setEnabled(state == 2)
                if state == 2:
                    self.fitting_spinboxes[accesorio_name].setValue(1)
                else:
                    self.fitting_spinboxes[accesorio_name].setValue(0)
                break
    
    def create_points_section(self, layout):
        """Crea la sección de puntos del sistema"""
        group = QGroupBox("Puntos del Sistema")
        group_layout = QFormLayout(group)
        
        # Elevaciones
        self.z1_input = QDoubleSpinBox()
        self.z1_input.setRange(-100, 1000)
        self.z1_input.setDecimals(1)
        self.z1_input.setSuffix(" m")
        self.z1_input.setValue(2.0)
        group_layout.addRow("Elevación Punto 1:", self.z1_input)
        
        self.z2_input = QDoubleSpinBox()
        self.z2_input.setRange(-100, 1000)
        self.z2_input.setDecimals(1)
        self.z2_input.setSuffix(" m")
        self.z2_input.setValue(8.0)
        group_layout.addRow("Elevación Punto 2:", self.z2_input)
        
        # Presiones
        self.p1_atm_check = QCheckBox("Atmosférica")
        self.p1_atm_check.setChecked(True)
        self.p1_atm_check.stateChanged.connect(self.on_p1_atm_changed)
        
        self.p1_input = QDoubleSpinBox()
        self.p1_input.setRange(0, 1000000)
        self.p1_input.setDecimals(0)
        self.p1_input.setSuffix(" Pa")
        self.p1_input.setValue(101325)
        self.p1_input.setEnabled(False)
        
        p1_layout = QHBoxLayout()
        p1_layout.addWidget(self.p1_atm_check)
        p1_layout.addWidget(self.p1_input)
        group_layout.addRow("Presión Punto 1:", p1_layout)
        
        self.p2_atm_check = QCheckBox("Atmosférica")
        self.p2_atm_check.setChecked(True)
        self.p2_atm_check.stateChanged.connect(self.on_p2_atm_changed)
        
        self.p2_input = QDoubleSpinBox()
        self.p2_input.setRange(0, 1000000)
        self.p2_input.setDecimals(0)
        self.p2_input.setSuffix(" Pa")
        self.p2_input.setValue(101325)
        self.p2_input.setEnabled(False)
        
        p2_layout = QHBoxLayout()
        p2_layout.addWidget(self.p2_atm_check)
        p2_layout.addWidget(self.p2_input)
        group_layout.addRow("Presión Punto 2:", p2_layout)
        
        layout.addWidget(group)
    
    def on_p1_atm_changed(self, state):
        """Cambia el estado del input de presión P1"""
        self.p1_input.setEnabled(state != 2)
        if state == 2:
            self.p1_input.setValue(101325)  # Presión atmosférica
    
    def on_p2_atm_changed(self, state):
        """Cambia el estado del input de presión P2"""
        self.p2_input.setEnabled(state != 2)
        if state == 2:
            self.p2_input.setValue(101325)  # Presión atmosférica
    
    def on_fluid_changed(self, fluid_name):
        """Actualiza cuando cambia el fluido seleccionado"""
        # Aquí podríamos actualizar propiedades específicas si es necesario
        pass
    
    def create_action_buttons(self, layout):
        """Crea los botones de acción"""
        button_layout = QHBoxLayout()
        
        # Botón calcular
        calculate_btn = QPushButton("Calcular Sistema")
        calculate_btn.setProperty("class", "primary")
        calculate_btn.clicked.connect(self.on_calculate)
        calculate_btn.setMinimumHeight(40)
        
        # Botón limpiar
        clear_btn = QPushButton("Limpiar Datos")
        clear_btn.setProperty("class", "danger")
        clear_btn.clicked.connect(self.clear_data)
        clear_btn.setMinimumHeight(40)
        
        button_layout.addWidget(calculate_btn)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
    
    def on_calculate(self):
        """Manejador del botón calcular"""
        try:
            sistema = self.create_sistema_from_inputs()
            self.data_ready.emit(sistema)
            self.calculate_requested.emit()
        except Exception as e:
            # TODO: Mostrar mensaje de error
            print(f"Error: {e}")
    
    def create_sistema_from_inputs(self):
        """Crea el objeto SistemaTuberias desde los inputs"""
        # Obtener fluido
        fluid_name = self.fluid_combo.currentText()
        fluido = self.fluidos_data[fluid_name]
        
        # Crear sistema
        sistema = SistemaTuberias(
            fluido=fluido,
            caudal=self.caudal_input.value() / 1000.0,  # Convertir L/s a m³/s
            eficiencia_bomba=self.eficiencia_input.value(),
            elevacion_punto1=self.z1_input.value(),
            elevacion_punto2=self.z2_input.value(),
            presion_punto1=self.p1_input.value(),
            presion_punto2=self.p2_input.value()
        )
        
        # Agregar tramos
        for i in range(self.pipes_layout.count()):
            pipe_widget = self.pipes_layout.itemAt(i).widget()
            if hasattr(pipe_widget, 'longitud_input'):
                sistema.agregar_tramo(
                    longitud=pipe_widget.longitud_input.value(),
                    orientacion=pipe_widget.orient_combo.currentText(),
                    diametro=pipe_widget.diametro_input.value()
                )
        
        # Agregar accesorios
        for accesorio_name, accesorio in self.accesorios_data.items():
            checkbox = self.fitting_checkboxes[accesorio_name]
            spinbox = self.fitting_spinboxes[accesorio_name]
            
            if checkbox.isChecked() and spinbox.value() > 0:
                accesorio_copy = accesorio
                accesorio_copy.cantidad = spinbox.value()
                sistema.agregar_accesorio(accesorio_copy)
        
        return sistema
    
    def clear_data(self):
        """Limpia todos los datos del formulario"""
        # Reiniciar valores básicos
        self.caudal_input.setValue(10.0)
        self.eficiencia_input.setValue(0.70)
        self.z1_input.setValue(2.0)
        self.z2_input.setValue(8.0)
        
        # Limpiar tramos (dejar solo uno)
        while self.pipes_layout.count() > 1:
            widget = self.pipes_layout.itemAt(0).widget()
            self.remove_pipe_section(widget)
        
        # Reiniciar primer tramo
        if self.pipes_layout.count() > 0:
            pipe_widget = self.pipes_layout.itemAt(0).widget()
            pipe_widget.longitud_input.setValue(10.0)
            pipe_widget.orient_combo.setCurrentIndex(0)
            pipe_widget.diametro_input.setValue(0.100)
        
        # Limpiar accesorios
        for checkbox in self.fitting_checkboxes.values():
            checkbox.setChecked(False)
        for spinbox in self.fitting_spinboxes.values():
            spinbox.setValue(0)
            spinbox.setEnabled(False)
