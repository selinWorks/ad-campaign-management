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

// Render backend base url (ör: https://ad-campaign-management.onrender.com)
// Eğer yoksa boş kalır ve baseURL "/api" olur (local/proxy için)
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export const api = axios.create({
  baseURL: BASE_URL + "/api",
  timeout: 30000,
});

// DashboardPage uyumlu helper'lar
export async function apiGetRecords() {
  return fetchRecords();
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