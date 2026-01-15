@echo off
setlocal enabledelayedexpansion

:: =============================================================================
:: Sistema de Cálculo de Bombeo - Script de Empaquetado Automático para Windows
:: =============================================================================
:: Este script automatiza todo el proceso de empaquetado siguiendo los pasos
:: que se realizaron manualmente durante el desarrollo.
::
:: Compatible con: Windows 10/11
:: Para macOS/Linux: usar build_package.sh
::
:: Uso: build_package.bat
:: =============================================================================

set "RED=[31m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "BLUE=[34m"
set "NC=[0m"

:: Función para imprimir mensajes coloreados
:print_status
echo %BLUE%[INFO]%NC% %~1
goto :eof

:print_success
echo %GREEN%[SUCCESS]%NC% %~1
goto :eof

:print_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:print_error
echo %RED%[ERROR]%NC% %~1
goto :eof

:: =============================================================================
:: LIMPIEZA INICIAL - Eliminar paquetes anteriores
:: =============================================================================
call :print_status "🧹 Limpiando paquetes anteriores para empaquetar desde cero..."

:: Eliminar entorno virtual anterior si existe
if exist "packaging_env" (
    call :print_warning "Eliminando entorno virtual anterior..."
    rmdir /s /q "packaging_env"
)

:: Eliminar directorios de build anteriores
if exist "build" (
    call :print_warning "Eliminando directorio build anterior..."
    rmdir /s /q "build"
)

if exist "dist" (
    call :print_warning "Eliminando directorio dist anterior..."
    rmdir /s /q "dist"
)

call :print_success "✅ Limpieza completada - Listo para empaquetar desde cero"

:: =============================================================================
:: PASO 1: VERIFICACIÓN PREVIA
:: =============================================================================
call :print_status "🔍 Verificando entorno de empaquetado..."

:: Verificar que estamos en el directorio correcto
if not exist "main.py" (
    call :print_error "No se encuentra main.py. Asegúrate de estar en el directorio raíz del proyecto."
    exit /b 1
)

:: Verificar archivos de datos
set "DATA_FILES=src\data\accesorios.csv src\data\constantes.csv src\data\fluidos.csv"
for %%f in (%DATA_FILES%) do (
    if not exist "%%f" (
        call :print_error "Archivo de datos faltante: %%f"
        exit /b 1
    )
)

call :print_success "✅ Todos los archivos necesarios encontrados"

:: =============================================================================
:: PASO 2: LIMPIEZA DE ENTORNOS ANTERIORES (redundante pero seguro)
:: =============================================================================
call :print_status "🧹 Verificando limpieza completa..."

:: Verificación adicional de que no queden residuos
if exist "packaging_env" (
    call :print_warning "Eliminando residuos de entorno virtual..."
    rmdir /s /q "packaging_env" 2>nul
)

if exist "build" (
    call :print_warning "Eliminando residuos de build..."
    rmdir /s /q "build" 2>nul
)

if exist "dist" (
    call :print_warning "Eliminando residuos de dist..."
    rmdir /s /q "dist" 2>nul
)

:: Eliminar builds específicos de plataforma
if exist "windows" (
    call :print_warning "Eliminando builds Windows anteriores..."
    rmdir /s /q "windows" 2>nul
)

call :print_success "✅ Verificación de limpieza completada"

:: =============================================================================
:: PASO 3: CREACIÓN DE ENTORNO VIRTUAL
:: =============================================================================
call :print_status "🐍 Creando entorno virtual para empaquetado..."

python -m venv packaging_env
call packaging_env\Scripts\activate

call :print_success "✅ Entorno virtual creado y activado"

:: =============================================================================
:: PASO 4: INSTALACIÓN DE DEPENDENCIAS
:: =============================================================================
call :print_status "📦 Instalando dependencias..."

:: Actualizar pip
python -m pip install --upgrade pip

:: Instalar dependencias desde requirements.txt
if exist "requirements.txt" (
    pip install -r requirements.txt
    call :print_success "✅ Dependencias instaladas desde requirements.txt"
) else (
    :: Instalar dependencias manualmente si no existe requirements.txt
    pip install PyQt6==6.10.2
    pip install PyInstaller==6.18.0
    call :print_success "✅ Dependencias instaladas manualmente"
)

:: =============================================================================
:: PASO 5: VERIFICACIÓN DE RUTAS DE DATOS
:: =============================================================================
call :print_status "🔧 Verificando configuración de rutas de datos..."

:: Crear script de prueba para verificar rutas
(
echo import os
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
) > test_data_paths.py

python test_data_paths.py
del test_data_paths.py

call :print_success "✅ Configuración de rutas verificada"

:: =============================================================================
:: PASO 6: CREACIÓN DE ARCHIVO DE ESPECIFICACIONES
:: =============================================================================
call :print_status "📄 Creando archivo de especificaciones PyInstaller..."

:: Crear archivo .spec para Windows
(
echo # -*- mode: python ; coding: utf-8 -*-

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
) > bombeo.spec

call :print_success "✅ Archivo de especificaciones creado para Windows"

:: =============================================================================
:: PASO 7: EMPAQUETADO CON PYINSTALLER
:: =============================================================================
call :print_status "🏗️ Iniciando empaquetado con PyInstaller..."
call :print_warning "Este proceso puede tomar varios minutos..."

:: Ejecutar PyInstaller
pyinstaller bombeo.spec

if %errorlevel% neq 0 (
    call :print_error "❌ Error durante el empaquetado"
    exit /b 1
)

call :print_success "✅ Empaquetado completado exitosamente"

:: =============================================================================
:: PASO 8: VERIFICACIÓN DEL EJECUTABLE
:: =============================================================================
call :print_status "🧪 Verificando ejecutable generado..."

:: Verificar que el ejecutable exista
set "EXECUTABLE_PATH=dist\SistemaBombeo\SistemaBombeo.exe"

if not exist "%EXECUTABLE_PATH%" (
    call :print_error "❌ El ejecutable no se generó correctamente"
    exit /b 1
)

:: Verificar tamaño del ejecutable
for %%F in ("%EXECUTABLE_PATH%") do set "size=%%~zF"
call :print_success "✅ Ejecutable generado: %size% bytes"

:: Verificar archivos de datos en el paquete
set "DATA_DIR=dist\SistemaBombeo\_internal\data"
call :print_status "📋 Verificando archivos de datos incluidos..."

for %%f in (%DATA_FILES%) do (
    set "filename=%%~nxf"
    if exist "%DATA_DIR%\%%filename%" (
        for %%F in ("%DATA_DIR%\%%filename%") do set "size=%%~zF"
        call :print_success "  ✅ %%filename% (%size% bytes)"
    ) else (
        call :print_error "  ❌ %%filename% (faltante)"
    )
)

:: =============================================================================
:: PASO 9: CREAR SCRIPT DE PRUEBA
:: =============================================================================
call :print_status "🧪 Creando script de prueba del ejecutable..."

(
echo #!/usr/bin/env python3
"""
Script de prueba para verificar que el ejecutable funciona correctamente
"""
import subprocess
import sys
import os

def test_executable():
    """Prueba el ejecutable del Sistema de Bombeo"""
    exe_path = "./SistemaBombeo.exe"
    
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
) > dist\SistemaBombeo\test_executable.py

call :print_success "✅ Script de prueba creado (Windows)"

:: Ejecutar prueba
cd dist\SistemaBombeo
python test_executable.py
cd ..\..

if %errorlevel% neq 0 (
    call :print_error "❌ La prueba del ejecutable falló"
    exit /b 1
)

call :print_success "✅ Prueba del ejecutable completada exitosamente"

:: =============================================================================
:: PASO 10: CREAR PAQUETE DE DISTRIBUCIÓN
:: =============================================================================
call :print_status "📦 Creando paquete de distribución final..."

:: Crear directorio específico para Windows si no existe
if not exist "windows" (
    mkdir windows
)

:: Mover archivos generados al directorio Windows
if exist "dist" (
    call :print_status "📂 Moviendo archivos a directorio Windows..."
    xcopy /E /I dist\* windows\
    call :print_success "✅ Archivos movidos a windows\"
)

:: Crear archivo ZIP para distribución
set "DIST_DIR=windows"
set "ZIP_NAME=SistemaBombeo-v1.0-Windows.zip"

where zip >nul 2>&1
if %errorlevel% equ 0 (
    cd windows
    zip -r "%ZIP_NAME%" SistemaBombeo\
    cd ..
    call :print_success "✅ Paquete ZIP creado: windows\%ZIP_NAME%"
) else (
    call :print_warning "⚠️ zip no disponible, omitiendo creación de paquete ZIP"
)

:: =============================================================================
:: PASO 11: LIMPIEZA FINAL
:: =============================================================================
call :print_status "🧹 Realizando limpieza final..."

:: Desactivar entorno virtual
call deactivate 2>nul

:: Opcional: comentar la siguiente línea si quieres mantener el entorno virtual
:: rmdir /s /q packaging_env

call :print_success "✅ Limpieza completada"

:: =============================================================================
:: RESUMEN FINAL
:: =============================================================================
echo.
echo ==============================================================================
call :print_success "🎉 ¡EMPAQUETADO COMPLETADO EXITOSAMENTE!"
echo ==============================================================================
echo.
echo 📦 Archivos generados:
echo    📁 windows\SistemaBombeo\          ← Aplicación ejecutable Windows
echo    📄 windows\%ZIP_NAME%           ← Paquete de distribución Windows
echo.
echo 🚀 Para usar la aplicación:
echo    1. Copia la carpeta 'SistemaBombeo' desde windows\
echo    2. Haz doble clic en 'SistemaBombeo.exe'
echo    3. ¡Listo para usar!
echo.
echo 📋 Para verificar:
echo    cd windows\SistemaBombeo
echo    python test_executable.py
echo.
echo 📄 Documentación:
echo    📖 README_INSTALACION.md ← Guía completa
echo    📋 requirements.txt       ← Dependencias
echo    🔨 build_package.sh        ← Script para macOS/Linux
echo    📁 macos/                 ← Builds de macOS
echo.
call :print_success "✨ ¡El Sistema de Cálculo de Bombeo está listo para distribuir! ✨"
echo ==============================================================================
echo.
pause
