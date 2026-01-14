# backend/app/services/calculate/budget.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
import math


Key = Tuple[str, str]  # (campaign_name, platform)


def _get(r: Any, name: str, default=None):
    """
    Record objesi attribute veya dict olabilir.
    """
    if isinstance(r, dict):
        return r.get(name, default)
    return getattr(r, name, default)


def _to_float(x, default: float = 0.0) -> float:
    try:
        if x is None or x == "":
            return default
        return float(x)
    except Exception:
        return default


def _nonneg(x) -> float:
    v = _to_float(x, 0.0)
    return v if v > 0 else 0.0


def is_india(campaign_name: str) -> bool:
    return "india" in (campaign_name or "").lower()


def compute_remaining_days(label_budget, label_cost, label_remaining_budget) -> float:
    """
    Gün sayısını sabitlemeden (15 yok) dinamik hesap.
    RemainingDays = (Label budget - Label cost) / Label remaining budget
    """
    lb = _to_float(label_budget, 0.0)
    lc = _to_float(label_cost, 0.0)
    lrb = _to_float(label_remaining_budget, 0.0)
    if lrb <= 0:
        return 0.0
    remaining = max(0.0, lb - lc)
    return remaining / lrb


def allocate_weighted(records: List[Any], total: float) -> Dict[Key, float]:
    """
    weight = camp_3d_cost
    weights=0 ise eşit dağıtım
    """
    total = _nonneg(total)
    n = len(records)
    if n == 0:
        return {}

    weights = [_nonneg(_get(r, "camp_3d_cost", 0.0)) for r in records]
    s = sum(weights)

    out: Dict[Key, float] = {}
    if s <= 0:
        each = total / n if n else 0.0
        for r in records:
            key = (_get(r, "campaign_name", ""), _get(r, "platform", "") or "")
            out[key] = each
        return out

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
    """
    Min 5 + fizibilite:
    - total_daily < 5*N ise: aktif seçim (en yüksek weight) -> aktiflere 5, diğerlerine 0
    - total_daily >= 5*N ise: 5 altını 5'e çek, kalan bütçeyi ağırlıklı dağıt
    """
    keys = list(alloc.keys())
    n = len(keys)
    total_daily = _nonneg(total_daily)

    if n == 0:
        return {}

    # Fizibilite yoksa: aktif kampanya seçimi
    if total_daily < min_value * n:
        max_active = int(math.floor(total_daily / min_value))
        if max_active <= 0:
            return {k: 0.0 for k in keys}

        sorted_keys = sorted(keys, key=lambda k: weights_by_key.get(k, 0.0), reverse=True)
        active = set(sorted_keys[:max_active])
        return {k: (min_value if k in active else 0.0) for k in keys}

    # Clamp
    fixed: Dict[Key, float] = {}
    free: Dict[Key, float] = {}
    for k, v in alloc.items():
        if v < min_value:
            fixed[k] = min_value
        else:
            free[k] = v

    fixed_sum = sum(fixed.values())
    remaining = total_daily - fixed_sum

    if remaining < 0:
        # güvenlik
        return apply_minimum_and_rebalance(alloc, weights_by_key, total_daily, min_value=min_value)

    if not free:
        return fixed

    free_keys = list(free.keys())
    free_weights = [max(0.0, weights_by_key.get(k, 0.0)) for k in free_keys]
    s = sum(free_weights)

    out = dict(fixed)
    if s <= 0:
        each = remaining / len(free_keys)
        for k in free_keys:
            out[k] = each
    else:
        for k, w in zip(free_keys, free_weights):
            out[k] = remaining * (w / s)

    return out


def compute_new_daily_budgets_for_label(
    records_for_one_label: List[Any],
    india_cap_ratio: float = 0.30,
    min_daily_budget: float = 5.0
) -> Dict[Key, float]:
    if not records_for_one_label:
        return {}

    total_daily = _nonneg(_get(records_for_one_label[0], "label_remaining_budget", 0.0))
    india_cap = india_cap_ratio * total_daily

    india = [r for r in records_for_one_label if is_india(str(_get(r, "campaign_name", "")))]
    non_india = [r for r in records_for_one_label if not is_india(str(_get(r, "campaign_name", "")))]

    # weights map (global)
    weights_by_key: Dict[Key, float] = {}
    for r in records_for_one_label:
        k = (str(_get(r, "campaign_name", "")), str(_get(r, "platform", "") or ""))
        weights_by_key[k] = _nonneg(_get(r, "camp_3d_cost", 0.0))

    # --- 1) INDIA: cap içinde kalacak şekilde min-5 + fizibilite uygula
    india_total = min(india_cap, total_daily)
    india_alloc0 = allocate_weighted(india, india_total)

    india_alloc = apply_minimum_and_rebalance(
        alloc=india_alloc0,
        weights_by_key=weights_by_key,
        total_daily=india_total,          # <-- kritik: total = india_total
        min_value=min_daily_budget
    )

    used_india = sum(india_alloc.values())
    # güvenlik: cap'i asla aşma
    if used_india > india_cap + 1e-6:
        # teoride buraya düşmemeli, ama garantileyelim: oransal kırp
        scale = india_cap / used_india if used_india > 0 else 0.0
        india_alloc = {k: v * scale for k, v in india_alloc.items()}
        used_india = sum(india_alloc.values())

    # --- 2) NON-INDIA: kalan bütçe içinde min-5 + fizibilite uygula
    non_india_total = max(0.0, total_daily - used_india)
    non_india_alloc0 = allocate_weighted(non_india, non_india_total)

    non_india_alloc = apply_minimum_and_rebalance(
        alloc=non_india_alloc0,
        weights_by_key=weights_by_key,
        total_daily=non_india_total,      # <-- kritik: total = non_india_total
        min_value=min_daily_budget
    )

    out = dict(india_alloc)
    out.update(non_india_alloc)

    return {k: round(v, 4) for k, v in out.items()}

