from app.services.calculate.budget import compute_new_daily_budgets_for_label

class R:
    def __init__(self, label, campaign_name, platform, label_remaining_budget, camp_3d_cost):
        self.label = label
        self.campaign_name = campaign_name
        self.platform = platform
        self.label_remaining_budget = label_remaining_budget
        self.camp_3d_cost = camp_3d_cost

def test_india_cap_and_min5():
    rows = [
        R("L1", "AAA India", "Android", 100, 30),
        R("L1", "BBB India", "iOS",     100, 10),
        R("L1", "CCC TR",    "Android", 100, 40),
        R("L1", "DDD TR",    "iOS",     100, 20),
    ]
    out = compute_new_daily_budgets_for_label(rows)
    india_sum = out[("AAA India","Android")] + out[("BBB India","iOS")]
    assert india_sum <= 30.0001
    assert all(v >= 5 or v == 0 for v in out.values())

def test_feasibility_active_selection():
    # TotalDaily=12, 5 kampanya -> max_active=floor(12/5)=2
    rows = [
        R("L1", "A", "", 12, 100),
        R("L1", "B", "", 12, 90),
        R("L1", "C", "", 12, 10),
        R("L1", "D", "", 12, 5),
        R("L1", "E", "", 12, 1),
    ]
    out = compute_new_daily_budgets_for_label(rows)
    active = sum(1 for v in out.values() if v == 5)
    assert active == 2
