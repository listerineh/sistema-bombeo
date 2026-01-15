"""
Visualizador del sistema de tuberías.

Este módulo contiene la clase SystemViewer que proporciona una representación
gráfica interactiva del sistema de bombeo, incluyendo tuberías, accesorios,
elevaciones y controles de zoom y navegación.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, 
    QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem,
    QGraphicsPolygonItem, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QFont, QPainter, QPolygonF


class SystemViewer(QWidget):
    """Widget para visualizar el sistema de tuberías de forma interactiva.
    
    Este visualizador muestra:
    - Diagrama esquemático del sistema con tuberías y accesorios
    - Diferencias de elevación con líneas de referencia
    - Etiquetas descriptivas para cada componente
    - Controles de zoom y navegación
    - Leyenda completa de símbolos utilizados
    """
    
    def __init__(self):
        super().__init__()
        self.sistema = None
        self.zoom_factor = 1.0
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del visualizador con controles de zoom."""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Visualización del Sistema")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Descripción
        desc = QLabel("Diagrama esquemático del sistema de tuberías")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #666; font-size: 11px; margin-bottom: 8px;")
        layout.addWidget(desc)
        
        # Controles de zoom
        controls_layout = QHBoxLayout()
        
        # Botones de zoom
        zoom_in_btn = QPushButton("Zoom +")
        zoom_in_btn.setMaximumWidth(80)
        zoom_in_btn.clicked.connect(self.zoom_in)
        
        zoom_out_btn = QPushButton("Zoom -")
        zoom_out_btn.setMaximumWidth(80)
        zoom_out_btn.clicked.connect(self.zoom_out)
        
        reset_view_btn = QPushButton("Reset Vista")
        reset_view_btn.setMaximumWidth(100)
        reset_view_btn.clicked.connect(self.reset_view)
        
        # Etiqueta de zoom
        self.zoom_label = QLabel("Zoom: 100%")
        self.zoom_label.setStyleSheet("color: #ccc; font-size: 10px;")
        
        controls_layout.addWidget(zoom_in_btn)
        controls_layout.addWidget(zoom_out_btn)
        controls_layout.addWidget(reset_view_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(self.zoom_label)
        
        layout.addLayout(controls_layout)
        
        # Vista gráfica
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        
        # Habilitar navegación
        self.graphics_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.graphics_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        layout.addWidget(self.graphics_view)
        
        # Información del sistema
        self.info_label = QLabel("Sin sistema configurado")
        self.info_label.setStyleSheet("color: #666; font-size: 10px; padding: 5px;")
        layout.addWidget(self.info_label)
    
    def update_system(self, sistema):
        """Actualiza la visualización con el nuevo sistema configurado.
        
        Args:
            sistema: Objeto SistemaTuberias con la configuración completa
        """
        self.sistema = sistema
        self.draw_system()
        self.update_info()
    
    def clear_system(self):
        """Limpia la visualización y elimina el sistema actual."""
        self.sistema = None
        self.graphics_scene.clear()
        self.info_label.setText("Sin sistema configurado")
    
    def draw_system(self):
        """Dibuja el diagrama completo del sistema de tuberías.
        
        Incluye tuberías, accesorios, tanques, elevaciones y línea de referencia.
        """
        if not self.sistema:
            return
        
        self.graphics_scene.clear()
        
        # Configurar escala y posición
        scale = 60  # 60 pixels por metro (más grande)
        start_x = 80
        start_y = 400  # Más abajo para dejar espacio para elevación
        
        current_x = start_x
        current_y = start_y
        
        # Calcular posición Y inicial basada en elevación P1
        current_y = start_y - (self.sistema.elevacion_punto1 * scale)
        
        # Dibujar punto 1 (tanque de succión)
        self.draw_tank(current_x, current_y, "P1", f"Succión\nZ={self.sistema.elevacion_punto1}m")
        
        # Guardar posición inicial para línea de elevación
        elevation_start_x = current_x
        elevation_start_y = current_y
        
        # Dibujar tramos de tubería
        for i, tramo in enumerate(self.sistema.tramos):
            if tramo.orientacion == 'horizontal':
                # Dibujar tramo horizontal (misma elevación)
                end_x = current_x + tramo.longitud * scale
                self.draw_pipe(current_x, current_y, end_x, current_y, tramo.diametro * scale)
                
                # Dibujar accesorios en este tramo
                self.draw_fittings_on_pipe(current_x, current_y, end_x, current_y, tramo.diametro * scale, i)
                
                # Agregar etiqueta de longitud
                mid_x = (current_x + end_x) / 2
                length_text = QGraphicsTextItem(f"{tramo.longitud}m")
                length_text.setDefaultTextColor(QColor(255, 255, 255))
                length_text.setFont(QFont("Arial", 10))
                length_text.setPos(mid_x - 20, current_y + 30)
                self.graphics_scene.addItem(length_text)
                
                current_x = end_x
            else:  # vertical
                # Dibujar tramo vertical (independiente de la elevación)
                end_y = current_y - tramo.longitud * scale  # hacia arriba es negativo
                self.draw_pipe(current_x, current_y, current_x, end_y, tramo.diametro * scale)
                
                # Dibujar accesorios en este tramo
                self.draw_fittings_on_pipe(current_x, current_y, current_x, end_y, tramo.diametro * scale, i)
                
                # Agregar etiqueta de longitud
                mid_y = (current_y + end_y) / 2
                length_text = QGraphicsTextItem(f"{tramo.longitud}m")
                length_text.setDefaultTextColor(QColor(255, 255, 255))
                length_text.setFont(QFont("Arial", 10))
                length_text.setPos(current_x + 30, mid_y - 10)
                self.graphics_scene.addItem(length_text)
                
                current_y = end_y
        
        # Calcular posición Y final basada en elevación P2 (independiente de los tramos)
        final_y = start_y - (self.sistema.elevacion_punto2 * scale)
        
        # Dibujar línea de elevación (diferencia de altura entre puntos)
        if abs(self.sistema.elevacion_punto2 - self.sistema.elevacion_punto1) > 0.1:  # Si hay diferencia significativa
            # Línea de elevación con estilo diferente
            elevation_line = QGraphicsLineItem(elevation_start_x, elevation_start_y, current_x, final_y)
            elevation_line.setPen(QPen(QColor(255, 200, 100), 4))  # Línea amarilla gruesa para elevación
            self.graphics_scene.addItem(elevation_line)
            
            # Etiqueta de cambio de elevación
            mid_elev_x = (elevation_start_x + current_x) / 2
            mid_elev_y = (elevation_start_y + final_y) / 2
            
            # Fondo para la etiqueta de elevación
            elev_bg = QGraphicsRectItem(mid_elev_x - 5, mid_elev_y - 15, 120, 25)
            elev_bg.setBrush(QBrush(QColor(50, 50, 50)))
            elev_bg.setPen(QPen(QColor(255, 200, 100), 2))
            self.graphics_scene.addItem(elev_bg)
            
            elev_text = QGraphicsTextItem(f"ΔZ = {abs(self.sistema.elevacion_punto2 - self.sistema.elevacion_punto1):.1f}m")
            elev_text.setDefaultTextColor(QColor(255, 200, 100))
            elev_text.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            elev_text.setPos(mid_elev_x, mid_elev_y - 12)
            self.graphics_scene.addItem(elev_text)
        
        # Dibujar punto 2 (tanque de descarga)
        self.draw_tank(current_x, final_y, "P2", f"Descarga\nZ={self.sistema.elevacion_punto2}m")
        
        # Dibujar línea de referencia (elevación 0)
        self.draw_reference_line(start_y)
        
        # Agregar leyenda mejorada
        self.draw_legend()
        
        # Ajustar la vista
        self.graphics_view.fitInView(self.graphics_scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
    
    def draw_tank(self, x, y, label, description):
        """Dibuja un tanque en la posición especificada.
        
        Args:
            x (float): Posición X del centro del tanque
            y (float): Posición Y del centro del tanque
            label (str): Etiqueta del tanque (P1, P2)
            description (str): Descripción con elevación
        """
        # Rectángulo del tanque
        tank_size = 50  # Más grande
        tank = QGraphicsRectItem(x - tank_size//2, y - tank_size//2, tank_size, tank_size)
        tank.setBrush(QBrush(QColor(70, 130, 180)))  # Azul más oscuro
        tank.setPen(QPen(QColor(100, 150, 200), 3))  # Borde más grueso
        self.graphics_scene.addItem(tank)
        
        # Etiqueta del tanque
        text = QGraphicsTextItem(f"{label}\n{description}")
        text.setDefaultTextColor(QColor(255, 255, 255))
        text.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        text.setPos(x - 25, y + tank_size//2 + 10)
        self.graphics_scene.addItem(text)
    
    def draw_pipe(self, x1, y1, x2, y2, diameter):
        """Dibuja una tubería entre dos puntos con el diámetro especificado.
        
        Args:
            x1, y1 (float): Coordenadas del punto inicial
            x2, y2 (float): Coordenadas del punto final
            diameter (float): Diámetro visual de la tubería
        """
        # Línea principal (más gruesa)
        pipe = QGraphicsLineItem(x1, y1, x2, y2)
        pipe.setPen(QPen(QColor(180, 180, 180), diameter))
        self.graphics_scene.addItem(pipe)
        
        # Línea de borde (más visible)
        border = QGraphicsLineItem(x1, y1, x2, y2)
        border.setPen(QPen(QColor(100, 100, 100), diameter + 4))
        self.graphics_scene.addItem(border)
    
    def draw_fittings_on_pipe(self, x1, y1, x2, y2, pipe_diameter, tramo_index):
        """Dibuja accesorios sobre una tubería específica con ubicación inteligente.
        
        Args:
            x1, y1 (float): Coordenadas del punto inicial de la tubería
            x2, y2 (float): Coordenadas del punto final de la tubería
            pipe_diameter (float): Diámetro de la tubería
            tramo_index (int): Índice del tramo para ubicación inteligente
        """
        if not self.sistema or not self.sistema.accesorios:
            return
        
        # Determinar qué accesorios van en este tramo
        fittings_for_this_tramo = []
        
        # Debug: imprimir información del tramo
        print(f"DEBUG: Tramo {tramo_index}, x1={x1}, y1={y1}, x2={x2}, y2={y2}")
        print(f"DEBUG: Es vertical: {x1 == x2}, Es horizontal: {x1 != x2}")
        
        for accesorio in self.sistema.accesorios:
            if accesorio.cantidad > 0:
                # Lógica de ubicación según tipo de accesorio
                accesorio_type = accesorio.tipo.value
                print(f"DEBUG: Accesorio encontrado: {accesorio_type}, cantidad: {accesorio.cantidad}")
                
                # Entrada de tanque: siempre en el primer tramo
                if 'entrada_tanque' in accesorio_type and tramo_index == 0:
                    print(f"DEBUG: Entrada tanque asignada al tramo {tramo_index}")
                    fittings_for_this_tramo.extend([accesorio_type] * accesorio.cantidad)
                
                # Codos: en cambios de dirección (tramos verticales)
                elif 'codo' in accesorio_type and tramo_index > 0:
                    # Verificar si este tramo es vertical
                    if x1 == x2:  # Tramo vertical
                        print(f"DEBUG: Codo asignado al tramo vertical {tramo_index}")
                        fittings_for_this_tramo.extend([accesorio_type] * accesorio.cantidad)
                
                # Salida de tanque: siempre en el último tramo
                elif 'salida_tanque' in accesorio_type and tramo_index == len(self.sistema.tramos) - 1:
                    print(f"DEBUG: Salida tanque asignada al último tramo {tramo_index}")
                    fittings_for_this_tramo.extend([accesorio_type] * accesorio.cantidad)
                
                # Válvulas y otros: en tramos horizontales intermedios
                elif ('valvula' in accesorio_type or 'tee' in accesorio_type):
                    if tramo_index > 0 and tramo_index < len(self.sistema.tramos) - 1:
                        if x1 != x2:  # Tramo horizontal
                            print(f"DEBUG: Válvula/Tee asignada al tramo horizontal intermedio {tramo_index}")
                            fittings_for_this_tramo.extend([accesorio_type] * accesorio.cantidad)
                        else:
                            print(f"DEBUG: Válvula/Tee NO asignada (tramo vertical) {tramo_index}")
                    else:
                        print(f"DEBUG: Válvula/Tee NO asignada (tramo extremo) {tramo_index}")
        
        print(f"DEBUG: Accesorios en tramo {tramo_index}: {fittings_for_this_tramo}")
        
        if not fittings_for_this_tramo:
            return
        
        # Dibujar accesorios en este tramo
        spacing = 0.8  # Espaciado entre accesorios
        current_pos = 0.1
        
        for fitting_type in fittings_for_this_tramo:
            # Calcular posición del accesorio
            if x1 == x2:  # Vertical
                y = y1 + (y2 - y1) * current_pos
                x = x1
            else:  # Horizontal
                x = x1 + (x2 - x1) * current_pos
                y = y1
            
            # Dibujar símbolo del accesorio
            self.draw_fitting_symbol(x, y, pipe_diameter, fitting_type)
            
            current_pos += spacing
            if current_pos > 0.9:
                current_pos = 0.1
    
    def draw_fitting_symbol(self, x, y, pipe_diameter, fitting_type):
        """Dibuja el símbolo de un accesorio con etiqueta descriptiva.
        
        Args:
            x, y (float): Coordenadas del centro del símbolo
            pipe_diameter (float): Diámetro de la tubería para escalar el símbolo
            fitting_type (str): Tipo de accesorio para determinar el símbolo
        """
        symbol_size = pipe_diameter * 2.0  # Más grande
        
        if 'codo' in fitting_type:
            # Dibujar un cuadrado para codo
            rect = QGraphicsRectItem(x - symbol_size//2, y - symbol_size//2, symbol_size, symbol_size)
            rect.setBrush(QBrush(QColor(200, 100, 100)))
            rect.setPen(QPen(QColor(255, 150, 150), 2))
            self.graphics_scene.addItem(rect)
            
            # Etiqueta del accesorio
            label = QGraphicsTextItem("Codo")
            label.setDefaultTextColor(QColor(255, 255, 255))
            label.setFont(QFont("Arial", 8))
            label.setPos(x - 15, y + symbol_size//2 + 5)
            self.graphics_scene.addItem(label)
            
        elif 'valvula' in fitting_type:
            # Dibujar un círculo para válvula
            circle = QGraphicsEllipseItem(x - symbol_size//2, y - symbol_size//2, symbol_size, symbol_size)
            circle.setBrush(QBrush(QColor(100, 200, 100)))
            circle.setPen(QPen(QColor(150, 255, 150), 2))
            self.graphics_scene.addItem(circle)
            
            # Etiqueta del accesorio
            label = QGraphicsTextItem("Válvula")
            label.setDefaultTextColor(QColor(255, 255, 255))
            label.setFont(QFont("Arial", 8))
            label.setPos(x - 20, y + symbol_size//2 + 5)
            self.graphics_scene.addItem(label)
            
        elif 'tee' in fitting_type:
            # Dibujar un rombo para tee
            diamond = QGraphicsRectItem(x - symbol_size//3, y - symbol_size//2, symbol_size*2/3, symbol_size)
            diamond.setBrush(QBrush(QColor(200, 200, 100)))
            diamond.setPen(QPen(QColor(255, 255, 150), 2))
            self.graphics_scene.addItem(diamond)
            
            # Etiqueta del accesorio
            label = QGraphicsTextItem("Tee")
            label.setDefaultTextColor(QColor(255, 255, 255))
            label.setFont(QFont("Arial", 8))
            label.setPos(x - 10, y + symbol_size//2 + 5)
            self.graphics_scene.addItem(label)
            
        elif 'entrada_tanque' in fitting_type:
            # Dibujar triángulo para entrada
            polygon = QPolygonF([
                QPointF(x, y - symbol_size//2),
                QPointF(x - symbol_size//2, y + symbol_size//2),
                QPointF(x + symbol_size//2, y + symbol_size//2)
            ])
            triangle = QGraphicsPolygonItem(polygon)
            triangle.setBrush(QBrush(QColor(150, 150, 200)))
            triangle.setPen(QPen(QColor(200, 200, 255), 2))
            self.graphics_scene.addItem(triangle)
            
            # Etiqueta del accesorio
            label = QGraphicsTextItem("Entrada")
            label.setDefaultTextColor(QColor(255, 255, 255))
            label.setFont(QFont("Arial", 8))
            label.setPos(x - 20, y + symbol_size//2 + 5)
            self.graphics_scene.addItem(label)
            
        else:
            # Dibujar un círculo para otros accesorios
            circle = QGraphicsEllipseItem(x - symbol_size//2, y - symbol_size//2, symbol_size, symbol_size)
            circle.setBrush(QBrush(QColor(150, 150, 200)))
            circle.setPen(QPen(QColor(200, 200, 255), 2))
            self.graphics_scene.addItem(circle)
            
            # Etiqueta del accesorio
            label = QGraphicsTextItem("Accesorio")
            label.setDefaultTextColor(QColor(255, 255, 255))
            label.setFont(QFont("Arial", 8))
            label.setPos(x - 25, y + symbol_size//2 + 5)
            self.graphics_scene.addItem(label)
    
    def draw_legend(self):
        """Dibuja una leyenda completa con todos los símbolos utilizados.
        
        Incluye descripciones detalladas para cada tipo de componente
        del sistema de tuberías.
        """
        legend_x = 50
        legend_y = 50
        
        # Fondo de la leyenda
        legend_bg = QGraphicsRectItem(legend_x - 10, legend_y - 10, 280, 180)
        legend_bg.setBrush(QBrush(QColor(40, 40, 40)))
        legend_bg.setPen(QPen(QColor(100, 100, 100), 1))
        self.graphics_scene.addItem(legend_bg)
        
        # Título de la leyenda
        title = QGraphicsTextItem("Leyenda:")
        title.setDefaultTextColor(QColor(255, 255, 255))
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setPos(legend_x, legend_y)
        self.graphics_scene.addItem(title)
        
        # Símbolos con descripciones detalladas
        symbols = [
            ("Entrada", "triangle", QColor(150, 150, 200), "Entrada de tanque"),
            ("Codo", "square", QColor(200, 100, 100), "Codo 90°"),
            ("Válvula", "circle", QColor(100, 200, 100), "Válvula compuerta"),
            ("Tee", "diamond", QColor(200, 200, 100), "Conexión Tee"),
            ("Tubería", "line", QColor(180, 180, 180), "Tubería principal"),
            ("Elevación", "elevation", QColor(255, 200, 100), "Diferencia de elevación")
        ]
        
        for i, (name, shape, color, description) in enumerate(symbols):
            y_pos = legend_y + 25 + i * 22
            
            # Dibujar símbolo
            if shape == "square":
                symbol = QGraphicsRectItem(legend_x, y_pos, 15, 15)
            elif shape == "diamond":
                symbol = QGraphicsRectItem(legend_x + 2, y_pos - 2, 11, 19)
            elif shape == "line":
                symbol = QGraphicsLineItem(legend_x, y_pos + 7, legend_x + 15, y_pos + 7)
                symbol.setPen(QPen(color, 3))
            elif shape == "elevation":
                symbol = QGraphicsLineItem(legend_x, y_pos + 7, legend_x + 15, y_pos + 7)
                symbol.setPen(QPen(color, 4))
            elif shape == "triangle":
                polygon = QPolygonF([
                    QPointF(legend_x + 7, y_pos),
                    QPointF(legend_x, y_pos + 15),
                    QPointF(legend_x + 15, y_pos + 15)
                ])
                symbol = QGraphicsPolygonItem(polygon)
            else:  # circle
                symbol = QGraphicsEllipseItem(legend_x, y_pos, 15, 15)
            
            if shape != "line" and shape != "elevation":
                symbol.setBrush(QBrush(color))
                symbol.setPen(QPen(color.lighter(150), 1))
            
            self.graphics_scene.addItem(symbol)
            
            # Etiqueta principal
            label = QGraphicsTextItem(name)
            label.setDefaultTextColor(QColor(255, 255, 255))
            label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            label.setPos(legend_x + 25, y_pos - 2)
            self.graphics_scene.addItem(label)
            
            # Descripción
            desc = QGraphicsTextItem(description)
            desc.setDefaultTextColor(QColor(200, 200, 200))
            desc.setFont(QFont("Arial", 8))
            desc.setPos(legend_x + 25, y_pos + 10)
            self.graphics_scene.addItem(desc)
    
    def zoom_in(self):
        """Aumenta el zoom en un 20%."""
        self.zoom_factor *= 1.2
        self.graphics_view.scale(1.2, 1.2)
        self.update_zoom_label()
    
    def zoom_out(self):
        """Disminuye el zoom en un 20%."""
        self.zoom_factor /= 1.2
        self.graphics_view.scale(1/1.2, 1/1.2)
        self.update_zoom_label()
    
    def reset_view(self):
        """Restablece la vista al zoom inicial y ajusta al contenido."""
        self.graphics_view.resetTransform()
        self.zoom_factor = 1.0
        self.update_zoom_label()
        # Ajustar vista al contenido
        self.graphics_view.fitInView(self.graphics_scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
    
    def update_zoom_label(self):
        """Actualiza la etiqueta de zoom con el porcentaje actual."""
        zoom_percent = int(self.zoom_factor * 100)
        self.zoom_label.setText(f"Zoom: {zoom_percent}%")
    
    def draw_reference_line(self, reference_y):
        """Dibuja una línea de referencia para elevación 0.
        
        Args:
            reference_y (float): Posición Y de la línea de referencia
        """
        # Encontrar el límite derecho del sistema
        max_x = 80
        if self.sistema.tramos:
            for tramo in self.sistema.tramos:
                if tramo.orientacion == 'horizontal':
                    max_x += tramo.longitud * 60  # scale
        
        # Línea de referencia horizontal
        ref_line = QGraphicsLineItem(50, reference_y, max_x + 100, reference_y)
        ref_line.setPen(QPen(QColor(100, 100, 100), 2, Qt.PenStyle.DashLine))
        self.graphics_scene.addItem(ref_line)
        
        # Etiqueta de referencia
        ref_text = QGraphicsTextItem("Z = 0m (Referencia)")
        ref_text.setDefaultTextColor(QColor(150, 150, 150))
        ref_text.setFont(QFont("Arial", 9))
        ref_text.setPos(55, reference_y + 5)
        self.graphics_scene.addItem(ref_text)
    
    def update_info(self):
        """Actualiza la información del sistema mostrada en el panel."""
        if not self.sistema:
            return
        
        info_text = f"""
        <b>Información del Sistema:</b><br>
        • Longitud total: {self.sistema.longitud_total:.2f} m<br>
        • Número de tramos: {len(self.sistema.tramos)}<br>
        • Tramos verticales: {len(self.sistema.obtener_tramos_verticales())}<br>
        • Tramos horizontales: {len(self.sistema.obtener_tramos_horizontales())}<br>
        • Fluido: {self.sistema.fluido.nombre}<br>
        • Caudal: {self.sistema.caudal*1000:.1f} L/s<br>
        • Número de accesorios: {len(self.sistema.accesorios)}
        """
        self.info_label.setText(info_text.strip())
