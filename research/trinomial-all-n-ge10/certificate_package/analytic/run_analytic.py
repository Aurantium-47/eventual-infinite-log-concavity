"""Regenerate the analytic proof's exact arithmetic certificates (not edge jets).
All mathematical contour/geometric arguments remain in the accompanying proof.
"""
if not __debug__:raise RuntimeError('Assertions must remain enabled; do not use python -O')
from pathlib import Path
import argparse,subprocess,sys,json
HERE=Path(__file__).resolve().parent
STEPS=['check_16_saddle_algebra.py','check_complex_variance_conditioning.py','check_sharp_real_cumulant_bounds.py','check_uniform_cumulant_bounds.py','check_wide_box_cumulant_bounds.py','check_first_saddle_correction_independent.py','audit_local_moments_independent.py','audit_local_budget_independent.py','check_model_tail_norm.py','check_gaussian_correction_box_tails.py','audit_actual_torus_certificates.py','independent_audit_v250_arithmetic.py','check_phase_bridge_algebra.py','independent_final_join_250.py','audit_461_bulk_bypass_independent.py']
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--full',action='store_true',help='Run all exact arithmetic, including cumulant and moment reconstruction');a=p.parse_args()
 if not a.full:print('No verification run. Full arithmetic sequence:\n'+'\n'.join(STEPS)+'\nUse --full to execute; this is not a hash-only check.')
 else:
  table=json.loads((HERE/'ALL249_HARMONIC_RATIONAL_CANDIDATES.json').read_text())
  join=json.loads((HERE/'FINAL_HARMONIC_JOIN_250_RECEIPT.json').read_text())
  assert table['nodes'][-1]['node']==249 and table['nodes'][-1]['endpoints']==join['nodes']
  logs=HERE/'run_logs';logs.mkdir(exist_ok=True)
  for name in STEPS:
   print('RUN',name,flush=True)
   with (logs/(name+'.log')).open('w') as log:subprocess.run([sys.executable,str(HERE/name)],cwd=HERE,stdout=log,stderr=subprocess.STDOUT,check=True)
  print('PASS: all exact analytic arithmetic stages completed. Mathematical proof text remains a separate premise.')
