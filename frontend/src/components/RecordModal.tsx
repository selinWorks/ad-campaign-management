import { useEffect, useState } from "react";
import styles from "./RecordModal.module.css";
import type { RecordItem } from "../types/record";

type Props = {
  open: boolean;
  mode: "create" | "edit";
  initial?: RecordItem | null;
  onClose: () => void;
  onSubmit: (payload: any) => Promise<void>;
};

export default function RecordModal({ open, mode, initial, onClose, onSubmit }: Props) {
  const [label, setLabel] = useState("");
  const [campaign, setCampaign] = useState("");
  const [platform, setPlatform] = useState("");
  const [campCost, setCampCost] = useState<string>("");
  const [campCpa, setCampCpa] = useState<string>("");

  useEffect(() => {
    if (!open) return;

    if (mode === "edit" && initial) {
      setLabel(initial.label ?? "");
      setCampaign(initial.campaign_name ?? "");
      setPlatform(initial.platform ?? "");
      setCampCost(initial.camp_cost == null ? "" : String(initial.camp_cost));
      setCampCpa(initial.camp_cpa == null ? "" : String(initial.camp_cpa));
    } else {
      setLabel("");
      setCampaign("");
      setPlatform("");
      setCampCost("");
      setCampCpa("");
    }
  }, [open, mode, initial]);

  if (!open) return null;

  async function submit() {
    const payload: any = {
      label,
      campaign_name: campaign,
      platform: platform || null,
      camp_cost: campCost === "" ? null : Number(campCost),
      camp_cpa: campCpa === "" ? null : Number(campCpa),
    };
    if (mode === "edit" && initial) payload.id = initial.id;

    await onSubmit(payload);
    onClose();
  }

  return (
    <div className={styles.backdrop} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.top}>
          <div className={styles.title}>{mode === "create" ? "Yeni Kayıt" : "Kayıt Düzenle"}</div>
          <button className={styles.btn} onClick={onClose}>Kapat</button>
        </div>

        <div className={styles.grid}>
          <div className={styles.field}>
            <label>Label</label>
            <input value={label} onChange={(e) => setLabel(e.target.value)} disabled={mode === "edit"} />
          </div>
          <div className={styles.field}>
            <label>Campaign name</label>
            <input value={campaign} onChange={(e) => setCampaign(e.target.value)} disabled={mode === "edit"} />
          </div>
          <div className={styles.field}>
            <label>Platform</label>
            <input value={platform} onChange={(e) => setPlatform(e.target.value)} />
          </div>
          <div className={styles.field}>
            <label>Camp cost</label>
            <input value={campCost} onChange={(e) => setCampCost(e.target.value)} />
          </div>
          <div className={styles.field}>
            <label>Camp CPA</label>
            <input value={campCpa} onChange={(e) => setCampCpa(e.target.value)} />
          </div>
        </div>

        <div className={styles.row}>
          <button className={styles.btn} onClick={onClose}>İptal</button>
          <button className={styles.btn} onClick={submit}>
            Kaydet
          </button>
        </div>
      </div>
    </div>
  );
}