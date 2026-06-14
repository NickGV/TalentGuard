# TalentGuard 🛡️

## Sistema Inteligente para la Predicción del Riesgo de Rotación de Empleados

**Autor:** Nicolas Gomez  
**Programa:** Tecnología en Desarrollo de Software  
**Diplomado:** Desarrollo Web para Analítica de Datos  
**Fecha:** Junio 2026

---

## Descripción

TalentGuard es una aplicación web analítica orientada a predecir el riesgo de rotación voluntaria de empleados en empresas de construcción e ingeniería. A partir de variables como satisfacción laboral, horas extra, balance vida-trabajo, antigüedad e ingresos mensuales, el sistema clasifica a cada empleado según su probabilidad de abandono (Yes / No), con el fin de apoyar al área de Recursos Humanos en la priorización de estrategias de retención de talento.

El proyecto integra un pipeline de limpieza de datos, un modelo de clasificación binaria (Logistic Regression) y un dashboard interactivo desarrollado con Streamlit.

---

## Pregunta Analítica

> ¿Es posible clasificar el riesgo de abandono voluntario (`Attrition`: Yes/No) de un empleado en una empresa de construcción e ingeniería, a partir de variables como satisfacción laboral, horas extra (`OverTime`), balance vida-trabajo, antigüedad e ingresos mensuales, con el fin de apoyar la identificación temprana de colaboradores con alta probabilidad de abandono y priorizar estrategias de retención por parte del área de Recursos Humanos?

---

## Dataset

| Atributo              | Detalle                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------ |
| **Nombre**            | IBM HR Analytics Employee Attrition & Performance                                          |
| **Fuente**            | [Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) |
| **Licencia**          | CC0 (Dominio Público) — uso académico y comercial permitido sin restricciones              |
| **Registros**         | 1.470                                                                                      |
| **Variables**         | 35 (3 constantes eliminadas, 1 identificador eliminado → 31 efectivas)                     |
| **Variable objetivo** | `Attrition` (Yes / No)                                                                     |
| **Desbalance**        | 83.9% No — 16.1% Yes                                                                       |

### Variables principales

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `OverTime` | Binaria | Horas extra (Yes/No) |
| `JobSatisfaction` | Ordinal (1-4) | Satisfacción laboral |
| `WorkLifeBalance` | Ordinal (1-4) | Balance vida-trabajo |
| `MonthlyIncome` | Numérica | Ingreso mensual (USD) |
| `YearsAtCompany` | Numérica | Antigüedad en la empresa |
| `EnvironmentSatisfaction` | Ordinal (1-4) | Satisfacción con el entorno |
| `Department` | Categórica | Departamento |
| `Age` | Numérica | Edad del empleado |

Para la lista completa de las 44 columnas del dataset procesado, consultar [`docs/diccionario_datos.md`](docs/diccionario_datos.md).

---

## Tipo de Tarea y Métrica

- **Tarea:** Clasificación binaria
- **Métrica principal:** F1-Score (macro)
- **Justificación:** El dataset presenta desbalance de clases (83.9% No / 16.1% Yes). El accuracy puede ser engañoso: un modelo que siempre prediga "No" obtendría un 83.9% sin identificar ningún caso real. F1-Score combina precisión y recall, evaluando de forma equilibrada la capacidad del modelo para detectar empleados con riesgo de abandono.

---

## Arquitectura de la Solución

El sistema sigue una arquitectura de 5 capas, más una API REST opcional:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐    ┌──────────────────────┐
│   DATOS      │    │  PIPELINE    │    │  MODELO ML       │    │  DASHBOARD           │
│   CRUDOS     │───▶│  DE ETL      │───▶│  (Pipeline       │───▶│  STREAMLIT           │
│  data/raw/   │    │ 02_EDA_      │    │   sklearn)       │    │  app_final.py        │
│              │    │ limpieza     │    │  .pkl + JSON     │    │  7 secciones + filt. │
└──────────────┘    └──────────────┘    └──────────────────┘    └──────────────────────┘
                                                                          │
                                                                          ▼
                                                              ┌──────────────────────┐
                                                              │  API REST (Bonus)    │
                                                              │  FastAPI             │
                                                              │  /predict + /docs    │
                                                              └──────────────────────┘
