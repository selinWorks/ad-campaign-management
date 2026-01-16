
import styles from "./Navbar.module.css";

export default function Navbar() {
  return (
    <div className={styles.nav}>
      <div className={styles.brand}>
        <div className={styles.logo} />
        <div>
          <div className={styles.title}>Campaign Optimizer</div>
          <div className={styles.subtitle}>Advanced Internet Programming</div>
        </div>
      </div>

      <div className={styles.right}>
        <span className={styles.chip}>Live</span>
      </div>
    </div>
  );
}