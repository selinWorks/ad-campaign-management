import styles from "./Toolbar.module.css";

export default function Toolbar({ onRefresh }: { onRefresh: () => void }) {
  function exportExcel() {
    // backend streaming endpoint
    window.location.href = "/api/export/excel";
  }

  return (
    <div className={styles.bar}>
      <button className={styles.btn} onClick={onRefresh}>Yenile</button>
      <button className={styles.btnPrimary} onClick={exportExcel}>Excel İndir</button>
    </div>
  );
}