# TalentGuard 🛡️
## Sistema Inteligente para la Predicción del Riesgo de Rotación de Empleados

**Autor:** Nicolas Gomez  
**Programa:** Tecnología en Desarrollo de Software  
**Diplomado:** Desarrollo Web para Analítica de Datos  
**Fecha:** Junio 2026  

---

## Descripción del Proyecto

TalentGuard es una aplicación web analítica orientada a predecir el riesgo de rotación voluntaria de empleados en empresas de construcción e ingeniería. A partir de variables como satisfacción laboral, horas extra, balance vida-trabajo, antigüedad e ingresos mensuales, el sistema clasifica a cada empleado según su probabilidad de abandono (Yes / No), con el fin de apoyar al área de Recursos Humanos en la priorización de estrategias de retención de talento.

---

## Problema

Las organizaciones de construcción e ingeniería enfrentan alta rotación en áreas estratégicas como planeación y gestión de proyectos. Sin una herramienta predictiva, las intervenciones de retención ocurren de forma reactiva, cuando ya es demasiado tarde para revertir la decisión del empleado.

---

## Pregunta Analítica

¿Es posible clasificar el riesgo de abandono voluntario (`Attrition`: Yes/No) de un empleado a partir de variables como satisfacción laboral, horas extra, balance vida-trabajo, antigüedad e ingresos mensuales, con el fin de priorizar estrategias de retención por parte del área de Recursos Humanos?

---

## Dataset

| Atributo | Detalle |
|---|---|
| **Nombre** | IBM HR Analytics Employee Attrition & Performance |
| **Fuente** | [Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) |
| **Licencia** | CC0 (Dominio Público) |
| **Registros** | 1.470 |
| **Variables originales** | 35 |
| **Variables tras limpieza** | 44 (con OHE) |
| **Variable objetivo** | `Attrition` (Yes / No → 1 / 0) |

---

## Tipo de Tarea y Métrica

- **Tarea:** Clasificación binaria
- **Métrica principal:** F1-Score
- **Justificación:** El dataset presenta desbalance de clases (83.9% No / 16.1% Yes), por lo que el F1-Score es más adecuado que el accuracy para evaluar el modelo.

---

## Hallazgos Principales del EDA

- Empleados con horas extra tienen tasa de abandono del **30.5%** vs **10.4%** sin horas extra
- Mediana salarial: quienes abandonan **$3.202** vs quienes permanecen **$5.204**
- El **61%** de los abandonos ocurren en los primeros **3 años** de antigüedad
- A menor satisfacción laboral, mayor tasa de abandono: **22.8%** en nivel Low vs **11.3%** en Very High

---

## Pipeline de Datos

El dataset crudo (35 variables) pasa por un pipeline reproducible que genera un dataset procesado listo para el modelado:

| Paso | Acción | Resultado |
|---|---|---|
| Diagnóstico inicial | Shape, dtypes, nulos, duplicados | Sin problemas detectados |
| Columnas constantes | Eliminación de `EmployeeCount`, `Over18`, `StandardHours`, `EmployeeNumber` | −4 columnas |
| Codificación binaria | `Attrition`, `OverTime`, `Gender` → 0/1 | — |
| Codificación ordinal | `BusinessTravel` → 0/1/2 | — |
| One-Hot Encoding | `Department`, `EducationField`, `JobRole`, `MaritalStatus` | +17 columnas dummy |
| Split train/test | 80% / 20%, `stratify=Attrition`, `random_state=42` | 1.176 train / 294 test |

El escalado numérico se aplica en el notebook de modelado, ajustado exclusivamente sobre el conjunto de entrenamiento para evitar fuga de datos.

---

## Resultados del Modelo

Se compararon dos algoritmos sobre el conjunto de test (294 registros, split 80/20 estratificado):

| Modelo | Accuracy | F1-macro | F1-Yes | Precision | Recall | ROC-AUC |
|---|---|---|---|---|---|---|
| **Logistic Regression** ✅ | 0.7653 | **0.6611** | 0.4733 | 0.6464 | 0.7225 | 0.7986 |
| Random Forest | 0.8299 | 0.6135 | 0.3243 | 0.6567 | 0.5973 | 0.7793 |

**Modelo seleccionado:** Logistic Regression — mejor F1-macro sobre test.

El modelo detecta **2 de cada 3 empleados** que realmente van a renunciar (recall clase Yes = 0.66). La configuración `class_weight='balanced'` prioriza no perder casos reales de abandono (minimizar falsos negativos), que en el contexto de RRHH es el error más costoso.

El modelo serializado responde directamente la pregunta analítica del proyecto y será cargado por el dashboard sin reentrenamiento en tiempo de ejecución.

---

## Arquitectura de la Solución

