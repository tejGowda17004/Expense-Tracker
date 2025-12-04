from typing import List, Dict


def compare_spending_vs_budget(budgets: List[dict], spending: List[dict], alert_threshold=0.0):
    res = []
    spend_map = {s['category']: s['spent'] for s in spending}
    for b in budgets:
        cat = b['category']
        limit = b['limit']
        spent = spend_map.get(cat, 0.0)
        remaining = limit - spent
        pct_left = remaining / limit if limit else None
        res.append({'category': cat, 'limit': limit, 'spent': spent, 'remaining': remaining, 'pct_left': pct_left})
    return res
