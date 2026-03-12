- # Score-Gated RAG

  ## Versión 1

  La **v1** implementa un flujo RAG con *score gating* donde:

  - Se consulta Pinecone y se obtienen *N* posibles respuestas junto con su `score`.
  - El agente evalúa primero casos sensibles (derivación humana).
  - Si **todos los scores son menores al umbral configurado**, se responde con *fallback*.
  - Si existe al menos una respuesta con score mayor o igual al umbral, el agente devuelve **directamente el texto completo** de la respuesta seleccionada desde Pinecone.
  - El manejo de respuestas finales (*fallback*, *human_needed*, *canned_answer*) se realiza utilizando nodos **Set**.

  Esta versión prioriza la simplicidad, pero acopla fuertemente al agente con el contenido textual de la respuesta.

  ---

  ## Análisis de errores detectados

  Durante el uso de la **v1** se identificaron dos problemas principales:

  - El agente, al devolver el texto completo, **eliminaba o alteraba links** presentes en las respuestas almacenadas en Pinecone.
  - El mensaje de *fallback* presentaba **problemas de formato**, debido a limitaciones del nodo **Set** al manejar strings largos y saltos de línea.

  ---

  ## Versión 2

  La **v2** introduce mejoras estructurales para resolver estos problemas:

  - El agente **ya no devuelve el texto**, sino únicamente un identificador (`response_num`) de la respuesta seleccionada.
  - La respuesta final se reconstruye **fuera del LLM**, utilizando un nodo **Code** que recupera el texto exacto desde Pinecone.
  - Esto garantiza que las respuestas:
    - No pierdan links.
    - No sean modificadas por el modelo.
  - Los mensajes de *fallback* y *derivación humana* se generan con nodos **Code**, evitando errores de formato.
  - Se mantiene la lógica de *score gating*, incorporando un  **umbral configurable** que puede ajustarse según el modelo de *embedding* utilizado.

  ---

  ## Versión 2 Secure

  La **v2 Secure** extiende la versión 2 incorporando validaciones adicionales orientadas a seguridad y uso eficiente de recursos:

  - El flujo **solo procesa inputs de tipo texto**.
  - Si el input del usuario corresponde a otro tipo de contenido (imagen, video, audio o archivo):
    - No se ejecutan consultas a Pinecone.
    - No se invocan modelos LLM.
    - Se responde inmediatamente con un mensaje controlado.
  - Se conserva el esquema de reconstrucción de respuestas fuera del LLM y la lógica de *score gating* con **umbral configurable**.
  - Incluye un **mensaje de error predeterminado** que se devuelve al usuario cuando el agente falla en generar una respuesta.
  
  Esta versión está pensada para entornos productivos, donde es importante evitar consumo innecesario de recursos y asegurar un comportamiento predecible ante inputs no soportados o fallas del agente.

