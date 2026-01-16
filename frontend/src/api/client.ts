// --- src/api/client.ts ---
import axios from "axios";
import { fetchRecords, runCalculate, createOrUpdateRecord, patchRecord, deleteRecord } from "./endpoints";
import type { RecordItem } from "../types/record";


export const api = axios.create({
  baseURL: "/api", // vite proxy -> http://127.0.0.1:9100
  timeout: 30000,
});

// DashboardPage uyumlu helper'lar
export async function apiGetRecords() {
  const res = await fetchRecords();
  return res.data;
}

export async function apiCalculate() {
  return runCalculate();
}

export async function apiCreateRecord(payload: { label: string; campaign_name: string } & Partial<RecordItem>) {
  return createOrUpdateRecord(payload);
}

export async function apiPatchRecord(id: number, payload: Partial<RecordItem>) {
  return patchRecord(id, payload);
}

export async function apiDeleteRecord(id: number) {
  return deleteRecord(id);
}