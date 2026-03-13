# Evaluación Scored-Gated-RAG

Se generalizaron las evaluaciones para permitir definir, desde el nodo de configuración, los principales parámetros del proceso de evaluación. Esto incluye el **dataset a evaluar** (`dataset`), la **URL de Langfuse** (`langfuse_host_url`) lo que permite alternar fácilmente entre una instancia local o en la nube y el **nombre de las trazas** (`trace_name`), que además se utiliza como nombre del *dataset run* asociado a la evaluación.

> ⚠️ **Nota sobre Langfuse Cloud**  
>  Si se utiliza **Langfuse Cloud**, es necesario activar el nodo **Esperar 20 Segundos** que se encuentra al final de cada evaluador. Este nodo introduce una pequeña pausa entre la carga de una traza y otra para evitar superar el **rate limit de carga** de Langfuse Cloud durante las evaluaciones.

## Generadores de trazas

Los siguientes nodos permiten generar las trazas necesarias para evaluar distintas versiones de Scored-Gated-RAG.
 Cada uno incluye la lógica para llamar, como **subworkflow**, a cualquiera de los evaluadores disponibles, dependiendo de qué métrica se desee medir:

- **`generate_traces_score-gated-rag-v1`**
   Genera las trazas para la primera versión de Scored-Gated-RAG.
- **`generate_traces_score-gated-rag-v2`**
   Genera las trazas para la segunda versión de Scored-Gated-RAG.
- **`generate_traces_score-gated-rag-v2-multiturno`**
   Genera las trazas para la segunda versión de Scored-Gated-RAG con soporte adicional para manejar memoria dentro de una misma conversación.
   Para utilizar este generador, el dataset multiturno asociado debe contar con un **ID de conversación**, lo que permite evaluar la relevancia y correcta utilización del contexto previo.

> **Nota:**
>  Dentro de cada *generate traces* se puede seleccionar dinámicamente cuál evaluador ejecutar como subworkflow (`evaluation_metrics_accuracy`, `evaluation_metrics_accuracy+wildbench` o `evaluation_metrics_wildbench`), dependiendo de los objetivos de evaluación.

## Evaluadores compatibles

Los siguientes evaluadores soportan la configuración de parámetros generalizados y pueden ser llamados desde cualquiera de los generadores de trazas:

1. **`evaluation_metrics_accuracy`**
    Calcula únicamente **accuracy**.
2. **`evaluation_metrics_accuracy+wildbench`**
    Calcula **accuracy** y también genera un registro del benchmark **WildBench**.
3. **`evaluation_metrics_wildbench`**
    Ejecuta exclusivamente la evaluación **WildBench**, sin métricas de accuracy.

Más información sobre WildBench en el paper oficial:
 👉 [WildBench: Benchmarking LLMs for Instruction Following](https://allenai.github.io/WildBench/WildBench_paper.pdf)

## Parámetros configurables

Al utilizar evaluadores que incluyen **WildBench** (2 y 3), es necesario configurar correctamente el nodo **`set checklist for wildbench`**, donde se define la *checklist* utilizada por el modelo seleccionado como **LLM-as-a-Judge** para evaluar las respuestas del chatbot.