from __future__ import annotations  # Type hint'lerde (List[str] vb.) ileri referans rahat çalışsın diye ekledim
from typing import Any, Dict, List, Tuple  # Tipler: fonksiyonların ne alıp ne döndürdüğünü netleştirmek için
import math  # floor gibi matematiksel işlemler için


Key = Tuple[str, str]  # Kampanyayı tekil tanımlamak için anahtar: (campaign_name, platform)


def _get(r: Any, name: str, default=None):
    # Kayıtlar bazen dict bazen model objesi olabiliyor.
    # Bu yüzden tek fonksiyonla hem r["x"] hem r.x şeklinde okuyabilmek için yazdım.
    if isinstance(r, dict):
        return r.get(name, default)
    return getattr(r, name, default)


def _to_float(x, default: float = 0.0) -> float:
    # Excel'den gelen değerler None / boş string / yanlış format olabiliyor.
    # Hesaplama patlamasın diye güvenli şekilde float'a çeviriyorum.
    try:
        if x is None or x == "":
            return default
        return float(x)
    except Exception:
        return default


def _nonneg(x) -> float:
    # Bütçe/harcama gibi değerler negatif olmamalı.
    # Negatif gelirse 0'a çekip algoritmanın bozulmasını engelliyorum.
    v = _to_float(x, 0.0)
    return v if v > 0 else 0.0


def is_india(campaign_name: str) -> bool:
    # India kampanyalarını isimden tespit ediyorum (en basit ve savunulabilir kural).
    return "india" in (campaign_name or "").lower()


def compute_remaining_days(label_budget, label_cost, label_remaining_budget) -> float:
    # "15 günü sabitleme" hatasını çözmek için kalan gün sayısını dinamik hesaplıyorum:
    # RemainingDays = (Label budget - Label cost) / Label remaining budget
    lb = _to_float(label_budget, 0.0)
    lc = _to_float(label_cost, 0.0)
    lrb = _to_float(label_remaining_budget, 0.0)
    if lrb <= 0:
        return 0.0
    remaining = max(0.0, lb - lc)
    return remaining / lrb


def allocate_weighted(records: List[Any], total: float) -> Dict[Key, float]:
    # Kampanyalara bütçe dağıtımı yapıyorum.
    # Ağırlık olarak Camp 3D cost kullanıyorum (son 3 gün harcayan yarın da harcar mantığı).
    # Eğer ağırlıklar 0 çıkarsa (hiç harcama yoksa) eşit dağıtım yapıyorum.
    total = _nonneg(total)
    n = len(records)
    if n == 0:
        return {}

    weights = [_nonneg(_get(r, "camp_3d_cost", 0.0)) for r in records]  # weight = camp_3d_cost
    s = sum(weights)

    out: Dict[Key, float] = {}
    if s <= 0:
        # Eğer tüm ağırlıklar 0 ise eşit paylaştırıyorum.
        each = total / n if n else 0.0
        for r in records:
            key = (_get(r, "campaign_name", ""), _get(r, "platform", "") or "")
            out[key] = each
        return out

    # Ağırlıklı oransal dağıtım: budget_i = total * (w_i / sum_w)
    for r, w in zip(records, weights):
        key = (_get(r, "campaign_name", ""), _get(r, "platform", "") or "")
        out[key] = total * (w / s)
    return out


def apply_minimum_and_rebalance(
    alloc: Dict[Key, float],
    weights_by_key: Dict[Key, float],
    total_daily: float,
    min_value: float = 5.0
) -> Dict[Key, float]:
    # Bu fonksiyon "New Daily Budget >= 5" kuralını uygular.
    # 5'in altına düşenleri 5'e çekiyorum, sonra toplamı bozmamak için yeniden dengeleme yapıyorum.
    # Eğer toplam bütçe yetmiyorsa (5*N > total) bu sefer "aktif kampanya seçimi" yapıyorum.
    keys = list(alloc.keys())
    n = len(keys)
    total_daily = _nonneg(total_daily)

    if n == 0:
        return {}

    # 1) Fizibilite kontrolü:
    # total_daily < 5 * kampanya_sayısı ise hepsine 5 vermek imkansız.
    # Bu durumda en yüksek weight'e sahip kampanyaları aktif bırakıyorum.
    if total_daily < min_value * n:
        max_active = int(math.floor(total_daily / min_value))  # Kaç kampanya minimum 5 alabilir?
        if max_active <= 0:
            return {k: 0.0 for k in keys}  # bütçe hiç yetmiyorsa hepsi 0

        # weight'e göre sırala, en yüksek max_active kampanya aktif
        sorted_keys = sorted(keys, key=lambda k: weights_by_key.get(k, 0.0), reverse=True)
        active = set(sorted_keys[:max_active])
        return {k: (min_value if k in active else 0.0) for k in keys}

    # 2) Clamp (min-5):
    # 5'in altında kalanları fixed grubuna alıp 5'e çekiyorum.
    fixed: Dict[Key, float] = {}
    free: Dict[Key, float] = {}
    for k, v in alloc.items():
        if v < min_value:
            fixed[k] = min_value
        else:
            free[k] = v

    fixed_sum = sum(fixed.values())
    remaining = total_daily - fixed_sum  # fixed'e ayırınca geriye ne kaldı?

    if remaining < 0:
        # Güvenlik: teoride olmaması gerekir ama olur ise tekrar hesaplatıyorum
        return apply_minimum_and_rebalance(alloc, weights_by_key, total_daily, min_value=min_value)

    if not free:
        # Eğer herkes 5'e sabitlendi ise direkt döndür
        return fixed

    # 3) Rebalance:
    # Kalan bütçeyi free grubuna weight'leri ile oransal dağıtıyorum.
    free_keys = list(free.keys())
    free_weights = [max(0.0, weights_by_key.get(k, 0.0)) for k in free_keys]
    s = sum(free_weights)

    out = dict(fixed)
    if s <= 0:
        # free grubunda da ağırlık yoksa eşit dağıt
        each = remaining / len(free_keys)
        for k in free_keys:
            out[k] = each
    else:
        # Ağırlıklı dağıt
        for k, w in zip(free_keys, free_weights):
            out[k] = remaining * (w / s)

    return out


