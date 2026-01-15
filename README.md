<div align="center">

# 🚀 Sistema de Cálculo de Bombeo

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.10.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

*Aplicación de escritorio para calcular parámetros de bombeo en sistemas de tuberías sin lecho poroso*

Desarrollado con ❤️ para Nayehi

</div>

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 📋 Tabla de Contenidos

- [🎯 Características Principales](#-características-principales)
- [🔧 Requisitos del Sistema](#-requisitos-del-sistema)
- [🚀 Instalación Rápida](#-instalación-rápida)
- [📖 Guía de Uso](#-guía-de-uso)
- [🏗️ Construcción y Empaquetado](#-construcción-y-empaquetado)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🧮 Cálculos Realizados](#-cálculos-realizados)
- [🎨 Características de la Interfaz](#-características-de-la-interfaz)
- [🔍 Solución de Problemas](#-solución-de-problemas)
- [📄 Licencia](#-licencia)

## 🎯 Características Principales

### 🧮 **Cálculos Hidráulicos Precisos**

- **Número de Reynolds**: Determina el régimen de flujo
- **Factor de Fricción**: Calculado según el número de Reynolds
- **Velocidad del Fluido**: Basada en caudal y diámetro de tubería
- **Pérdidas de Energía**: Mayores (fricción) y menores (accesorios)
- **Carga Total de Bomba (Ht)**: Altura manométrica total requerida
- **Potencia Requerida**: Hidráulica y potencia de bomba
- **NPSH Disponible**: Verificación contra cavitación

### 🎨 **Interfaz Gráfica Moderna**

- **Tema Oscuro Profesional**: Reducción de fatiga visual
- **Visualización Interactiva**: Diagrama esquemático del sistema
- **Zoom y Navegación**: Controles para explorar el diagrama
- **Leyenda Completa**: Símbolos y descripciones detalladas
- **Resultados Organizados**: Principales y detallados en pestañas

### 📊 **Visualización del Sistema**

- **Diagrama Esquemático**: Representación visual del sistema
- **Tanques de Entrada/Salida**: Con elevaciones etiquetadas
- **Tuberías**: Con longitudes y orientaciones correctas
- **Accesorios**: Codos, válvulas, tees con ubicación inteligente
- **Líneas de Elevación**: Diferencia de altura visual
- **Referencia de Elevación 0**: Línea base para mediciones

### 🔧 **Configuración Flexible**

- **Fluidos Predefinidos**: Agua, aceites, etc. con propiedades reales
- **Múltiples Tramos**: Configuración de sistemas complejos
- **Accesorios Variados**: Codos, válvulas, tees con factores K
- **Puntos del Sistema**: Elevaciones y presiones personalizadas
- **Unidades Consistentes**: Sistema métrico decimal

## 🔧 Requisitos del Sistema

### Mínimos Requeridos

- **Sistema Operativo**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Memoria RAM**: 4 GB mínimo
- **Espacio en Disco**: 100 MB disponibles
- **Procesador**: Multi-core recomendado
- **Pantalla**: 1280x720 resolución mínima

### Para Desarrollo

- **Python**: 3.8+ con pip
- **Git**: Para clonar el repositorio
- **Editor de Código**: VS Code, PyCharm, etc.

## 🚀 Instalación Rápida

### Opción 1: Ejecutable Independiente (Recomendado)

1. **Descargar** el paquete para tu plataforma:
   - Windows: `SistemaBombeo-v1.0-Windows.zip`
   - macOS: `SistemaBombeo-v1.0-macos.zip`
   - Linux: `SistemaBombeo-v1.0-Linux.zip`

2. **Descomprimir** el archivo ZIP

3. **Ejecutar** la aplicación:
   - Windows: Doble clic en `SistemaBombeo.exe`
   - macOS/Linux: Doble clic en `SistemaBombeo`

4. **¡Listo para usar!** 🎉

### Opción 2: Desde Código Fuente

```bash
# 1. Clonar el repositorio
git clone <repositorio-url>
cd proyecto-nay

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python main.py
```

## 📖 Guía de Uso

### 🎯 **Paso 1: Configurar el Sistema**

1. **Seleccionar Fluido**: Elige de la lista desplegable
2. **Ingresar Caudal**: En L/s (litros por segundo)
3. **Configurar Eficiencia**: Eficiencia de la bomba (decimal)
4. **Definir Puntos**:
   - Punto 1: Elevación y presión de succión
   - Punto 2: Elevación y presión de descarga

### 🔧 **Paso 2: Agregar Tramos de Tubería**

Para cada tramo:

1. **Longitud**: En metros
2. **Diámetro**: En metros
3. **Orientación**: Horizontal o Vertical
4. **Material**: Rugosidad del material
5. **Agregar** tramos según necesites

### 📦 **Paso 3: Configurar Accesorios**

Selecciona los accesorios y sus cantidades:

- **Entrada de Tanque**: Conexión inicial
- **Codos**: Cambios de dirección (45°, 90°)
- **Válvulas**: Control de flujo
- **Tees**: Divisiones de flujo
- **Salida de Tanque**: Conexión final

### ⚡ **Paso 4: Calcular Sistema**

1. **Revisar Configuración**: Verifica todos los datos
2. **Hacer Clic en "Calcular Sistema"**
3. **Ver Resultados**: En pestaña de resultados
4. **Explorar Visualización**: En pestaña de visualización

### 📊 **Interpretación de Resultados**

#### Resultados Principales

- **Ht (m)**: Carga total que debe vencer la bomba
- **NPSHa (m)**: Altura de succión neta disponible
- **Potencia (kW)**: Potencia requerida del motor
- **Velocidad (m/s)**: Velocidad del fluido en tuberías
- **Re**: Número de Reynolds (régimen de flujo)
- **f**: Factor de fricción

#### Resultados Detallados

- **Altura de Elevación**: Diferencia de altura entre puntos
- **Pérdidas Mayores**: Por fricción en tuberías
- **Pérdidas Menores**: Por accesorios
- **Potencia Hidráulica**: Potencia teórica del fluido

## 🏗️ Construcción y Empaquetado

### 📦 **Scripts Automatizados**

El proyecto incluye scripts para construir ejecutables independientes:

#### macOS/Linux

```bash
./build_package.sh
```

#### Windows

```cmd
build_package.bat
```

### 🔧 **Proceso de Construcción**

1. **Limpieza**: Elimina builds anteriores
2. **Entorno Virtual**: Crea entorno aislado
3. **Dependencias**: Instala PyQt6 y PyInstaller
4. **Empaquetado**: Genera ejecutable con PyInstaller
5. **Verificación**: Prueba el ejecutable generado
6. **Distribución**: Crea paquete ZIP

### 📋 **Archivos Generados**

```
dist/
└── SistemaBombeo/
    ├── SistemaBombeo(.exe) ← Ejecutable principal
    ├── _internal/
    │   ├── data/ ← Archivos CSV de ingeniería
    │   ├── PyQt6/ ← Framework GUI
    │   └── python3.13/ ← Runtime
    └── test_executable.py ← Script de verificación
```

## 📁 Estructura del Proyecto

```
proyecto-nay/
├── src/                          ← Código fuente
│   ├── gui/                     ← Interfaz gráfica
│   │   ├── main_window.py       ← Ventana principal
│   │   ├── input_panel.py       ← Panel de entrada
│   │   ├── results_panel.py     ← Panel de resultados
│   │   ├── system_viewer.py     ← Visualizador
│   │   └── styles.py            ← Estilos CSS
│   ├── calculations/             ← Motor de cálculos
│   │   ├── bombeo.py           ← Cálculos de bombeo
│   │   ├── hidraulica.py        ← Cálculos hidráulicos
│   │   └── data_loader.py       ← Carga de datos
│   ├── models/                   ← Modelos de datos
│   │   ├── sistema.py           ← Sistema de tuberías
│   │   ├── tramo.py             ← Tramos de tubería
│   │   ├── accesorio.py         ← Accesorios
│   │   └── fluido.py            ← Fluidos
│   └── data/                     ← Datos de ingeniería
│       ├── accesorios.csv       ← Factores K de accesorios
│       ├── constantes.csv       ← Constantes físicas
│       └── fluidos.csv          ← Propiedades de fluidos
├── main.py                      ← Punto de entrada
├── requirements.txt             ← Dependencias Python
├── build_package.sh             ← Script macOS/Linux
├── build_package.bat            ← Script Windows
├── bombeo.spec                 ← Configuración PyInstaller
├── README_INSTALACION.md        ← Guía de instalación
└── dist/                        ← Ejecutables generados
```

## 🧮 Cálculos Realizados

### 🔬 **Fundamentos Teóricos**

#### Ecuación de Bernoulli Generalizada

```
Ht = (P2/ρg + Z2 + V²²/2g) - (P1/ρg + Z1 + V1²/2g) + hf
```

#### Número de Reynolds

```
Re = (ρ × V × D) / μ
```

#### Factor de Fricción (Darcy-Weisbach)

```
f = 0.316 / Re^0.25  (para flujo turbulento)
```

### 📊 **Pérdidas de Energía**

#### Pérdidas Mayores (Fricción)

```
hf = f × (L/D) × (V²/2g)
```

#### Pérdidas Menores (Accesorios)

```
hm = K × (V²/2g)
```

### ⚡ **Potencia**

#### Potencia Hidráulica

```
Ph = ρ × g × Q × Ht
```

#### Potencia de Bomba

```
Pb = Ph / η
```

### 🌊 **NPSH**

#### NPSH Disponible

```
NPSHa = (Patm/ρg) - (Pv/ρg) - hf - hm - (V²/2g)
```

## 🎨 Características de la Interfaz

### 🖼️ **Diseño Visual**

- **Tema Oscuro**: Fondo #2b2b2b con texto blanco
- **Colores Vibrantes**: Resaltados en verde, azul, amarillo
- **Tipografía**: Arial, sans-serif para legibilidad
- **Iconos**: Símbolos intuitivos para cada función

### 📱 **Layout Responsivo**

- **Splitter Horizontal**: 60% entrada / 40% resultados
- **Pestañas**: Resultados y visualización
- **Scroll**: Para contenido extenso
- **Pantalla Completa**: Maximizado por defecto

### 🎮 **Controles Interactivos**

- **Zoom**: Botones +20% / -20% / Reset
- **Navegación**: Click y arrastrar en visualización
- **Validación**: Entrada de datos en tiempo real
- **Autocompletado**: Sugerencias para campos comunes

### 📊 **Visualización del Sistema**

- **Escala**: 60 pixels por metro
- **Tanques**: 50x50px con etiquetas
- **Tuberías**: Líneas con grosor proporcional
- **Accesorios**: Símbolos geométricos con colores
- **Leyenda**: Esquina superior izquierda

## 🔍 Solución de Problemas

### ❌ **Errores Comunes**

#### "La aplicación no inicia"

**Windows**: "SistemaBombeo no puede abrirse porque es de un desarrollador no identificado"

- **Solución**: Clic derecho → Abrir → Abrir de todos modos

**macOS**: "La aplicación está dañada"

- **Solución**: `sudo xattr -rd com.apple.quarantine SistemaBombeo`

#### "Error al cargar datos"

- **Causa**: Archivos CSV faltantes
- **Solución**: Verificar que `_internal/data/` contenga los 3 archivos CSV

#### "Cálculos incorrectos"

- **Causa**: Unidades incorrectas o datos inválidos
- **Solución**: Revisar que todos los campos tengan valores válidos

### ⚠️ **Advertencias**

#### "Valores fuera de rango"

- **Caudal**: Debe ser positivo
- **Diámetro**: Entre 0.01 y 2.0 metros
- **Eficiencia**: Entre 0.1 y 1.0 (10-100%)

#### "Sistema no configurado"

- **Causa**: Faltan datos obligatorios
- **Solución**: Completar todos los campos requeridos

### 🔧 **Mantenimiento**

#### Actualización de Datos

- **Fluidos**: Editar `src/data/fluidos.csv`
- **Accesorios**: Editar `src/data/accesorios.csv`
- **Constantes**: Editar `src/data/constantes.csv`

#### Rendimiento

- **Cerrar aplicaciones** innecesarias
- **Reiniciar** después de uso prolongado
- **Verificar** espacio en disco disponible

## 📄 Licencia

Copyright © 2026 Listerineh

Este software fue desarrollado para uso personal y educativo con ❤️ para Nayehi.

### 📋 Permisos

- ✅ Uso personal y educativo
- ✅ Modificación del código fuente
- ✅ Distribución de ejecutables modificados

### 🚫 Restricciones

- ❌ Uso comercial sin permiso
- ❌ Distribución como software propio
- ❌ Eliminación de avisos de copyright
