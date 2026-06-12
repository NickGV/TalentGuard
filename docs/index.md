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

## Estructura del Repositorio

```
TalentGuard/
├── data/
│   ├── raw/
│   │   └── WA_Fn-UseC_-HR-Employee-Attrition.csv
│   └── processed/
│       ├── dataset_limpio.csv
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       └── y_test.csv
├── notebooks/
│   ├── 01_exploracion.ipynb
│   ├── 02_eda_limpieza.ipynb
│   └── 03_modelado.ipynb
├── models/
│   ├── modelo_final.pkl
│   └── model_metadata.json
├── src/
│   └── ml/
│       └── entrenar_modelo.py
├── docs/
│   ├── ficha_proyecto.md
│   ├── analisis_dataset.md
│   ├── diccionario_datos.md
│   ├── arquitectura.md            ← en desarrollo
│   └── wireframe_dashboard.png
├── app_final.py                   ← en desarrollo
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Tecnologías Utilizadas

- Python 3.x
- pandas, numpy
- matplotlib, seaborn
- scikit-learn (train_test_split, LabelEncoder, Pipeline)
- joblib (serialización del modelo)
- Streamlit (dashboard web)
- Jupyter Notebook
- Git / GitHub
- MkDocs Material (documentación web)
- **Diseño UI:** [Stitch by Google](https://stitch.withgoogle.com/)

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

# 4. Exploración inicial
jupyter notebook notebooks/01_exploracion.ipynb

# 5. Pipeline de limpieza
jupyter notebook notebooks/02_eda_limpieza.ipynb

# 6. Modelado y serialización (notebook interactivo)
jupyter notebook notebooks/03_modelado.ipynb

# 6b. O bien, entrenar desde terminal (reproduce el mismo resultado)
python src/ml/entrenar_modelo.py

# 7. Dashboard
streamlit run app_final.py
```
