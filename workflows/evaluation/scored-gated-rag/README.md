# Evaluación Scored-Gated-RAG

Se generalizaron las evaluaciones para permitir definir, desde el nodo de configuración, los principales parámetros del proceso de evaluación. Esto incluye el **dataset a evaluar** (`dataset`), la **URL de Langfuse** (`langfuse_host_url`) lo que permite alternar fácilmente entre una instancia local o en la nube y el **nombre de las trazas** (`trace_name`), que además se utiliza como nombre del *dataset run* asociado a la evaluación.

## Generadores de trazas

Los siguientes nodos permiten generar las trazas necesarias para evaluar distintas versiones de Scored-Gated-RAG:

- **`generate_traces_score-gated-rag-v1`**: genera las trazas para la primera versión de Scored-Gated-RAG.

- **`generate_traces_score-gated-rag-v2`**: genera las trazas para la segunda versión de Scored-Gated-RAG.

- **`generate_traces_score-gated-rag-v2-multiturn`**: genera las trazas para la segunda versión de Scored-Gated-RAG con soporte adicional para manejar la memoria dentro de una misma conversación.  
  Para utilizar este generador, el dataset multiturno asociado debe contar con un **ID por conversación**, lo que permite evaluar qué tan relevante fue el contexto previo y medir su correcta utilización.

## Evaluadores compatibles

Para aprovechar esta generalización de parámetros, es necesario utilizar alguno de los siguientes evaluadores, que soportan estas variables adicionales:

1. **`evaluation_metrics_v2`**  
2. **`evaluation_metrics_accuracy+wildbench`**

El primer evaluador mide únicamente **accuracy**, mientras que el segundo, además de calcular accuracy, genera un registro del benchmark **WildBench**.  
Más información en el paper oficial:  
👉 [WildBench: Benchmarking LLMs for Instruction Following](https://allenai.github.io/WildBench/WildBench_paper.pdf)

## Parámetros configurables

Al utilizar **`evaluation_metrics_accuracy+wildbench`**, es importante configurar correctamente el nodo **`set checklist for wildbench`**, donde se define la *checklist* que será utilizada posteriormente por el modelo seleccionado como **LLM-as-a-Judge** para evaluar las respuestas del chatbot.