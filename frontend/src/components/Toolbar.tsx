
import styles from "./Toolbar.module.css";

type Props = {
  onRefresh: () => void;
  onCreate?: () => void;
};

export default function Toolbar({ onRefresh, onCreate }: Props) {
  function exportExcel() {
    // PROD: VITE_API_BASE_URL = https://ad-campaign-management.onrender.com
    // LOCAL: boşsa vite proxy ile /api çalışır
    const base = import.meta.env.VITE_API_BASE_URL || "";
    const url = base ? `${base}/api/export/excel` : `/api/export/excel`;

    window.location.href = url;
  }

  return (
    <div className={styles.bar}>
      <div className={styles.left}>
        <button className={styles.btn} onClick={onRefresh}>
          Yenile
        </button>
      </div>

      <div className={styles.right}>
        {onCreate && (
          <button className={styles.btn} onClick={onCreate}>
            Yeni Kayıt
          </button>
        )}

        <button className={styles.btnPrimary} onClick={exportExcel}>
          Excel İndir
        </button>
      </div>
    </div>
  );
}