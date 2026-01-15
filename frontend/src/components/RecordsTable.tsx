import { useMemo, useState, useEffect } from "react";
import type { RecordRow } from "../types/record";
import styles from "./RecordsTable.module.css";

export default function RecordsTable({ rows }: { rows: RecordRow[] }) {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(15);

  const totalPages = Math.max(1, Math.ceil(rows.length / pageSize));

  // rows değişince sayfa taşmasın
  useEffect(() => {
    if (page > totalPages) setPage(totalPages);
  }, [rows.length, page, totalPages]);

  const pagedRows = useMemo(() => {
    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    return rows.slice(start, end);
  }, [rows, page, pageSize]);

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
              setPageSize(Number(e.target.value));
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
            </tr>
          </thead>
          <tbody>
            {pagedRows.map((r) => (
              <tr key={r.id}>
                <td>{r.label}</td>
                <td className={styles.mono}>{r.campaign_name}</td>
                <td>{r.platform ?? "-"}</td>
                <td>{fmt(r.camp_cost)}</td>
                <td>{fmt(r.camp_cpa)}</td>
                <td>{fmt(r.new_daily_budget)}</td>
                <td>{fmt(r.new_target_cpa)}</td>
              </tr>
            ))}

            {rows.length === 0 && (
              <tr>
                <td colSpan={7} className={styles.empty}>
                  Henüz veri yok. Excel yükleyin.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {rows.length > 0 && (
        <div className={styles.pager}>
          <button
            className={styles.btn}
            onClick={() => setPage(1)}
            disabled={page === 1}
          >
            {"<<"}
          </button>
          <button
            className={styles.btn}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
          >
            {"<"}
          </button>

          <div className={styles.pageInfo}>
            Sayfa <b>{page}</b> / {totalPages}
          </div>

          <button
            className={styles.btn}
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
          >
            {">"}
          </button>
          <button
            className={styles.btn}
            onClick={() => setPage(totalPages)}
            disabled={page === totalPages}
          >
            {">>"}
          </button>
        </div>
      )}
    </div>
  );
}

function fmt(v: number | null | undefined) {
  if (v === null || v === undefined) return "-";
  return Number(v).toFixed(4).replace(/\.?0+$/, "");
}