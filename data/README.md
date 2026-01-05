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
| `pregunta` | La consulta del usuario o la variante. |
| `respuesta` | El texto que se almacenará en los metadatos y se mostrará al usuario para responder a la consulta. |
| `categoria` | Etiqueta para marcar el tipo de pregunta (P. ej., "ingreso", "cursado"). |
