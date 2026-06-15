"use client";

import { useState, useCallback } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { postPredict } from "@/lib/api";
import type { PredictRequest, PredictResponse } from "@/lib/types";

const GENDER_LABELS: Record<number, string> = { 0: "Femenino", 1: "Masculino" };
const SAT_LABELS: Record<number, string> = { 1: "Bajo", 2: "Medio", 3: "Alto", 4: "Muy Alto" };
const WORKLIFE_LABELS: Record<number, string> = { 1: "Malo", 2: "Bueno", 3: "Mejor", 4: "Óptimo" };
const TRAVEL_LABELS: Record<number, string> = { 0: "Sin viajes", 1: "Viaja raramente", 2: "Viaja frecuentemente" };

const DEPARTMENTS = ["Sales", "Research & Development", "Human Resources"];
const JOB_ROLES = [
  "Sales Executive", "Research Scientist", "Laboratory Technician",
  "Manufacturing Director", "Healthcare Representative", "Manager",
  "Sales Representative", "Research Director", "Human Resources",
];
const MARITAL_STATUSES = ["Divorced", "Married", "Single"];
const EDUCATION_FIELDS = [
  "Life Sciences", "Medical", "Marketing", "Other",
  "Technical Degree", "Human Resources",
];

const INITIAL: PredictRequest = {
  Age: 35,
  Gender: 1,
  MaritalStatus: "Married",
  NumCompaniesWorked: 2,
  DistanceFromHome: 7,
  TotalWorkingYears: 10,
  Department: "Research & Development",
  JobRole: "Research Scientist",
  EducationField: "Life Sciences",
  MonthlyIncome: 5000,
  YearsAtCompany: 5,
  YearsInCurrentRole: 3,
  YearsSinceLastPromotion: 2,
  OverTime: 0,
  JobSatisfaction: 3,
  WorkLifeBalance: 3,
  EnvironmentSatisfaction: 3,
  BusinessTravel: 1,
};

function riscoColor(riesgo: string) {
  switch (riesgo) {
    case "ALTO": return "bg-red-50 border-red-200 text-red-700";
    case "MEDIO": return "bg-amber-50 border-amber-200 text-amber-700";
    default: return "bg-emerald-50 border-emerald-200 text-emerald-700";
  }
}

function riscoLabel(riesgo: string) {
  switch (riesgo) {
    case "ALTO": return "🔴 Alto riesgo de abandono";
    case "MEDIO": return "🟡 Riesgo moderado";
    default: return "🟢 Bajo riesgo de abandono";
  }
}