```

1. **Datos:** Dataset original en `data/raw/`, procesado en `data/processed/`
2. **Pipeline ETL:** Notebook `02_eda_limpieza.ipynb` con limpieza, codificación y split
3. **Modelo ML:** Logistic Regression con StandardScaler en Pipeline, serializado con joblib
4. **Dashboard (obligatorio):** Streamlit con 7 secciones, sidebar, filtros interactivos y factores de riesgo
5. **API REST (bonificación):** FastAPI expone el modelo como servicio con documentación Swagger en `/docs`

Para el detalle completo, ver [`docs/arquitectura.md`](docs/arquitectura.md).

---

## Estructura del Repositorio

```
TalentGuard/
├── README.md                      ← Este archivo
├── .gitignore
├── requirements.txt               ← Dependencias con versiones fijas
├── app_final.py                   ← Dashboard Streamlit (7 secciones, sidebar)
├── mkdocs.yml                     ← Configuración documentación web
│
├── api/                           ← Bonus: API FastAPI (Ruta A)
│   ├── __init__.py
│   ├── main.py                    ← App FastAPI con 6 endpoints + Swagger
│   └── schemas.py                 ← Modelos Pydantic con validaciones
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
│   ├── 01_exploracion.ipynb       ← Análisis exploratorio inicial (Entrega 1)
│   ├── 02_eda_limpieza.ipynb      ← Pipeline de limpieza y preparación
│   └── 03_modelado.ipynb          ← Experimentación y selección del modelo
│
├── src/
│   └── ml/
│       └── entrenar_modelo.py     ← Script de entrenamiento local reproducible
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
│   ├── ficha_proyecto.md          ← Formulación del proyecto (Entrega 1)
│   ├── analisis_dataset.md        ← Análisis cualitativo del dataset
│   ├── diccionario_datos.md       ← Variables documentadas con tipo, rol y descripción
│   ├── arquitectura.md            ← Arquitectura del sistema
│   ├── reflexion_etica.md         ← Reflexión ética actualizada
│   ├── wiregrame_dashboard.png    ← Wireframe del dashboard
│   └── charts/                    ← Visualizaciones del EDA
│
└── .github/
    └── workflows/
        └── deploy-docs.yml        ← CI/CD para GitHub Pages
```

---

## Instalación y Ejecución

### Requisitos

- Python 3.10+
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/NickGV/TalentGuard.git
cd TalentGuard

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate    # Linux/macOS
# venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el dashboard (obligatorio)
streamlit run app_final.py
# Abre http://localhost:8501

# 5. (Opcional) Ejecutar la API REST (bonificación)
uvicorn api.main:app --reload
# Documentación Swagger: http://127.0.0.1:8000/docs

# 6. (Opcional) Reentrenar el modelo
python src/ml/entrenar_modelo.py

# 7. (Opcional) Explorar notebooks
jupyter notebook notebooks/
```

### Documentación Web

La documentación completa del proyecto está publicada en GitHub Pages:

🔗 **https://nickgv.github.io/TalentGuard/**

Para ejecutarla localmente:
```bash
pip install mkdocs-material
mkdocs serve
# Abre http://127.0.0.1:8008
```

---

## Resultados del Modelo

### Modelo seleccionado: **Logistic Regression**

| Métrica | Valor |
|---------|-------|
| **F1-macro** (principal) | **0.6611** |
| F1-Yes (clase abandono) | 0.4733 |
| Accuracy | 0.7653 |
| Precision (macro) | 0.6464 |
| Recall (macro) | 0.7225 |
| ROC-AUC | 0.7986 |

### Comparación con Random Forest

| Modelo | F1-macro | F1-Yes | ROC-AUC |
|--------|----------|--------|---------|
| **Logistic Regression** | **0.6611** | 0.4733 | **0.7986** |
| Random Forest | 0.6135 | 0.3243 | 0.7793 |

### Interpretación de resultados

