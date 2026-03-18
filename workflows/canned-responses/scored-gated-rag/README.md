# Score-Gated RAG

**score-gated-rag-v2-secure** extiende la versión 2 (presente en [experimentals/](../experimentals/)) incorporando validaciones adicionales orientadas a seguridad y uso eficiente de recursos:

- El flujo **solo procesa inputs de tipo texto**.
- Si el input del usuario corresponde a otro tipo de contenido (imagen, video, audio o archivo):
  - No se ejecutan consultas a Pinecone.
  - No se invocan modelos LLM.
  - Se responde inmediatamente con un mensaje controlado.
- Se conserva el esquema de reconstrucción de respuestas fuera del LLM y la lógica de *score gating* con **umbral configurable**.
- Incluye un **mensaje de error predeterminado** que se devuelve al usuario cuando el agente falla en generar una respuesta.

Esta versión está pensada para entornos productivos, donde es importante evitar consumo innecesario de recursos y asegurar un comportamiento predecible ante inputs no soportados o fallas del agente.

