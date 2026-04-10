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

El workflow etiqueta las trazas de Langfuse con los modelos utilizados (LLM y embedding) para agilizar su búsqueda. Cada traza sigue el formato estándar RAG: [Modelo LLM] + [Modelo Embedding], lo que facilita la búsqueda eficiente de las ejecuciones.

Este flujo de trabajo fue utilizado para generar los datos que se pueden ver en el [siguiente documento](https://docs.google.com/spreadsheets/d/1Ju_nYXmQ5IoaE8zZeokdkeOTUwz35U6rZhQE_9gpCXI/edit?gid=841843015#gid=841843015) sobre el consumo de tokens de diferentes modelos para nuestra tarea.

>  ⚠️ **IMPORTANTE:** Al cambiar el modelo, en las últimas versiones de n8n, es necesario "Publicar" además de guardar el flujo de trabajo para poder llamarlo desde otro flujo de trabajo.

## 📊 Monitoreo y Consumo de Tokens en Langfuse

Una ejecución de `generate_traces_v2` o `generate_traces_v3` no solo registra las entradas y las salidas obtenidas, sino que también registra automáticamente el número de tokens consumidos por los modelos.

A continuación, se detalla cómo visualizar estas métricas:

### 1. Vista General (Dashboard)
Los dashboard nos permiten visualizar rápidamente algunos indicadores, ya sea de todas las trazas almacenadas o de las seleccionadas mediante los filtros disponibles.

En esta sección explicaremos cómo construir el siguiente: 

<img width="1164" height="551" alt="image" src="https://github.com/user-attachments/assets/d2b2d4eb-13a4-4dfc-acde-802b36f51c72" />

Un dashboard que cuenta con:
* Contador de Trazas: Número de trazas consideradas para calcular los demás indicadores.
* Latencia Promedio: Es el tiempo promedio, en milisegundos, para recuperar el contexto relevante y decidir la respuesta.
* Contador de Tokens Totales: Es la cantidad de tokens consumidos por el modelo generativo.
* Promedio de Tokens de Salida: Es el promedio de los tokens generados por el modelo.
* Promedio de Tokens de Entrada: Es el promedio de los tokens procesados por el modelo generativo.

Para crearlo, debemos ir a la opción Dashboard en el menú lateral de Langfuse. Al seleccionar "New Dashboard", se abrirá un espacio de trabajo vacío para añadir indicadores. Utilice el botón "Add Widget" y luego "Create New Widget" para incorporar cada uno de los cinco widgets cuyos valores del formulario detallaremos en los siguientes títulos.

#### Contador de Trazas
<p align="center">
  <img width="579" height="865" style="margin 0" alt="image" src="https://github.com/user-attachments/assets/f5424496-8c02-435c-84ee-896856037b73" />
</p>

#### Latencia Promedio
<p align="center">
  <img width="579" height="865" alt="image" src="https://github.com/user-attachments/assets/84840156-b1d9-4d9e-b2cf-59e060bb99f5" />
</p>

#### Indicadores de Tokens Consumidos
<p align="center">
  <img width="33%" height="865" alt="image" src="https://github.com/user-attachments/assets/75e8fe85-b70c-4369-8889-f24b18085967" />
  <img width="33%" height="865" alt="image" src="https://github.com/user-attachments/assets/8a9d04fa-be39-4865-9e45-c096f4bc98d7" />
  <img width="33%" height="865" alt="image" src="https://github.com/user-attachments/assets/315031a5-2fb3-4d69-a40b-c630e473fbec" />
</p>

>  ⚠️ **IMPORTANTE:** Recordar extender el intervalo de tiempo que se consideran las trazas. Por defecto es `Past 1 day`, pero si ejecutaste una traza hace unos días, deberás extenderlo o seleccionar la fecha de la ejecución.

### 2. Análisis Detallado por Traza (Traces)
Para conocer el consumo de una consulta específica, podemos revisar las trazas individuales, ahí podremos ver los tokens consumidos tanto por el modelo de embedding como por el LLM.

Para ver las trazas y los valores almacenados en ellas, dentro de Langfuse, en el menú lateral nos dirigimos a "Tracing" y para visualizar los datos:
1. Seleccionamos una traza de la lista (para ver todos los detalles tiene que ser una traza generada con el flujo `generate_traces_v3`).
2. Se abrirá un panel, donde visualizaremos la entrada (`Input`), la salida (`Output`) y metadatos entre los que se encuentran:
  * Nombres del LLM (`gen_ai.request.model`) y del modelo de embedding (`embedding.model_name`).
  * Tokens de entrada (`gen_ai.usage.input_tokens`), de salida (`gen_ai.usage.completion_tokens`) y totales del LLM (`gen_ai.usage.total_tokens`).
  * Tokens usados por el embedding (`embedding.usage.tokens`).

>  ⚠️ **IMPORTANTE:** Los modelos Ollama no exponen a través de la API que consultamos los tokens de salida, por eso veremos el valor 0.

<img width="1151" height="974" alt="image" src="https://github.com/user-attachments/assets/bfcc4924-5040-4812-9b89-1fee68eaab25" />

### 3. Filtrado por Modelos y Etiquetas (Tags)
Dado que el sistema puede usar modelos de Google u Ollama, cada traza del flujo `generate_traces_v3` se nombra siguiendo la convención `RAG: [nombre del LLM] + [nombre del modelo de embedding]` y se etiqueta con `gen:[nombre del LLM]` y `emb:[nombre del modelo de embedding]`, lo que facilita la búsqueda de trazas de un modelo específico.

#### Cómo filtrar en "Tracing":
  1. Nos dirigimos a "Tracing".
  2. Hacemos clic en "Show Filters", ahí podremos buscar usando **Tags** los modelos que nos interesen o directamente usando el **Trace Name**.
  3. Escribe el nombre del modelo (por ejemplo, ` gemini-2.5-flash-lite`).
  4. La tabla se actualizará para mostrar *solo* las ejecuciones de ese modelo en particular.

#### Cómo filtrar en el "Dashboard":
  1. Vamos a "Dashboard" desde el menú lateral y seleccionamos el que creamos o cualquier otro que nos interese.
  2. Hacemos clic en "Filters" y luego en "Add Filter". Aquí podremos buscar usando etiquetas o el nombre de traza (recordar la convención mencionada al principio de esta sección).
     * Por nombre de traza: *Where `Trace Name` `any of`* y del desplegable de nombres de traza seleccionamos la que nos interese (podemos buscar `RAG:` para ver aquellas generadas con el flujo `generate_traces_v3`).
     * Por etiqueta: *Where `Tags` `any of`* y del desplegable seleccionamos los modelos de embedding / LLM que nos interesen considerar.
    
A continuación, mostraremos ejemplos de filtrados desde un Dashboard:

<img width="1165" height="623" alt="image" src="https://github.com/user-attachments/assets/e9ddada2-d60c-4095-8f53-207f4a242de9" />

<img width="1165" height="623" alt="image" src="https://github.com/user-attachments/assets/32503734-25b7-4293-8e49-6a19d6e496de" />

