/* ──────────────────────────────────────────
   TalentGuard — Tipos compartidos
   ────────────────────────────────────────── */

export type Riesgo = "BAJO" | "MEDIO" | "ALTO";

export interface HealthResponse {
  status: string;
  modelo: string;
  version: string;
  f1_macro: number;
}

export interface DatosResponse {
  filas: number;
  columnas: number;
  tasa_rotacion: number;
  empleados_analizados: number;
  abandonos: number;
  permanencias: number;
}

export interface CampoFormulario {
  nombre: string;
  tipo: "int" | "float" | "str";
  descripcion: string;
  minimo?: number;
  maximo?: number;
  valores_aceptados?: (string | number)[];
  requerido: boolean;
}

export interface VariablesResponse {
  campos: CampoFormulario[];
  total_campos: number;
}

export interface MetricasResponse {
  modelo: string;
  version: string;
  fecha_entrenamiento: string;
  metricas: {
    accuracy: number;
    f1_macro: number;
    f1_yes: number;
    precision_macro: number;
    recall_macro: number;
    roc_auc: number;
  };
  clase_balanceada: boolean;
  class_weight: string;
}

export interface PredictRequest {
  Age: number;
  Gender: number;
  MaritalStatus: string;
  NumCompaniesWorked: number;
  DistanceFromHome: number;
  TotalWorkingYears: number;
  Department: string;
  JobRole: string;
  EducationField: string;
  MonthlyIncome: number;
  YearsAtCompany: number;
  YearsInCurrentRole: number;
  YearsSinceLastPromotion: number;
  OverTime: number;
  JobSatisfaction: number;
  WorkLifeBalance: number;
  EnvironmentSatisfaction: number;
  BusinessTravel: number;
}

export interface PredictResponse {
  probabilidad_abandono: number;
  probabilidad_permanencia: number;
  riesgo: Riesgo;
  prediccion: number;
  advertencia: string;
}

export interface ApiError {
  detail: string;
}
