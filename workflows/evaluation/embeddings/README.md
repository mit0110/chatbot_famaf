# 📊 Pipeline de Evaluación RAG: Modelos de Embedding

Este directorio contiene flujos de trabajo en **n8n** diseñados para evaluar el rendimiento, la latencia y la precisión de modelos de embedding en el sistema de recuperación (*Retrieval*) del chatbot.

El pipeline automatiza el ciclo de vida completo: desde la ingesta en la base de datos, las consultas de prueba, hasta el cálculo objetivo de métricas de calidad (*Recall@1* y *MRR@5*) y la limpieza de recursos.

## 📂 Archivos del Pipeline

El proceso tiene tres flujos principales:

1. **`embedding_latency.json` (Punto de partida)**
   Se encarga de crear dinámicamente un índice en Pinecone, descargar la base de conocimiento (`faq_dataset_v1.csv`), generar los embeddings y registrar la **latencia** total del proceso de la ingesta.
2. **`embedding_generate_traces.json`**
   Simula el consultas de usuarios descargando un dataset de prueba desde Langfuse. Realiza búsquedas de similitud (Top-K=5), envía la telemetría (trazas OTLP) a Langfuse y, al finalizar, elimina el índice de Pinecone para evitar costos innecesarios.
3. **`embedding_metrics.json`**
   Cruza los datos recuperados con los valores esperados del dataset original para calcular métricas de calidad. Evalúa la **Exactitud (Accuracy)** considerando un umbral de *fallback* dado y calcula el **MRR (Mean Reciprocal Rank)**.

> **Nota:** `embedding_metrics.json` usa un sub-workflow llamado `save_metrics`, invocado al final del proceso para almacenar los resultados.

---

## 🚀 Cómo Realizar un Experimento

Sigue estos pasos para evaluar un nuevo modelo de embedding:

### 1. Importación y Enlace
Importa los tres archivos `.json` en tu entorno de n8n. Como n8n genera nuevos IDs internos al importar flujos, debes actualizar los nodos de tipo **"Execute Workflow"** en cada archivo para asegurarte de que apunten correctamente al flujo siguiente:
* En `embedding_latency` -> Actualiza el nodo que llama a `embedding_generate_traces`.
* En `embedding_generate_traces` -> Actualiza el nodo que llama a `embedding_metrics`.
* En `embedding_metrics` -> Actualiza los nodos que llaman a `save_metrics`.

### 2. Configuración del Modelo a Evaluar
Abre el flujo **`embedding_latency`** y localiza el nodo llamado **"Rellenar Datos sobre el Modelo"**. Modifica los siguientes parámetros según el modelo que desees probar:
* `supplier`: Ej. `google`, `ollama`, `ccad`.
* `model_name`: Ej. `gemini-embedding-001`.
* `dimension`: La dimensión del vector que genera el modelo (ej. `3072`).
* `accuracy_threshold`: El punto de corte para dar la respuesta *fallback* (ej. 0.73).

*Asegúrate también de actualizar el nodo correspondiente ("Embedding") con las credenciales y el modelo exacto dentro del flujo `embedding_latency` y `embedding_generate_traces`.

### 3. Ejecución
Una vez configurado, haz clic en el nodo **"Ejecución Manual"** dentro de `embedding_latency`. El sistema se encargará del resto:
1. Creará el índice `proveedor-modelo-dimension`.
2. Ingestará los datos.
3. Probará las 100 consultas.
4. Generará las métricas en Langfuse con el punto de corte proporcionado.
5. Destruirá el índice de Pinecone automáticamente al finalizar.

> **Nota:** Las métricas Macro F1 Score y AUC ROC se calculan en el *Jupyter Notebook* disponible en el directorio `notebooks/` debido a la complejidad de hacerlo usando flujos de n8n.
