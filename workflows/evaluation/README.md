## 🧪 Configuración de Experimentos y Evaluaciones

Para realizar experimentos controlados y visualizar correctamente las métricas agrupadas en Langfuse, es **obligatorio** actualizar los identificadores de ejecución antes de cada prueba.

> **⚠️ IMPORTANTE:** Asegúrate de que el nombre del `datasetRun` sea único para cada experimento. Si reutilizas un nombre, LangFuse promediará los nuevos resultados con los viejos, ensuciando los datos.

### Ejecución Estándar (Sin Umbral)
*Usa este procedimiento para el flujo base `generate_traces`.*

1.  **En el flujo `generate_traces`:**
    * Ubica el nodo **"Establecer Nombre de las Trazas"**.
    * Modifica el nombre para reflejar la prueba (p. ej. `exp-no-threshold`).

2.  **En el flujo `evaluation_metrics`:**
    * Ubica el nodo **"Enlazar con el Dataset en LangFuse vía API"**.
    * Actualiza el parámetro `run_name` en el JSON (p. ej. `run-base-v1`).
    * Este será el nombre con el que se verá en el menú Dataset Runs de Langfuse.

---

### Ejecución con Corte (Umbral)
*Usa este procedimiento para el flujo modificado `generate_traces_threshold`.*

1.  **En el flujo `generate_traces_threshold`:**
    * **Nombre de Traza:** En el nodo **"Establecer Nombre de las Trazas"**, asigna un nombre que las identifique (p. ej. `exp-threshold-0.78`).
    * **Valor del Umbral:** En el nodo **"Si Similitud >= Punto de Corte"**, modifica el *Value 2* con el valor deseado (p. ej., `0.78`).

2.  **En el flujo `evaluation_metrics`:**
    * Ubica el nodo **"Enlazar con el Dataset en LangFuse vía API"**.
    * Actualiza el parámetro `run_name` en el JSON para diferenciarlo del run base (p. ej. `run-threshold-0.79-v1`).

---
