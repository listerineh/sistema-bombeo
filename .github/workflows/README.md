# 🚀 GitHub Actions Workflows

Este directorio contiene los workflows de GitHub Actions para construir automáticamente los ejecutables del Sistema de Cálculo de Bombeo para diferentes plataformas.

## 📋 Workflows Disponibles

### 🔨 `build-windows.yml`
- **Plataforma:** Windows Server 2019/2022
- **Python:** 3.11
- **Salida:** `SistemaBombeo.exe` + ZIP
- **Características:**
  - Build completo con PyInstaller
  - Verificación automática del ejecutable
  - Creación de paquete ZIP para distribución
  - Upload de artifacts por 30 días
  - Release automático en tags

### 🍎 `build-macos.yml`
- **Plataforma:** macOS 11/12
- **Python:** 3.11
- **Salida:** `SistemaBombeo` + ZIP
- **Características:**
  - Build completo con PyInstaller
  - Verificación automática del ejecutable
  - Creación de paquete ZIP para distribución
  - Upload de artifacts por 30 días
  - Release automático en tags

### 🐧 `build-linux.yml` (en build-all.yml)
- **Plataforma:** Ubuntu 20.04/22.04
- **Python:** 3.11
- **Salida:** `SistemaBombeo` + ZIP
- **Características:**
  - Build completo con PyInstaller
  - Creación de paquete ZIP para distribución
  - Upload de artifacts por 30 días

### 🔄 `build-all.yml`
- **Plataformas:** Windows, macOS, Linux
- **Ejecución:** Paralela en 3 jobs
- **Salida:** 3 archivos ZIP + release automático
- **Características:**
  - Builds simultáneos para todas las plataformas
  - Release automático con todos los ejecutables
  - Notas de release generadas automáticamente

## 🎯 Cómo Usar los Workflows

### **1. Build Manual**
```bash
# Push al repositorio
git push origin main

# O ejecutar manualmente desde GitHub Actions
# Repository → Actions → Select workflow → Run workflow
```

### **2. Build Automático**
Los workflows se ejecutan automáticamente en:
- **Push** a rama `main`
- **Pull Request** a rama `main`
- **Release** (tags)

### **3. Release Automático**
```bash
# Crear un tag para release automático
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions creará el release con todos los ejecutables
```

## 📦 Artefacts Generados

### **Windows:**
- `windows-executable`: `SistemaBombeo-v1.0-Windows.zip`
- Contiene: `SistemaBombeo.exe` + `_internal/data/`

### **macOS:**
- `macos-executable`: `SistemaBombeo-v1.0-macos.zip`
- Contiene: `SistemaBombeo` + `_internal/data/`

### **Linux:**
- `linux-executable`: `SistemaBombeo-v1.0-Linux.zip`
- Contiene: `SistemaBombeo` + `_internal/data/`

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
2. Seleccionar workflow
3. Ver logs y artifacts

### **Descargar Artefacts:**
1. Actions → Select workflow run
2. Artifacts section → Download

### **Verificar Ejecutables:**
- Los ejecutables se prueban automáticamente
- Verificar logs para confirmar éxito
- Descargar y probar localmente si es necesario

## 🛠️ Personalización

### **Modificar Versiones:**
Editar en cada workflow:
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

## 📝 Notas Importantes

- **Costo:** GitHub Actions es gratuito para repositorios públicos
- **Límites:** 2000 minutos/mes para repositorios privados
- **Storage:** Los artifacts se eliminan automáticamente
- **Seguridad:** Los builds se ejecutan en entornos aislados
- **Reproducibilidad:** Los builds son consistentes y versionados

---

**🎉 Con estos workflows, puedes construir automáticamente ejecutables para todas las plataformas sin necesidad de tener máquinas Windows o Linux físicas!**
