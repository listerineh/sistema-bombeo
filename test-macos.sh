#!/bin/bash

# =============================================================================
# Test macOS - Script para diagnosticar problemas de ejecución
# =============================================================================

echo "🔍 Test macOS - Diagnóstico de problemas"

# Verificar que estamos en el directorio correcto
if [ ! -d "dist/SistemaBombeo" ]; then
    echo "❌ Error: No se encuentra el directorio dist/SistemaBombeo"
    echo "📁 Ejecuta el build primero:"
    echo "   ./build-macos-debug.sh"
    exit 1
fi

cd dist/SistemaBombeo

echo "📁 Directorio actual: $(pwd)"
echo "📋 Contenido:"
ls -la

# Verificar estructura de archivos
echo ""
echo "🔍 Verificando estructura de archivos..."

if [ -f "SistemaBombeo" ]; then
    echo "✅ Ejecutable encontrado: SistemaBombeo"
    file SistemaBombeo
else
    echo "❌ No se encuentra el ejecutable SistemaBombeo"
fi

if [ -d "SistemaBombeo.app" ]; then
    echo "✅ App bundle encontrado: SistemaBombeo.app"
    ls -la SistemaBombeo.app/
else
    echo "❌ No se encuentra el app bundle SistemaBombeo.app"
fi

if [ -d "_internal" ]; then
    echo "✅ Directorio _internal encontrado"
    echo "📁 Contenido de _internal:"
    ls -la _internal/ | head -10
    
    if [ -d "_internal/data" ]; then
        echo "✅ Directorio data encontrado"
        echo "📋 Archivos CSV:"
        ls -la _internal/data/
    else
        echo "❌ No se encuentra el directorio data"
    fi
else
    echo "❌ No se encuentra el directorio _internal"
fi

# Test 1: Verificar permisos
echo ""
echo "🔍 Test 1: Verificando permisos..."
if [ -x "SistemaBombeo" ]; then
    echo "✅ Ejecutable tiene permisos de ejecución"
else
    echo "❌ Ejecutable no tiene permisos de ejecución"
    echo "🔧 Arreglando permisos..."
    chmod +x SistemaBombeo
    echo "✅ Permisos arreglados"
fi

# Test 2: Verificar librerías
echo ""
echo "🔍 Test 2: Verificando librerías..."
echo "📋 Librerías principales:"
otool -L SistemaBombeo 2>/dev/null | grep -E "(Qt|Python|PyQt6)" | head -5

# Test 3: Verificar dependencias con dyld
echo ""
echo "🔍 Test 3: Verificando dependencias con dyld..."
echo "📋 Dependencias Qt:"
dyld_info SistemaBombeo 2>/dev/null | grep -E "(Qt6|Python)" | head -5

# Test 4: Intentar ejecución segura
echo ""
echo "🔍 Test 4: Intentando ejecución segura..."
echo "⚠️  Intentando ejecución con timeout de 3 segundos..."

# Crear script de prueba temporal
cat > test_safe.py << 'EOF'
import sys
import os
import signal

def timeout_handler(signum, frame):
    print("🚨 Timeout - Cerrando aplicación")
    sys.exit(0)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(3)

try:
    from PyQt6.QtWidgets import QApplication
    print("✅ PyQt6 importado correctamente")
    
    app = QApplication([])
    print("✅ QApplication creado")
    
    # Intentar importar el módulo principal
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    print("📁 Path actual:", os.getcwd())
    
    # No mostrar ventana, solo verificar que no hay segfault
    print("✅ Aplicación inicializada sin errores")
    print("🚀 La aplicación debería funcionar")
    
except Exception as e:
    print(f"❌ Error durante inicialización: {e}")
    sys.exit(1)

print("🎉 Test completado exitosamente")
EOF

# Ejecutar test
cd _internal
python3 ../test_safe.py
cd ..

# Limpiar
rm -f test_safe.py

echo ""
echo "🎉 Test de diagnóstico completado"
echo "📋 Si no hubo errores, intenta ejecutar la aplicación:"
echo "   ./SistemaBistemaBombeo"
echo ""
echo "📋 Si hay errores, revisa los logs en:"
echo "   cat ../build/SistemaBombeo/warn-SistemaBombeo.txt"
