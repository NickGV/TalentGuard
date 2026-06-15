"use client";

import { useEffect, useState } from "react";
import { getMetricas } from "@/lib/api";
import type { MetricasResponse } from "@/lib/types";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { KpiCard } from "@/components/kpi-card";
import { Skeleton } from "@/components/ui/skeleton";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell,
} from "recharts";

export default function ModelPage() {
  const [data, setData] = useState<MetricasResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    getMetricas()
      .then(setData)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-48" />
        <Skeleton className="h-72 rounded-xl" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="py-12 text-center text-muted-foreground">
        <p className="text-lg font-medium">API no disponible</p>
      </div>
    );
  }

  const { metricas } = data;

  const chartData = [
    { name: "Accuracy", value: metricas.accuracy, fill: "#4A6FA5" },
    { name: "Recall", value: metricas.recall_macro, fill: "#E17055" },
    { name: "F1-macro", value: metricas.f1_macro, fill: "#00B894" },
    { name: "ROC-AUC", value: metricas.roc_auc, fill: "#F39C12" },
    { name: "Precisión", value: metricas.precision_macro, fill: "#6C5CE7" },
  ];

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-[#2D3436]">
        📈 Métricas del modelo
      </h1>
      <p className="text-muted-foreground">
        Rendimiento del modelo <strong>{data.modelo}</strong> sobre el conjunto
        de prueba (294 registros reservados). Entrenado el{" "}
        {new Date(data.fecha_entrenamiento).toLocaleDateString("es-ES")}.
      </p>

      {/* Model info badge */}
      <div className="flex flex-wrap gap-2">
        <Badge variant="outline" className="text-sm">
          {data.modelo}
        </Badge>
        <Badge variant="outline" className="text-sm">
          v{data.version}
        </Badge>
        <Badge variant="outline" className="text-sm">
          class_weight={data.class_weight}
        </Badge>
      </div>

      {/* KPI cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard
          title="F1-macro"
          value={metricas.f1_macro.toFixed(3)}
          subtitle="Métrica principal"
        />
        <KpiCard
          title="Accuracy"
          value={`${(metricas.accuracy * 100).toFixed(0)}%`}
          subtitle={`${(metricas.accuracy * 100).toFixed(1)}%`}
        />
        <KpiCard
          title="ROC-AUC"
          value={metricas.roc_auc.toFixed(3)}
          subtitle="Poder predictivo"
        />
        <KpiCard
          title="Precisión macro"
          value={metricas.precision_macro.toFixed(3)}
          subtitle="Media de clases"
        />
      </div>

      {/* Chart */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-lg font-semibold text-[#2D3436]">
            Comparativa de métricas
          </h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={chartData}
                layout="vertical"
                margin={{ left: 80, right: 40, top: 10, bottom: 10 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis
                  type="number"
                  domain={[0, 1]}
                  tickFormatter={(v) => v.toFixed(1)}
                />
                <YAxis
                  type="category"
                  dataKey="name"
                  tick={{ fontSize: 13 }}
                />
                <Tooltip formatter={(v) => Number(v).toFixed(3)} />
                <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={28}>
                  {chartData.map((entry, i) => (
                    <Cell key={i} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Lectura sencilla */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-lg font-semibold text-[#2D3436]">
            📖 Lectura sencilla de las métricas
          </h2>
          <div className="space-y-4 text-sm leading-relaxed text-muted-foreground">
            <p>
              <strong>Recall ({(metricas.recall_macro * 100).toFixed(0)}%):</strong>{" "}
              De cada 10 empleados que realmente abandonan, el modelo detecta
              aproximadamente{" "}
              <strong>{Math.round(metricas.recall_macro * 10)}</strong>. Este es
              el número más importante para el negocio — preferimos identificar a
              alguien en riesgo aunque de vez en cuando marquemos un falso
              positivo.
            </p>
            <p>
              <strong>Accuracy ({(metricas.accuracy * 100).toFixed(0)}%):</strong>{" "}
              El modelo acierta en {Math.round(metricas.accuracy * 100)} de cada
              100 predicciones. En un dataset desbalanceado (84% permanecen, 16%
              abandonan), esta métrica por sí sola no cuenta toda la historia.
            </p>
            <p>
              <strong>ROC-AUC ({metricas.roc_auc.toFixed(3)}):</strong> Mide la
              capacidad del modelo para separar empleados que se quedan de los
              que se van. Un valor de 0.5 es aleatorio, 1.0 es perfecto. Nuestro
              modelo obtiene <strong>{metricas.roc_auc.toFixed(3)}</strong>, lo
              que indica un poder predictivo sólido.
            </p>
            <p>
              <strong>F1-Yes ({metricas.f1_yes.toFixed(3)}):</strong> Mide el
              rendimiento específicamente en la clase minoritaria (abandono). Es
              menor que el F1-macro porque la clase de abandono tiene solo 47
              casos en el conjunto de prueba — un error individual pesa más.
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Por qué recall y no accuracy */}
      <Card className="border-emerald-200 bg-emerald-50">
        <CardContent className="p-4 text-sm text-emerald-800 leading-relaxed">
          <strong>¿Por qué recall y no accuracy?</strong> En retención de
          talento, el costo de un falso negativo (no detectar a alguien que se
          va) es mucho mayor que el de un falso positivo (agendar una reunión
          innecesaria). Por eso optimizamos el modelo para maximizar el recall,
          incluso si eso reduce la precisión general.
        </CardContent>
      </Card>
    </div>
  );
}
