"""
AI Pathfinder Entry Point.
This is a minimalist launcher that abstracts all implementation details,
simply initializing the application orchestrator.
"""
import sys
import os

# Add the parent directory (src) to the Python path so we can find 'logic' and 'ui'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic.app import PathfinderApp

def main():
    app = PathfinderApp()
    app.run()

if __name__ == "__main__":
    main()
