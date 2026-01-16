// --- src/components/RecordsTable.tsx ---
import { useMemo, useState } from "react";
import type { RecordRow } from "../types/record";
import styles from "./RecordsTable.module.css";

type Props = {
  rows: RecordRow[];
  onEdit: (row: RecordRow) => void;
  onDelete: (row: RecordRow) => void;
};

export default function RecordsTable({ rows, onEdit, onDelete }: Props) {
  const [pageSize, setPageSize] = useState<number>(15);
  const [page, setPage] = useState<number>(1);

  const totalPages = Math.max(1, Math.ceil(rows.length / pageSize));

  const { pageRows, clampPage } = useMemo(() => {
    const tp = Math.max(1, Math.ceil(rows.length / pageSize));
    const cp = Math.min(Math.max(1, page), tp);
    const start = (cp - 1) * pageSize;
    const end = start + pageSize;
    return { pageRows: rows.slice(start, end), clampPage: cp };
  }, [rows, pageSize, page]);

  if (clampPage !== page) {
    setTimeout(() => setPage(clampPage), 0);
  }

  const from = rows.length === 0 ? 0 : (clampPage - 1) * pageSize + 1;
  const to = rows.length === 0 ? 0 : Math.min(clampPage * pageSize, rows.length);

  return (
    <div className={styles.wrap}>
      <div className={styles.header}>
        <div className={styles.title}>Records</div>

        <div className={styles.right}>
          <div className={styles.count}>{rows.length} rows</div>

          <select
            className={styles.select}
            value={pageSize}
            onChange={(e) => {
              const next = Number(e.target.value);
              setPageSize(next);
              setPage(1);
            }}
          >
            <option value={10}>10 / sayfa</option>
            <option value={15}>15 / sayfa</option>
            <option value={25}>25 / sayfa</option>
            <option value={50}>50 / sayfa</option>
          </select>
        </div>
      </div>

      <div className={styles.tableWrap}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Label</th>
              <th>Campaign</th>
              <th>Platform</th>
              <th>Camp Cost</th>
              <th>Camp CPA</th>
              <th>New Daily Budget</th>
              <th>New Target CPA</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {pageRows.map((r) => (
              <tr key={r.id}>
                <td>{r.label}</td>
                <td className={styles.mono}>{r.campaign_name}</td>
                <td>{r.platform ?? "-"}</td>
                <td>{fmt(r.camp_cost)}</td>
                <td>{fmt(r.camp_cpa)}</td>
                <td>{fmt(r.new_daily_budget)}</td>
                <td>{fmt(r.new_target_cpa)}</td>

                <td className={styles.actions}>
  <button className={styles.iconBtn} onClick={() => onEdit(r)} title="Düzenle">
  <span className={styles.icon}>✏️</span>
</button>

  <button className={`${styles.iconBtn} ${styles.danger}`} onClick={() => onDelete(r)} title="Sil">
  <span className={styles.icon}>🗑️</span>
</button>
</td>
              </tr>
            ))}

            {pageRows.length === 0 && (
              <tr>
                <td colSpan={8} className={styles.empty}>
                  Henüz veri yok. Excel yükleyin.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className={styles.pager}>
        <button className={styles.btn} disabled={clampPage <= 1} onClick={() => setPage(1)}>
          {"<<"}
        </button>
        <button
          className={styles.btn}
          disabled={clampPage <= 1}
          onClick={() => setPage((p) => Math.max(1, p - 1))}
        >
          {"<"}
        </button>

        <div className={styles.pageInfo}>
          {from}-{to} / {rows.length} • Sayfa {clampPage} / {totalPages}
        </div>

        <button
          className={styles.btn}
          disabled={clampPage >= totalPages}
          onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
        >
          {">"}
        </button>
        <button className={styles.btn} disabled={clampPage >= totalPages} onClick={() => setPage(totalPages)}>
          {">>"}
        </button>
      </div>
    </div>
  );
}

function fmt(v: number | null | undefined) {
  if (v === null || v === undefined) return "-";
  const n = Number(v);
  if (Number.isNaN(n)) return "-";
  return n.toFixed(4).replace(/\.?0+$/, "");
}



