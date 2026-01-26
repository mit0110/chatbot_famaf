# Rephrase Question 

## V1 – Reformulación con memoria

- El agente reformula la pregunta del usuario para mejorar la recuperación de información.
- Utiliza una **memoria volátil de los últimos 5 mensajes** para incorporar contexto conversacional relevante.
- Siempre devuelve **una única pregunta reformulada**.
- No valida si la pregunta es ambigua o si falta contexto.
- La respuesta que se devuelve al usuario es la asociada a la pregunta reformulada, obtenida a partir de la búsqueda por similaridad en el *embedding*.

---

## V2 – Agente consciente del contexto

- El agente evalúa si la pregunta del usuario tiene **contexto suficiente** para ser utilizada.
- Utiliza una **memoria volátil de los últimos 5 mensajes**.
- Si el contexto es suficiente, devuelve la **respuesta asociada a la pregunta descriptiva **generada por el agente a partir de la original, obteniendo la respuesta mediante búsqueda por similaridad en el *embedding*.
- Si el contexto es insuficiente, devuelve al usuario una **repregunta aclaratoria** para obtener la información faltante.
- El agente decide explícitamente si avanzar con la recuperación de información o esperar más contexto del usuario.