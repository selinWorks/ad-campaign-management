from app.services.calculate.budget import compute_new_daily_budgets_for_label

def apply_betul_budget(records: list):
    # label bazında grupluyoruz
    by_label = {}
    for r in records:
        by_label.setdefault(r.label, []).append(r)

    for label, items in by_label.items():
        budgets = compute_new_daily_budgets_for_label(items)

        for rec in items:
            key = (rec.campaign_name, rec.platform or "")
            rec.new_daily_budget = budgets.get(key, 0.0)  # veya None
