import { useRef, useState } from "react";
import styles from "./UploadBox.module.css";

export default function UploadBox({ onUploaded }: { onUploaded?: () => void }) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  async function upload(file: File) {
    setLoading(true);
    setMsg(null);

    try {
      const fd = new FormData();
      fd.append("file", file);

      const res = await fetch("/api/excel/upload", { method: "POST", body: fd });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail?.message || data?.detail || "Upload failed");

      setMsg(`Yüklendi: ${data.filename} — ${data.row_count} satır`);
      onUploaded?.();
    } catch (e: any) {
      setMsg(`Hata: ${e.message || "Upload error"}`);
    } finally {
      setLoading(false);
    }
  }

  function onPick() {
    inputRef.current?.click();
  }

  function onChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    upload(file);
  }

  function onDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (!file) return;
    upload(file);
  }

  return (
    <div className={styles.card} onDragOver={(e) => e.preventDefault()} onDrop={onDrop}>
      <div className={styles.header}>
        <div>
          <div className={styles.title}>Excel Upload</div>
          <div className={styles.sub}>Drag & drop veya dosya seç (.xlsx)</div>
        </div>

        <button className={styles.btn} onClick={onPick} disabled={loading}>
          {loading ? "Yükleniyor..." : "Dosya Seç"}
        </button>

        <input ref={inputRef} type="file" accept=".xlsx" style={{ display: "none" }} onChange={onChange} />
      </div>

      {msg && <div className={styles.msg}>{msg}</div>}
    </div>
  );
}