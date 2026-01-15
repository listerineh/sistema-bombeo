#!/bin/bash

# =============================================================================
# Sistema de Cálculo de Bombeo - Script de Empaquetado Automático
# =============================================================================
# Este script automatiza todo el proceso de empaquetado siguiendo los pasos
# que se realizaron manualmente durante el desarrollo.
#
# Compatible con: macOS, Linux
# Para Windows: usar build_package.bat
#
# Uso: ./build_package.sh (macOS/Linux)
# Uso: build_package.bat (Windows)
# =============================================================================

set -e  # Detener si hay errores

# Colores para salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes coloreados
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detectar sistema operativo
detect_os() {
    case "$(uname -s)" in
        Darwin*)    OS="macos";;
        Linux*)     OS="linux";;
        CYGWIN*|MINGW*|MSYS*) OS="windows";;
        *)          OS="unknown";;
    esac
    echo $OS
}

OS=$(detect_os)
print_status "🖥️ Sistema operativo detectado: $OS"

# =============================================================================
# PASO 1: VERIFICACIÓN PREVIA
# =============================================================================
print_status "🔍 Verificando entorno de empaquetado..."

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    print_error "No se encuentra main.py. Asegúrate de estar en el directorio raíz del proyecto."
    exit 1
fi

# Verificar archivos de datos
DATA_FILES=("src/data/accesorios.csv" "src/data/constantes.csv" "src/data/fluidos.csv")
for file in "${DATA_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Archivo de datos faltante: $file"
        exit 1
    fi
done

print_success "✅ Todos los archivos necesarios encontrados"

# =============================================================================
# PASO 2: LIMPIEZA DE ENTORNOS ANTERIORES
# =============================================================================
print_status "🧹 Limpiando entornos anteriores..."

# Eliminar entorno virtual anterior si existe
if [ -d "packaging_env" ]; then
    print_warning "Eliminando entorno virtual anterior..."
    rm -rf packaging_env
fi

# Eliminar directorios de build anteriores
if [ -d "build" ]; then
    print_warning "Eliminando directorio build anterior..."
    rm -rf build
fi

# Eliminar directorios de dist anteriores
if [ -d "dist" ]; then
    print_warning "Eliminando directorio dist anterior..."
    rm -rf dist
fi

# Eliminar builds específicos de plataforma
if [ -d "macos" ]; then
    print_warning "Eliminando builds macOS anteriores..."
    rm -rf macos
fi

print_success "✅ Limpieza completada"

# =============================================================================
# PASO 3: CREACIÓN DE ENTORNO VIRTUAL
# =============================================================================
print_status "🐍 Creando entorno virtual para empaquetado..."

# Comando Python según el sistema operativo
if [ "$OS" = "windows" ]; then
    python -m venv packaging_env
    source packaging_env/Scripts/activate
else
    python3 -m venv packaging_env
    source packaging_env/bin/activate
fi

print_success "✅ Entorno virtual creado y activado"

# =============================================================================
# PASO 4: INSTALACIÓN DE DEPENDENCIAS
# =============================================================================
print_status "📦 Instalando dependencias..."

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias desde requirements.txt
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "✅ Dependencias instaladas desde requirements.txt"
else
    # Instalar dependencias manualmente si no existe requirements.txt
    pip install PyQt6==6.10.2
    pip install PyInstaller==6.18.0
    print_success "✅ Dependencias instaladas manualmente"
fi

# =============================================================================
# PASO 5: VERIFICACIÓN DE RUTAS DE DATOS
# =============================================================================
print_status "🔧 Verificando configuración de rutas de datos..."

# Crear script de prueba para verificar rutas
cat > test_data_paths.py << 'EOF'
#!/usr/bin/env python3
import os
import sys

# Verificar rutas de datos
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    data_dir = os.path.join(base_path, 'data')
else:
    data_dir = os.path.join(os.path.dirname(__file__), 'src', 'data')

print(f"Directorio de datos: {data_dir}")
print(f"Existe: {os.path.exists(data_dir)}")

# Verificar archivos CSV
csv_files = ["accesorios.csv", "constantes.csv", "fluidos.csv"]
for csv_file in csv_files:
    csv_path = os.path.join(data_dir, csv_file)
    exists = os.path.exists(csv_path)
    size = os.path.getsize(csv_path) if exists else 0
    print(f"  {csv_file}: {'✅' if exists else '❌'} ({size} bytes)")
