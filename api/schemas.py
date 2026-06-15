from pydantic import BaseModel, Field
from typing import Optional


class EmpleadoRequest(BaseModel):
    """Datos del empleado para realizar una predicción."""
    Age: int = Field(ge=18, le=70, description="Edad del empleado")
    Gender: int = Field(ge=0, le=1, description="Género (0=Femenino, 1=Masculino)")
    MaritalStatus: str = Field(description="Estado civil (Divorced, Married, Single)")
    NumCompaniesWorked: int = Field(ge=0, le=20, description="Número de empresas anteriores")
    DistanceFromHome: int = Field(ge=1, le=50, description="Distancia al trabajo (km)")
    TotalWorkingYears: int = Field(ge=0, le=50, description="Años totales de experiencia")
    Department: str = Field(description="Departamento (Sales, Research & Development, Human Resources)")
    JobRole: str = Field(description="Rol del puesto")
    EducationField: str = Field(description="Campo de estudio")
    MonthlyIncome: float = Field(ge=1000, le=50000, description="Ingreso mensual (USD)")
    YearsAtCompany: int = Field(ge=0, le=40, description="Años en la empresa")
    YearsInCurrentRole: int = Field(ge=0, le=20, description="Años en el rol actual")
    YearsSinceLastPromotion: int = Field(ge=0, le=20, description="Años desde última promoción")
    OverTime: int = Field(ge=0, le=1, description="Horas extra (0=No, 1=Sí)")
    JobSatisfaction: int = Field(ge=1, le=4, description="Satisfacción laboral (1-4)")
    WorkLifeBalance: int = Field(ge=1, le=4, description="Balance vida-trabajo (1-4)")
    EnvironmentSatisfaction: int = Field(ge=1, le=4, description="Satisfacción con el entorno (1-4)")
    BusinessTravel: int = Field(ge=0, le=2, description="Viajes (0=No viaja, 1=Raramente, 2=Frecuentemente)")


class PrediccionResponse(BaseModel):
    """Resultado de la predicción."""
    probabilidad_abandono: float = Field(description="Probabilidad estimada de abandono (0-1)")
    probabilidad_permanencia: float = Field(description="Probabilidad estimada de permanencia (0-1)")
    riesgo: str = Field(description="Nivel de riesgo (BAJO, MEDIO, ALTO)")
    prediccion: int = Field(description="Predicción binaria (0=No abandona, 1=Abandona)")
    advertencia: str = Field(description="Advertencia de uso responsable")


class HealthResponse(BaseModel):
    """Estado del servicio."""
    status: str = Field(description="Estado del API")
    modelo: str = Field(description="Nombre del modelo cargado")
    version: str = Field(description="Versión del modelo")
    f1_macro: float = Field(description="Métrica principal del modelo")
