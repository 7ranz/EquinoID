"""Caso económico hipotético; nunca se alimenta con los resultados de detección."""
import json
from pathlib import Path

def calculate(file):
    x=json.loads(Path(file).read_text(encoding='utf-8'))
    capex=sum(x['capex'].values());opex=sum(x['annual_opex'].values())
    before=x['lost_before']*x['value_per_horse']+(x['search_hours_before']+x['admin_hours_before'])*x['hourly_cost']
    after=x['lost_after']*x['value_per_horse']+(x['search_hours_after']+x['admin_hours_after'])*x['hourly_cost']+opex
    net=before-after
    return dict(x,capex_total=capex,opex_total=opex,cost_before=before,cost_after=after,gross_benefit=net+opex,
                net_annual_benefit=net,first_year_net=net-capex,payback_months=12*capex/net if net>0 else None,
                first_year_roi=(net-capex)/capex)
