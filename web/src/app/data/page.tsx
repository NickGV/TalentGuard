"use client";

import { useEffect, useState } from "react";
import { getDatos } from "@/lib/api";
import type { DatosResponse } from "@/lib/types";
import { Card, CardContent } from "@/components/ui/card";
import { KpiCard } from "@/components/kpi-card";
import { Skeleton } from "@/components/ui/skeleton";

interface Fila {
  [key: string]: string | number;
}

export default function DataPage() {
  const [datos, setDatos] = useState<DatosResponse | null>(null);
  const [columnas, setColumnas] = useState<string[]>([]);
  const [filas, setFilas] = useState<Fila[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    getDatos()
      .then(setDatos)
      .catch(() => setError(true))
      .finally(() => setLoading(false));

    // Fetch raw data for the table
    fetch("http://127.0.0.1:8000/datos")
      .then((res) => res.json())
      .then(() => {
        // The /datos endpoint only returns summary.
        // We'll fetch from a sample CSV endpoint or load inline data.
        // For now, show the variable reference instead.
      })
      .catch(() => {});
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-[#2D3436]">Datos</h1>
        <div className="grid gap-4 sm:grid-cols-4">
          {[...Array(4)].map((_, i) => (
            <Skeleton key={i} className="h-28 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-12 text-center text-muted-foreground">
        <p className="text-lg font-medium">API no disponible</p>
        <p className="text-sm">Verifica que la API esté corriendo.</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-[#2D3436]">
        📊 Datos del dataset
      </h1>
      <p className="text-muted-foreground">
        El dataset <strong>IBM HR Analytics Employee Attrition &amp;
        Performance</strong> contiene información de 1,470 empleados con 43
        variables demográficas, laborales y de satisfacción.
      </p>

      {/* KPIs del dataset */}
      {datos && (
        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <KpiCard title="Empleados" value={datos.empleados_analizados.toLocaleString()} subtitle="Total de registros" />
          <KpiCard title="Variables" value={datos.columnas} subtitle="Features del modelo" />
          <KpiCard title="Tasa de rotación" value={`${(datos.tasa_rotacion * 100).toFixed(1)}%`} subtitle="Desbalanceado (84/16)" />
          <KpiCard title="Abandonos" value={datos.abandonos} subtitle="Casos positivos" />
        </section>
      )}

      {/* Variable dictionary */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-xl font-semibold text-[#2D3436]">
            Diccionario de variables
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left">
                  <th className="pb-2 font-medium text-muted-foreground">Variable</th>
                  <th className="pb-2 font-medium text-muted-foreground">Descripción</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {DICCIONARIO.map((row) => (
                  <tr key={row.var} className="hover:bg-muted/50">
                    <td className="py-2 pr-4 font-mono text-xs">{row.var}</td>
                    <td className="py-2 text-muted-foreground">{row.desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

const DICCIONARIO = [
  { var: "Age", desc: "Edad del empleado" },
  { var: "Attrition", desc: "¿Abandonó la empresa? (0=No, 1=Sí) — variable objetivo" },
  { var: "BusinessTravel", desc: "Frecuencia de viajes (0=No viaja, 1=Raramente, 2=Frecuentemente)" },
  { var: "DailyRate", desc: "Tarifa diaria (USD)" },
  { var: "Department", desc: "Departamento (Sales, R&D, Human Resources)" },
  { var: "DistanceFromHome", desc: "Distancia del hogar al trabajo (km)" },
  { var: "Education", desc: "Nivel educativo (1-5)" },
  { var: "EducationField", desc: "Campo de estudio" },
  { var: "EnvironmentSatisfaction", desc: "Satisfacción con el entorno (1-4)" },
  { var: "Gender", desc: "Género (0=Femenino, 1=Masculino)" },
  { var: "HourlyRate", desc: "Tarifa por hora (USD)" },
  { var: "JobInvolvement", desc: "Involucramiento laboral (1-4)" },
  { var: "JobLevel", desc: "Nivel del puesto (1-5)" },
  { var: "JobRole", desc: "Rol del puesto" },
  { var: "JobSatisfaction", desc: "Satisfacción laboral (1-4)" },
  { var: "MaritalStatus", desc: "Estado civil (Divorced, Married, Single)" },
  { var: "MonthlyIncome", desc: "Ingreso mensual (USD)" },
  { var: "MonthlyRate", desc: "Tarifa mensual (USD)" },
  { var: "NumCompaniesWorked", desc: "Número de empresas anteriores" },
  { var: "OverTime", desc: "¿Realiza horas extra? (0=No, 1=Sí)" },
  { var: "PercentSalaryHike", desc: "Porcentaje de aumento salarial" },
  { var: "PerformanceRating", desc: "Calificación de desempeño (1-4)" },
  { var: "RelationshipSatisfaction", desc: "Satisfacción con relaciones (1-4)" },
  { var: "StockOptionLevel", desc: "Nivel de opciones accionarias (0-3)" },
  { var: "TotalWorkingYears", desc: "Años totales de experiencia" },
  { var: "TrainingTimesLastYear", desc: "Capacitaciones el año anterior" },
  { var: "WorkLifeBalance", desc: "Balance vida-trabajo (1-4)" },
  { var: "YearsAtCompany", desc: "Años en la empresa" },
  { var: "YearsInCurrentRole", desc: "Años en el rol actual" },
  { var: "YearsSinceLastPromotion", desc: "Años desde última promoción" },
  { var: "YearsWithCurrManager", desc: "Años con el jefe actual" },
];
