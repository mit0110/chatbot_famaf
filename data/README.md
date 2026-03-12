# Estructura de Datos del Chatbot

Este directorio contiene la Base de Conocimiento (Knowledge Base) y los Conjuntos de Datos de Evaluación.

## Estructura de Directorios

- **`knowledge_base/`**: información cuyos embeddings serán almacenados en la Base de Datos Vectorial.
  - `faq_dataset_vX.csv`: versión actual de la base de conocimiento.
  - `archive/`: bases de conocimientos anteriores.
- **`evaluation/`**: información utilizada para evaluar el rendimiento del bot.
  - `validation.csv`: usado para ajustar hiperparámetros y ver el rendimiento del modelo.
  - `test.csv`: usado para la evaluación final de métricas.

## Columnas de los Conjuntos de Datos

Todos los archivos `.csv` siguen este formato:

| Columna | Descripción |
| :--- | :--- |
| `Preguntas` | La consulta del usuario o la variante. |
| `Respuesta` | La respuesta a la pregunta que se usó para generar la "respuesta mejorada" . |
| `Respuesta Mejorada` | Respuesta que el bot le dará al usuario cuando haga una pregunta similar a la que responde. Formateada para mensaje de WhatsApp. |
| `Categoría` | Etiqueta para marcar el tipo de pregunta (P. ej., "ingreso", "cursado"). |
