import styles from "./Toolbar.module.css";

type Props = {
  onRefresh: () => void;
  onCreate?: () => void; // <-- eklendi
};

export default function Toolbar({ onRefresh, onCreate }: Props) {
  function exportExcel() {
    // backend streaming endpoint
    window.location.href = "/api/export/excel";
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