# Arquitectura del Sistema — TalentGuard

**Proyecto:** TalentGuard: Sistema Inteligente para la Predicción del Riesgo de Rotación de Empleados  
**Autor:** Nicolas Gomez  
**Programa:** Tecnología en Desarrollo de Software  
**Diplomado:** Desarrollo Web para Analítica de Datos  
**Fecha:** Junio 2026

---

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           TALENTGUARD                                    │
│                  Sistema de Predicción de Rotación                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────────┐   │
│  │   DATOS       │    │  PIPELINE    │    │     MODELO ML             │   │
│  │              │    │  DE ETL      │    │                          │   │
│  │  raw/        │───▶│              │───▶│  Logistic Regression      │   │
│  │  WA_Fn...csv │    │ 02_EDA_     │    │  + StandardScaler         │   │
│  │              │    │ limpieza    │    │                          │   │
│  │  Kaggle IBM  │    │              │    │  modelo_final.pkl         │   │
│  │  HR Dataset  │    │ - limpieza  │    │  model_metadata.json      │   │
│  └──────────────┘    │ - OHE       │    └─────────────┬────────────┘   │
│                       │ - split     │                  │                │
│                       └──────────────┘                  │                │
│                                                         │ joblib.load   │
│                                                         ▼                │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                   DASHBOARD STREAMLIT                             │   │
│  │                                                                  │   │
│  │  ┌─────────────────────────┐  ┌──────────────────────────────┐   │   │
│  │  │  Tab 1: Análisis        │  │  Tab 2: Predicción           │   │   │
│  │  │  Exploratorio           │  │                              │   │   │
│  │  │                         │  │  Formulario de entrada       │   │   │
│  │  │  - 5 visualizaciones    │  │  → modelo → resultado        │   │   │
│  │  │  - Filtros interactivos │  │  → interpretación            │   │   │
│  │  │  - Métricas dinámicas   │  │  → factores de riesgo        │   │   │
│  │  └─────────────────────────┘  └──────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │              DOCUMENTACIÓN (GitHub Pages / MkDocs)                │   │
│  │  docs/ → ficha_proyecto, analisis_dataset, diccionario_datos,    │   │
│  │           arquitectura, reflexion_etica, wireframe_dashboard      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Componentes del Sistema

### 1.1 Capa de Datos

| Componente | Descripción | Tecnología |
|-----------|-------------|------------|
| `data/raw/` | Dataset original sin modificar (IBM HR Analytics CSV) | CSV |
| `data/processed/` | Dataset limpio y codificado listo para modelado (`dataset_limpio.csv`, `X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`) | pandas, scikit-learn |

### 1.2 Capa de Preparación (ETL)

| Componente | Descripción | Tecnología |
|-----------|-------------|------------|
| `notebooks/01_exploracion.ipynb` | Análisis exploratorio inicial y visualizaciones | pandas, matplotlib, seaborn |
| `notebooks/02_eda_limpieza.ipynb` | Pipeline de limpieza: eliminación de constantes, codificación OHE, separación train/test | pandas, scikit-learn |

**Transformaciones aplicadas:**
- Eliminación de columnas constantes (`EmployeeCount`, `Over18`, `StandardHours`)
- Eliminación de `EmployeeNumber` (sin valor predictivo)
- Codificación binaria: `Gender` (Male→1/Female→0), `OverTime` (Yes→1/No→0)
- Codificación ordinal: `BusinessTravel` (Non-Travel→0, Travel_Rarely→1, Travel_Frequently→2)
- One-Hot Encoding: `Department`, `EducationField`, `JobRole`, `MaritalStatus`
- Separación train/test: 80/20 estratificada con `random_state=42`

### 1.3 Capa de Modelado

| Componente | Descripción | Tecnología |
|-----------|-------------|------------|
| `notebooks/03_modelado.ipynb` | Experimentación: comparación de 2 algoritmos, selección del mejor | scikit-learn |
| `src/ml/entrenar_modelo.py` | Script reproducible de entrenamiento (alternativa al notebook) | scikit-learn, joblib |
| `models/modelo_final.pkl` | Pipeline serializado: StandardScaler + Logistic Regression | joblib |
| `models/model_metadata.json` | Métricas de evaluación y metadatos del modelo | JSON |

**Pipeline del modelo:**
```
StandardScaler → LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
```

### 1.4 Capa de Presentación (Dashboard)

| Componente | Descripción | Tecnología |
|-----------|-------------|------------|
| `app_final.py` | Dashboard interactivo con dos pestañas | Streamlit |
| Tab 1: Análisis Exploratorio | 5 visualizaciones, 3 filtros interactivos, métricas del dataset | matplotlib, Streamlit |
| Tab 2: Predicción | Formulario de 15 campos, predicción en vivo, interpretación, factores de riesgo | Streamlit, joblib |

**Características del dashboard:**
- Carga del modelo serializado con `@st.cache_resource`
- Métricas dinámicas desde `model_metadata.json` (sin valores hardcodeados)
- Advertencia ética: "El resultado es una estimación, no una decisión automática"
- Interpretación en lenguaje natural del resultado
- Factores de riesgo contextuales basados en el perfil ingresado

### 1.5 Capa de Documentación

