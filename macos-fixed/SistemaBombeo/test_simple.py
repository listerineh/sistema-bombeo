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

