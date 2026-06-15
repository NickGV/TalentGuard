# Arquitectura del Sistema — TalentGuard

**Proyecto:** TalentGuard: Sistema Inteligente para la Predicción del Riesgo de Rotación de Empleados  
**Autor:** Nicolas Gomez  
**Programa:** Tecnología en Desarrollo de Software  
**Diplomado:** Desarrollo Web para Analítica de Datos  
**Fecha:** Junio 2026

---

## Diagrama de Arquitectura

```
┌──────────────────────────────────────────────────────────────────────────┐
│                            TALENTGUARD                                     │
│                   Sistema de Predicción de Rotación                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────────────────────┐   │
│  │   DATOS      │    │  PIPELINE    │    │       MODELO ML            │   │
│  │   CRUDOS     │    │  DE ETL      │    │                            │   │
│  │              │    │              │    │  Logistic Regression        │   │
│  │  raw/        │───▶│ 02_EDA_     │───▶│  + StandardScaler           │   │
│  │  WA_Fn...csv │    │ limpieza    │    │                            │   │
│  │              │    │              │    │  modelo_final.pkl           │   │
│  │  Kaggle IBM  │    │ - limpieza  │    │  model_metadata.json        │   │
│  │  HR Dataset  │    │ - OHE       │    └─────────────┬──────────────┘   │
│  └──────────────┘    │ - split     │                  │                  │
│                       └──────────────┘                  │                  │
│                                                         │ joblib.load     │
│                                                         ▼                  │
│                    ┌────────────────────────────────────────────────────┐  │
│                    │                  DASHBOARD STREAMLIT                │  │
│                    │  ┌──────────────┐  ┌───────────────────────────┐   │  │
│                    │  │ 7 secciones  │  │  Predicción               │   │  │
│                    │  │ sidebar nav  │  │  Form 18 campos           │   │  │
│                    │  │ 5 charts EDA │  │  → modelo → resultado     │   │  │
│                    │  │ + filtros    │  │  → interpretación         │   │  │
│                    │  └──────────────┘  └───────────────────────────┘   │  │
│                    │  :8501 — app_final.py                              │  │
│                    └────────────────────────────────────────────────────┘  │
│                                                                           │
│                    ┌────────────────────────────────────────────────────┐  │
│                    │             API REST — FastAPI                      │  │
│                    │                                                     │  │
│                    │   GET  /health    GET  /datos    GET  /variables    │  │
│                    │   GET  /metricas  POST /predict                     │  │
│                    │   Documentación Swagger en /docs                    │  │
│                    │  :8000 — api/main.py                                │  │
│                    └──────────────────┬─────────────────────────────────┘  │
│                                       │                                    │
│                                       ▼                                    │
│                    ┌────────────────────────────────────────────────────┐  │
│                    │           WEB APP — Next.js 16                     │  │
│                    │                                                     │  │
│                    │   /          Inicio (KPIs + CTA)                    │  │
│                    │   /data      Datos (diccionario)                   │  │
│                    │   /insights  Análisis (5 charts + filtros)         │  │
│                    │   /predict   Predicción (form + resultado)         │  │
│                    │   /model     Métricas del modelo                   │  │
│                    │   /about     Acerca + ética                        │  │
│                    │  :3000 — web/ (Next.js + TS + Tailwind)            │  │
│                    └────────────────────────────────────────────────────┘  │
│                                                                           │
│                    ┌────────────────────────────────────────────────────┐  │
│                    │        DOCUMENTACIÓN (GitHub Pages / MkDocs)        │  │
│                    │  docs/ → ficha_proyecto, analisis_dataset,         │  │
│                    │  diccionario_datos, arquitectura, reflexion_etica  │  │
│                    └────────────────────────────────────────────────────┘  │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Componentes del Sistema

### 1.1 Capa de Datos

| Componente | Descripción | Tecnología |
|-----------|-------------|------------|
| `data/raw/` | Dataset original sin modificar (IBM HR Analytics CSV) | CSV |
| `data/processed/` | Dataset limpio y codificado listo para modelado | pandas, scikit-learn |

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

### 1.4 Capa de Presentación — Dashboard Streamlit

| Componente | Descripción | Tecnología |
|-----------|-------------|------------|
| `app_final.py` | Dashboard interactivo con 7 secciones y sidebar | Streamlit |
| Sección 1-2: Inicio + Datos | KPIs principales, tabla de datos y diccionario de variables | Streamlit |
| Sección 3: Análisis Exploratorio | 5 visualizaciones, 3 filtros interactivos | matplotlib, Streamlit |
| Sección 4-5: Modelo + Métricas | Explicación del modelo y métricas con interpretación | Streamlit |
| Sección 6: Predicción | Formulario de 18 campos, predicción en vivo, interpretación | Streamlit, joblib |
| Sección 7: Conclusiones | Hallazgos, limitaciones y próximos pasos | Streamlit |

### 1.5 Capa de Servicios — API REST

| Componente | Descripción | Tecnología |
|-----------|-------------|------------|
| `api/main.py` | FastAPI con 6 endpoints y documentación Swagger | FastAPI, uvicorn |
| `api/schemas.py` | Modelos Pydantic con validación de datos | Pydantic |

**Endpoints:**

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Información general |
| `GET` | `/health` | Estado del servicio |
| `GET` | `/datos` | Resumen del dataset |
| `GET` | `/variables` | Campos del formulario de predicción |
| `GET` | `/metricas` | Métricas del modelo |
| `POST` | `/predict` | Predecir riesgo de abandono |

### 1.6 Capa de Presentación — Web App (Next.js)

| Componente | Descripción | Tecnología |
|-----------|-------------|------------|
| `web/` | Frontend moderno que consume la API REST | Next.js 16 + TypeScript |
| Página Inicio (`/`) | Hero + KPIs principales desde la API | Tailwind CSS, shadcn/ui |
| Página Datos (`/data`) | Diccionario de variables y estadísticas | Tailwind CSS |
| Página Insights (`/insights`) | 5 charts interactivos con filtros | Recharts |
| Página Predict (`/predict`) | Formulario 18 campos + resultado con indicador de riesgo | React Hook Form, Zod |
| Página Model (`/model`) | Métricas del modelo con gráfico comparativo | Recharts |
| Página About (`/about`) | Hallazgos, limitaciones, advertencia ética | Tailwind CSS |

### 1.7 Capa de Documentación

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
│  ├── modelo_final.pkl      │  ← Pipeline serializado (joblib)
│  └── model_metadata.json   │  ← Métricas y metadatos
└────────────────────────────┘
        │
        ├──────────────────────────────────────────────────┐
        │                                                  │
        ▼                                                  ▼
┌──────────────────────────────────┐    ┌──────────────────────────────┐
│  app_final.py (Streamlit)        │    │  api/main.py (FastAPI)       │
│  :8501                           │    │  :8000                       │
│                                  │    │                              │
│  joblib.load → predicción        │    │  joblib.load → /predict      │
│  pandas → EDA + visualizaciones  │    │  pandas → /datos             │
│  matplotlib → charts             │    │  JSON → /metricas, /health   │
└──────────────────────────────────┘    └──────────────┬───────────────┘
                                                        │
                                                        ▼
                                              ┌──────────────────────────┐
                                              │  web/ (Next.js)          │
                                              │  :3000                   │
                                              │                          │
                                              │  fetch → getHealth()     │
                                              │  fetch → getDatos()      │
                                              │  fetch → getMetricas()   │
                                              │  fetch → postPredict()   │
                                              │  fetch → datos.json (st) │
                                              └──────────────────────────┘
```

