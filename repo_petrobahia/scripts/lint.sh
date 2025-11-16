#!/usr/bin/env bash
set -euo pipefail

echo "Rodando pylint em 'src'..."
# Retornamos código 0 mesmo que o pylint encontre problemas para não quebrar pipelines locais.
pylint src || true

echo "Lint finalizado. Verifique a saída do pylint para detalhes."
