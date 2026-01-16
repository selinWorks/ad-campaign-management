// --- src/api/client.ts ---
import axios from "axios";
import type { RecordItem } from "../types/record";

const RAW = import.meta.env.VITE_API_BASE_URL ?? "";
const ORIGIN = RAW.replace(/\/+$/, ""); // sondaki / temizle

export const api = axios.create({
  // Prod: https://...onrender.com/api
  // Dev: /api (vite proxy)
  baseURL: ORIGIN ? `${ORIGIN}/api` : "/api",
  timeout: 30000,
});

// DashboardPage uyumlu helper'lar (tek tip)
export async function apiGetRecords() {
  // returns: { success, count, data }
  const res = await api.get<{ success: boolean; count: number; data: RecordItem[] }>("/records/");
  return res.data;
}

export async function apiCalculate() {
  const res = await api.post("/calculate/");
  return res.data;
}

export async function apiCreateRecord(payload: { label: string; campaign_name: string } & Partial<RecordItem>) {
  const res = await api.post("/records/", payload);
  return res.data;
}

export async function apiPatchRecord(id: number, payload: Partial<RecordItem>) {
  const res = await api.patch(`/records/${id}`, payload);
  return res.data;
}

export async function apiDeleteRecord(id: number) {
  const res = await api.delete(`/records/${id}`);
  return res.data;
}

export async function apiUploadExcel(file: File) {
  const fd = new FormData();
  fd.append("file", file);
  const res = await api.post("/excel/upload", fd, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function apiDownloadExportExcel() {
  const res = await api.get("/export/excel", { responseType: "blob" });
  return res.data as Blob;
}