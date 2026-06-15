/* ──────────────────────────────────────────
   TalentGuard — Cliente API
   ────────────────────────────────────────── */

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `Error ${res.status}`);
  }
  return res.json();
}

import type {
  HealthResponse,
  DatosResponse,
  VariablesResponse,
  MetricasResponse,
  PredictRequest,
  PredictResponse,
} from "./types";

export function getHealth(): Promise<HealthResponse> {
  return fetchJson<HealthResponse>("/health");
}

export function getDatos(): Promise<DatosResponse> {
  return fetchJson<DatosResponse>("/datos");
}

export function getVariables(): Promise<VariablesResponse> {
  return fetchJson<VariablesResponse>("/variables");
}

export function getMetricas(): Promise<MetricasResponse> {
  return fetchJson<MetricasResponse>("/metricas");
}

export function postPredict(data: PredictRequest): Promise<PredictResponse> {
  return fetchJson<PredictResponse>("/predict", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
