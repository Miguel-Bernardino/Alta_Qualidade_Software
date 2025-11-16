#!/usr/bin/env bash
set -euo pipefail

echo "Rodando isort..."
isort .

echo "Rodando black..."
black .

echo "Formatação concluída."
