#!/usr/bin/env python3
"""GUI entry point for Santa's Helper."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from santas_helper.gui import main

if __name__ == "__main__":
    main()
