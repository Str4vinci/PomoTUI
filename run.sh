#!/bin/bash
cd "$(dirname "$0")"
PYTHONPATH=. uv run textual run src/app.py
