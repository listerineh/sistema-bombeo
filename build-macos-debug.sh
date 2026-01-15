#!/bin/bash

# =============================================================================
# Build macOS Debug - Solución para Segmentation Fault
# =============================================================================

set -e

echo "🍎 Build macOS Debug - Solución para Segmentation Fault"

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

# Build con opciones mínimas para evitar segfault
echo "🏗️ Construyendo ejecutable (modo debug)..."
pyinstaller \
    --onedir \
    --windowed \
    --add-data "src/data:data" \
    --name=SistemaBombeo \
    --noupx \
    --noconfirm \
    --debug all \
    --strip \
    main.py

# Verificar build
echo "🧪 Verificando ejecutable..."
if [ -d "dist/SistemaBombeo" ]; then
    echo "✅ Build completado exitosamente"
    echo "📁 Ubicación: dist/SistemaBombeo/"
    
    # Verificar que sea ejecutable
    if [ -x "dist/SistemaBombeo/SistemaBombeo" ]; then
        echo "✅ Ejecutable es ejecutable"
    else
        echo "❌ Ejecutable no es ejecutable"
        exit 1
    fi
    
    # Verificar datos
    if [ -d "dist/SistemaBombeo/_internal/data" ]; then
        echo "✅ Directorio de datos encontrado"
        ls -la dist/SistemaBombeo/_internal/data/
    else
        echo "❌ Directorio de datos no encontrado"
        exit 1
    fi
else
    echo "❌ Error en el build"
    exit 1
fi

# Test básico del ejecutable
echo "🧪 Test básico del ejecutable..."
cd dist/SistemaBombeo

# Test 1: Verificar que no se bloquee inmediatamente
echo "📋 Test 1: Verificación inicial..."
timeout 5s ./SistemaBombeo --help 2>/dev/null || echo "⚠️ El ejecutable se cierra inmediatamente"

# Test 2: Verificar librerías
echo "📋 Test 2: Verificación de librerías..."
otool -L ./SistemaBombeo | head -10

# Test 3: Verificar dependencias
echo "📋 Test 3: Verificación de dependencias..."
dyld_info ./SistemaBombeo | grep -E "(Qt|Python)" | head -5

cd ..

echo "🎉 Build debug completado!"
echo "📦 Ejecutable en: dist/SistemaBombeo/"
echo "🔍 Logs guardados en build/SistemaBombeo/warn-SistemaBombeo.txt"

# Limpiar entorno virtual
echo "🧹 Limpiando entorno virtual..."
deactivate
rm -rf packaging_env

echo "📋 Para probar manualmente:"
echo "   cd dist/SistemaBombeo"
echo "   ./SistemaBombeo"
echo ""
echo "📋 Si hay segfault, revisar logs:"
echo "   cat build/SistemaBombeo/warn-SistemaBombeo.txt"
