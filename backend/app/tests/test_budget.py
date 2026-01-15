from app.services.calculate.budget import compute_new_daily_budgets_for_label


class R:
    def __init__(self, label, campaign_name, platform, label_remaining_budget, camp_3d_cost):
        self.label = label
        self.campaign_name = campaign_name
        self.platform = platform
        self.label_remaining_budget = label_remaining_budget
        self.camp_3d_cost = camp_3d_cost


def run_india_cap_scenario():
    # India + Non-India karışık senaryo (TotalDaily=100)
    rows = [
        R("L1", "AAA India", "Android", 100, 30),
        R("L1", "BBB India", "iOS",     100, 10),
        R("L1", "CCC TR",    "Android", 100, 40),
        R("L1", "DDD TR",    "iOS",     100, 20),
    ]

    out = compute_new_daily_budgets_for_label(rows)
    print("OUTPUT-INDIA:", out)

    # India kampanyalarına giden toplamın 30'u geçmediğini kontrol ediyorum
    india_sum = out[("AAA India", "Android")] + out[("BBB India", "iOS")]
    assert india_sum <= 30.0001, f"India toplam cap'i aştı: {india_sum}"

    # Minimum değer kontrolü: her değer ya 5 ve üstü olmalı ya da 0 olmalı
    assert all(v >= 5 or abs(v) < 1e-9 for v in out.values()), f"Min kuralı bozuldu: {out}"

    # Toplam dağıtım pacing ile uyumlu mu? (TotalDaily=100)
    assert abs(sum(out.values()) - 100.0) < 1e-3, f"Toplam mismatch: {sum(out.values())}"


def run_low_budget_scenario():
    # Bütçenin yetmediği senaryo (TotalDaily=12, 5 kampanya)
    rows = [
        R("L1", "A", "", 12, 100),
        R("L1", "B", "", 12, 90),
        R("L1", "C", "", 12, 10),
        R("L1", "D", "", 12, 5),
        R("L1", "E", "", 12, 1),
    ]

    out = compute_new_daily_budgets_for_label(rows)
    print("OUTPUT-LOW:", out)

    # En az 5 alan kampanya sayısı 2 olmalı (floor(12/5)=2)
    active = sum(1 for v in out.values() if v >= 5)
    assert active == 2, f"Aktif sayısı beklenenden farklı: {active}"

    # Toplam bütçe boşa gitmesin: toplam 12 olmalı
    assert abs(sum(out.values()) - 12.0) < 1e-6, f"Toplam mismatch: {sum(out.values())}"


if __name__ == "__main__":
    # Dosyayı direkt Run ettiğinde iki senaryoyu da test eder.
    run_india_cap_scenario()
    run_low_budget_scenario()
    print("ALL TESTS PASSED")
