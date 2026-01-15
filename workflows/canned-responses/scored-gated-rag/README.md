# Score-Gated RAG 

## Versión 1 

La **v1** implementa un flujo RAG con *score gating* donde:

- Se consulta Pinecone y se obtienen 4 posibles respuestas con su `score`.
- El agente evalúa primero casos sensibles (derivación humana).
- Si **todos los scores son < 0.73**, responde con *fallback*.
- Si existe al menos una respuesta con score ≥ 0.73, el agente devuelve **directamente el texto completo** de la respuesta seleccionada desde Pinecone.
- El manejo de respuestas finales (*fallback*, *human_needed*, *canned_answer*) se realiza usando nodos **Set**.

Esta versión prioriza simplicidad, pero acopla fuertemente al agente con el contenido textual de la respuesta.

------

## Análisis de errores detectados

Durante el uso de la v1 se identificaron dos problemas principales:

- El agente, al devolver el texto completo, **eliminaba o alteraba links** presentes en las respuestas almacenadas en Pinecone.
- El mensaje de *fallback* tenía **problemas de formato**, debido a limitaciones del nodo **Set** al manejar strings largos y saltos de línea.

------

## Versión 2 

La **v2** introduce mejoras estructurales para resolver estos problemas:

- El agente **ya no devuelve el texto**, sino únicamente un identificador (`response_num`) de la respuesta seleccionada.
- La respuesta final se reconstruye **fuera del LLM**, usando un nodo **Code** que recupera el texto exacto desde Pinecone.
- Esto garantiza que las respuestas:
  - No pierdan links.
  - No sean modificadas por el modelo.
- Los mensajes de *fallback* y *derivación humana* se generan con nodos **Code**, evitando errores de formato.
- Se mantiene el mismo criterio de *score gating* (umbral 0.73) y la lógica de decisión.