| Componente | Descripción | Tecnología |
|-----------|-------------|------------|
| `docs/` | Documentación técnica del proyecto | Markdown |
| `mkdocs.yml` | Configuración de sitio web de documentación | MkDocs Material |
| GitHub Pages | Documentación desplegada automáticamente | GitHub Actions + MkDocs |

---

## 2. Flujo de Datos

```
[Kaggle IBM HR Dataset] 
        │
        ▼
┌───────────────────┐
│  data/raw/        │  ← Dataset original (1.470 registros, 35 columnas)
└───────────────────┘
        │
        ▼
┌──────────────────────────────────────────────┐
│  notebooks/02_eda_limpieza.ipynb              │
│                                              │
│  1. Carga y diagnóstico                       │
│  2. Eliminación de constantes (3 columnas)    │
│  3. Eliminación de EmployeeNumber             │
│  4. Codificación de categóricas               │
│  5. One-Hot Encoding (4 variables → 19 cols) │
│  6. Separación train/test (80/20)             │
└──────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────┐
│  data/processed/           │  ← Dataset procesado (1.470 × 44)
│  ├── dataset_limpio.csv    │
│  ├── X_train.csv (1.176)   │
│  ├── X_test.csv  (294)     │
│  ├── y_train.csv           │
│  └── y_test.csv            │
└────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────┐
│  src/ml/entrenar_modelo.py / 03_modelado.ipynb│
│                                              │
│  1. Carga de datos procesados                 │
│  2. Definición de pipelines                   │
│  3. Entrenamiento: LogisticRegression vs RF   │
│  4. Evaluación sobre test                     │
│  5. Selección del mejor (F1-macro)            │
│  6. Serialización con joblib                  │
└──────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────┐
│  models/                    │
│  ├── modelo_final.pkl      │  ← Pipeline serializado
│  └── model_metadata.json   │  ← Métricas y metadatos
└────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────┐
│  app_final.py (Streamlit)                     │
│                                              │
│  joblib.load(modelo_final.pkl)                │
│  json.load(model_metadata.json)               │
│  pd.read_csv(dataset_limpio.csv)              │
│                                              │
│  ┌─────────────┐   ┌────────────────┐        │
│  │ EDA + filtros│   │ Predicción     │        │
│  │ + visualizac.│   │ + formulario   │        │
│  └─────────────┘   │ + resultado    │        │
│                     │ + interpretac. │        │
│                     └────────────────┘        │
└──────────────────────────────────────────────┘
```

---

## 3. Tecnologías por Capa

| Capa | Tecnología | Versión | Propósito |
|-----|-----------|---------|-----------|
| **Lenguaje** | Python | 3.12 | Lenguaje principal del proyecto |
| **Procesamiento** | pandas | 2.1.4 | Manipulación y limpieza de datos |
| **Numérico** | numpy | 1.26.2 | Operaciones numéricas y matriciales |
| **Machine Learning** | scikit-learn | 1.3.2 | Modelado, pipelines, métricas |
| **Serialización** | joblib | 1.3.2 | Guardado/carga del modelo |
| **Dashboard** | Streamlit | 1.29.0 | Visualización interactiva web |
| **Visualización** | matplotlib | 3.8.2 | Gráficos estáticos |
| | seaborn | 0.13.0 | Visualización estadística |
| **Entorno** | Jupyter | 1.1.1 | Notebooks de exploración y modelado |
| **Documentación** | MkDocs Material | 9.5.27 | Sitio web de documentación |
| **Control de versiones** | Git / GitHub | — | Repositorio y despliegue |

---

## 4. Decisiones Técnicas

### 4.1 Pipeline de Modelado (no data leakage)

Se utiliza `sklearn.pipeline.Pipeline` para encapsular `StandardScaler` + `LogisticRegression`. El escalado se ajusta **exclusivamente sobre el conjunto de entrenamiento** y se aplica sobre test, evitando fuga de datos.

### 4.2 Serialización Local

El modelo se entrena y serializa en el mismo entorno local donde corre Streamlit. Esto evita conflictos de versiones de scikit-learn (error crítico si se entrena en Colab y se carga localmente).

### 4.3 Manejo del Desbalance

Se usa `class_weight='balanced'` para compensar el desbalance 84/16 en `Attrition`. La métrica principal es F1-macro, no accuracy.

### 4.4 Caché en Streamlit

Se aplican `@st.cache_resource` y `@st.cache_data` para evitar recargar el modelo, metadatos y datos en cada interacción del usuario.

---

## 5. Diagrama de Despliegue

```
┌─────────────────────────────────────────┐
│         Computador Local                │
│                                         │
│  ┌───────────────┐  ┌────────────────┐  │
│  │ Entorno       │  │ Dashboard      │  │
│  │ Virtual (venv)│  │ Streamlit      │  │
│  │               │  │                │  │
│  │ Python 3.12   │  │ localhost:8501 │  │
│  │ scikit-learn  │  │                │  │
│  │ joblib        │  │ app_final.py   │  │
│  └───────────────┘  └────────────────┘  │
│                                         │
│  ┌─────────────────────────────────────┐ │
│  │ Repositorio GitHub                  │ │
│  │ github.com/NickGV/TalentGuard       │ │
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

*Documento generado como parte de la documentación técnica del Proyecto Integrador*  
*Diplomado en Desarrollo Web — Tecnología en Desarrollo de Software*