---

## 3. Tecnologías por Capa

### Backend (Python)

| Capa | Tecnología | Versión | Propósito |
|-----|-----------|---------|-----------|
| **Lenguaje** | Python | 3.12 | Lenguaje principal del proyecto |
| **Procesamiento** | pandas | 3.0.3 | Manipulación y limpieza de datos |
| **Numérico** | numpy | 2.4.6 | Operaciones numéricas y matriciales |
| **Machine Learning** | scikit-learn | 1.9.0 | Modelado, pipelines, métricas |
| **Serialización** | joblib | 1.5.0 | Guardado/carga del modelo |
| **Dashboard** | Streamlit | 1.58.0 | Visualización interactiva web |
| **API REST** | FastAPI | 0.136.3 | Servicio REST |
| **Servidor ASGI** | uvicorn | 0.49.0 | Servidor para FastAPI |
| **Validación** | pydantic | 2.13.4 | Validación de datos en API |
| **Visualización** | matplotlib | 3.10.9 | Gráficos estáticos |
| | seaborn | 0.13.2 | Visualización estadística |

### Frontend (Web)

| Capa | Tecnología | Versión | Propósito |
|-----|-----------|---------|-----------|
| **Framework** | Next.js | 16.2.9 | Framework React con App Router |
| **Lenguaje** | TypeScript | 5.x | Tipado estático |
| **Estilos** | Tailwind CSS | 4.x | Estilos utilitarios |
| **Componentes** | shadcn/ui | 4.x | Componentes de UI accesibles |
| **Gráficos** | Recharts | 2.x | Visualizaciones interactivas |
| **Formularios** | React Hook Form | — | Manejo de formularios |
| **Validación** | Zod | — | Validación de esquemas |

