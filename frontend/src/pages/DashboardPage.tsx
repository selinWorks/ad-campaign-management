// --- src/pages/DashboardPage.tsx ---
import { useCallback, useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import UploadBox from "../components/UploadBox";
import CalculatePanel from "../components/CalculatePanel";
import RecordsTable from "../components/RecordsTable";
import Toolbar from "../components/Toolbar";
import RecordModal from "../components/RecordModal";

import type { RecordRow } from "../types/record";
import {
  apiCalculate,
  apiGetRecords,
  apiCreateRecord,
  apiPatchRecord,
  apiDeleteRecord,
} from "../api/client";

export default function DashboardPage() {
  const [rows, setRows] = useState<RecordRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<"create" | "edit">("create");
  const [editing, setEditing] = useState<RecordRow | null>(null);


  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiGetRecords();   // { success, count, data }
      setRows(res.data as RecordRow[]);
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
        if (!editing) throw new Error("Edit kaydı bulunamadı (editing null).");
        await apiPatchRecord(editing.id, payload);
      }

      await apiCalculate();
      await refresh();
      setModalOpen(false);
    } catch (e: any) {
      setError(e?.message || "Save failed");
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(row: RecordRow) {
    const ok = window.confirm(
      `Bu kaydı silmek istiyor musunuz?\n\nLabel: ${row.label}\nCampaign: ${row.campaign_name}`
    );
    if (!ok) return;

    setLoading(true);
    setError(null);
    try {
      await apiDeleteRecord(row.id);
      await refresh();
    } catch (e: any) {
      setError(e?.message || "Delete failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <div className="container">
        <Navbar />
        <div className="statsBar">
  <div className="chipGlow">
    <span className="chipDot" />
    {rows.length} records
  </div>
  <div className="chipGlow chipGlow2">
    <span className="chipDot" />
    {Array.from(new Set(rows.map((r) => r.platform).filter(Boolean))).length} platforms
  </div>
</div>


        <div className="grid-2">
          <UploadBox onUploaded={refresh} />
          <CalculatePanel onDone={refresh} onCalculate={onCalculate} />
        </div>

        <Toolbar onRefresh={refresh} onCreate={openCreate} />

        {error && <div className="alert alert-error">{error}</div>}
        {loading && <div className="alert">Loading...</div>}

        <RecordsTable rows={rows} onEdit={openEdit} onDelete={handleDelete} />

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