- El modelo detecta correctamente **2 de cada 3** empleados que realmente van a abandonar (recall de 0.66 en clase Yes).
- El F1-Yes (0.47) es estructuralmente más bajo debido al desbalance 84/16: con solo 47 casos de abandono en test, cada error tiene un impacto desproporcionado.
- `class_weight='balanced'` prioriza el recall sobre la precisión, que es la estrategia correcta para retención de talento: es mejor tener una conversación innecesaria (falso positivo) que perder a un empleado sin haber intentado retenerlo (falso negativo).

---

## API REST (Bonificación — Ruta A)

TalentGuard expone el modelo de Machine Learning como servicio REST a través de FastAPI, con documentación Swagger interactiva.

### Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Información general de la API |
| `GET` | `/health` | Estado del servicio y versión del modelo |
| `GET` | `/datos` | Resumen del dataset (filas, tasa de rotación) |
| `GET` | `/variables` | Lista de 18 campos aceptados por `/predict` |
| `GET` | `/metricas` | Métricas de evaluación del modelo |
| `POST` | `/predict` | Predice el riesgo de abandono de un empleado |

### Documentación Swagger

La API incluye documentación interactiva generada automáticamente:

🔗 **http://127.0.0.1:8000/docs**

### Ejemplo de uso

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 35,
    "Gender": 1,
    "MaritalStatus": "Single",
    "MonthlyIncome": 5000,
    "OverTime": 1,
    "JobSatisfaction": 3,
    "Department": "Sales",
    "JobRole": "Sales Executive"
    ...
  }'
```

Respuesta:
```json
{
  "probabilidad_abandono": 0.7516,
  "probabilidad_permanencia": 0.2484,
  "riesgo": "ALTO",
  "prediccion": 1,
  "advertencia": "Estimación estadística basada en patrones históricos..."
}
```

---

## Consideraciones Éticas

TalentGuard está diseñado como una **herramienta de apoyo a la retención de talento**, no como un sistema de evaluación automática de personal.

### Principios guía

1. **El resultado es una estimación**, no una decisión automática.
2. **La decisión final** es responsabilidad exclusiva del área de Recursos Humanos.
3. **El modelo puede equivocarse**: 1 de cada 2 empleados con riesgo de abandono podría no ser detectado (F1-Yes de 0.47).
4. **Los datos son sintéticos**: el modelo fue entrenado con datos generados artificialmente, no con datos reales del sector.

### Mitigaciones implementadas

- Advertencia ética visible en el dashboard.
- Interpretación en lenguaje natural (no solo un número).
- Transparencia en factores de riesgo que contribuyen a la predicción.
- Métricas reportadas honestamente, incluyendo limitaciones.

Para el análisis completo, ver [`docs/reflexion_etica.md`](docs/reflexion_etica.md).

---

## Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| Python | 3.12 | Lenguaje principal |
| pandas | 3.0.3 | Manipulación de datos |
| numpy | 2.4.6 | Operaciones numéricas |
| scikit-learn | 1.9.0 | Modelado y pipelines |
| joblib | 1.5.0 | Serialización del modelo |
| Streamlit | 1.58.0 | Dashboard web |
| FastAPI | 0.136.3 | API REST (bonificación) |
| uvicorn | 0.49.0 | Servidor ASGI para FastAPI |
| pydantic | 2.13.4 | Validación de datos en API |
| matplotlib | 3.10.9 | Visualización |
| seaborn | 0.13.2 | Visualización estadística |
| MkDocs Material | 9.5.27 | Documentación web |
| Git / GitHub | — | Control de versiones |

---

## Resultados de Aprendizaje

Durante el desarrollo de este proyecto integrador se aplicaron los siguientes conocimientos:

- **Semana 1:** Formulación del problema analítico y selección del dataset
- **Semana 2:** Pipeline de limpieza, EDA, codificación de variables y diccionario de datos
- **Semana 3:** Modelado ML, comparación de algoritmos, serialización y dashboard Streamlit
- **Semana 4:** Documentación técnica, arquitectura, reflexión ética, API REST (Ruta A), dashboard con 7 secciones, y presentación final

---

## Autor

**Nicolas Gomez**  
Tecnología en Desarrollo de Software  
Diplomado en Desarrollo Web para Analítica de Datos  
Junio 2026

---

[![Documentación](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://nickgv.github.io/TalentGuard/)
[![Dataset](https://img.shields.io/badge/dataset-Kaggle-20BEFF)](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
