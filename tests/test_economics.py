import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from equinoid.economics import calculate

class EconomicsTests(unittest.TestCase):
 def test_case_reconciles(self):
  e=calculate(Path(__file__).resolve().parents[1]/'data/economics_scenario.json')
  self.assertEqual(e['capex_total'],4800);self.assertEqual(e['cost_before'],20320)
  self.assertEqual(e['cost_after'],9912);self.assertEqual(e['net_annual_benefit'],10408)
  self.assertEqual(e['first_year_net'],5608);self.assertAlmostEqual(e['payback_months'],5.5342,places=3)
  self.assertEqual(e['status'],'SIMULADO_NO_OBSERVADO')
