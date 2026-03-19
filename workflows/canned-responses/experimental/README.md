# 🧪 Experimentos

Este directorio contiene workflows de n8n que son:
* **Versiones de prueba o experimentación:** Workflows utilizados para validar lógicas específicas o realizar experimentos (P. ej., `telegram-faq-bot` o `telegram-faq-bot-thershold`).
* **Iteraciones:** Estructuras iniciales y mejoras antes de la versión final (P. ej., `telegram-faq-bot-rate-limit` es la versión con *rate limit* de `telegram-faq-bot-thershold`).
* **PoC (Proof of Concept):** Pruebas aisladas de integración con APIs y bases de datos (p. ej., `create-question-embedding`).

Fue creado con el objetivo de mantener la raíz del proyecto limpia y organizada, manteniendo solo las versiones finales.

> Dentro del subdirectorio `scored-gated-rag` se encontrarán las iteraciones previas al flujo de trabajo `score-gated-rag-v2-secure`, lo dividimos del resto para mantener la estructura de `canned-responses`.

## Archivos del Directorio

### Flujos de Trabajo de Telegram

El workflow `telegram-faq-bot` es una versión de prueba inicial de un bot que recibe un mensaje desde Telegram y lo utiliza para hacer una búsqueda semántica en una base de datos vectorial que contiene preguntas frecuentes, extrayendo de ella la pregunta que mayor valor de similitud obtenga junto con sus metadatos, donde está guardada la respuesta a dicha pregunta, y responde a la consulta realizada por Telegram.

El flujo `telegram-faq-bot-threshold` viene a solucionar uno de los problemas de `telegram-faq-bot`: responder con la respuesta de la pregunta extraída de la base de datos sin importar la puntuación de similitud. Para eso, se agregó un condicional que verifica el valor de similitud justo después de la extracción y si es bajo, comparado con el valor determinado por el usuario del flujo, responde usando *fallback*.

> `telegram-faq-bot-threshold` fue el flujo utilizado en [este experimento](https://docs.google.com/document/d/1EC6ADsilP3oBhF6OFeuoPqWHkgeqJGgf4ot6L1j5cTw/edit?tab=t.0).

El flujo `telegram-faq-bot-rate-limit` es una mejora a `telegram-faq-bot-threshold` que usa una base de datos Redis para verificar que los usuarios del bot no puedan realizar más de `message_limit_per_duration` consultas en `duration_in_sconds` (ambos valores pueden ser cambiados desde el workflow).

Estos flujos formaron la base para los que están en `score-gated-rag/`.

### Flujos para Generar Embeddings

`create-question-embedding` es un flujo de trabajo que extrae un archivo `.csv` desde este repositorio que contiene preguntas, respuestas y categorías, genera los vectores de las preguntas usando un modelo de embedding y los inserta dentro de la base de datos de Pinecone. Funcionó como una prueba de concepto para comprender la integración con Pinecone.

`create-question-embedding-via-admin` es un workflow que se ejecuta de manera manual y se encarga de obtener todas las preguntas con su respectiva respuesta y categoría desde el panel de administrador para insertarlas a la base de datos vectorial. Fue una iteración anterior a `create-question-embedding-webhook`.

### RAG
El subdirectorio `score-gated-rag/` contiene las versiones anteriores a la de producción (`score-gated-rag-v2-secure`). En estos workflows se reemplazó la lógica estática de un punto de corte o *threshold* por un modelo que decida cuándo responder.

`score-gated-rag-v1` implementa una lógica RAG (*Retrieval-Augmented Generation*) donde:

- Se consulta Pinecone y se obtienen *N* posibles respuestas junto con su `score`.
- El agente evalúa primero casos sensibles (derivación humana).
- Si **todos los scores son menores al umbral configurado**, se responde con *fallback*.
- Si existe al menos una respuesta con score mayor o igual al umbral, el agente devuelve **directamente el texto completo** de la respuesta seleccionada desde Pinecone.

Mientras que, `score-gated-rag-v2` viene a solucionar dos problemas de su versión anterior:
1. El agente, al devolver el texto completo, **eliminaba o alteraba links** presentes en las respuestas almacenadas en Pinecone.
2. El mensaje de *fallback* presentaba **problemas de formato**, debido a limitaciones del nodo **Set** al manejar strings largos y saltos de línea.

Introduciendo las siguientes mejoras estructurales:

- El agente **ya no devuelve el texto**, sino únicamente un identificador (`response_num`) de la respuesta seleccionada.
- La respuesta final se reconstruye **fuera del LLM**, utilizando un nodo **Code** que recupera el texto exacto desde Pinecone, garantizando que
  - No se pierdan links.
  - No sean modificadas por el modelo.
- Los mensajes de *fallback* y *derivación humana* se generan con nodos **Code**, evitando errores de formato.
- Se mantiene la lógica de *score gating*, incorporando un  **umbral configurable** que puede ajustarse según el modelo de *embedding* utilizado.

---

## Consideraciones de Uso
Los archivos en este directorio **no están destinados a producción**:
* Pueden contener nodos con configuraciones de prueba o información *hardcodeada*.
* Se mantienen como **referencia histórica** y consulta técnica.


