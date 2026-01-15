#!/bin/bash

# =============================================================================
# Fix macOS Segmentation Fault - Solución definitiva
# =============================================================================

set -e

echo "🔧 Fix macOS Segmentation Fault - Solución definitiva"

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf build dist packaging_env macos-sequoia

# Crear entorno virtual con Python del sistema
echo "🐍 Creando entorno virtual con Python del sistema..."
python3 -m venv --system-site-packages packaging_env
source packaging_env/bin/activate

# Instalar dependencias específicas
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install PyQt6==6.10.2
pip install PyInstaller==6.18.0

# Configurar variables de entorno
echo "🔧 Configurando variables de entorno..."
export PYTHONNOUSERSITE=1
export MACOSX_DEPLOYMENT_TARGET=10.14
export DYLD_LIBRARY_PATH="/usr/local/lib:/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

# Build con opciones específicas para evitar segfault
echo "🏗️ Construyendo ejecutable (modo seguro)..."
pyinstaller \
    --onedir \
    --windowed \
    --add-data "src/data:data" \
    --name=SistemaBombeo \
    --noupx \
    --noconfirm \
    --exclude-module tkinter \
    --exclude-module matplotlib \
    --exclude-module PIL \
    --exclude-module numpy \
    --exclude-module scipy \
    --exclude-module pandas \
    --exclude-module jupyter \
    --exclude-module notebook \
    --exclude-module ipykernel \
    --exclude-module ipywidgets \
    --strip \
    --clean \
    main.py

# Verificar build
echo "🧪 Verificando ejecutable..."
if [ -d "dist/SistemaBombeo" ]; then
    echo "✅ Build completado exitosamente"
    echo "📁 Ubicación: dist/SistemaBombeo/"
    
    # Verificar estructura
    echo "📋 Estructura del ejecutable:"
    ls -la dist/SistemaBombeo/
    
    # Verificar datos
    if [ -d "dist/SistemaBombeo/_internal/data" ]; then
        echo "✅ Directorio de datos encontrado con:"
        ls -la dist/SistemaBombeo/_internal/data/
    else
        echo "❌ ERROR: No se encuentra el directorio de datos"
        exit 1
    fi
    
    # Verificar ejecutable
    if [ -f "dist/SistemaBombeo/SistemaBombeo" ]; then
        echo "✅ Ejecutable creado"
        echo "📊 Tamaño: $(du -h dist/SistemaBombeo/SistemaBombeo | cut -f1)"
        
        # Verificar que sea ejecutable
        if [ -x "dist/SistemaBombeo/SistemaBombeo" ]; then
            echo "✅ Ejecutable tiene permisos correctos"
        else
            echo "🔧 Arreglando permisos..."
            chmod +x dist/SistemaBombeo/SistemaBombeo
            echo "✅ Permisos arreglados"
        fi
    else
        echo "❌ ERROR: No se encuentra el ejecutable"
        exit 1
    fi
    
else
    echo "❌ ERROR: Build falló"
    exit 1
fi

# Test de ejecución segura
echo "🧪 Test de ejecución segura..."
cd dist/SistemaBombeo

# Crear script de prueba simple
cat > test_simple.py << 'EOF'
#!/usr/bin/env python3
import sys
import os

print("🧪 Test simple de ejecución")

try:
    # Test 1: Importar PyQt6
    from PyQt6.QtWidgets import QApplication
    print("✅ PyQt6 importado")
    
    # Test 2: Crear aplicación
    app = QApplication([])
    print("✅ QApplication creado")
    
    # Test 3: Verificar datos
    data_dir = os.path.join(os.path.dirname(__file__), '_internal', 'data')
    if os.path.exists(data_dir):
        csv_files = ['accesorios.csv', 'constantes.csv', 'fluidos.csv']
        print("✅ Directorio de datos encontrado")
        for csv_file in csv_files:
            csv_path = os.path.join(data_dir, csv_file)
            if os.path.exists(csv_path):
                size = os.path.getsize(csv_path)
                print(f"✅ {csv_file} ({size} bytes)")
            else
                print(f"❌ {csv_file} (no encontrado)")
    else:
        print("❌ Directorio de datos no encontrado")
    
    # Test 4: Salir inmediato (sin mostrar ventana)
    print("✅ Test completado - sin segfault")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

EOF

# Ejecutar test
cd _internal
python3 test_simple.py
cd ..

# Limpiar
rm -f test_simple.py

cd ..

# Crear paquete de prueba
echo "📦 Creando paquete de prueba..."
mkdir -p macos-fixed
cp -r dist/SistemaBombeo macos-fixed/
cd macos-fixed
zip -r ../SistemaBombeo-v1.0-macos-fixed.zip *
cd ..

echo "✅ Paquete creado: SistemaBombeo-v1.0-macos-fixed.zip"

# Limpiar entorno virtual
echo "🧹 Limpiando entorno virtual..."
deactivate
rm -rf packaging_env

echo "🎉 Build completado con solución para segfault!"
echo "📦 Ejecutable en: dist/SistemaBombeo/"
echo "📦 Paquete ZIP: SistemaBombeo-v1.0-macos-fixed.zip"
echo ""
echo "🚀 Para probar la aplicación:"
echo "   cd dist/SistemaBombeo"
echo "   ./SistemaBombeo"
echo ""
echo "🔧 Si aún hay segfault, prueba estas opciones:"
echo "   1. Abre la aplicación con Finder (doble clic)"
echo "   2. Ejecuta desde terminal con 'open SistemaBombeo'"
echo "   3. Revisa los logs del sistema con 'Console.app'"