### Documentación

| Capa | Tecnología | Versión | Propósito |
|-----|-----------|---------|-----------|
| **Documentación** | MkDocs Material | 9.5.27 | Sitio web de documentación |
| **Control de versiones** | Git / GitHub | — | Repositorio y despliegue |

---

## 4. Flujo de Datos entre Aplicaciones

```
                    ┌──────────────────────┐
                    │   model_metadata.json │
                    │   modelo_final.pkl    │
                    └──────────┬───────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
    │  Streamlit   │    │   FastAPI    │    │   Next.js    │
    │              │    │              │    │              │
    │  Carga local │    │  Carga local │    │  HTTP fetch  │
    │  joblib.load │    │  joblib.load │    │  → /predict  │
    └──────────────┘    └──────┬───────┘    └──────────────┘
                               │
                               │ CORS allow_origins=["*"]
                               │
                        (consumido por Next.js)
```

---

## 5. Decisiones Técnicas

### 5.1 Pipeline de Modelado (no data leakage)

Se utiliza `sklearn.pipeline.Pipeline` para encapsular `StandardScaler` + `LogisticRegression`. El escalado se ajusta **exclusivamente sobre el conjunto de entrenamiento** y se aplica sobre test, evitando fuga de datos.

### 5.2 Serialización Local

El modelo se entrena y serializa en el mismo entorno local donde corre Streamlit. Esto evita conflictos de versiones de scikit-learn (error crítico si se entrena en Colab y se carga localmente).

### 5.3 Manejo del Desbalance

Se usa `class_weight='balanced'` para compensar el desbalance 84/16 en `Attrition`. La métrica principal es F1-macro, no accuracy.

### 5.4 Caché en Streamlit

Se aplican `@st.cache_resource` y `@st.cache_data` para evitar recargar el modelo, metadatos y datos en cada interacción del usuario.

### 5.5 API como Middle Layer

La API REST actúa como capa intermedia entre el modelo y el frontend Next.js. Esto permite que el frontend no necesite Python ni joblib, y que cualquier cliente HTTP pueda consumir el modelo.

### 5.6 Frontend con shadcn/ui

Se eligió shadcn/ui v4 sobre bibliotecas como Material UI o Chakra por:
- Componentes headless accesibles (basados en @base-ui/react)
- Estilos nativos de Tailwind CSS (sin runtime CSS-in-JS)
- Bundle más pequeño al copiar solo los componentes usados

---

## 6. Diagrama de Despliegue

```
                    ┌─────────────────────────────────────┐
                    │         Computador Local             │
                    │                                     │
                    │  ┌───────────────┐                   │
                    │  │ Entorno       │                   │
                    │  │ Virtual (venv)│                   │
                    │  │               │                   │
                    │  │ Python 3.12   │                   │
                    │  │ scikit-learn  │                   │
                    │  │ joblib        │                   │
                    │  └───────────────┘                   │
                    │                                     │
                    │  ┌──────────────┐  ┌──────────────┐  │
                    │  │ Dashboard    │  │ API REST     │  │
                    │  │ Streamlit    │  │ FastAPI      │  │
                    │  │ :8501        │  │ :8000        │  │
                    │  └──────────────┘  └──────────────┘  │
                    │                                     │
                    │  ┌────────────────────────────────┐  │
                    │  │ Frontend Next.js                │  │
                    │  │ :3000                           │  │
                    │  └────────────────────────────────┘  │
                    │                                     │
                    │  ┌────────────────────────────────┐  │
                    │  │ Documentación MkDocs            │  │
                    │  │ :8008                           │  │
                    │  └────────────────────────────────┘  │
                    └─────────────────────────────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────┐
                    │        GitHub / GitHub Pages         │
                    │                                     │
                    │  ┌─────────────────────────────┐     │
                    │  │ Repositorio                 │     │
                    │  │ github.com/NickGV/TalentGuard│     │
                    │  └─────────────────────────────┘     │
                    │                                     │
                    │  ┌─────────────────────────────┐     │
                    │  │ GitHub Pages (Documentación) │     │
                    │  │ nickgv.github.io/TalentGuard │     │
                    │  └─────────────────────────────┘     │
                    └─────────────────────────────────────┘
```

---

*Documento generado como parte de la documentación técnica del Proyecto Integrador*  
*Diplomado en Desarrollo Web — Tecnología en Desarrollo de Software*
