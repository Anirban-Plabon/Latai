from tui.app import LataiApp
import sys
from loguru import logger

def main() -> None:
    # Disable stderr logging to prevent TUI visual glitches (red text on screen)
    logger.remove()
    logger.add("latai.log", rotation="1 MB", level="INFO")
    
    app = LataiApp()
    app.run()


if __name__ == "__main__":
    main()
