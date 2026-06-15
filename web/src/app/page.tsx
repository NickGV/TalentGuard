"use client";

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { KpiCard } from "@/components/kpi-card";
import { getHealth, getDatos, getMetricas } from "@/lib/api";
import type { HealthResponse, DatosResponse, MetricasResponse } from "@/lib/types";
import Link from "next/link";

export default function Home() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [datos, setDatos] = useState<DatosResponse | null>(null);
  const [metricas, setMetricas] = useState<MetricasResponse | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    Promise.all([getHealth(), getDatos(), getMetricas()])
      .then(([h, d, m]) => {
        setHealth(h);
        setDatos(d);
        setMetricas(m);
      })
      .catch(() => setError(true));
  }, []);

  return (
    <div className="space-y-12">
      {/* Hero */}
      <section className="text-center space-y-4 py-6 sm:py-8">
        <h1 className="text-3xl font-bold tracking-tight text-[#2D3436] sm:text-4xl md:text-5xl">
          TalentGuard
        </h1>
        <p className="mx-auto max-w-2xl text-base sm:text-lg text-muted-foreground">
          Predicción del riesgo de rotación de empleados usando Machine Learning.
          Identifica talento en riesgo y toma decisiones informadas para
          retenerlo.
        </p>
        <div className="flex justify-center gap-4 pt-2">
          <Link
            href="/predict"
            className="inline-flex h-9 items-center justify-center rounded-lg bg-[#E17055] px-5 text-sm font-medium text-white transition-colors hover:bg-[#d0654e]"
          >
            Probar predicción
          </Link>
          <Link
            href="/insights"
            className="inline-flex h-9 items-center justify-center rounded-lg border border-border bg-background px-5 text-sm font-medium transition-colors hover:bg-muted"
          >
            Ver análisis
          </Link>
        </div>
      </section>

      {/* KPIs */}
      {!error && datos && metricas && (
        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <KpiCard
            title="Empleados analizados"
            value={datos.empleados_analizados.toLocaleString()}
            subtitle={`${datos.filas} filas · ${datos.columnas} variables`}
            icon={<UsersIcon />}
          />
          <KpiCard
            title="Tasa de rotación"
            value={`${(datos.tasa_rotacion * 100).toFixed(1)}%`}
            subtitle={`${datos.abandonos} abandonos · ${datos.permanencias} permanencias`}
            icon={<RotateIcon />}
          />
          <KpiCard
            title="Recall del modelo"
            value={`${(metricas.metricas.recall_macro * 100).toFixed(0)}%`}
            subtitle="Detección de abandonos reales"
            icon={<RecallIcon />}
          />
          <KpiCard
            title="Accuracy"
            value={`${(metricas.metricas.accuracy * 100).toFixed(0)}%`}
            subtitle={`F1-macro: ${metricas.metricas.f1_macro.toFixed(3)}`}
            icon={<AccuracyIcon />}
          />
        </section>
      )}

      {error && (
        <Card>
          <CardContent className="p-8 text-center text-muted-foreground">
            <p className="mb-2 text-lg font-medium">API no disponible</p>
            <p className="text-sm">
              Asegúrate de que la API esté corriendo en{" "}
              <code className="rounded bg-muted px-1 py-0.5 text-xs">
                http://127.0.0.1:8000
              </code>
            </p>
          </CardContent>
        </Card>
      )}

      {/* Cómo funciona */}
      <section className="grid gap-6 md:grid-cols-3">
        <Card>
          <CardContent className="p-6 space-y-2">
            <div className="flex size-10 items-center justify-center rounded-lg bg-[#E17055]/10 text-[#E17055] font-bold">
              1
            </div>
            <h3 className="font-semibold">Ingresa los datos</h3>
            <p className="text-sm text-muted-foreground">
              Completa el formulario con la información del empleado: datos
              demográficos, laborales y de satisfacción.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 space-y-2">
            <div className="flex size-10 items-center justify-center rounded-lg bg-[#E17055]/10 text-[#E17055] font-bold">
              2
            </div>
            <h3 className="font-semibold">El modelo analiza</h3>
            <p className="text-sm text-muted-foreground">
              Nuestro modelo de Regresión Logística compara el perfil contra
              patrones históricos de 1,470 empleados.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 space-y-2">
            <div className="flex size-10 items-center justify-center rounded-lg bg-[#E17055]/10 text-[#E17055] font-bold">
              3
            </div>
            <h3 className="font-semibold">Recibe el resultado</h3>
            <p className="text-sm text-muted-foreground">
              Obtén la probabilidad de abandono, el nivel de riesgo y los
              factores más influyentes.
            </p>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}

/* Iconos inline (sin lucide) */
function UsersIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  );
}

function RotateIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 12a9 9 0 1 1-6.219-8.56" />
      <path d="M21 3v5h-5" />
    </svg>
  );
}

function RecallIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
      <polyline points="22 4 12 14.01 9 11.01" />
    </svg>
  );
}

function AccuracyIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" x2="18" y1="20" y2="10" />
      <line x1="12" x2="12" y1="20" y2="4" />
      <line x1="6" x2="6" y1="20" y2="14" />
    </svg>
  );
}