def compute_new_daily_budgets_for_label(
    records_for_one_label: List[Any],
    india_cap_ratio: float = 0.30,
    min_daily_budget: float = 5.0
) -> Dict[Key, float]:
    # Betül'ün ana fonksiyonu:
    # 1) TotalDaily = Label remaining budget (pacing)
    # 2) India kampanyaları toplamı <= %30 cap
    # 3) Dağıtım: weight = camp_3d_cost
    # 4) Min 5 kuralı + fizibilite yönetimi
    if not records_for_one_label:
        return {}

    # Label bazında günlük dağıtılacak toplam bütçe
    total_daily = _nonneg(_get(records_for_one_label[0], "label_remaining_budget", 0.0))
    india_cap = india_cap_ratio * total_daily  # India kampanyaları için üst sınır

    # Kampanyaları India / Non-India diye ayırıyorum
    india = [r for r in records_for_one_label if is_india(str(_get(r, "campaign_name", "")))]
    non_india = [r for r in records_for_one_label if not is_india(str(_get(r, "campaign_name", "")))]

    # Rebalance sırasında kullanılacak global weight haritası: (campaign, platform) -> camp_3d_cost
    weights_by_key: Dict[Key, float] = {}
    for r in records_for_one_label:
        k = (str(_get(r, "campaign_name", "")), str(_get(r, "platform", "") or ""))
        weights_by_key[k] = _nonneg(_get(r, "camp_3d_cost", 0.0))

    # --- ÖNEMLİ DÜZELTME:
    # India cap'i min-5 sonrası bozulmasın diye India ve Non-India için min-5 + rebalance'i AYRI uyguluyorum.

    # 1) India havuzu: toplam en fazla india_cap
    india_total = min(india_cap, total_daily)
    india_alloc0 = allocate_weighted(india, india_total)  # India grubunda ağırlıklı dağıtım

    # India grubunda min-5 + fizibilite + rebalance (sadece india_total içinde kalacak)
    india_alloc = apply_minimum_and_rebalance(
        alloc=india_alloc0,
        weights_by_key=weights_by_key,
        total_daily=india_total,
        min_value=min_daily_budget
    )

    # Güvenlik: India toplamı cap'i aşarsa (teoride aşmamalı) ölçekleyerek geri çekiyorum
    used_india = sum(india_alloc.values())
    if used_india > india_cap + 1e-6:
        scale = india_cap / used_india if used_india > 0 else 0.0
        india_alloc = {k: v * scale for k, v in india_alloc.items()}
        used_india = sum(india_alloc.values())

    # 2) Non-India havuzu: kalan bütçe
    non_india_total = max(0.0, total_daily - used_india)
    non_india_alloc0 = allocate_weighted(non_india, non_india_total)  # Non-India grubunda ağırlıklı dağıtım

    # Non-India grubunda min-5 + fizibilite + rebalance (sadece non_india_total içinde kalacak)
    non_india_alloc = apply_minimum_and_rebalance(
        alloc=non_india_alloc0,
        weights_by_key=weights_by_key,
        total_daily=non_india_total,
        min_value=min_daily_budget
    )

    # Sonuç: India + Non-India bütçelerini birleştirip döndürüyorum
    out = dict(india_alloc)
    out.update(non_india_alloc)

    # Raporlama için 4 basamak yuvarlıyorum
    return {k: round(v, 4) for k, v in out.items()}
