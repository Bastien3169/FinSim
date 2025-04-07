from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).parent  # Pas besoin de toucher cette ligne !
sys.path.append(str(PROJECT_ROOT))  # Ajoute la racine aux chemins Python