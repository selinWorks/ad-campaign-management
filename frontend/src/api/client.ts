// --- src/api/client.ts ---
import axios from "axios";
import type { RecordItem } from "../types/record";

import {
  fetchRecords,
  runCalculate,
  createOrUpdateRecord,
  patchRecord,
  deleteRecord,
  uploadExcel,
  downloadExportExcel,
  pingHealth,
} from "./endpoints";

const BASE = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/+$/, "");

// API instance
export const api = axios.create({
  baseURL: BASE ? `${BASE}/api` : "/api",
  timeout: 30000,
});

// ===== Dashboard uyumlu helper'lar (tek tip: ham data dondur) =====

export async function apiPingHealth() {
  return pingHealth();
}

export async function apiGetRecords() {
  const res = await fetchRecords();
  // backend: { success, count, data: RecordItem[] }
  return res.data; // RecordItem[]
}

export async function apiCalculate() {
  return runCalculate();
}

export async function apiUploadExcel(file: File) {
  return uploadExcel(file);
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

export async function apiDownloadExportExcel() {
  return downloadExportExcel();
}