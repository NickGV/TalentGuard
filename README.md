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
| **Variables** | 35 |
| **Variable objetivo** | `Attrition` (Yes / No) |

---

## Tipo de Tarea y Métrica

- **Tarea:** Clasificación binaria
- **Métrica principal:** F1-Score
- **Justificación:** El dataset presenta desbalance de clases (83.9% No / 16.1% Yes), por lo que el F1-Score es más adecuado que el accuracy para evaluar el modelo.

---

## Estructura del Repositorio

~~~
TalentGuard/
├── data/
│   └── raw/
│       └── WA_Fn-UseC_-HR-Employee-Attrition.csv
├── notebooks/
│   └── 01_exploracion.ipynb
├── docs/
│   ├── ficha_proyecto.md
│   ├── analisis_dataset.md
│   └── wireframe_dashboard.png
├── charts/
│   ├── fig_attrition_distribucion.png
│   ├── fig_overtime_attrition.png
│   ├── fig_income_attrition.png
│   ├── fig_years_attrition.png
│   ├── fig_jobsatisfaction_attrition.png
│   ├── fig_worklife_attrition.png
│   └── fig_correlacion_attrition.png
├── .gitignore
├── requirements.txt
└── README.md
~~~

---

## Hallazgos Principales del EDA

- Empleados con horas extra tienen tasa de abandono del **30.5%** vs **10.4%** sin horas extra
- Mediana salarial: quienes abandonan **$3.202** vs quienes permanecen **$5.204**
- El **61%** de los abandonos ocurren en los primeros **3 años** de antigüedad
- A menor satisfacción laboral, mayor tasa de abandono: **22.8%** en nivel Low vs **11.3%** en Very High

---

## Tecnologías Utilizadas

- Python 3.x
- pandas, numpy
- matplotlib, seaborn
- scikit-learn
- Jupyter Notebook
- Git / GitHub
- **Diseño UI:** [Stitch by Google](https://stitch.withgoogle.com/)

---

## 📚 Documentación Web

La documentación completa del proyecto está publicada en **GitHub Pages**:

🔗 **https://nickgv.github.io/TalentGuard/**

Incluye:
- **Inicio** — Resumen del proyecto (este README)
- **Ficha del Proyecto** — Formulación completa del proyecto integrador
- **Análisis del Dataset** — EDA detallado con 7 visualizaciones

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

# 4. Ejecutar Jupyter Notebook
jupyter notebook notebooks/01_exploracion.ipynb
```

---

## Entrega 1 — Estado actual

- [x] Planteamiento del problema analítico
- [x] Pregunta analítica
- [x] Análisis cualitativo del dataset
- [x] Ficha de formulación del proyecto
- [x] Repositorio GitHub con estructura completa
- [x] Wireframe del dashboard*
