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

  // Campaign metrics
  const [campBudget, setCampBudget] = useState<string>("");
  const [campCost, setCampCost] = useState<string>("");
  const [camp3dCost, setCamp3dCost] = useState<string>("");
  const [campConv, setCampConv] = useState<string>("");
  const [campCpa, setCampCpa] = useState<string>("");
  const [campTcpa, setCampTcpa] = useState<string>("");
  const [mtdClusterSpend, setMtdClusterSpend] = useState<string>("");

  // Label metrics
  const [labelBudget, setLabelBudget] = useState<string>("");
  const [labelCost, setLabelCost] = useState<string>("");
  const [label3dCost, setLabel3dCost] = useState<string>("");
  const [labelConv, setLabelConv] = useState<string>("");
  const [labelRemainingBudget, setLabelRemainingBudget] = useState<string>("");
  const [labelKpiValue, setLabelKpiValue] = useState<string>("");
  const [labelCpa, setLabelCpa] = useState<string>("");

  function toNumberOrNull(v: string): number | null {
    if (v.trim() === "") return null;
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  }

  useEffect(() => {
    if (!open) return;

    if (mode === "edit" && initial) {
      setLabel(initial.label ?? "");
      setCampaign(initial.campaign_name ?? "");
      setPlatform(initial.platform ?? "");

      setCampBudget(initial.camp_budget == null ? "" : String(initial.camp_budget));
      setCampCost(initial.camp_cost == null ? "" : String(initial.camp_cost));
      setCamp3dCost(initial.camp_3d_cost == null ? "" : String(initial.camp_3d_cost));
      setCampConv(initial.camp_conv == null ? "" : String(initial.camp_conv));
      setCampCpa(initial.camp_cpa == null ? "" : String(initial.camp_cpa));
      setCampTcpa(initial.camp_tcpa == null ? "" : String(initial.camp_tcpa));
      setMtdClusterSpend(initial.mtd_cluster_spend == null ? "" : String(initial.mtd_cluster_spend));

      setLabelBudget(initial.label_budget == null ? "" : String(initial.label_budget));
      setLabelCost(initial.label_cost == null ? "" : String(initial.label_cost));
      setLabel3dCost(initial.label_3d_cost == null ? "" : String(initial.label_3d_cost));
      setLabelConv(initial.label_conv == null ? "" : String(initial.label_conv));
      setLabelRemainingBudget(
        initial.label_remaining_budget == null ? "" : String(initial.label_remaining_budget)
      );
      setLabelKpiValue(initial.label_kpi_value == null ? "" : String(initial.label_kpi_value));
      setLabelCpa(initial.label_cpa == null ? "" : String(initial.label_cpa));
    } else {
      setLabel("");
      setCampaign("");
      setPlatform("");

      setCampBudget("");
      setCampCost("");
      setCamp3dCost("");
      setCampConv("");
      setCampCpa("");
      setCampTcpa("");
      setMtdClusterSpend("");

      setLabelBudget("");
      setLabelCost("");
      setLabel3dCost("");
      setLabelConv("");
      setLabelRemainingBudget("");
      setLabelKpiValue("");
      setLabelCpa("");
    }
  }, [open, mode, initial]);

  if (!open) return null;

  async function submit() {
    const payload: any = {
      label,
      campaign_name: campaign,
      platform,

      // Campaign metrics
      camp_budget: toNumberOrNull(campBudget),
      camp_cost: toNumberOrNull(campCost),
      camp_3d_cost: toNumberOrNull(camp3dCost),
      camp_conv: toNumberOrNull(campConv),
      camp_cpa: toNumberOrNull(campCpa),
      camp_tcpa: toNumberOrNull(campTcpa),
      mtd_cluster_spend: toNumberOrNull(mtdClusterSpend),

      // Label metrics
      label_budget: toNumberOrNull(labelBudget),
      label_cost: toNumberOrNull(labelCost),
      label_3d_cost: toNumberOrNull(label3dCost),
      label_conv: toNumberOrNull(labelConv),
      label_remaining_budget: toNumberOrNull(labelRemainingBudget),
      label_kpi_value: toNumberOrNull(labelKpiValue),
      label_cpa: toNumberOrNull(labelCpa),
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
          <button className={styles.btn} onClick={onClose}>
            Kapat
          </button>
        </div>

        <div className={styles.grid}>
          <div className={styles.field}>
            <label>Label</label>
            <input
              value={label}
              onChange={(e) => setLabel(e.target.value)}
              disabled={mode === "edit"}
            />
          </div>

          <div className={styles.field}>
            <label>Campaign name</label>
            <input
              value={campaign}
              onChange={(e) => setCampaign(e.target.value)}
              disabled={mode === "edit"}
            />
          </div>

          <div className={styles.field}>
            <label>Platform</label>
            <input value={platform} onChange={(e) => setPlatform(e.target.value)} />
          </div>

          <div className={styles.section}>Campaign metrics</div>

          <div className={styles.field}>
            <label>Camp budget</label>
            <input type="number" value={campBudget} onChange={(e) => setCampBudget(e.target.value)} />
          </div>

          <div className={styles.field}>
            <label>Camp cost</label>
            <input type="number" value={campCost} onChange={(e) => setCampCost(e.target.value)} />
          </div>

          <div className={styles.field}>
            <label>Camp 3d cost</label>
            <input type="number" value={camp3dCost} onChange={(e) => setCamp3dCost(e.target.value)} />
          </div>

          <div className={styles.field}>
            <label>Camp conv</label>
            <input type="number" value={campConv} onChange={(e) => setCampConv(e.target.value)} />
          </div>

          <div className={styles.field}>
            <label>Camp CPA</label>
            <input type="number" value={campCpa} onChange={(e) => setCampCpa(e.target.value)} />
          </div>

          <div className={styles.field}>
            <label>Camp tCPA</label>
            <input type="number" value={campTcpa} onChange={(e) => setCampTcpa(e.target.value)} />
          </div>

          <div className={styles.field}>
            <label>MTD cluster spend</label>
            <input
              type="number"
              value={mtdClusterSpend}
              onChange={(e) => setMtdClusterSpend(e.target.value)}
            />
          </div>

          <div className={styles.section}>Label metrics</div>

          <div className={styles.field}>
            <label>Label budget</label>
            <input type="number" value={labelBudget} onChange={(e) => setLabelBudget(e.target.value)} />
          </div>

          <div className={styles.field}>
            <label>Label cost</label>
            <input type="number" value={labelCost} onChange={(e) => setLabelCost(e.target.value)} />
          </div>

          <div className={styles.field}>
            <label>Label 3d cost</label>
            <input type="number" value={label3dCost} onChange={(e) => setLabel3dCost(e.target.value)} />
          </div>

          <div className={styles.field}>
            <label>Label conv</label>
            <input type="number" value={labelConv} onChange={(e) => setLabelConv(e.target.value)} />
          </div>

          <div className={styles.field}>
            <label>Label remaining budget</label>
            <input
              type="number"
              value={labelRemainingBudget}
              onChange={(e) => setLabelRemainingBudget(e.target.value)}
            />
          </div>

          <div className={styles.field}>
            <label>Label KPI value</label>
            <input
              type="number"
              value={labelKpiValue}
              onChange={(e) => setLabelKpiValue(e.target.value)}
            />
          </div>

          <div className={styles.field}>
            <label>Label CPA</label>
            <input type="number" value={labelCpa} onChange={(e) => setLabelCpa(e.target.value)} />
          </div>
        </div>

        <div className={styles.row}>
          <button className={styles.btn} onClick={onClose}>
            İptal
          </button>
          <button className={styles.btn} onClick={submit}>
            Kaydet
          </button>
        </div>
      </div>
    </div>
  );
}
