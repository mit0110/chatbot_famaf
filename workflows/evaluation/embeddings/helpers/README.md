# 🛠️ Workflows Auxiliares (Helpers)

Este directorio contiene **sub-workflows** útiles diseñados para ser llamados por los flujos principales de trabajo. Su función es encapsular la lógica de workflows principales para mantener el workflow padre principal limpio y legible.

## 📂 Contenido del Directorio

### 1. 🧠 `RAG_no_memory`
Este sub-workflow es un Agente RAG sin memoria, es decir, no guarda mensajes anteriores (historial) del usuario, sino que recibe un input y decide la respuesta.
* **Entrada:** Query del usuario + Documentos recuperados.
* **Objetivo:** Evalúa la relevancia del contexto y detecta casos sensibles.
* **Uso:** Se invoca en el workflow padre después de realizar la búsqueda vectorial.

La separación de esta parte del flujo del resto fue importante para extraer los datos sobre los tokens consumidos ya que redujo considerablemente el tamaño del archivo que devuelve el nodo `Get an Execution` y esto facilitó la búsqueda de la información relacionada al uso de tokens.

### 2. 📊 `save_traces_to_langfuse`
Un sub-workflow que se llama para enviar métricas a **Langfuse** (MLOps).
* **Objetivo:** Formatear correctamente los datos para cumplir con el estándar **OpenTelemetry (OTLP)** y enviar a Langfuse (Servidor de Observabilidad).
* **Características:** Vincula la ejecución con datasets de prueba, registra latencias y tokens usados por los modelos.
* **Dependencia:** Llama internamente a `get_execution_info` para obtener el modelo y tokens usados.

### 3. 🔍 `get_execution_info` (Utilidad Interna)
Un workflow de utilidad que interactúa con la API de n8n.
* **Objetivo:** Extraer metadatos de la ejecución (tokens consumidos, modelos usados) que no están disponibles en el contexto estándar del workflow para el número de ejecución que se le suministró.
* **Compatibilidad:** Normaliza la salida de tokens para proveedores Google Gemini y Ollama.

Para extraer la cantidad de tokens usados, usa el índice que ocupa el nodo del modelo dentro de `RAG_no_memory` puede que sea necesario cambiar el número del nodo que ahora ocupa el modelo en el nodo `Return Token Usage for Google Models` y `Return Token Usage for CCAD Models`.

> ⚠️ **Importante:** Para obtener la información de una ejecución se usa la API de n8n por lo que, n8n debe estar en un servidor o bien exponer el puerto usando ngrok si se está usando de manera local. Además, debe [crearse una API Key](https://docs.n8n.io/api/authentication/) para usar la API.

---

## 🔄 Flujo de Dependencias

Estos helpers están diseñados para trabajar en cadena. El siguiente esquema muestra cómo se relacionan entre sí dentro de este directorio:

```mermaid
graph LR
    MainApp[generate_traces_v3] -.-> |Llama a| RAG[🧠 RAG_no_memory]
    MainApp -.-> |Llama a| Logger[📊 save_traces_to_langfuse]
    
    subgraph Helpers [Directorio Helpers]
        RAG
        Logger --> |Depende de| GetInfo[🔍 get_execution_info]
    end

    style MainApp fill:#333,stroke:#fff,stroke-width:2px,color:#fff
    style RAG fill:#7d2ea0,stroke:#fff,stroke-width:2px,color:#fff
    style Logger fill:#0056b3,stroke:#fff,stroke-width:2px,color:#fff
    style GetInfo fill:#008080,stroke:#fff,stroke-width:2px,color:#fff
    style Helpers fill:#222,stroke:#888,stroke-dasharray: 5 5,color:#fff
```
