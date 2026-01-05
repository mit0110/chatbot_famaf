## 🧪 Configuración de Experimentos y Evaluaciones

Para realizar experimentos controlados y visualizar correctamente las métricas agrupadas en LangFuse, es **obligatorio** actualizar los identificadores de ejecución antes de lanzar cada prueba.

Si no se actualizan estos valores, las nuevas métricas se mezclarán con las de experimentos anteriores, ensuciando los resultados.

### 📝 Pasos para configurar una nueva ejecución (Run)

Debes modificar dos flujos de trabajo en n8n:

#### 1. En el flujo `generate_traces`
Ubica el nodo llamado **"Establecer Nombre de Trazas"** y modifica el nombre de la traza para reflejar la configuración actual.
* **Ejemplo:** `no-threshold` o `threshold-0.8`.

#### 2. En el flujo `evaluation_metrics`
Ubica el nodo llamado **"Enlazar con el Dataset en LangFuse vía API"** y actualiza el parámetro `run_name` dentro del cuerpo JSON. Esto sirve para agrupar las puntuaciones dentro de LangFuse dentro de la pestaña _Datasets_
* **Ejemplo:** `experimento-no-threshold`.

---

> **⚠️ IMPORTANTE:** Asegúrate de que el nombre del `datasetRun` sea único para cada experimento. Si reutilizas un nombre, LangFuse promediará los nuevos resultados con los viejos.
