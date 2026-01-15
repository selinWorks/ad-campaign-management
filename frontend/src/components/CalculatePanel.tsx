import styles from "./CalculatePanel.module.css";

export default function CalculatePanel({
  onDone,
  onCalculate,
}: {
  onDone?: () => void;
  onCalculate?: () => Promise<void>;
}) {
  async function run() {
    if (onCalculate) await onCalculate();
    onDone?.();
  }

  return (
    <div className={styles.card}>
      <div className={styles.title}>Hesaplama</div>
      <div className={styles.sub}>New Daily Budget + New Target CPA üret</div>

      <button className={styles.btn} onClick={run}>
        Hesapla
      </button>
    </div>
  );
}