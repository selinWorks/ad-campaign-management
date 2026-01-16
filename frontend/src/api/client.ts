// --- src/api/client.ts ---
import axios from "axios";
import type { RecordItem } from "../types/record";

import {
  fetchRecords,
  runCalculate,
  createOrUpdateRecord,
  patchRecord,
  deleteRecord,
} from "./endpoints";

// Vercel env: VITE_API_BASE_URL="https://ad-campaign-management.onrender.com"
// Local dev: env yoksa Vite proxy ile "/api" çalışır.
const BASE = import.meta.env.VITE_API_BASE_URL as string | undefined;

export const api = axios.create({
  baseURL: BASE ? `${BASE.replace(/\/$/, "")}/api` : "/api",
  timeout: 30000,
});

// DashboardPage uyumlu helper'lar
export async function apiGetRecords() {
  const res = await fetchRecords();
  return res.data; // { success, count, data }
}

export async function apiCalculate() {
  return runCalculate();
}

export async function apiCreateRecord(
  payload: { label: string; campaign_name: string } & Partial<RecordItem>
) {
  return createOrUpdateRecord(payload);
}

export async function apiPatchRecord(id: number, payload: Partial<RecordItem>) {
  return patchRecord(id, payload);
}

export async function apiDeleteRecord(id: number) {
  return deleteRecord(id);
}