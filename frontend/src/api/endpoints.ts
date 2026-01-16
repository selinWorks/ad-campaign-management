// --- src/api/endpoints.ts ---
import { api } from "./client";
import type { RecordItem } from "../types/record";

export function pingHealth() {
  // health /api altında değilse bunu kullanma; backendine göre ayarla
  return api.get<{ ok: boolean }>("/health");
}

export function fetchRecords() {
  return api.get<{ success: boolean; count: number; data: RecordItem[] }>("/records/");
}

export function uploadExcel(file: File) {
  const fd = new FormData();
  fd.append("file", file);
  return api.post("/excel/upload", fd, {
    headers: { "Content-Type": "multipart/form-data" },
  });
}

export function createOrUpdateRecord(payload: Partial<RecordItem> & { label: string; campaign_name: string }) {
  return api.post("/records/", payload);
}

export function patchRecord(id: number, payload: Partial<RecordItem>) {
  return api.patch(`/records/${id}`, payload);
}

export function deleteRecord(id: number) {
  return api.delete(`/records/${id}`);
}

export function runCalculate() {
  return api.post("/calculate/");
}

export function downloadExportExcel() {
  return api.get("/export/excel", { responseType: "blob" });
}