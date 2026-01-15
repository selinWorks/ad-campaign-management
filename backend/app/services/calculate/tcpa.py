from __future__ import annotations
from typing import Any, Dict, List, Tuple


Key = Tuple[str, str]  # (campaign_name, platform)


def _get(r: Any, name: str, default=None):
    # dict veya model objesi destekler
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


def clamp(val: float, lo: float, hi: float) -> float:
    return max(lo, min(val, hi))


def safe_div(a: float, b: float, default: float = 0.0) -> float:
    b = _to_float(b, 0.0)
    if b <= 0:
        return default
    return _to_float(a, 0.0) / b


def compute_label_cpa(label_cost, label_conv, label_cpa_value=None) -> float:
    """
    Öncelik: cost/conv (hocanın beklediği tanım).
    Eğer conv yoksa ama Label CPA kolonu doluysa onu fallback olarak kullan.
    """
    conv = _to_float(label_conv, 0.0)
    cost = _to_float(label_cost, 0.0)

    if conv > 0 and cost > 0:
        return cost / conv

    # fallback: excel'de label cpa varsa
    cpa = _to_float(label_cpa_value, 0.0)
    return cpa if cpa > 0 else 0.0


def compute_adjustment_for_label(
    label_kpi_value,
    label_cost,
    label_conv,
    label_cpa_value=None,
    min_ratio: float = 0.85,
    max_ratio: float = 1.15,
) -> float:
    """
    ratio = KPI / LabelCPA
    clamp to [0.85, 1.15]
    Edge-case: KPI <= 0 veya LabelCPA <= 0 => 1.0
    """
    kpi = _to_float(label_kpi_value, 0.0)
    if kpi <= 0:
        return 1.0

    label_cpa = compute_label_cpa(label_cost, label_conv, label_cpa_value=label_cpa_value)
    if label_cpa <= 0:
        return 1.0

    ratio = kpi / label_cpa
    return clamp(ratio, min_ratio, max_ratio)


def compute_new_target_cpas_for_label(
    records_for_one_label: List[Any],
    min_target_cpa: float = 0.01,
    min_ratio: float = 0.85,
    max_ratio: float = 1.15,
    precision: int = 4,
) -> Dict[Key, float]:
    """
    Hira'nın ana fonksiyonu.
    Input: Tek label'a ait kampanya kayıtları
    Output: (campaign_name, platform) -> new_target_cpa

    Beklenen alanlar (records içinde):
      - campaign_name
      - platform (yoksa "" kabul)
      - camp_tcpa  (Camp. tCPA)
      Label seviyesinde (ilk satırdan alınır):
      - label_kpi_value
      - label_cost
      - label_conv
      - label_cpa (opsiyonel fallback)
    """
    if not records_for_one_label:
        return {}

    first = records_for_one_label[0]

    adj = compute_adjustment_for_label(
        label_kpi_value=_get(first, "label_kpi_value", 0.0),
        label_cost=_get(first, "label_cost", 0.0),
        label_conv=_get(first, "label_conv", 0.0),
        label_cpa_value=_get(first, "label_cpa", None),
        min_ratio=min_ratio,
        max_ratio=max_ratio,
    )

    out: Dict[Key, float] = {}

    for r in records_for_one_label:
        campaign_name = str(_get(r, "campaign_name", "") or "")
        platform = str(_get(r, "platform", "") or "")
        key: Key = (campaign_name, platform)

        old_tcpa = _to_float(_get(r, "camp_tcpa", 0.0), 0.0)

        if old_tcpa <= 0:
            new_tcpa = min_target_cpa
        else:
            new_tcpa = max(old_tcpa * adj, min_target_cpa)

        out[key] = round(new_tcpa, precision)

    return out
