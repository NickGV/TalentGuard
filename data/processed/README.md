# Datos Procesados (Processed Data)

Archivos generados por el pipeline de ETL (`notebooks/02_eda_limpieza.ipynb`).

## Archivos

| Archivo | Registros | Columnas | Descripción |
|---------|-----------|----------|-------------|
| `dataset_limpio.csv` | 1.470 | 44 | Dataset completo después de limpieza, codificación y OHE |
| `X_train.csv` | 1.176 (80%) | 43 | Features de entrenamiento |
| `X_test.csv` | 294 (20%) | 43 | Features de prueba |
| `y_train.csv` | 1.176 | 1 | Target de entrenamiento (`Attrition`) |
| `y_test.csv` | 294 | 1 | Target de prueba (`Attrition`) |

## Transformaciones aplicadas

1. Eliminación de columnas constantes (`EmployeeCount`, `Over18`, `StandardHours`)
2. Eliminación de `EmployeeNumber` (sin valor predictivo)
3. Codificación binaria: `Gender` (Male→1/Female→0), `OverTime` (Yes→1/No→0)
4. Codificación ordinal: `BusinessTravel` (Non-Travel→0, Travel_Rarely→1, Travel_Frequently→2)
5. One-Hot Encoding: `Department`, `EducationField`, `JobRole`, `MaritalStatus`
6. Separación train/test: 80/20 estratificada con `random_state=42`

## Uso

Estos archivos son consumidos por:
- `src/ml/entrenar_modelo.py` — Script de entrenamiento
- `notebooks/03_modelado.ipynb` — Experimentación
- `api/main.py` — FastAPI (usa `dataset_limpio.csv` para el endpoint `/datos`)
