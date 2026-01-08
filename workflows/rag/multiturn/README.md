## 🤖 Workflows RAG – Reformulación y búsqueda por embeddings

Este repositorio contiene **dos workflows RAG en n8n** que procesan preguntas de usuarios (vía Telegram) para devolver **respuestas enlatadas** mediante búsqueda por similitud en un índice de embeddings (Pinecone).

En **ambas versiones** el flujo base es el mismo:

- La pregunta del usuario se **reformula con un LLM** (usando contexto reciente cuando es relevante).
- La pregunta reformulada se utiliza para **buscar en el embedding**.
- Se devuelve al usuario la respuesta asociada al resultado más similar.

La diferencia principal entre las versiones es **si el sistema puede o no repreguntar al usuario** cuando falta contexto.

------

## 📌 Workflow V1 – Reformula y busca (sin repreguntas)

**Archivo:** `rag_query_ollama_ccad-memory-gen-V1.json`

**Qué hace:**

- Reformula la pregunta del usuario para hacerla más clara y explícita.
- Usa hasta 5 mensajes previos solo si ayudan a mejorar la reformulación.
- Ejecuta siempre la búsqueda por similitud en el embedding.
- Devuelve una respuesta enlatada basada en el resultado.

------

## 📌 Workflow V2 – Reformula, evalúa contexto y puede repreguntar

**Archivo:** `rag_query_ollama_ccad-memory-gen-V2.json`

**Qué hace:**

- Reformula la pregunta del usuario igual que V1.
- Evalúa si la pregunta tiene contexto suficiente para buscar en el embedding.

**Comportamiento:**

- Si hay contexto suficiente:
  - Busca en el embedding.
  - Devuelve la respuesta enlatada.
- Si NO hay contexto suficiente:
  - No busca en el embedding.
  - Hace una única repregunta mínima para obtener el contexto faltante.

------

## 🔍 Diferencias clave

| Aspecto                | V1        | V2                     |
| ---------------------- | --------- | ---------------------- |
| Reformula la pregunta  | ✅ Sí      | ✅ Sí                   |
| Busca en embeddings    | ✅ Siempre | ✅ Solo si hay contexto |
| Repreguntas al usuario | ❌ No      | ✅ Sí                   |