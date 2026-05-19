import os
from dotenv import load_dotenv

# Load .env before anything else is imported
load_dotenv()

from tui.app import LataiApp

def main():
    app = LataiApp()
    app.run()

if __name__ == "__main__":
    main()
