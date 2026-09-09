from pathlib import Path
import json
import subprocess
import sys

RAIZ = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(RAIZ / "scripts" / "validate_energy_data.py")], check=True)
subprocess.run([sys.executable, str(RAIZ / "scripts" / "detect_anomalies.py")], check=True)
subprocess.run([sys.executable, "-m", "pytest", "-q", str(RAIZ / "tests"), "-p", "no:cacheprovider"], check=True)
print("Projeto validado. Consulte resumo_portfolio.json e RELATORIO_VALIDACAO.md.")