El sistema se organiza en cuatro capas que transforman el dataset crudo en un dashboard interactivo de predicción:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   DATOS      │    │  PIPELINE    │    │  MODELO ML       │    │  DASHBOARD       │
│   CRUDOS     │───▶│  DE ETL      │───▶│  (Pipeline       │───▶│  STREAMLIT       │
│  data/raw/   │    │ 02_EDA_      │    │   sklearn)       │    │  app_final.py    │
│              │    │ limpieza     │    │  .pkl + JSON     │    │  tabs + filtros  │
└──────────────┘    └──────────────┘    └──────────────────┘    └──────────────────┘
```

Para el detalle completo, ver la página de [Arquitectura](arquitectura.md).

---

## Estructura del Repositorio

```
TalentGuard/
├── README.md
├── .gitignore
├── requirements.txt               ← Dependencias con versiones fijas
├── app_final.py                   ← Dashboard Streamlit
│
├── data/
│   ├── raw/                       ← Dataset original sin modificar
│   │   └── WA_Fn-UseC_-HR-Employee-Attrition.csv
│   └── processed/                 ← Dataset limpio listo para modelado
│       ├── dataset_limpio.csv     ← 1.470 registros × 44 columnas
│       ├── X_train.csv            ← 1.176 registros (80%)
│       ├── X_test.csv             ← 294 registros (20%)
│       ├── y_train.csv
│       └── y_test.csv
│
├── notebooks/
│   ├── 01_exploracion.ipynb       ← Análisis exploratorio inicial
│   ├── 02_eda_limpieza.ipynb      ← Pipeline de limpieza y preparación
│   └── 03_modelado.ipynb          ← Experimentación y selección del modelo
│
├── src/
│   └── ml/
│       └── entrenar_modelo.py     ← Script de entrenamiento reproducible
│
├── models/
│   ├── modelo_final.pkl           ← Pipeline serializado (StandardScaler + LR)
│   └── model_metadata.json        ← Métricas y metadatos del modelo
│
├── charts/                        ← Gráficos generados por los notebooks
│   ├── fig_attrition_distribucion.png
│   ├── fig_comparacion_modelos.png
│   ├── fig_curva_roc.png
│   ├── fig_matriz_confusion.png
│   ├── fig_feature_importance.png
│   ├── fig_overtime_attrition.png
│   ├── fig_income_attrition.png
│   ├── fig_years_attrition.png
│   ├── fig_jobsatisfaction_attrition.png
│   ├── fig_worklife_attrition.png
│   └── fig_correlacion_attrition.png
│
├── docs/                          ← Documentación técnica
│   ├── ficha_proyecto.md
│   ├── analisis_dataset.md
│   ├── diccionario_datos.md
│   ├── arquitectura.md
│   ├── reflexion_etica.md
│   ├── wireframe_dashboard.png
│   └── charts/
│
└── .github/
    └── workflows/
        └── deploy-docs.yml        ← CI/CD para GitHub Pages
```

---

## Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| Python | 3.12 | Lenguaje principal |
| pandas | 2.1.4 | Manipulación de datos |
| numpy | 1.26.2 | Operaciones numéricas |
| scikit-learn | 1.3.2 | Modelado, pipelines, métricas |
| joblib | 1.3.2 | Serialización del modelo |
| Streamlit | 1.29.0 | Dashboard web interactivo |
| matplotlib | 3.8.2 | Visualización de datos |
| seaborn | 0.13.0 | Visualización estadística |
| MkDocs Material | 9.5.27 | Documentación web |
| Git / GitHub | — | Control de versiones y CI/CD |

---

## Consideraciones Éticas

TalentGuard está diseñado como una **herramienta de apoyo a la retención de talento**, no como un sistema de evaluación o clasificación automática de personal. Principios fundamentales:

1. **El resultado es una estimación**, no una decisión automática.
2. **La decisión final** es responsabilidad exclusiva del área de Recursos Humanos.
3. **El modelo puede equivocarse**: el F1 para la clase de abandono (Yes) es de 0.47, lo que significa que aproximadamente 1 de cada 2 empleados en riesgo podría no ser detectado.
4. **Los datos son sintéticos**: fueron generados por IBM, no provienen de una empresa real del sector construcción.

El dashboard incluye una advertencia ética visible y el resultado se presenta siempre con interpretación en lenguaje natural, no como un número aislado.

Para el análisis completo, ver la página de [Reflexión Ética](reflexion_etica.md).

---

## Cómo Ejecutar

```bash
# 1. Clonar el repositorio
git clone https://github.com/NickGV/TalentGuard.git
cd TalentGuard

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el dashboard
streamlit run app_final.py
# Abre http://localhost:8501

# 5. (Opcional) Reentrenar el modelo desde terminal
python src/ml/entrenar_modelo.py

# 6. (Opcional) Explorar notebooks
jupyter notebook notebooks/
```
