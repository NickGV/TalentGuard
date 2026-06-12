# Diccionario de Datos — TalentGuard

**Dataset:** IBM HR Analytics Employee Attrition & Performance  
**Fuente:** [Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)  
**Estado:** Dataset procesado (`data/processed/dataset_limpio.csv`)  
**Dimensiones finales:** 1.470 filas × 44 columnas  

---

## Convenciones

| Rol | Descripción |
|-----|-------------|
| `objetivo` | Variable que el modelo predice |
| `feature` | Variable de entrada al modelo |
| `eliminada` | Columna presente en el raw pero excluida del modelado |

| Tipo codificado | Descripción |
|-----------------|-------------|
| `int64 (binario)` | 0 / 1 |
| `int64 (ordinal)` | Escala numérica con orden implícito |
| `int64 (escala Likert)` | Escala 1–4 o 1–5 sin orden garantizado entre extremos |
| `int64 (OHE)` | Dummy 0/1 generado por One-Hot Encoding |
| `int64 (continua)` | Variable numérica original sin transformar |

---

## Variables del Dataset Procesado

### Variable objetivo

| Variable | Tipo | Rol | Descripción | Codificación |
|----------|------|-----|-------------|--------------|
| `Attrition` | int64 (binario) | objetivo | Rotación voluntaria del empleado | `Yes` → 1, `No` → 0 |

---

### Variables numéricas originales

| Variable | Tipo | Rol | Descripción | Rango observado |
|----------|------|-----|-------------|-----------------|
| `Age` | int64 (continua) | feature | Edad del empleado en años | 18 – 60 |
| `DailyRate` | int64 (continua) | feature | Tarifa diaria de compensación (USD) | 102 – 1.499 |
| `DistanceFromHome` | int64 (continua) | feature | Distancia entre hogar y lugar de trabajo (km) | 1 – 29 |
| `Education` | int64 (ordinal) | feature | Nivel educativo alcanzado | 1 (Below College) – 5 (Doctor) |
| `EnvironmentSatisfaction` | int64 (escala Likert) | feature | Satisfacción con el ambiente laboral | 1 (Low) – 4 (Very High) |
| `HourlyRate` | int64 (continua) | feature | Tarifa horaria de compensación (USD) | 30 – 100 |
| `JobInvolvement` | int64 (escala Likert) | feature | Nivel de involucramiento con el puesto | 1 (Low) – 4 (Very High) |
| `JobLevel` | int64 (ordinal) | feature | Nivel jerárquico dentro de la organización | 1 (Entry) – 5 (Executive) |
| `JobSatisfaction` | int64 (escala Likert) | feature | Satisfacción con el trabajo | 1 (Low) – 4 (Very High) |
| `MonthlyIncome` | int64 (continua) | feature | Ingreso mensual del empleado (USD) | 1.009 – 19.999 |
| `MonthlyRate` | int64 (continua) | feature | Tasa mensual de compensación (USD) | 2.094 – 26.999 |
| `NumCompaniesWorked` | int64 (continua) | feature | Número de empresas donde trabajó anteriormente | 0 – 9 |
| `PercentSalaryHike` | int64 (continua) | feature | Porcentaje de aumento salarial en el último período | 11 – 25 |
| `PerformanceRating` | int64 (escala Likert) | feature | Calificación de desempeño del último período | 3 (Excellent) – 4 (Outstanding) |
| `RelationshipSatisfaction` | int64 (escala Likert) | feature | Satisfacción con las relaciones laborales | 1 (Low) – 4 (Very High) |
| `StockOptionLevel` | int64 (ordinal) | feature | Nivel de opciones sobre acciones otorgadas | 0 – 3 |
| `TotalWorkingYears` | int64 (continua) | feature | Años totales de experiencia laboral | 0 – 40 |
| `TrainingTimesLastYear` | int64 (continua) | feature | Número de capacitaciones recibidas en el último año | 0 – 6 |
| `WorkLifeBalance` | int64 (escala Likert) | feature | Percepción del balance vida-trabajo | 1 (Bad) – 4 (Best) |
| `YearsAtCompany` | int64 (continua) | feature | Años de antigüedad en la empresa actual | 0 – 40 |
| `YearsInCurrentRole` | int64 (continua) | feature | Años en el rol actual | 0 – 18 |
| `YearsSinceLastPromotion` | int64 (continua) | feature | Años desde la última promoción | 0 – 15 |
| `YearsWithCurrManager` | int64 (continua) | feature | Años trabajando con el gerente actual | 0 – 17 |

