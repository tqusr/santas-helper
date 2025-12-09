#!/usr/bin/env python3
"""CLI entry point for Santa's Helper."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from santas_helper.cli import main

if __name__ == "__main__":
    main()
