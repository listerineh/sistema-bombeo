"""
Estilos oscuros modernos para la interfaz GUI del Sistema de Bombeo.

Este módulo proporciona una hoja de estilos completa con tema oscuro
para toda la aplicación, incluyendo widgets personalizados, estados interactivos
y una paleta de colores consistente y profesional.
"""

def apply_modern_style(app):
    """Aplica estilos oscuros modernos a toda la aplicación.
    
    Args:
        app: Instancia de QApplication a la que se aplicarán los estilos
    """
    
    app.setStyleSheet("""
        /* Estilo general */
        QMainWindow {
            background-color: #2b2b2b;
        }
        
        QWidget {
            font-family: Arial, sans-serif;
            font-size: 12px;
            color: white;
        }
        
        /* Botones */
        QPushButton {
            background-color: #404040;
            color: white;
            border: 2px solid #555;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #505050;
            border-color: #666;
        }
        
        QPushButton:pressed {
            background-color: #353535;
        }
        
        QPushButton:disabled {
            background-color: #333;
            color: #888;
            border-color: #444;
        }
        
        /* Botón primario */
        QPushButton[class="primary"] {
            background-color: #4CAF50;
            color: white;
            border-color: #45a049;
        }
        
        QPushButton[class="primary"]:hover {
            background-color: #45a049;
        }
        
        /* Botón de peligro */
        QPushButton[class="danger"] {
            background-color: #f44336;
            color: white;
            border-color: #da190b;
        }
        
        QPushButton[class="danger"]:hover {
            background-color: #da190b;
        }
        
        /* Campos de entrada */
        QLineEdit, QSpinBox, QDoubleSpinBox {
            border: 2px solid #555;
            border-radius: 4px;
            padding: 6px;
            background-color: #404040;
            color: white;
        }
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border-color: #2196F3;
        }
        
        /* Combobox */
        QComboBox {
            border: 2px solid #555;
            border-radius: 4px;
            padding: 6px;
            background-color: #404040;
            color: white;
            min-width: 100px;
        }
        
        QComboBox:focus {
            border-color: #2196F3;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid #ccc;
            margin-right: 4px;
        }
        
        QComboBox QAbstractItemView {
            background-color: #404040;
            color: white;
            border: 1px solid #555;
            selection-background-color: #2196F3;
        }
        
        /* Checkboxes */
        QCheckBox {
            spacing: 8px;
            font-size: 11px;
            color: white;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 2px solid #555;
            border-radius: 3px;
            background-color: #404040;
        }
        
        QCheckBox::indicator:checked {
            background-color: #2196F3;
            border-color: #2196F3;
        }
        
        /* Group boxes */
        QGroupBox {
            font-weight: bold;
            border: 2px solid #555;
            border-radius: 5px;
            margin-top: 8px;
            padding-top: 8px;
            color: white;
            background-color: #333;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 4px 0 4px;
            color: white;
        }
        
        /* Pestañas */
        QTabWidget::pane {
            border: 1px solid #555;
            background-color: #2b2b2b;
        }
        
        QTabBar::tab {
            background-color: #404040;
            border: 1px solid #555;
            padding: 8px 16px;
            margin-right: 2px;
            color: white;
        }
        
        QTabBar::tab:selected {
            background-color: #2b2b2b;
            border-bottom: 2px solid #2196F3;
        }
        
        QTabBar::tab:hover {
            background-color: #505050;
        }
        
        /* Tablas */
        QTableWidget {
            gridline-color: #555;
            background-color: #2b2b2b;
            alternate-background-color: #333;
            color: white;
        }
        
        QTableWidget::item {
            padding: 4px;
            color: white;
        }
        
        QTableWidget::item:selected {
            background-color: #2196F3;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #404040;
            padding: 6px;
            border: 1px solid #555;
            font-weight: bold;
            color: white;
        }
        
        /* Labels */
        QLabel {
            color: white;
            font-size: 12px;
        }
        
        QLabel[class="title"] {
            font-size: 16px;
            font-weight: bold;
            color: #2196F3;
            margin: 8px 0;
            padding: 8px;
        }
        
        QLabel[class="subtitle"] {
            font-size: 13px;
            font-weight: bold;
            color: #ccc;
            margin: 4px 0;
            background-color: #404040;
            padding: 4px 8px;
            border-radius: 3px;
        }
        
        QLabel[class="result"] {
            font-size: 14px;
            font-weight: bold;
            color: #2196F3;
            padding: 8px 12px;
            background-color: #1e3a5f;
            border: 1px solid #2196F3;
            border-radius: 6px;
            margin: 2px;
        }
        
        QLabel[class="warning"] {
            color: #ff6b6b;
            font-weight: bold;
            background-color: #4a2a2a;
            padding: 4px 8px;
            border-radius: 3px;
        }
        
        QLabel[class="success"] {
            color: #4CAF50;
            font-weight: bold;
            background-color: #2a4a2a;
            padding: 4px 8px;
            border-radius: 3px;
        }
        
        /* Separadores */
        QFrame {
            border: 1px solid #555;
        }
        
        QFrame[class="separator"] {
            border: none;
            border-top: 2px solid #555;
            margin: 8px 0;
        }
        
        /* Scrollbars */
        QScrollBar:vertical {
            border: none;
            background-color: #2b2b2b;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #555;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #666;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        
        /* Status bar */
        QStatusBar {
            background-color: #2b2b2b;
            border-top: 1px solid #555;
            color: #ccc;
        }
        
        /* Menu bar */
        QMenuBar {
            background-color: #2b2b2b;
            border-bottom: 1px solid #555;
            color: white;
        }
        
        QMenuBar::item {
            padding: 6px 12px;
            background-color: transparent;
            color: white;
        }
        
        QMenuBar::item:selected {
            background-color: #404040;
        }
        
        QMenu {
            background-color: #404040;
            border: 1px solid #555;
            color: white;
        }
        
        QMenu::item {
            padding: 6px 20px;
            color: white;
        }
        
        QMenu::item:selected {
            background-color: #505050;
        }
        
        /* Scroll area */
        QScrollArea {
            background-color: #2b2b2b;
            border: none;
        }
    """)