---

### Variables categóricas codificadas (binaria / ordinal)

| Variable | Tipo | Rol | Descripción | Codificación |
|----------|------|-----|-------------|--------------|
| `Gender` | int64 (binario) | feature | Género del empleado | `Male` → 1, `Female` → 0 |
| `OverTime` | int64 (binario) | feature | Realiza horas extra habitualmente | `Yes` → 1, `No` → 0 |
| `BusinessTravel` | int64 (ordinal) | feature | Frecuencia de viajes por trabajo | `Non-Travel` → 0, `Travel_Rarely` → 1, `Travel_Frequently` → 2 |

---

### Variables categóricas — One-Hot Encoding (Department)

Categoría de referencia eliminada: `Department_Human Resources`

| Variable | Tipo | Rol | Descripción |
|----------|------|-----|-------------|
| `Department_Research & Development` | int64 (OHE) | feature | 1 si el empleado pertenece a I+D |
| `Department_Sales` | int64 (OHE) | feature | 1 si el empleado pertenece a Ventas |

---

### Variables categóricas — One-Hot Encoding (EducationField)

Categoría de referencia eliminada: `EducationField_Human Resources`

| Variable | Tipo | Rol | Descripción |
|----------|------|-----|-------------|
| `EducationField_Life Sciences` | int64 (OHE) | feature | 1 si estudió Ciencias de la Vida |
| `EducationField_Marketing` | int64 (OHE) | feature | 1 si estudió Marketing |
| `EducationField_Medical` | int64 (OHE) | feature | 1 si estudió Medicina / Salud |
| `EducationField_Other` | int64 (OHE) | feature | 1 si estudió otra disciplina |
| `EducationField_Technical Degree` | int64 (OHE) | feature | 1 si tiene título técnico |

---

### Variables categóricas — One-Hot Encoding (JobRole)

Categoría de referencia eliminada: `JobRole_Healthcare Representative`

| Variable | Tipo | Rol | Descripción |
|----------|------|-----|-------------|
| `JobRole_Human Resources` | int64 (OHE) | feature | 1 si el rol es Recursos Humanos |
| `JobRole_Laboratory Technician` | int64 (OHE) | feature | 1 si el rol es Técnico de Laboratorio |
| `JobRole_Manager` | int64 (OHE) | feature | 1 si el rol es Gerente |
| `JobRole_Manufacturing Director` | int64 (OHE) | feature | 1 si el rol es Director de Manufactura |
| `JobRole_Research Director` | int64 (OHE) | feature | 1 si el rol es Director de Investigación |
| `JobRole_Research Scientist` | int64 (OHE) | feature | 1 si el rol es Científico de Investigación |
| `JobRole_Sales Executive` | int64 (OHE) | feature | 1 si el rol es Ejecutivo de Ventas |
| `JobRole_Sales Representative` | int64 (OHE) | feature | 1 si el rol es Representante de Ventas |

---

### Variables categóricas — One-Hot Encoding (MaritalStatus)

Categoría de referencia eliminada: `MaritalStatus_Divorced`

| Variable | Tipo | Rol | Descripción |
|----------|------|-----|-------------|
| `MaritalStatus_Married` | int64 (OHE) | feature | 1 si el empleado es casado/a |
| `MaritalStatus_Single` | int64 (OHE) | feature | 1 si el empleado es soltero/a |

---

## Variables eliminadas del dataset crudo

| Variable | Motivo de eliminación |
|----------|-----------------------|
| `EmployeeCount` | Constante — valor único `1` en todos los registros |
| `Over18` | Constante — valor único `Y` en todos los registros |
| `StandardHours` | Constante — valor único `80` en todos los registros |
| `EmployeeNumber` | Identificador sin valor predictivo |

---

## Notas de calidad

- **Valores nulos:** 0 (ninguna columna requirió imputación)
- **Duplicados eliminados:** 0
- **Desbalance de clases:** 83.9% `No` (0) / 16.1% `Yes` (1) — justifica uso de F1-Score como métrica principal
- **Split:** 80% train (1.176 registros) / 20% test (294 registros), `stratify=Attrition`, `random_state=42`
