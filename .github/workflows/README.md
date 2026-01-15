# 🚀 GitHub Actions Workflow

Este directorio contiene el workflow de GitHub Actions para construir automáticamente los ejecutables del Sistema de Cálculo de Bombeo para todas las plataformas.

## 📋 Workflow Disponible

### 🔄 `build-all.yml`
- **Plataformas:** Windows, macOS, Linux (simultáneo)
- **Python:** 3.11
- **Ejecución:** Paralela en 3 jobs
- **Salida:** 3 archivos ZIP + release automático
- **Características:**
  - Builds simultáneos para todas las plataformas
  - Verificación automática de ejecutables
  - Creación de paquetes ZIP para distribución
  - Upload de artifacts por 30 días
  - Release automático en tags
  - Notas de release generadas automáticamente

## 🎯 Cómo Usar el Workflow

### **1. Build Automático**
```bash
# Push al repositorio
git push origin main

# O ejecutar manualmente desde GitHub Actions
# Repository → Actions → build-all → Run workflow
```

### **2. Build Automático**
El workflow se ejecuta automáticamente en:
- **Push** a rama `main`
- **Pull Request** a rama `main`
- **Release** (tags)
- **Ejecución manual** (workflow_dispatch)

### **3. Release Automático**
```bash
# Crear un tag para release automático
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions creará el release con todos los ejecutables
```

## 📦 Artefacts Generados

### **🔄 build-all.yml (Completo):**
- **windows:** `SistemaBombeo-v1.0-Windows.zip`
- **macos:** `SistemaBombeo-v1.0-macos.zip`
- **linux:** `SistemaBombeo-v1.0-Linux.zip`

### **Contenido de cada ZIP:**
- **Windows:** `SistemaBombeo.exe` + `_internal/data/`
- **macOS:** `SistemaBombeo` + `_internal/data/`
- **Linux:** `SistemaBombeo` + `_internal/data/`

## 🔧 Configuración

### **Variables de Entorno**
- `GITHUB_TOKEN`: Automático para releases
- `PYTHON_VERSION`: 3.11 (configurable)

### **Secrets Necesarios**
- `GITHUB_TOKEN`: Automático proporcionado por GitHub

### **Cache**
- Dependencies pip cache para builds más rápidos
- Duración: 7 días

## 📊 Tiempos de Build Aproximados

| Plataforma | Tiempo de Build | Tiempo de Upload |
|------------|-----------------|------------------|
| Windows    | 5-8 minutos    | 2-3 minutos      |
| macOS      | 4-6 minutos    | 1-2 minutos      |
| Linux      | 3-5 minutos    | 1-2 minutos      |
| **Total**  | **10-15 min**  | **4-7 min**      |

## 🚀 Flujo de Trabajo Recomendado

### **Desarrollo Local:**
```bash
# Desarrollar en tu plataforma local
./build_package.sh  # macOS/Linux
# build_package.bat  # Windows
```

### **Build Automático:**
```bash
# Push para builds automáticos
git add .
git commit -m "Update application"
git push origin main
```

### **Release:**
```bash
# Crear tag para release
git tag v1.0.0
git push origin v1.0.0 --tags
```

## 🔍 Monitoreo y Logs

### **Verificar Builds:**
1. GitHub → Repository → Actions
2. Seleccionar workflow `build-all`
3. Ver logs y artifacts

### **Descargar Artefacts:**
1. Actions → Select workflow run
2. Artifacts section → Download
3. Elegir plataforma: windows, macos, linux

### **Verificar Ejecutables:**
- Los ejecutables se prueban automáticamente
- Verificar logs para confirmar éxito
- Descargar y probar localmente si es necesario

## 🛠️ Personalización

### **Modificar Versiones:**
Editar en el workflow:
```yaml
pip install PyQt6==6.10.2
pip install PyInstaller==6.18.0
```

### **Cambiar Python:**
```yaml
python-version: '3.11'
```

### **Modificar Tiempo de Retención:**
```yaml
retention-days: 30
```

### **Cambiar Nombres de Artifacts:**
```yaml
name: windows  # o macos, linux
```

## 📝 Notas Importantes

- **Costo:** GitHub Actions es gratuito para repositorios públicos
- **Límites:** 2000 minutos/mes para repositorios privados
- **Storage:** Los artifacts se eliminan automáticamente
- **Seguridad:** Los builds se ejecutan en entornos aislados
- **Reproducibilidad:** Los builds son consistentes y versionados
- **Eficiencia:** Un solo workflow para todas las plataformas

## 🎯 Ventajas del Diseño Actual

### **✨ Simplicidad:**
- **Un solo workflow** que maneja todo
- **Menos mantenimiento** de configuración
- **Fácil de entender** y modificar

### **✨ Eficiencia:**
- **Ejecución paralela** de las 3 plataformas
- **Menos tiempo total** de build
- **Optimización** de recursos

### **✨ Consistencia:**
- **Misma configuración** para todas las plataformas
- **Resultados uniformes** y predecibles
- **Menos posibilidades** de errores

---

**🎉 Con este único workflow, puedes construir automáticamente ejecutables para todas las plataformas sin complicaciones!**
