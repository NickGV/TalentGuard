"use client";

import { useEffect, useState, useMemo } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, Legend,
} from "recharts";
import { Card, CardContent } from "@/components/ui/card";
import { KpiCard } from "@/components/kpi-card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";

const CORAL = "#E17055";
const SLATE = "#4A6FA5";
const COLORS = [SLATE, CORAL, "#00B894", "#F39C12", "#6C5CE7", "#FD79A8"];

type Fila = Record<string, number>;
type Filters = { overtime: string; satisfaction: string; attrition: string };

const SAT_LABELS: Record<number, string> = {
  1: "Bajo", 2: "Medio", 3: "Alto", 4: "Muy Alto",
};

export default function InsightsPage() {
  const [data, setData] = useState<Fila[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<Filters>({
    overtime: "todos",
    satisfaction: "todas",
    attrition: "todos",
  });

  useEffect(() => {
    fetch("/datos.json")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    let f = data;
    if (filters.overtime !== "todos") {
      f = f.filter((r) => r.OverTime === Number(filters.overtime));
    }
    if (filters.satisfaction !== "todas") {
      f = f.filter((r) => r.JobSatisfaction === Number(filters.satisfaction));
    }
    if (filters.attrition !== "todos") {
      f = f.filter((r) => r.Attrition === Number(filters.attrition));
    }
    return f;
  }, [data, filters]);

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-48" />
        <Skeleton className="h-8 w-96" />
        <div className="grid gap-4 sm:grid-cols-4">
          {[...Array(4)].map((_, i) => (
            <Skeleton key={i} className="h-28 rounded-xl" />
          ))}
        </div>
        <Skeleton className="h-80 rounded-xl" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-[#2D3436]">
        🔍 Análisis exploratorio
      </h1>
      <p className="text-muted-foreground">
        Visualizaciones interactivas para entender los factores asociados a la
        rotación de empleados.
      </p>

      {/* Filters */}
      <Card>
        <CardContent className="p-6">
          <h2 className="mb-4 text-sm font-semibold text-muted-foreground uppercase tracking-wider">
            Filtros
          </h2>
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="space-y-1.5">
              <label className="text-sm font-medium">Horas extra</label>
              <Select
                value={filters.overtime}
                onValueChange={(v) =>
                  setFilters((f) => ({ ...f, overtime: v ?? "todos" }))
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="todos">Todos</SelectItem>
                  <SelectItem value="1">Con horas extra</SelectItem>
                  <SelectItem value="0">Sin horas extra</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-medium">Satisfacción laboral</label>
              <Select
                value={filters.satisfaction}
                onValueChange={(v) =>
                  setFilters((f) => ({ ...f, satisfaction: v ?? "todas" }))
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="todas">Todas</SelectItem>
                  <SelectItem value="1">Bajo (1)</SelectItem>
                  <SelectItem value="2">Medio (2)</SelectItem>
                  <SelectItem value="3">Alto (3)</SelectItem>
                  <SelectItem value="4">Muy Alto (4)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-medium">Estado de rotación</label>
              <Select
                value={filters.attrition}
                onValueChange={(v) =>
                  setFilters((f) => ({ ...f, attrition: v ?? "todos" }))
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="todos">Todos</SelectItem>
                  <SelectItem value="1">Abandonó</SelectItem>
                  <SelectItem value="0">Permaneció</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <p className="mt-3 text-xs text-muted-foreground">
            Registros mostrados: {filtered.length} de {data.length}
          </p>
        </CardContent>
      </Card>

      {/* Filtered KPIs */}
      <div className="grid gap-4 sm:grid-cols-4">
        <KpiCard
          title="Tasa de abandono"
          value={
            filtered.length
              ? `${(
                  (filtered.filter((r) => r.Attrition === 1).length /
                    filtered.length) *
                  100
                ).toFixed(1)}%`
              : "—"
          }
        />
        <KpiCard
          title="Ingreso mediano"
          value={
            filtered.length
              ? `$${median(filtered.map((r) => r.MonthlyIncome)).toLocaleString()}`
              : "—"
          }
        />
        <KpiCard
          title="Antigüedad mediana"
          value={
            filtered.length
              ? `${median(filtered.map((r) => r.YearsAtCompany)).toFixed(0)} años`
              : "—"
          }
        />
        <KpiCard
          title="Con horas extra"
          value={
            filtered.length
              ? `${(
                  (filtered.filter((r) => r.OverTime === 1).length /
                    filtered.length) *
                  100
                ).toFixed(1)}%`
              : "—"
          }
        />
      </div>

      {/* Visualizations */}
      {filtered.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-muted-foreground">
            No hay registros para la combinación de filtros seleccionada.
          </CardContent>
        </Card>
      ) : (
        <Tabs defaultValue="distribucion" className="space-y-4">
          <TabsList className="w-full overflow-x-auto flex-nowrap gap-1 hide-scrollbar">
            <TabsTrigger value="distribucion">Distribución</TabsTrigger>
            <TabsTrigger value="overtime">Horas extra</TabsTrigger>
            <TabsTrigger value="income">Ingreso</TabsTrigger>
            <TabsTrigger value="satisfaction">Satisfacción</TabsTrigger>
            <TabsTrigger value="tenure">Antigüedad</TabsTrigger>
          </TabsList>

          {/* Viz 1: Distribución */}
          <TabsContent value="distribucion">
            <Card>
              <CardContent className="p-6 space-y-4">
                <h3 className="text-lg font-semibold text-[#2D3436]">
                  1. Distribución de rotación
                </h3>
                <div className="grid gap-6 md:grid-cols-2">
                  <div className="h-72">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={[
                            {
                              name: "No abandona",
                              value: filtered.filter((r) => r.Attrition === 0)
                                .length,
                            },
                            {
                              name: "Abandona",
                              value: filtered.filter((r) => r.Attrition === 1)
                                .length,
                            },
                          ]}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={100}
                          paddingAngle={4}
                          dataKey="value"
                          label={({ name, percent }) =>
                            `${name} ${((percent ?? 0) * 100).toFixed(1)}%`
                          }
                        >
                          <Cell fill={SLATE} />
                          <Cell fill={CORAL} />
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="flex items-center">
                    <p className="text-sm leading-relaxed text-muted-foreground">
                      El dataset presenta un desbalance significativo: 
                      aproximadamente el <strong>16%</strong> de los empleados 
                      abandonó la organización. Este desbalance justifica el uso 
                      de <strong>F1-Score</strong> como métrica principal y el 
                      ajuste de pesos de clase en el modelo.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Viz 2: Horas extra */}
          <TabsContent value="overtime">
            <Card>
              <CardContent className="p-6 space-y-4">
                <h3 className="text-lg font-semibold text-[#2D3436]">
                  2. Impacto de las horas extra en la rotación
                </h3>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={calcOvertimeAttrition(filtered)}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                      <XAxis dataKey="name" />
                      <YAxis
                        unit="%"
                        domain={[0, 50]}
                        tickFormatter={(v) => `${v}%`}
                      />
                      <Tooltip formatter={(v) => `${Number(v).toFixed(1)}%`} />
                      <Bar
                        dataKey="tasa"
                        radius={[6, 6, 0, 0]}
                        barSize={120}
                      >
                        {calcOvertimeAttrition(filtered).map((_, i) => (
                          <Cell key={i} fill={i === 0 ? SLATE : CORAL} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <p className="text-sm text-muted-foreground">
                  Los empleados con horas extra tienen una tasa de abandono ~3
                  veces mayor.
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Viz 3: Ingreso mensual */}
          <TabsContent value="income">
            <Card>
              <CardContent className="p-6 space-y-4">
                <h3 className="text-lg font-semibold text-[#2D3436]">
                  3. Distribución del ingreso mensual
                </h3>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={calcIncomeBins(filtered)}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                      <XAxis dataKey="bin" tick={{ fontSize: 11 }} />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar
                        dataKey="No abandona"
                        fill={SLATE}
                        radius={[4, 4, 0, 0]}
                      />
                      <Bar
                        dataKey="Abandona"
                        fill={CORAL}
                        radius={[4, 4, 0, 0]}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <p className="text-sm text-muted-foreground">
                  Los empleados que abandonan se concentran en rangos salariales
                  más bajos.
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Viz 4: Satisfacción */}
          <TabsContent value="satisfaction">
            <Card>
              <CardContent className="p-6 space-y-4">
                <h3 className="text-lg font-semibold text-[#2D3436]">
                  4. Tasa de abandono por satisfacción laboral
                </h3>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={calcSatisfaction(filtered)}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                      <XAxis dataKey="name" />
                      <YAxis
                        unit="%"
                        domain={[0, 35]}
                        tickFormatter={(v) => `${v}%`}
                      />
                      <Tooltip formatter={(v) => `${Number(v).toFixed(1)}%`} />
                      <Bar
                        dataKey="tasa"
                        radius={[6, 6, 0, 0]}
                        barSize={80}
                        fill={SLATE}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <p className="text-sm text-muted-foreground">
                  A menor satisfacción laboral, mayor probabilidad de abandono.
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Viz 5: Antigüedad */}
          <TabsContent value="tenure">
            <Card>
              <CardContent className="p-6 space-y-4">
                <h3 className="text-lg font-semibold text-[#2D3436]">
                  5. Riesgo de abandono por antigüedad en la empresa
                </h3>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={calcTenureGroups(filtered)}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                      <XAxis dataKey="name" />
                      <YAxis
                        unit="%"
                        domain={[0, 50]}
                        tickFormatter={(v) => `${v}%`}
                      />
                      <Tooltip formatter={(v) => `${Number(v).toFixed(1)}%`} />
                      <Bar
                        dataKey="tasa"
                        radius={[6, 6, 0, 0]}
                        barSize={60}
                        fill={SLATE}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <p className="text-sm text-muted-foreground">
                  El 61% de los abandonos ocurren en los primeros 3 años —
                  período crítico para las estrategias de retención temprana.
                </p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}

/* ── Helpers ── */

function median(arr: number[]): number {
  const s = [...arr].sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
}

function calcOvertimeAttrition(data: Fila[]) {
  const groups = [
    { name: "Sin horas extra", key: 0 },
    { name: "Con horas extra", key: 1 },
  ];
  return groups.map((g) => {
    const subset = data.filter((r) => r.OverTime === g.key);
    return {
      name: g.name,
      tasa: subset.length
        ? (subset.filter((r) => r.Attrition === 1).length / subset.length) * 100
        : 0,
    };
  });
}

function calcIncomeBins(data: Fila[]) {
  const bins = [
    { bin: "< $3K", min: 0, max: 3000 },
    { bin: "$3-5K", min: 3000, max: 5000 },
    { bin: "$5-7K", min: 5000, max: 7000 },
    { bin: "$7-10K", min: 7000, max: 10000 },
    { bin: "$10-15K", min: 10000, max: 15000 },
    { bin: "$15K+", min: 15000, max: Infinity },
  ];
  return bins.map((b) => {
    const inBin = data.filter(
      (r) => r.MonthlyIncome >= b.min && r.MonthlyIncome < b.max
    );
    return {
      bin: b.bin,
      "No abandona": inBin.filter((r) => r.Attrition === 0).length,
      Abandona: inBin.filter((r) => r.Attrition === 1).length,
    };
  });
}

function calcSatisfaction(data: Fila[]) {
  return [1, 2, 3, 4].map((level) => {
    const subset = data.filter((r) => r.JobSatisfaction === level);
    return {
      name: SAT_LABELS[level],
      tasa: subset.length
        ? (subset.filter((r) => r.Attrition === 1).length / subset.length) * 100
        : 0,
    };
  });
}

function calcTenureGroups(data: Fila[]) {
  const groups = [
    { name: "0-1 año", min: 0, max: 1 },
    { name: "2-3 años", min: 2, max: 3 },
    { name: "4-7 años", min: 4, max: 7 },
    { name: "8-15 años", min: 8, max: 15 },
    { name: "16+ años", min: 16, max: Infinity },
  ];
  return groups.map((g) => {
    const subset = data.filter(
      (r) => r.YearsAtCompany >= g.min && r.YearsAtCompany <= g.max
    );
    return {
      name: g.name,
      tasa: subset.length
        ? (subset.filter((r) => r.Attrition === 1).length / subset.length) * 100
        : 0,
    };
  });
}
