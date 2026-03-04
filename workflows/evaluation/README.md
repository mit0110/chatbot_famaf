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
### Generar Trazas con Tokens Consumidos y Latencia (solo Recuperación)
*Usa este procedimiento en el flujo de trabajo `generate_traces_v2`.*

>  ⚠️ **IMPORTANTE:** Antes de ejecutar este flujo, se debe generar un índice en Pinecone con el modelo de embedding a utilizar.

En el flujo `generate_traces_v2`:
* **Nombre del Modelo de Embedding:** en el nodo **"Establecer Nombre del Modelo de Embedding"** colocar en `embedding_model_name` el nombre del modelo y en `supplier` colocar
   * `ollama`: si se quiere probar algún modelo self-hosted en ollama o alojado en CCAD.
   * `google`: si el modelo a probar es de Google (p. ej. `gemini-embedding-001`, `text-embedding-004`).
* **Índice en Pinecone:** en el nodo **"HTTP Request API de Pinecone (Gemini)"** o **"HTTP Request API de Pinecone (Ollama)"**, según corresponda con el modelo, cambiar la base URL por la del índice ya creado con **el mismo modelo de embedding** en Pinecone.
   * **En caso de ser necesario** cambiar los valores en el cuerpo de la consulta.

### Generar Trazas con Tokens Consumidos y Latencia (RAG)
*Usa este procedimiento en el flujo de trabajo `generate_traces_v3`.* Este a diferencia del anterior calcula los tokens consumidos por el embedding y también por el LLM.

>  ⚠️ **IMPORTANTE:** Este flujo utiliza todos los flujos del `helpers/` y debe exponer el puerto de n8n con Ngrok.

En el flujo `generate_traces_v3`:
* **Nombre del Modelo de Embedding y Conjunto de Datos de Langfuse:** en el nodo **"Establecer Nombre del Modelo de Embedding"** colocar en `langfuse_dataset_name` el nombre del conjunto de datos de donde se van a extraer las preguntas de prueba,  en `embedding_model_name` el nombre del modelo y en `supplier` colocar
   * `ollama`: si se quiere probar algún modelo self-hosted en ollama o alojado en CCAD.
   * `google`: si el modelo a probar es de Google (p. ej. `gemini-embedding-001`, `text-embedding-004`).
* **Índice en Pinecone:** en el nodo **"HTTP Request API de Pinecone (Gemini)"** o **"HTTP Request API de Pinecone (Ollama)"**, según corresponda con el modelo, cambiar la base URL por la del índice ya creado con **el mismo modelo de embedding** en Pinecone.
   * **En caso de ser necesario** cambiar los valores en el cuerpo de la consulta.
* **Modelo de Generación:** Ir al subflujo desde el nodo "RAG-no-memory" y cambiar el modelo a utilizar.
