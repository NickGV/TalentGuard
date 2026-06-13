# Reflexión Ética — TalentGuard

**Proyecto:** TalentGuard: Sistema Inteligente para la Predicción del Riesgo de Rotación de Empleados  
**Autor:** Nicolas Gomez  
**Programa:** Tecnología en Desarrollo de Software  
**Diplomado:** Desarrollo Web para Analítica de Datos  
**Fecha:** Junio 2026

---

## 1. Introducción

El presente documento actualiza la reflexión ética inicial formulada en la Entrega 1, incorporando los aprendizajes obtenidos durante el desarrollo del pipeline de datos, el entrenamiento del modelo y la implementación del dashboard. TalentGuard es una herramienta de apoyo a la toma de decisiones en el área de Recursos Humanos, no un sistema automatizado de evaluación de personal.

---

## 2. Riesgos Identificados en el Dataset y el Modelo

### 2.1 Desbalance de Clases

El dataset presenta un desbalance significativo: **83.9%** de empleados que permanecen frente a **16.1%** que abandonan. Este desbalance tiene implicaciones éticas directas:

- **Falsos negativos** (no detectar a un empleado que va a renunciar): el área de RRHH pierde la oportunidad de intervenir, el empleado se va y la organización incurre en costos de reemplazo. Es el error más costoso para el negocio.
- **Falsos positivos** (marcar a alguien que no va a renunciar): se agenda una conversación de seguimiento innecesaria. El costo es bajo, pero puede generar incomodidad o desconfianza en el empleado si no se maneja con cuidado.

**Acción tomada:** Se priorizó el recall sobre la precisión mediante `class_weight='balanced'`, maximizando la detección de casos reales de abandono (recall de 0.66 en clase Yes). El trade-off es aceptable porque el costo de un falso positivo (una conversación) es significativamente menor que el de un falso negativo (pérdida de talento).

### 2.2 Variables Demográficas como Predictores

El modelo incluye variables como `Gender`, `Age` y `MaritalStatus`. Aunque estas variables pueden tener correlación estadística con la rotación, su uso plantea riesgos de sesgo y discriminación:

| Variable | Riesgo |
|----------|--------|
| `Gender` | El modelo podría perpetuar sesgos de género si asocia un género específico con mayor probabilidad de abandono. |
| `Age` | Podría discriminar por edad si empleados mayores o menores son sistemáticamente marcados como riesgo. |
| `MaritalStatus` | Podría penalizar a personas solteras o divorciadas sin justificación laboral real. |

**Acción tomada:**
- El dashboard **incluye una advertencia ética explícita** que recuerda al usuario que el resultado es una estimación y debe ser revisado por una persona responsable.
- La decisión final recae en el área de RRHH, no en el modelo.
- En un despliegue real, se recomienda **evaluar el impacto de estas variables** y considerar su exclusión si introducen sesgo injustificado.

### 2.3 Limitaciones del Dataset Sintético

El dataset utilizado (IBM HR Analytics Employee Attrition & Performance) es **sintético**, creado por científicos de datos de IBM. Aunque replica patrones realistas, no captura la complejidad de una organización real del sector construcción e ingeniería.

**Implicación:** Las predicciones del modelo pueden no generalizar correctamente a un contexto empresarial real. Esto se documenta como una limitación explícita en el dashboard y en este documento.

---

## 3. Grupos Afectados por Errores del Modelo

| Grupo | Cómo podría afectarles un error del modelo |
|-------|---------------------------------------------|
| **Empleados clasificados como alto riesgo** | Podrían ser estigmatizados o tratados de forma diferente si la información no se maneja con confidencialidad. |
| **Empleados no detectados (falsos negativos)** | El área de RRHH no intervendría a tiempo para retenerlos, perdiendo oportunidades de desarrollo y bienestar. |
| **Equipo de RRHH** | Podría tomar decisiones basadas en información inexacta si no se entienden las limitaciones del modelo. |
| **Organización** | Podría invertir recursos en retención de empleados que no estaban en riesgo real (falsos positivos). |

---

## 4. Acciones de Mitigación Implementadas

### 4.1 En el Dashboard (app_final.py)

- **Advertencia ética visible:** Mensaje `st.info()` en la pestaña de predicción:
  > "El resultado es una estimación generada por el modelo. Debe ser revisado por una persona responsable del área de Recursos Humanos antes de tomar cualquier decisión sobre el empleado."

