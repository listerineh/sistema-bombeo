#!/bin/bash

# =============================================================================
# Build para macOS Sequoia - Solución para Python Shared Library Error
# =============================================================================

set -e

echo "🍎 Build para macOS Sequoia - Solución Python Shared Library"

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf build dist packaging_env

# Crear entorno virtual
echo "🐍 Creando entorno virtual..."
python3 -m venv packaging_env
source packaging_env/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install PyQt6==6.10.2
pip install PyInstaller==6.18.0

# Configurar variables de entorno para macOS Sequoia
echo "🔧 Configurando para macOS Sequoia..."
export PYTHONNOUSERSITE=1
export MACOSX_DEPLOYMENT_TARGET=10.14

# Build con opciones específicas para macOS Sequoia
echo "🏗️ Construyendo ejecutable..."
pyinstaller \
    --onedir \
    --windowed \
    --add-data "src/data:data" \
    --name=SistemaBombeo \
    --noupx \
    --noconfirm \
    --strip \
    main.py

# Verificar build
echo "🧪 Verificando ejecutable..."
if [ -d "dist/SistemaBombeo" ]; then
    echo "✅ Build completado exitosamente"
    echo "📁 Ubicación: dist/SistemaBombeo/"
    echo "🚀 Para ejecutar: open dist/SistemaBombeo/SistemaBombeo.app"
else
    echo "❌ Error en el build"
    exit 1
fi

# Crear paquete de distribución
echo "📦 Creando paquete de distribución..."
mkdir -p macos-sequoia
cp -r dist/SistemaBombeo macos-sequoia/
cd macos-sequoia
zip -r ../SistemaBombeo-v1.0-macos-sequoia.zip *
cd ..

echo "✅ Paquete creado: SistemaBombeo-v1.0-macos-sequoia.zip"

# Limpiar entorno virtual
echo "🧹 Limpiando entorno virtual..."
deactivate
rm -rf packaging_env

echo "🎉 Build completado para macOS Sequoia!"
echo "📦 Ejecutable en: macos-sequoia/SistemaBombeo/"
echo "📦 Paquete ZIP: SistemaBombeo-v1.0-macos-sequoia.zip"
