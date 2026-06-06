# Ficha de Formulación del Proyecto Integrador

## 1. Datos del Estudiante

- **Nombre completo:** Nicolas Gomez
- **Programa:** Tecnología en Desarrollo de Software
- **Fecha:** Junio 2026

---

## 2. Nombre del Proyecto

**TalentGuard: Sistema Inteligente para la Predicción del Riesgo de Rotación de Empleados**

---

## 3. Planteamiento del Problema

En el contexto de una empresa de construcción e ingeniería con múltiples proyectos simultáneos, se presenta una alta rotación voluntaria de personal en áreas estratégicas como planeación y gestión de proyectos. Esta situación afecta directamente al área de Recursos Humanos, que actualmente no cuenta con una herramienta que le permita anticipar qué empleados tienen mayor probabilidad de abandonar la organización antes de que la decisión sea tomada. La rotación recurrente genera costos significativos asociados al reclutamiento, capacitación y pérdida del ritmo operativo, especialmente en roles donde la curva de adaptación impacta directamente la ejecución de los proyectos. Por ello, se propone desarrollar una aplicación web analítica que, a partir del *IBM HR Analytics Employee Attrition & Performance Dataset* (1.470 registros, 35 variables relacionadas con satisfacción laboral, compensación, carga de trabajo, balance vida-trabajo y antigüedad), permita clasificar a cada empleado según su riesgo de abandono (Yes / No), con el fin de que el Gerente de Recursos Humanos pueda priorizar acciones concretas de retención como reuniones de seguimiento, ajustes de carga laboral y programas de desarrollo profesional.

---

## 4. Pregunta Analítica

¿Es posible clasificar el riesgo de abandono voluntario (`Attrition`: Yes/No) de un empleado en una empresa de construcción e ingeniería, a partir de variables como satisfacción laboral, horas extra (`OverTime`), balance vida-trabajo, antigüedad e ingresos mensuales, con el fin de apoyar la identificación temprana de colaboradores con alta probabilidad de abandono y priorizar estrategias de retención por parte del área de Recursos Humanos?

---

## 5. Tipo de Tarea y Métrica de Evaluación

- **Tipo de tarea:** Clasificación binaria
- **Variable objetivo:** `Attrition` — representa si un empleado abandonó la organización (`Yes`) o permaneció en ella (`No`)
- **Métrica principal:** F1-Score
- **Justificación de la métrica:** El dataset presenta un desbalance entre las clases de la variable objetivo `Attrition` (aproximadamente 16% de empleados que abandonan frente a 84% que permanecen). Por lo anterior, la exactitud (*accuracy*) puede ser engañosa, ya que un modelo que siempre prediga "No" obtendría una precisión aparentemente alta sin identificar ningún caso real de abandono. El F1-Score combina *Precision* y *Recall* en una única medida, permitiendo evaluar de forma equilibrada la capacidad del modelo para detectar empleados con riesgo de rotación (`Attrition = Yes`).

---

## 6. Descripción del Dataset

- **Nombre:** IBM HR Analytics Employee Attrition & Performance Dataset
- **Fuente (URL):** https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
- **Licencia:** CC0 (Dominio Público) — uso académico y comercial permitido sin restricciones
- **Número de filas:** 1.470
- **Número de columnas:** 35
- **Descripción general:** Conjunto de datos sintético creado por científicos de datos de IBM. Contiene información demográfica, laboral, salarial y de satisfacción organizacional de empleados, diseñado específicamente para explorar los factores que influyen en la rotación voluntaria de personal. No presenta valores nulos ni registros duplicados, lo que facilita el preprocesamiento. Se identificaron 3 columnas constantes sin valor analítico (`EmployeeCount`, `Over18`, `StandardHours`) que serán eliminadas antes del modelado.

---

## 7. Variables

- **Variable objetivo (y):** `Attrition` — indica si el empleado abandonó (`Yes`) o permaneció (`No`) en la organización.

- **Variables de entrada principales (X):**

| Variable | Tipo | Descripción |
|---|---|---|
| `OverTime` | Categórica | Indica si el empleado realiza horas extra (Yes/No). |
| `JobSatisfaction` | Ordinal (1-4) | Nivel de satisfacción laboral reportado por el empleado. |
| `WorkLifeBalance` | Ordinal (1-4) | Percepción del equilibrio entre vida personal y laboral. |
| `MonthlyIncome` | Numérica | Ingreso mensual del empleado. |
| `YearsAtCompany` | Numérica | Cantidad de años que el empleado ha permanecido en la organización. |
| `EnvironmentSatisfaction` | Ordinal (1-4) | Nivel de satisfacción con el entorno laboral. |
| `Department` | Categórica | Departamento al que pertenece el empleado. |
| `Age` | Numérica | Edad del empleado. |

---

## 8. Usuario Final y Decisión

- **Usuario:** Gerente de Recursos Humanos y equipo del área de gestión del talento humano.
- **Decisión que apoyará:** Identificar empleados con alto riesgo de abandono para priorizar de forma anticipada estrategias de retención como reuniones de seguimiento, ajustes de carga laboral, planes de bienestar y programas de desarrollo profesional.

---

## 9. Implicaciones Éticas

Este proyecto trabaja con datos de empleados y sus predicciones pueden tener un impacto directo en decisiones organizacionales. Se identifican los siguientes riesgos y sus respectivas medidas de mitigación:

| Riesgo | Descripción | Mitigación |
|---|---|---|
| **Sesgo por variables demográficas** | El modelo podría asociar variables como `Gender`, `Age` o `MaritalStatus` con mayor riesgo de abandono, generando predicciones discriminatorias. | Evaluar el impacto de variables demográficas en el modelo. Considerar su exclusión si introducen sesgo injustificado. |
| **Uso punitivo de las predicciones** | La herramienta está diseñada para retener talento, no para despedir empleados. Un uso indebido podría vulnerar los derechos laborales de los trabajadores identificados como "alto riesgo". | Documentar explícitamente que el dashboard es una herramienta de apoyo a la retención. Las decisiones finales deben ser tomadas por personas, no por el modelo. |
| **Privacidad de datos personales** | El procesamiento de datos individuales de empleados puede implicar riesgos de privacidad y confidencialidad. | En un entorno real, aplicar anonimización de datos sensibles y garantizar el cumplimiento de la normativa de protección de datos vigente (Ley 1581 de 2012 en Colombia). |

---

## 10. URL del Repositorio GitHub

> https://github.com/NickGV/TalentGuard

---

*Documento elaborado como parte de la Entrega 1 — Proyecto Integrador*  
*Diplomado en Desarrollo Web — Tecnología en Desarrollo de Software*
