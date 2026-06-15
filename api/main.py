"""
TalentGuard API — Predicción de rotación de empleados

Ruta A del proyecto integrador (bonificación).
Expone el modelo de Machine Learning como servicio REST con documentación Swagger.

Ejecutar:
    uvicorn api.main:app --reload

Documentación automática:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import joblib
import json
import pandas as pd

from api.schemas import EmpleadoRequest, PrediccionResponse, HealthResponse

# ─────────────────────────────────────────
# Configuración
# ─────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="TalentGuard API",
    description=(
        "API para la predicción del riesgo de rotación de empleados. "
        "Expone el modelo de Regresión Logística entrenado sobre "
        "el dataset IBM HR Analytics Employee Attrition & Performance."
    ),
    version="1.0.0",
    contact={
        "name": "TalentGuard",
        "url": "https://github.com/nickgv/TalentGuard",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# Carga del modelo
# ─────────────────────────────────────────
try:
    modelo = joblib.load(BASE / "models" / "modelo_final.pkl")
    metadata = json.loads((BASE / "models" / "model_metadata.json").read_text())
except FileNotFoundError as e:
    raise RuntimeError(f"Error al cargar el modelo: {e}. Asegúrate de ejecutar el script de entrenamiento primero.")

# Medianas para features no expuestas en la API
MEDIANS = {
    "DailyRate": 802, "HourlyRate": 66, "MonthlyRate": 14236,
    "Education": 3, "JobInvolvement": 3, "JobLevel": 2,
    "PercentSalaryHike": 14, "PerformanceRating": 3,
    "RelationshipSatisfaction": 3, "StockOptionLevel": 1,
    "TrainingTimesLastYear": 3,
}


def _transformar_empleado(emp: EmpleadoRequest) -> pd.DataFrame:
    """
    Transforma los datos del empleado al formato esperado por el pipeline.
    Aplica el mismo One-Hot Encoding que se usó durante el entrenamiento.
    """
    feature_names = metadata["variables_entrada"]

    # Base con medianas para features no expuestas
    input_dict = {col: MEDIANS.get(col, 0) for col in feature_names}

    # Valores numéricos directos
    input_dict.update({
        "Age":                     emp.Age,
        "Gender":                  emp.Gender,
        "MonthlyIncome":           emp.MonthlyIncome,
        "YearsAtCompany":          emp.YearsAtCompany,
        "YearsInCurrentRole":      emp.YearsInCurrentRole,
        "YearsSinceLastPromotion": emp.YearsSinceLastPromotion,
        "OverTime":                emp.OverTime,
        "JobSatisfaction":         emp.JobSatisfaction,
        "WorkLifeBalance":         emp.WorkLifeBalance,
        "EnvironmentSatisfaction": emp.EnvironmentSatisfaction,
        "BusinessTravel":          emp.BusinessTravel,
        "TotalWorkingYears":       emp.TotalWorkingYears,
        "NumCompaniesWorked":      emp.NumCompaniesWorked,
        "DistanceFromHome":        emp.DistanceFromHome,
    })

    # OHE — Department (referencia: Human Resources)
    input_dict["Department_Research & Development"] = int(emp.Department == "Research & Development")
    input_dict["Department_Sales"]                  = int(emp.Department == "Sales")

    # OHE — JobRole (referencia: Healthcare Representative)
    for role, col in {
        "Human Resources":        "JobRole_Human Resources",
        "Laboratory Technician":  "JobRole_Laboratory Technician",
        "Manager":                "JobRole_Manager",
        "Manufacturing Director": "JobRole_Manufacturing Director",
        "Research Director":      "JobRole_Research Director",
        "Research Scientist":     "JobRole_Research Scientist",
        "Sales Executive":        "JobRole_Sales Executive",
        "Sales Representative":   "JobRole_Sales Representative",
    }.items():
        input_dict[col] = int(emp.JobRole == role)

    # OHE — MaritalStatus (referencia: Divorced)
    input_dict["MaritalStatus_Married"] = int(emp.MaritalStatus == "Married")
    input_dict["MaritalStatus_Single"]  = int(emp.MaritalStatus == "Single")

    # OHE — EducationField (referencia: Human Resources)
    for field, col in {
        "Life Sciences":    "EducationField_Life Sciences",
        "Marketing":        "EducationField_Marketing",
        "Medical":          "EducationField_Medical",
        "Other":            "EducationField_Other",
        "Technical Degree": "EducationField_Technical Degree",
    }.items():
        if col in input_dict:
            input_dict[col] = int(emp.EducationField == field)

    return pd.DataFrame([input_dict])


# ══════════════════════════════════════════
# Endpoints
# ══════════════════════════════════════════

@app.get("/", tags=["General"])
def raiz():
    """Información general de la API."""
    return {
        "mensaje": "TalentGuard API — Predicción de rotación de empleados",
        "version": "1.0.0",
        "endpoints": {
            "GET  /": "Esta página",
            "GET  /health": "Estado del servicio",
            "GET  /datos": "Información del dataset",
            "GET  /variables": "Lista de campos para el formulario de predicción",
            "GET  /metricas": "Métricas del modelo",
            "POST /predict": "Predecir riesgo de abandono",
        },
        "docs": "/docs",
    }


@app.get("/health", tags=["General"], response_model=HealthResponse)
def health():
    """Verificar que el servicio está funcionando correctamente."""
    return HealthResponse(
        status="ok",
        modelo=metadata["modelo"],
        version=metadata["version"],
        f1_macro=metadata["valor_metrica"],
    )


@app.get("/datos", tags=["Datos"])
def datos():
    """Obtener información resumida del dataset."""
    df = pd.read_csv(BASE / "data" / "processed" / "dataset_limpio.csv")
    return {
        "filas": len(df),
        "columnas": len(df.columns),
        "tasa_rotacion": round(float(df["Attrition"].mean()), 4),
        "empleados_analizados": len(df),
        "abandonos": int(df["Attrition"].sum()),
        "permanencias": int((df["Attrition"] == 0).sum()),
    }


@app.get("/variables", tags=["Datos"])
def variables():
    """Obtener la lista de variables que acepta el endpoint /predict."""
    return {
        "campos": [
            {
                "nombre": "Age",
                "tipo": "int",
                "descripcion": "Edad del empleado",
                "minimo": 18,
                "maximo": 70,
                "requerido": True,
            },
            {
                "nombre": "Gender",
                "tipo": "int",
                "descripcion": "Género (0=Femenino, 1=Masculino)",
                "valores_aceptados": [0, 1],
                "requerido": True,
            },
            {
                "nombre": "MaritalStatus",
                "tipo": "str",
                "descripcion": "Estado civil",
                "valores_aceptados": ["Divorced", "Married", "Single"],
                "requerido": True,
            },
            {
                "nombre": "NumCompaniesWorked",
                "tipo": "int",
                "descripcion": "Número de empresas anteriores",
                "minimo": 0,
                "maximo": 20,
                "requerido": True,
            },
            {
                "nombre": "DistanceFromHome",
                "tipo": "int",
                "descripcion": "Distancia del hogar al trabajo (km)",
                "minimo": 1,
                "maximo": 50,
                "requerido": True,
            },
            {
                "nombre": "TotalWorkingYears",
                "tipo": "int",
                "descripcion": "Años totales de experiencia laboral",
                "minimo": 0,
                "maximo": 50,
                "requerido": True,
            },
            {
                "nombre": "Department",
                "tipo": "str",
                "descripcion": "Departamento",
                "valores_aceptados": ["Sales", "Research & Development", "Human Resources"],
                "requerido": True,
            },
            {
                "nombre": "JobRole",
                "tipo": "str",
                "descripcion": "Rol del puesto",
                "valores_aceptados": [
                    "Sales Executive", "Research Scientist", "Laboratory Technician",
                    "Manufacturing Director", "Healthcare Representative", "Manager",
                    "Sales Representative", "Research Director", "Human Resources",
                ],
                "requerido": True,
            },
            {
                "nombre": "EducationField",
                "tipo": "str",
                "descripcion": "Campo de estudio",
                "valores_aceptados": [
                    "Life Sciences", "Medical", "Marketing", "Other",
                    "Technical Degree", "Human Resources",
                ],
                "requerido": True,
            },
            {
                "nombre": "MonthlyIncome",
                "tipo": "float",
                "descripcion": "Ingreso mensual (USD)",
                "minimo": 1000,
                "maximo": 50000,
                "requerido": True,
            },
            {
                "nombre": "YearsAtCompany",
                "tipo": "int",
                "descripcion": "Años en la empresa",
                "minimo": 0,
                "maximo": 40,
                "requerido": True,
            },
            {
                "nombre": "YearsInCurrentRole",
                "tipo": "int",
                "descripcion": "Años en el rol actual",
                "minimo": 0,
                "maximo": 20,
                "requerido": True,
            },
            {
                "nombre": "YearsSinceLastPromotion",
                "tipo": "int",
                "descripcion": "Años desde la última promoción",
                "minimo": 0,
                "maximo": 20,
                "requerido": True,
            },
            {
                "nombre": "OverTime",
                "tipo": "int",
                "descripcion": "¿Realiza horas extra?",
                "valores_aceptados": [0, 1],
                "requerido": True,
            },
            {
                "nombre": "JobSatisfaction",
                "tipo": "int",
                "descripcion": "Satisfacción laboral (1=Bajo, 2=Medio, 3=Alto, 4=Muy Alto)",
                "minimo": 1,
                "maximo": 4,
                "requerido": True,
            },
            {
                "nombre": "WorkLifeBalance",
                "tipo": "int",
                "descripcion": "Balance vida-trabajo (1=Malo, 2=Bueno, 3=Mejor, 4=Óptimo)",
                "minimo": 1,
                "maximo": 4,
                "requerido": True,
            },
            {
                "nombre": "EnvironmentSatisfaction",
                "tipo": "int",
                "descripcion": "Satisfacción con el entorno (1-4)",
                "minimo": 1,
                "maximo": 4,
                "requerido": True,
            },
            {
                "nombre": "BusinessTravel",
                "tipo": "int",
                "descripcion": "Frecuencia de viajes (0=No viaja, 1=Raramente, 2=Frecuentemente)",
                "valores_aceptados": [0, 1, 2],
                "requerido": True,
            },
        ],
        "total_campos": 18,
    }


@app.get("/metricas", tags=["Modelo"])
def metricas():
    """Obtener las métricas de evaluación del modelo."""
    return {
        "modelo": metadata["modelo"],
        "version": metadata["version"],
        "fecha_entrenamiento": metadata["fecha_entrenamiento"],
        "metricas": {
            "accuracy": metadata["accuracy"],
            "f1_macro": metadata["valor_metrica"],
            "f1_yes": metadata["f1_yes"],
            "precision_macro": metadata["precision_macro"],
            "recall_macro": metadata["recall_macro"],
            "roc_auc": metadata["roc_auc"],
        },
        "clase_balanceada": False,
        "class_weight": metadata["class_weight"],
    }


@app.post("/predict", tags=["Predicción"], response_model=PrediccionResponse)
def predict(emp: EmpleadoRequest):
    """
    Predecir el riesgo de abandono de un empleado.

    Recibe los datos del empleado y devuelve la probabilidad estimada
    de abandono junto con el nivel de riesgo.
    """
    try:
        input_df = _transformar_empleado(emp)
        prediccion = int(modelo.predict(input_df)[0])
        probabilidad = modelo.predict_proba(input_df)[0]
        prob_abandono = round(float(probabilidad[1]), 4)
        prob_permanencia = round(float(probabilidad[0]), 4)

        if prob_abandono >= 0.6:
            riesgo = "ALTO"
        elif prob_abandono >= 0.4:
            riesgo = "MEDIO"
        else:
            riesgo = "BAJO"

        return PrediccionResponse(
            probabilidad_abandono=prob_abandono,
            probabilidad_permanencia=prob_permanencia,
            riesgo=riesgo,
            prediccion=prediccion,
            advertencia=(
                "Estimación estadística basada en patrones históricos. "
                "Debe ser revisada por una persona responsable de Recursos Humanos "
                "antes de tomar cualquier decisión sobre el empleado."
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la predicción: {str(e)}")