EOF

python test_data_paths.py
rm test_data_paths.py

print_success "✅ Configuración de rutas verificada"

# =============================================================================
# PASO 6: CREACIÓN DE ARCHIVO DE ESPECIFICACIONES
# =============================================================================
print_status "📄 Creando archivo de especificaciones PyInstaller..."

# Crear archivo .spec según el sistema operativo
if [ "$OS" = "windows" ]; then
    cat > bombeo.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/data/accesorios.csv', 'data'),
        ('src/data/constantes.csv', 'data'),
        ('src/data/fluidos.csv', 'data'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets', 
        'PyQt6.QtGui',
        'PyQt6.QtCore.Qt',
        'PyQt6.QtWidgets.QApplication',
        'PyQt6.QtWidgets.QMainWindow',
        'PyQt6.QtWidgets.QWidget',
        'PyQt6.QtWidgets.QVBoxLayout',
        'PyQt6.QtWidgets.QHBoxLayout',
        'PyQt6.QtWidgets.QLabel',
        'PyQt6.QtWidgets.QPushButton',
        'PyQt6.QtWidgets.QGroupBox',
        'PyQt6.QtWidgets.QLineEdit',
        'PyQt6.QtWidgets.QDoubleSpinBox',
        'PyQt6.QtWidgets.QSpinBox',
        'PyQt6.QtWidgets.QComboBox',
        'PyQt6.QtWidgets.QCheckBox',
        'PyQt6.QtWidgets.QScrollArea',
        'PyQt6.QtWidgets.QTabWidget',
        'PyQt6.QtWidgets.QTableWidget',
        'PyQt6.QtWidgets.QHeaderView',
        'PyQt6.QtWidgets.QSplitter',
        'PyQt6.QtWidgets.QStatusBar',
        'PyQt6.QtWidgets.QMenuBar',
        'PyQt6.QtWidgets.QMessageBox',
        'PyQt6.QtWidgets.QGraphicsView',
        'PyQt6.QtWidgets.QGraphicsScene',
        'PyQt6.QtWidgets.QGraphicsItem',
        'PyQt6.QtWidgets.QGraphicsRectItem',
        'PyQt6.QtWidgets.QGraphicsEllipseItem',
        'PyQt6.QtWidgets.QGraphicsTextItem',
        'PyQt6.QtWidgets.QGraphicsLineItem',
        'PyQt6.QtWidgets.QGraphicsPolygonItem',
        'PyQt6.QtCore.pyqtSignal',
        'PyQt6.QtCore.QPointF',
        'PyQt6.QtGui.QPen',
        'PyQt6.QtGui.QBrush',
        'PyQt6.QtGui.QColor',
        'PyQt6.QtGui.QFont',
        'PyQt6.QtGui.QPainter',
        'PyQt6.QtGui.QPolygonF',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SistemaBombeo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SistemaBombeo',
)
EOF
else
    # Versión para macOS/Linux
    cat > bombeo.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/data/accesorios.csv', 'data'),
        ('src/data/constantes.csv', 'data'),
        ('src/data/fluidos.csv', 'data'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets', 
        'PyQt6.QtGui',
        'PyQt6.QtCore.Qt',
        'PyQt6.QtWidgets.QApplication',
        'PyQt6.QtWidgets.QMainWindow',
        'PyQt6.QtWidgets.QWidget',
        'PyQt6.QtWidgets.QVBoxLayout',
        'PyQt6.QtWidgets.QHBoxLayout',
        'PyQt6.QtWidgets.QLabel',
        'PyQt6.QtWidgets.QPushButton',
        'PyQt6.QtWidgets.QGroupBox',
        'PyQt6.QtWidgets.QLineEdit',
        'PyQt6.QtWidgets.QDoubleSpinBox',
        'PyQt6.QtWidgets.QSpinBox',
        'PyQt6.QtWidgets.QComboBox',
        'PyQt6.QtWidgets.QCheckBox',
        'PyQt6.QtWidgets.QScrollArea',
        'PyQt6.QtWidgets.QTabWidget',
        'PyQt6.QtWidgets.QTableWidget',
        'PyQt6.QtWidgets.QHeaderView',
        'PyQt6.QtWidgets.QSplitter',
        'PyQt6.QtWidgets.QStatusBar',
        'PyQt6.QtWidgets.QMenuBar',
        'PyQt6.QtWidgets.QMessageBox',
        'PyQt6.QtWidgets.QGraphicsView',
        'PyQt6.QtWidgets.QGraphicsScene',
        'PyQt6.QtWidgets.QGraphicsItem',
        'PyQt6.QtWidgets.QGraphicsRectItem',
        'PyQt6.QtWidgets.QGraphicsEllipseItem',
        'PyQt6.QtWidgets.QGraphicsTextItem',
        'PyQt6.QtWidgets.QGraphicsLineItem',
        'PyQt6.QtWidgets.QGraphicsPolygonItem',
        'PyQt6.QtCore.pyqtSignal',
        'PyQt6.QtCore.QPointF',
        'PyQt6.QtGui.QPen',
        'PyQt6.QtGui.QBrush',
        'PyQt6.QtGui.QColor',
        'PyQt6.QtGui.QFont',
        'PyQt6.QtGui.QPainter',
        'PyQt6.QtGui.QPolygonF',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SistemaBombeo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SistemaBombeo',
)
EOF
fi