- **Advertencia al pie del resultado:**
  > "Este resultado es generado por un modelo de Machine Learning entrenado sobre datos históricos sintéticos. No representa una evaluación definitiva del empleado ni debe utilizarse como único criterio para decisiones de gestión de personal. La decisión final es responsabilidad exclusiva del área de Recursos Humanos."

- **Interpretación en lenguaje natural:** El resultado no es solo un número, sino un mensaje contextual que sugiere acciones concretas (reunión de seguimiento, plan de desarrollo, revisión salarial), siempre con la recomendación de que RRHH tome la decisión final.

- **Factores de riesgo transparentes:** El dashboard muestra explícitamente qué variables del perfil ingresado contribuyen al riesgo, permitiendo que el usuario entienda el "por qué" detrás de la predicción.

### 4.2 En el Modelo (notebooks/03_modelado.ipynb)

- **Selección por F1-macro:** Se eligió esta métrica porque penaliza el mal rendimiento en la clase minoritaria (abandono), forzando al modelo a aprender patrones relevantes para el caso de uso, no solo accuracy superficial.

- **class_weight='balanced':** Se ajustaron los pesos de clase para que el modelo preste atención equitativa a ambas clases durante el entrenamiento.

- **Evaluación honesta:** Se reportan métricas sobre el conjunto de prueba (no entrenamiento) y se incluye una discusión detallada sobre el trade-off entre precisión y recall en la célula 29 del notebook.

### 4.3 En el Pipeline de Datos (notebooks/02_eda_limpieza.ipynb)

- **No se eliminaron variables demográficas** porque el dataset es sintético y el propósito es académico. En un entorno real, se recomienda evaluar su exclusión si generan sesgo.
- **Separación train/test antes de cualquier transformación** para evitar fuga de datos (data leakage).

---

## 5. Limitaciones Conocidas del Sistema

| Limitación | Descripción | Impacto |
|-----------|-------------|---------|
| **Datos sintéticos** | El modelo fue entrenado con datos generados artificialmente, no con datos reales de una empresa de construcción. | Los patrones pueden no reflejar la realidad del sector. |
| **F1-Yes bajo (0.47)** | El modelo solo detecta correctamente el 47% de los casos de abandono (medido con F1 en clase Yes). | 1 de cada 2 empleados que renuncian podría no ser detectado. |
| **Sin dimensión temporal** | El dataset no incluye fechas, por lo que no es posible predecir *cuándo* ocurrirá el abandono, solo *si* ocurrirá. | La herramienta no puede priorizar por urgencia temporal. |
| **Sin validación en campo** | El modelo no ha sido probado en un entorno organizacional real. | Su eficacia real en retención de talento no ha sido validada. |
| **Variables limitadas** | No incluye factores relevantes como tipo de contrato, clima laboral, liderazgo del supervisor o condiciones del proyecto. | Podrían existir variables más predictivas no capturadas en el dataset. |

---

## 6. Declaración de Uso Responsable

> **El resultado generado por TalentGuard es una estimación basada en un modelo estadístico entrenado con datos sintéticos. No constituye una evaluación definitiva del empleado ni debe utilizarse como único criterio para decisiones de gestión de personal, incluyendo pero no limitándose a: despidos, promociones, cambios salariales o sanciones disciplinarias.**
>
> **La decisión final es responsabilidad exclusiva del área de Recursos Humanos y debe estar fundamentada en el juicio profesional, el conocimiento del contexto organizacional y el diálogo directo con el empleado.**
>
> **TalentGuard está diseñado como una herramienta de apoyo a la *retención* de talento, no como un sistema de evaluación o clasificación automática de personal.**

---

## 7. Recomendaciones para un Despliegue Real

1. **Reentrenar con datos reales** del sector construcción e ingeniería para mejorar la representatividad del modelo.
2. **Evaluar sesgo por variables demográficas** y considerar su exclusión si se detecta impacto discriminatorio.
3. **Implementar anonimización** de datos personales sensibles y cumplir con la normativa de protección de datos (Ley 1581 de 2012 en Colombia).
4. **Establecer un proceso de revisión humana** obligatorio antes de cualquier acción basada en la predicción.
5. **Monitorear el desempeño del modelo** periódicamente y actualizarlo con nuevos datos.
6. **Auditar el uso del sistema** para garantizar que no se desvíe de su propósito original de retención de talento.

---

*Documento actualizado como parte de la Entrega Final del Proyecto Integrador*  
*Diplomado en Desarrollo Web — Tecnología en Desarrollo de Software*
