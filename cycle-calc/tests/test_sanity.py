from cycle_calc.calculate_accessibility import main

def test_can_run():
  accs = main([1,2,3], ["job"])
  assert type(accs) == dict
  assert "job" in accs
  assert len(accs["job"]) == 3061
