# Datos Crudos (Raw Data)

## `WA_Fn-UseC_-HR-Employee-Attrition.csv`

**Fuente:** [IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) — Kaggle

**Licencia:** CC0 (Dominio Público)

**Descripción:** Dataset original sin modificar. Contiene 1.470 registros de empleados con 35 variables demográficas, laborales y de satisfacción.

**Uso:** Este archivo es la entrada del pipeline de ETL. No debe modificarse manualmente.

**Columnas principales:**
| Columna | Descripción |
|---------|-------------|
| `Age` | Edad del empleado |
| `Attrition` | Variable objetivo — ¿abandonó la empresa? (Yes/No) |
| `Department` | Departamento (Sales, Research & Development, Human Resources) |
| `JobRole` | Rol del puesto (9 roles) |
| `MonthlyIncome` | Ingreso mensual (USD) |
| `OverTime` | ¿Realiza horas extra? (Yes/No) |
| `JobSatisfaction` | Satisfacción laboral (1-4) |
| `WorkLifeBalance` | Balance vida-trabajo (1-4) |

Para más detalles, ver [`docs/diccionario_datos.md`](../../docs/diccionario_datos.md).
