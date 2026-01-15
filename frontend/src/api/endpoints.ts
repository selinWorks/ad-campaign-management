// --- src/api/endpoint.ts ---
import { api } from "./client";
import type { RecordItem } from "../types/record";

export async function pingHealth() {
  const res = await api.get("/health");
  return res.data as { ok: boolean };
}

export async function fetchRecords() {
  const res = await api.get("/records/");
  return res.data as { success: boolean; count: number; data: RecordItem[] };
}

export async function uploadExcel(file: File) {
  const fd = new FormData();
  fd.append("file", file);
  const res = await api.post("/excel/upload", fd, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export async function createOrUpdateRecord(
  payload: Partial<RecordItem> & { label: string; campaign_name: string }
) {
  const res = await api.post("/records/", payload);
  return res.data as { success: boolean; created?: boolean; id: number };
}

export async function patchRecord(id: number, payload: Partial<RecordItem>) {
  const res = await api.patch(`/records/${id}`, payload);
  return res.data as { success: boolean };
}

export async function runCalculate() {
  const res = await api.post("/calculate/");
  return res.data;
}

export async function downloadExportExcel() {
  const res = await api.get("/export/excel", { responseType: "blob" });
  return res.data as Blob;
}