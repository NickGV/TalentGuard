# TalentGuard 🛡️
## Sistema Inteligente para la Predicción del Riesgo de Rotación de Empleados

**Autor:** Nicolas Gomez  
**Programa:** Tecnología en Desarrollo de Software  
**Diplomado:** Desarrollo Web para Analítica de Datos  
**Fecha:** Junio 2026  

---

## Descripción del Proyecto

TalentGuard es una aplicación web analítica orientada a predecir el riesgo de rotación voluntaria de empleados. A partir de variables como satisfacción laboral, horas extra, balance vida-trabajo, antigüedad e ingresos mensuales, el sistema clasifica a cada empleado según su probabilidad de abandono (Yes / No), con el fin de apoyar al área de Recursos Humanos en la priorización de estrategias de retención de talento.

El proyecto integra tres aplicaciones:

- **Dashboard Streamlit** — Visualización interactiva y predicción local
- **API REST (FastAPI)** — Exposición del modelo como servicio
- **Web App (Next.js)** — Frontend moderno que consume la API

---

## Problema

Las organizaciones enfrentan alta rotación en áreas estratégicas. Sin una herramienta predictiva, las intervenciones de retención ocurren de forma reactiva, cuando ya es demasiado tarde para revertir la decisión del empleado.

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
- **Métrica principal:** F1-Score (macro)
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

---

## Arquitectura de la Solución

El sistema se organiza en tres aplicaciones que comparten el mismo modelo ML:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
│   DATOS      │    │  PIPELINE    │    │  MODELO ML       │
│   CRUDOS     │───▶│  DE ETL      │───▶│  (Pipeline       │
│  data/raw/   │    │ 02_EDA_      │    │   sklearn)       │
│              │    │ limpieza     │    │  .pkl + JSON     │
└──────────────┘    └──────────────┘    └────────┬─────────┘
                                                  │
                    ┌─────────────────────────────┼─────────────┐
                    │                             │             │
                    ▼                             ▼             ▼
        ┌──────────────────┐    ┌──────────────────┐    ┌──────────────┐
        │  DASHBOARD       │    │  API REST        │    │  WEB APP     │
        │  STREAMLIT       │    │  FastAPI         │    │  Next.js     │
        │  :8501           │    │  :8000           │    │  :3000       │
        └──────────────────┘    └──────────────────┘    └──────────────┘
```

Para el detalle completo, ver la página de [Arquitectura](arquitectura.md).

---

## Estructura del Repositorio

```
TalentGuard/
├── README.md
├── .gitignore
├── requirements.txt               ← Dependencias Python
├── app_final.py                   ← Dashboard Streamlit
│
├── api/                           ← API REST (FastAPI)
│   ├── main.py                    ← 6 endpoints + Swagger
│   └── schemas.py                 ← Modelos Pydantic
│
├── web/                           ← Frontend (Next.js + TypeScript)
│   ├── .env.local
│   ├── package.json
│   ├── src/
│   │   ├── app/                   ← 6 páginas (App Router)
│   │   ├── components/            ← Navbar, KPIs, shadcn/ui
│   │   └── lib/                   ← API client + types
│   └── public/
│       └── datos.json             ← Dataset para charts
│
├── data/
│   ├── raw/                       ← Dataset original
│   └── processed/                 ← Dataset limpio
│
├── notebooks/
│   ├── 01_exploracion.ipynb       ← EDA inicial
│   ├── 02_eda_limpieza.ipynb      ← Pipeline de limpieza
│   └── 03_modelado.ipynb          ← Experimentación
│
├── src/
│   └── ml/
│       └── entrenar_modelo.py     ← Script de entrenamiento
│
├── models/
│   ├── modelo_final.pkl           ← Pipeline serializado
│   └── model_metadata.json        ← Métricas y metadatos
│
├── charts/                        ← Gráficos generados
├── docs/                          ← Documentación técnica
└── .github/
    └── workflows/
        └── deploy-docs.yml        ← CI/CD GitHub Pages
```

---

## Tecnologías Utilizadas

### Backend (Python)

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| Python | 3.12 | Lenguaje principal |
| pandas | 3.0.3 | Manipulación de datos |
| numpy | 2.4.6 | Operaciones numéricas |
| scikit-learn | 1.9.0 | Modelado y pipelines |
| joblib | 1.5.0 | Serialización del modelo |
| Streamlit | 1.58.0 | Dashboard web |
| FastAPI | 0.136.3 | API REST |
| uvicorn | 0.49.0 | Servidor ASGI |
| pydantic | 2.13.4 | Validación de datos |
| matplotlib | 3.10.9 | Visualización |
| seaborn | 0.13.2 | Visualización estadística |

### Frontend (Web)

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| Next.js | 16.2.9 | Framework React |
| TypeScript | 5.x | Tipado estático |
| Tailwind CSS | 4.x | Estilos utilitarios |
| shadcn/ui | 4.x | Componentes de UI |
| Recharts | 2.x | Gráficos interactivos |

### Documentación

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| MkDocs Material | 9.5.27 | Sitio web de documentación |
| Git / GitHub | — | Control de versiones y CI/CD |

---

## Cómo Ejecutar

### Backend (Python)

```bash
# Clonar y preparar
git clone https://github.com/NickGV/TalentGuard.git
cd TalentGuard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Dashboard Streamlit
streamlit run app_final.py          # http://localhost:8501

# API REST (en otra terminal)
uvicorn api.main:app --reload       # http://localhost:8000/docs
```

### Frontend Next.js

```bash
# En otra terminal
cd web
npm install
npm run dev                         # http://localhost:3000
```

### Documentación

```bash
pip install mkdocs-material
mkdocs serve                        # http://localhost:8008
```

---

## Consideraciones Éticas

TalentGuard está diseñado como una **herramienta de apoyo a la retención de talento**, no como un sistema de evaluación o clasificación automática de personal. Principios fundamentales:

1. **El resultado es una estimación**, no una decisión automática.
2. **La decisión final** es responsabilidad exclusiva del área de Recursos Humanos.
3. **El modelo puede equivocarse**: el F1 para la clase de abandono (Yes) es de 0.47, lo que significa que aproximadamente 1 de cada 2 empleados en riesgo podría no ser detectado.
4. **Los datos son sintéticos**: fueron generados por IBM, no provienen de una empresa real del sector construcción.

El dashboard, la API y el frontend web incluyen advertencias éticas visibles y el resultado se presenta siempre con interpretación en lenguaje natural, no como un número aislado.

Para el análisis completo, ver la página de [Reflexión Ética](reflexion_etica.md).