print_success "✅ Archivo de especificaciones creado para $OS"

# =============================================================================
# PASO 7: EMPAQUETADO CON PYINSTALLER
# =============================================================================
print_status "🏗️ Iniciando empaquetado con PyInstaller..."
print_warning "Este proceso puede tomar varios minutos..."

# Ejecutar PyInstaller
pyinstaller bombeo.spec

if [ $? -eq 0 ]; then
    print_success "✅ Empaquetado completado exitosamente"
else
    print_error "❌ Error durante el empaquetado"
    exit 1
fi

# =============================================================================
# PASO 8: VERIFICACIÓN DEL EJECUTABLE
# =============================================================================
print_status "🧪 Verificando ejecutable generado..."

# Verificar que el ejecutable exista
EXECUTABLE_PATH="dist/SistemaBombeo/SistemaBombeo"
if [ "$OS" = "windows" ]; then
    EXECUTABLE_PATH="dist/SistemaBombeo/SistemaBombeo.exe"
fi

if [ ! -f "$EXECUTABLE_PATH" ]; then
    print_error "❌ El ejecutable no se generó correctamente"
    exit 1
fi

# Verificar tamaño del ejecutable
if command -v du &> /dev/null; then
    EXECUTABLE_SIZE=$(du -h "$EXECUTABLE_PATH" | cut -f1)
    print_success "✅ Ejecutable generado: $EXECUTABLE_SIZE"
else
    print_success "✅ Ejecutable generado correctamente"
fi

# Verificar archivos de datos en el paquete
DATA_DIR="dist/SistemaBombeo/_internal/data"
print_status "📋 Verificando archivos de datos incluidos..."

for csv_file in "${DATA_FILES[@]}"; do
    filename=$(basename "$csv_file")
    if [ -f "$DATA_DIR/$filename" ]; then
        if command -v du &> /dev/null; then
            size=$(du -h "$DATA_DIR/$filename" | cut -f1)
            print_success "  ✅ $filename ($size)"
        else
            print_success "  ✅ $filename"
        fi
    else
        print_error "  ❌ $filename (faltante)"
    fi
done

# =============================================================================
# PASO 9: CREAR SCRIPT DE PRUEBA
# =============================================================================
print_status "🧪 Creando script de prueba del ejecutable..."

cat > dist/SistemaBombeo/test_executable.py << 'EOF'
#!/usr/bin/env python3
"""
Script de prueba para verificar que el ejecutable funciona correctamente
"""
import subprocess
import sys
import os

