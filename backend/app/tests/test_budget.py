from app.services.calculate.budget import compute_new_daily_budgets_for_label
# Günlük bütçe hesaplama fonksiyonunu test etmek için import ediyorum.


class R:
    def __init__(self, label, campaign_name, platform, label_remaining_budget, camp_3d_cost):
        # Test sırasında kullanmak için basit bir kampanya nesnesi tanımlıyorum.
        # Gerçek uygulamada bu nesne Excel satırı veya veritabanı kaydı olacaktır.
        self.label = label
        self.campaign_name = campaign_name
        self.platform = platform
        self.label_remaining_budget = label_remaining_budget
        self.camp_3d_cost = camp_3d_cost


def test_india_cap_and_min5():
    # Bu testte iki temel durumu kontrol ediyorum:
    # - India kampanyalarına ayrılan bütçe toplamının sınırı aşmaması
    # - Kampanyalara verilen günlük bütçelerin minimum değerin altına düşmemesi

    rows = [
        # Aynı label altında India ve India olmayan kampanyalar oluşturuyorum
        R("L1", "AAA India", "Android", 100, 30),
        R("L1", "BBB India", "iOS",     100, 10),
        R("L1", "CCC TR",    "Android", 100, 40),
        R("L1", "DDD TR",    "iOS",     100, 20),
    ]

    # Günlük bütçe hesaplama fonksiyonunu çalıştırıyorum
    out = compute_new_daily_budgets_for_label(rows)

    # India kampanyalarına verilen bütçeleri toplayarak kontrol ediyorum
    india_sum = out[("AAA India", "Android")] + out[("BBB India", "iOS")]

    # Günlük toplam bütçe 100 olduğu için India tarafının 30'u geçmemesi gerekiyor
    assert india_sum <= 30.0001

    # Kampanyaların aldığı bütçeler:
    # ya minimum değerin üzerinde olmalı
    # ya da bütçe yetmediği durumda 0 olmalı
    assert all(v >= 5 or v == 0 for v in out.values())


def test_feasibility_active_selection():
    # Bu testte toplam bütçenin yetersiz olduğu bir durumu simüle ediyorum.
    # Toplam bütçe 12 ve kampanya sayısı 5 olduğu için herkese minimum değer verilemez.

    rows = [
        # Harcama ağırlıkları farklı olan 5 kampanya tanımlıyorum
        R("L1", "A", "", 12, 100),
        R("L1", "B", "", 12, 90),
        R("L1", "C", "", 12, 10),
        R("L1", "D", "", 12, 5),
        R("L1", "E", "", 12, 1),
    ]

    # Günlük bütçe hesaplama fonksiyonunu çalıştırıyorum
    out = compute_new_daily_budgets_for_label(rows)

    # Minimum bütçeyi alan kampanya sayısını sayıyorum
    active = sum(1 for v in out.values() if v == 5)

    # 12 / 5 = 2 olduğu için sadece 2 kampanya aktif kalmalı
    # Diğer kampanyalar bütçe alamamalı
    assert active == 2
