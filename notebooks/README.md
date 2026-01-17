# 📔 Notebooks de Análisis y Evaluación

Este directorio contiene Jupyter Notebooks utilizados durante los diversos experimentos realizados en el desarrollo del chatbot.

## Archivos

### 1. `embeddings_roc_auc.ipynb`
* **Descripción:** Este notebook se centra en calcular y visualizar la curva **ROC (Receiver Operating Characteristic)** y el puntaje **AUC (Area Under the Curve)** de distintos modelos de embedding sobre nuestro conjunto de prueba con 100 preguntas.
* **Objetivos:**
    * Usar la métrica para determinar qué modelo de embedding vamos a utilizar.
    * Probar todos los modelos del experimento con todos los thresholds posibles.

### 2. `retrieval_score_distribution.ipynb`
* **Descripción:** Realiza un análisis estadístico de la distribución de los puntajes de similitud obtenidos en el proceso de recuperación del modelo usando el conjunto de prueba.
* **Objetivos:**
    * Entender el comportamiento de los puntajes para consultas exitosas vs. fallidas.
    * Ayudar a determinar **umbrales (thresholds)** óptimos de corte.

---

## Uso
Para ejecutar estos notebooks, asegúrate de estar en el archivo `.env` correctamente configurado.