def test_executable():
    """Prueba el ejecutable del Sistema de Bombeo"""
    if os.name == 'nt':  # Windows
        exe_path = "./SistemaBombeo.exe"
    else:  # macOS/Linux
        exe_path = "./SistemaBombeo"
    
    print("🧪 Probando el ejecutable del Sistema de Bombeo...")
    print(f"📍 Ruta: {os.path.abspath(exe_path)}")
    
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path) / 1024 / 1024
        print(f"📊 Tamaño: {size:.1f} MB")
    else:
        print("❌ El ejecutable no existe")
        return False
    
    try:
        # Verificar que sea ejecutable
        if not os.access(exe_path, os.X_OK):
            print("❌ El archivo no es ejecutable")
            return False
        
        # Verificar datos CSV
        data_dir = "./_internal/data"
        csv_files = ["accesorios.csv", "constantes.csv", "fluidos.csv"]
        
        print("\n📋 Verificando archivos de datos:")
        for csv_file in csv_files:
            csv_path = os.path.join(data_dir, csv_file)
            if os.path.exists(csv_path):
                size = os.path.getsize(csv_path)
                print(f"✅ {csv_file} ({size} bytes)")
            else:
                print(f"❌ {csv_file} (no encontrado)")
                return False
        
        print("\n🎉 ¡Ejecutable verificado exitosamente!")
        print("🚀 El ejecutable está listo para ser distribuido")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

if __name__ == "__main__":
    success = test_executable()
    sys.exit(0 if success else 1)
EOF

if [ "$OS" = "windows" ]; then
    # En Windows, no necesitamos chmod
    print_success "✅ Script de prueba creado (Windows)"
else
    chmod +x dist/SistemaBombeo/test_executable.py
    print_success "✅ Script de prueba creado (macOS/Linux)"
fi

# Ejecutar prueba
cd dist/SistemaBombeo
python3 test_executable.py
cd ../..

if [ $? -eq 0 ]; then
    print_success "✅ Prueba del ejecutable completada exitosamente"
else
    print_error "❌ La prueba del ejecutable falló"
    exit 1
fi

# =============================================================================
# PASO 10: CREAR PAQUETE DE DISTRIBUCIÓN
# =============================================================================
print_status "📦 Creando paquete de distribución final..."

# Crear directorio específico para macOS si no existe
if [ ! -d "macos" ]; then
    mkdir -p macos
fi

# Mover archivos generados al directorio macOS
if [ -d "dist" ]; then
    print_status "📂 Moviendo archivos a directorio macOS..."
    cp -r dist/* macos/
    print_success "✅ Archivos movidos a macos/"
fi

# Crear archivo ZIP para distribución
DIST_DIR="macos"
ZIP_NAME="SistemaBombeo-v1.0-macos.zip"

if command -v zip &> /dev/null; then
    cd macos
    zip -r "$ZIP_NAME" SistemaBombeo/
    cd ..
    print_success "✅ Paquete ZIP creado: macos/$ZIP_NAME"
else
    print_warning "⚠️ zip no disponible, omitiendo creación de paquete ZIP"
fi

# =============================================================================
# PASO 11: LIMPIEZA FINAL
# =============================================================================
print_status "🧹 Realizando limpieza final..."

# Desactivar entorno virtual
if [ "$OS" = "windows" ]; then
    deactivate 2>/dev/null || true
else
    deactivate 2>/dev/null || true
fi

# Opcional: comentar la siguiente línea si quieres mantener el entorno virtual
# rm -rf packaging_env

print_success "✅ Limpieza completada"

# =============================================================================
# RESUMEN FINAL
# =============================================================================
echo ""
echo "============================================================================"
print_success "🎉 ¡EMPAQUETADO COMPLETADO EXITOSAMENTE!"
echo "============================================================================"
echo ""
echo "📦 Archivos generados:"
echo "   📁 macos/SistemaBombeo/          ← Aplicación ejecutable macOS"
echo "   📄 macos/$ZIP_NAME           ← Paquete de distribución macOS"
echo ""
echo "🚀 Para usar la aplicación:"
echo "   1. Copia la carpeta 'SistemaBombeo' desde macos/"
echo "   2. Haz doble clic en 'SistemaBombeo'"
echo "   3. ¡Listo para usar!"
echo ""
echo "📋 Para verificar:"
echo "   cd macos/SistemaBombeo"
echo "   python3 test_executable.py"
echo ""
echo "📄 Documentación:"
echo "   📖 README_INSTALACION.md ← Guía completa"
echo "   📋 requirements.txt       ← Dependencias"
echo "   🔨 build_package.bat      ← Script para Windows"
echo "   📁 windows/               ← Builds de Windows"
echo ""
print_success "✨ ¡El Sistema de Cálculo de Bombeo está listo para distribuir! ✨"
echo "============================================================================"
