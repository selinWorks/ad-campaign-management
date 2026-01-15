print("EXCEL EXPORT LOADED")

from io import BytesIO
from typing import List

from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from app.models.record import Record


HEADERS = [
    "label",
    "campaign_name",
    "platform",
    "camp_budget",
    "camp_cost",
    "camp_3d_cost",
    "camp_conv",
    "camp_cpa",
    "camp_tcpa",
    "mtd_cluster_spend",
    "label_budget",
    "label_cost",
    "label_3d_cost",
    "label_conv",
    "label_remaining_budget",
    "label_kpi_value",
    "label_cpa",
    "new_daily_budget",
    "new_target_cpa",
]


def records_to_excel(records: List[Record]) -> BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.title = "Calculated Data"

    # HEADER
    ws.append(HEADERS)

    # ROWS
    for r in records:
        ws.append([
            r.label,
            r.campaign_name,
            r.platform,
            r.camp_budget,
            r.camp_cost,
            r.camp_3d_cost,
            r.camp_conv,
            r.camp_cpa,
            r.camp_tcpa,
            r.mtd_cluster_spend,
            r.label_budget,
            r.label_cost,
            r.label_3d_cost,
            r.label_conv,
            r.label_remaining_budget,
            r.label_kpi_value,
            r.label_cpa,
            r.new_daily_budget,
            r.new_target_cpa,
        ])

    # Kolon genişlikleri
    for i, col in enumerate(HEADERS, start=1):
        ws.column_dimensions[get_column_letter(i)].width = max(len(col) + 2, 18)

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output