export default function PredictPage() {
  const [form, setForm] = useState<PredictRequest>(INITIAL);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const update = useCallback(
    <K extends keyof PredictRequest>(key: K, value: PredictRequest[K] | null) => {
      if (value !== null) {
        setForm((f) => ({ ...f, [key]: value }));
      }
    },
    []
  );

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      setLoading(true);
      setError(null);
      setResult(null);
      try {
        const res = await postPredict(form);
        setResult(res);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error al realizar la predicción");
      } finally {
        setLoading(false);
      }
    },
    [form]
  );

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-[#2D3436]">
        🎯 Predicción de riesgo de abandono
      </h1>

      <Card className="border-amber-200 bg-amber-50">
        <CardContent className="p-4 text-sm text-amber-800">
          ⚠️ El resultado es una <strong>estimación estadística</strong>. Debe
          ser revisado por una persona responsable de Recursos Humanos antes de
          tomar cualquier decisión sobre el empleado.
        </CardContent>
      </Card>

      <div className="grid gap-8 lg:grid-cols-5">
        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="lg:col-span-3 space-y-6"
        >
          <Card>
            <CardContent className="p-6 space-y-6">
              {/* Datos personales */}
              <fieldset>
                <legend className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-4">
                  Datos personales
                </legend>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-1.5">
                    <Label>Edad</Label>
                    <Input
                      type="number"
                      min={18}
                      max={70}
                      value={form.Age}
                      onChange={(e) => update("Age", Number(e.target.value))}
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label>Género</Label>
                    <Select
                      value={String(form.Gender)}
                      onValueChange={(v) => update("Gender", Number(v))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="0">Femenino</SelectItem>
                        <SelectItem value="1">Masculino</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1.5">
                    <Label>Estado civil</Label>
                    <Select
                      value={form.MaritalStatus}
                      onValueChange={(v) => update("MaritalStatus", v)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {MARITAL_STATUSES.map((s) => (
                          <SelectItem key={s} value={s}>
                            {s === "Divorced" ? "Divorciado" : s === "Married" ? "Casado" : "Soltero"}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1.5">
                    <Label>Empresas anteriores</Label>
                    <Input
                      type="number"
                      min={0}
                      max={20}
                      value={form.NumCompaniesWorked}
                      onChange={(e) => update("NumCompaniesWorked", Number(e.target.value))}
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label>Distancia al trabajo (km)</Label>
                    <Input
                      type="number"
                      min={1}
                      max={50}
                      value={form.DistanceFromHome}
                      onChange={(e) => update("DistanceFromHome", Number(e.target.value))}
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label>Años de experiencia total</Label>
                    <Input
                      type="number"
                      min={0}
                      max={50}
                      value={form.TotalWorkingYears}
                      onChange={(e) => update("TotalWorkingYears", Number(e.target.value))}
                    />
                  </div>
                </div>
              </fieldset>

              <Separator />

              {/* Puesto y compensación */}
              <fieldset>
                <legend className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-4">
                  Puesto y compensación
                </legend>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-1.5">
                    <Label>Departamento</Label>
                    <Select
                      value={form.Department}
                      onValueChange={(v) => update("Department", v)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {DEPARTMENTS.map((d) => (
                          <SelectItem key={d} value={d}>
                            {d === "Research & Development" ? "Investigación y Desarrollo" : d === "Human Resources" ? "Recursos Humanos" : "Ventas"}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1.5">
                    <Label>Rol del puesto</Label>
                    <Select
                      value={form.JobRole}
                      onValueChange={(v) => update("JobRole", v)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {JOB_ROLES.map((r) => (
                          <SelectItem key={r} value={r}>
                            {r}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1.5">
                    <Label>Campo de estudio</Label>
                    <Select
                      value={form.EducationField}
                      onValueChange={(v) => update("EducationField", v)}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {EDUCATION_FIELDS.map((f) => (
                          <SelectItem key={f} value={f}>
                            {f}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1.5">
                    <Label>Ingreso mensual (USD)</Label>
                    <Input
                      type="number"
                      min={1000}
                      max={50000}
                      step={100}
                      value={form.MonthlyIncome}
                      onChange={(e) => update("MonthlyIncome", Number(e.target.value))}
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label>Años en la empresa</Label>
                    <Input
                      type="number"
                      min={0}
                      max={40}
                      value={form.YearsAtCompany}
                      onChange={(e) => update("YearsAtCompany", Number(e.target.value))}
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label>Años en el rol actual</Label>
                    <Input
                      type="number"
                      min={0}
                      max={20}
                      value={form.YearsInCurrentRole}
                      onChange={(e) => update("YearsInCurrentRole", Number(e.target.value))}
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label>Años desde última promoción</Label>
                    <Input
                      type="number"
                      min={0}
                      max={20}
                      value={form.YearsSinceLastPromotion}
                      onChange={(e) => update("YearsSinceLastPromotion", Number(e.target.value))}
                    />
                  </div>
                </div>
              </fieldset>

              <Separator />

              {/* Satisfacción y condiciones */}
              <fieldset>
                <legend className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-4">
                  Satisfacción y condiciones
                </legend>
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-1.5">
                    <Label>Horas extra</Label>
                    <Select
                      value={String(form.OverTime)}
                      onValueChange={(v) => update("OverTime", Number(v))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="0">No</SelectItem>
                        <SelectItem value="1">Sí</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1.5">
                    <Label>Satisfacción laboral</Label>
                    <Select
                      value={String(form.JobSatisfaction)}
                      onValueChange={(v) => update("JobSatisfaction", Number(v))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {[1, 2, 3, 4].map((v) => (
                          <SelectItem key={v} value={String(v)}>
                            {SAT_LABELS[v]} ({v})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1.5">
                    <Label>Balance vida-trabajo</Label>
                    <Select
                      value={String(form.WorkLifeBalance)}
                      onValueChange={(v) => update("WorkLifeBalance", Number(v))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {[1, 2, 3, 4].map((v) => (
                          <SelectItem key={v} value={String(v)}>
                            {WORKLIFE_LABELS[v]} ({v})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1.5">
                    <Label>Satisfacción con el entorno</Label>
                    <Select
                      value={String(form.EnvironmentSatisfaction)}
                      onValueChange={(v) => update("EnvironmentSatisfaction", Number(v))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {[1, 2, 3, 4].map((v) => (
                          <SelectItem key={v} value={String(v)}>
                            {SAT_LABELS[v]} ({v})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-1.5 sm:col-span-2">
                    <Label>Frecuencia de viajes</Label>
                    <Select
                      value={String(form.BusinessTravel)}
                      onValueChange={(v) => update("BusinessTravel", Number(v))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="0">No viaja</SelectItem>
                        <SelectItem value="1">Viaja raramente</SelectItem>
                        <SelectItem value="2">Viaja frecuentemente</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </fieldset>

              <Button
                type="submit"
                className="w-full bg-[#E17055] hover:bg-[#d0654e] text-white"
                disabled={loading}
              >
                {loading ? "Procesando..." : "🎯 Predecir riesgo de abandono"}
              </Button>
            </CardContent>
          </Card>
        </form>

        {/* Results */}
        <div className="lg:col-span-2 space-y-4">
          {error && (
            <Card className="border-red-200 bg-red-50">
              <CardContent className="p-4 text-sm text-red-700">
                ❌ {error}
              </CardContent>
            </Card>
          )}

          {result && (
            <>
              <Card className={`border ${riscoColor(result.riesgo)}`}>
                <CardContent className="p-6 space-y-4">
                  <h2 className="text-lg font-semibold">Resultado de la predicción</h2>
                  <p className={`text-xl font-bold ${riscoColor(result.riesgo).split(" ")[2]}`}>
                    {riscoLabel(result.riesgo)}
                  </p>

                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">
                        Probabilidad de abandono
                      </p>
                      <div className="h-3 w-full rounded-full bg-gray-200 overflow-hidden">
                        <div
                          className="h-full rounded-full transition-all duration-500"
                          style={{
                            width: `${(result.probabilidad_abandono * 100).toFixed(1)}%`,
                            backgroundColor:
                              result.riesgo === "ALTO"
                                ? "#D63031"
                                : result.riesgo === "MEDIO"
                                ? "#F39C12"
                                : "#00B894",
                          }}
                        />
                      </div>
                      <p className="mt-1 text-right text-sm font-semibold">
                        {(result.probabilidad_abandono * 100).toFixed(1)}%
                      </p>
                    </div>
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div className="rounded-lg bg-muted p-3 text-center">
                        <p className="text-muted-foreground text-xs">Abandono</p>
                        <p className="text-lg font-bold">
                          {(result.probabilidad_abandono * 100).toFixed(1)}%
                        </p>
                      </div>
                      <div className="rounded-lg bg-muted p-3 text-center">
                        <p className="text-muted-foreground text-xs">Permanencia</p>
                        <p className="text-lg font-bold">
                          {(result.probabilidad_permanencia * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4 text-xs text-muted-foreground leading-relaxed">
                  ⚠️ {result.advertencia}
                </CardContent>
              </Card>
            </>
          )}

          {!result && !error && (
            <Card>
              <CardContent className="p-8 text-center text-muted-foreground">
                <p className="text-lg mb-2">🤖</p>
                <p>Completa el formulario y presiona</p>
                <p className="font-medium">&ldquo;Predecir riesgo de abandono&rdquo;</p>
                <p className="text-xs mt-2">para ver el resultado aquí.</p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
