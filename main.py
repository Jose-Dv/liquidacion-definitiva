import sys
from pathlib import Path


carpeta_src = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(carpeta_src))

from view.gui.liquidacion_gui import LiquidacionApp


if __name__ == "__main__":
    LiquidacionApp().run()