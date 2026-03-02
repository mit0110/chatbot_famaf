# Carga de datos en el Embedding

Hay dos formas de cargar datos para generar embeddings:

------

## 1. Desde un CSV en GitHub

Usar el workflow:

```
create-question-embedding.json
```

### Configuración

En el nodo **Get File**:

- Agregar la credencial de GitHub.
- Completar:
  - **Repository Owner**: usuario u organización del repositorio.
  - **Repository Name**: nombre del repositorio.
  - **File Path**: ruta exacta del archivo CSV dentro del repo (ej: `data/base.csv`).

------

## 2. Desde el Panel del Administrador (FastAPI)

Usar el workflow:

```
create-question-embedding-via-admin.json
```

### Configuración

En el nodo configurar url, completar:

```
FAST_API_URL
```

Con la URL donde está hosteado el panel del administrador.