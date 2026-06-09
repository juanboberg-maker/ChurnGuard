# ChurnGuard — Predicción de abandono de clientes

Proyecto final del Bootcamp de Data Analytics. El objetivo era construir un sistema capaz de predecir qué clientes de una compañía de telecomunicaciones tienen más probabilidad de abandonar el servicio, y hacerlo de forma que tenga sentido de negocio real, no solo técnico.

---

## El problema

El dataset de IBM Telco tiene una tasa de churn del 26.5%, lo que significa que aproximadamente 1 de cada 4 clientes se va. El reto no es solo predecirlo, sino predecirlo bien teniendo en cuenta lo que cuesta equivocarse.

Perder a un cliente que podría haberse retenido cuesta alrededor de 200 euros. Hacer una llamada de retención innecesaria cuesta 5 euros. Eso es un ratio de 40 a 1, y ese número lo cambia todo a la hora de tomar decisiones sobre el modelo.

---

## Los datos

Se trabajó con el dataset público de IBM Telco Customer Churn, que contiene 7.043 registros y 21 variables. Incluye información demográfica del cliente, los servicios contratados, el tipo de contrato, el método de pago y las cargas mensuales y totales.

Una cosa importante que se detectó durante el análisis: la variable TotalCharges es en gran medida el resultado de multiplicar tenure por MonthlyCharges, lo que introduce cierta multicolinealidad. No es un problema grave, pero hay que tenerlo en cuenta.

---

## El modelo

Se probaron cuatro algoritmos: Logistic Regression, Random Forest, AdaBoost y Gradient Boosting. Comparados con el threshold por defecto de 0.50, Gradient Boosting era el ganador claro en recall (0.82). Pero el threshold por defecto no tiene ningún sentido aquí.

Al bajar el threshold a 0.30, Logistic Regression alcanza un recall de 0.927, prácticamente idéntico al mejor modelo pero con una ventaja enorme: es completamente interpretable. Puedes mirar los coeficientes y saber exactamente qué está pasando. Con Gradient Boosting no tienes eso.

Se validó con GridSearchCV sobre 25 combinaciones y 5 folds. El parámetro óptimo resultó ser C=1, que es el valor por defecto. Eso no es un fracaso, es una confirmación de que el modelo base ya estaba bien calibrado.

---

## Hallazgos principales

El contrato mensual es el factor de riesgo más claro. Los clientes con contrato month-to-month tienen una tasa de churn muy superior a los que tienen contratos anuales o bianuales. Tiene sentido: menos compromiso, más facilidad para irse.

Los clientes de fibra óptica también presentan más churn que los de DSL. Puede parecer contraintuitivo porque es el servicio premium, pero probablemente refleja que hay más competencia en ese segmento y que las expectativas son más altas.

Los clientes nuevos, con menos de 12 meses de antigüedad, son los más vulnerables. Pasado ese primer año, la probabilidad de abandono baja considerablemente.

El método de pago con cheque electrónico también correlaciona con más churn. Posiblemente indica un perfil de cliente menos comprometido con la automatización del pago.

---

## Resultados

Con el threshold optimizado a 0.30 el modelo detecta 521 de los 561 churners reales del dataset. El AUC-ROC es de 0.844, que indica una capacidad discriminativa alta.

En términos de negocio, si se actúa sobre esas predicciones con una campaña de retención de 200 euros por cliente recuperado y 5 euros por llamada, el beneficio neto estimado es de alrededor de 101.800 euros por ciclo. Frente a los 0 euros que genera no hacer nada, la diferencia es evidente.

---

## Conclusiones

La decisión mas importante del proyecto no fue técnica, fue de negocio: entender que optimizar el threshold es más valioso que optimizar el algoritmo. Pasamos de detectar 236 churners a 521 simplemente ajustando ese parámetro.

La segunda conclusión es que la interpretabilidad tiene valor real. Un modelo que puedes explicar a un equipo de marketing o a un director comercial es mucho más útil que uno que da mejores métricas pero nadie entiende.

Y la tercera es que GridSearchCV confirmando el valor por defecto no es una mala noticia. Es información: el modelo no necesitaba más complejidad.

---

## Aspectos a mejorar

El dataset es estático y de 2017. Un modelo en producción necesitaría datos actualizados y un proceso de reentrenamiento periódico para no quedarse obsoleto.

No hay variables de satisfacción del cliente. NPS, tickets de soporte, tiempos de respuesta del servicio técnico... todo eso probablemente mejoraría la capacidad predictiva de forma significativa.

El modelo trata todos los casos de churn igual, pero no es lo mismo un cliente que se va porque encontró una oferta mejor que uno que se va porque tuvo una mala experiencia. Distinguir entre churn voluntario e involuntario permitiría estrategias de retención mucho más precisas.

Por último, el desbalance de clases (73.5% vs 26.5%) se gestionó con el ajuste de threshold, pero técnicas como SMOTE o class_weight podrían explorarse para ver si mejoran el rendimiento base antes de optimizar el umbral.

---

## Stack utilizado

Python, Pandas, Scikit-learn, Plotly, Streamlit. Dataset: IBM Telco Customer Churn (Kaggle).

---

Proyecto desarrollado por Juan Boberg Aguirre — Bootcamp Data Analytics 2024.