// --- src/types/record.ts ---

export type RecordRow = {
  id: number;
  label: string;
  campaign_name: string;
  platform: string | null;

  camp_budget: number | null;
  camp_cost: number | null;
  camp_3d_cost: number | null;
  camp_conv: number | null;
  camp_cpa: number | null;
  camp_tcpa: number | null;

  mtd_cluster_spend: number | null;

  label_budget: number | null;
  label_cost: number | null;
  label_3d_cost: number | null;
  label_conv: number | null;
  label_remaining_budget: number | null;
  label_kpi_value: number | null;
  label_cpa: number | null;

  new_daily_budget: number | null;
  new_target_cpa: number | null;
};

export type RecordItem = RecordRow;