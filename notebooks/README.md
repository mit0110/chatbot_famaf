# 📔 Notebooks de Análisis y Evaluación

Este directorio contiene Jupyter Notebooks utilizados durante los diversos experimentos realizados en el desarrollo del chatbot.

## Archivos

### 1. `embeddings_roc_auc_and_f1.ipynb`
* **Descripción:** Este notebook se centra en calcular y visualizar la curva **ROC (Receiver Operating Characteristic)** y el puntaje **AUC (Area Under the Curve)** de distintos modelos de embedding en nuestro conjunto de prueba con 100 preguntas.
* **Objetivos:**
    * Usar la métrica ROC AUC para determinar los mejores modelos de embedding.
    * Calcular F1 macro sobre los 6 mejores modelos.

### 2. `retrieval_score_distribution.ipynb`
* **Descripción:** Realiza un análisis estadístico de la distribución de los puntajes de similitud obtenidos en el proceso de recuperación del modelo usando el conjunto de prueba.
* **Objetivos:**
    * Entender el comportamiento de los puntajes para consultas exitosas vs. fallidas.
    * Ayudar a determinar **umbrales (thresholds)** óptimos de corte.

---

## Uso
Para ejecutar estos notebooks, asegúrate de estar en el archivo `.env` correctamente configurado.
