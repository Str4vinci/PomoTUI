#!/bin/bash
DIR="$( cd "$( dirname "$(readlink -f "$0")" )" &> /dev/null && pwd )"
cd "$DIR"
uv run python -m src.app
