// --- src/pages/DashboardPage.tsx ---
import { useCallback, useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";
import CalculatePanel from "../components/CalculatePanel";
import RecordsTable from "../components/RecordsTable";
import Toolbar from "../components/Toolbar";
import RecordModal from "../components/RecordModal";

import type { RecordRow } from "../types/record";
import { apiCalculate, apiGetRecords, apiCreateRecord, apiPatchRecord } from "../api/client";

export default function DashboardPage() {
  const [rows, setRows] = useState<RecordRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<"create" | "edit">("create");
  const [editing, setEditing] = useState<RecordRow | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiGetRecords();
      setRows(data);
    } catch (e: any) {
      setError(e?.message || "Load failed");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function onCalculate() {
    setLoading(true);
    setError(null);
    try {
      await apiCalculate();
      await refresh();
    } catch (e: any) {
      setError(e?.message || "Calculate failed");
    } finally {
      setLoading(false);
    }
  }

  function openCreate() {
    setModalMode("create");
    setEditing(null);
    setModalOpen(true);
  }

  function openEdit(row: RecordRow) {
    setModalMode("edit");
    setEditing(row);
    setModalOpen(true);
  }

  async function handleModalSubmit(payload: any) {
    setLoading(true);
    setError(null);
    try {
      if (modalMode === "create") {
        await apiCreateRecord(payload);
      } else {
        const id = Number(payload.id);
        const { id: _id, ...patch } = payload;
        await apiPatchRecord(id, patch);
      }
      await refresh();
    } catch (e: any) {
      setError(e?.message || "Save failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <div className="container">
        <Navbar />

        <div className="grid-2">
          <UploadBox onUploaded={refresh} />
          <CalculatePanel onDone={refresh} onCalculate={onCalculate} />
        </div>

        <Toolbar onRefresh={refresh} onCreate={openCreate} />

        {error && <div className="alert alert-error">{error}</div>}
        {loading && <div className="alert">Loading...</div>}

        <RecordsTable rows={rows} onEdit={openEdit} />

        <RecordModal
          open={modalOpen}
          mode={modalMode}
          initial={editing}
          onClose={() => setModalOpen(false)}
          onSubmit={handleModalSubmit}
        />
      </div>
    </div>
  );
}