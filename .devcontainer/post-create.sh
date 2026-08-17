#!/bin/bash
# Post-create setup for GitHub Codespaces / Dev Containers
set -e

echo "🏗️  Setting up Insurance Quote Intelligence Accelerator..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -e ".[dev]" 2>/dev/null || pip install -r requirements.txt 2>/dev/null || echo "⚠️  No dependencies file found — create pyproject.toml or requirements.txt"

# Install pre-commit hooks if available
if [ -f .pre-commit-config.yaml ]; then
    echo "🪝 Installing pre-commit hooks..."
    pip install pre-commit
    pre-commit install
fi

# Verify Azure CLI
echo "☁️  Verifying Azure CLI..."
az version --output table

# Verify azd
echo "🚀 Verifying Azure Developer CLI..."
azd version

# Create local .env from sample if it doesn't exist
if [ ! -f .env ] && [ -f .env.sample ]; then
    echo "📋 Creating .env from .env.sample..."
    cp .env.sample .env
    echo "   ⚠️  Update .env with your Azure resource values"
fi

# Display getting started info
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Environment ready!"
echo ""
echo "Quick Start:"
echo "  1. Login to Azure:    azd auth login"
echo "  2. Deploy Stage 1:    azd up"
echo "  3. Run tests:         pytest tests/ -v"
echo "  4. Start dev server:  python -m src.main"
echo ""
echo "📖 Full guide: docs/GETTING_STARTED.md"
echo "🏛️  Architecture: docs/ARCHITECTURE.md"
echo "🤖 Agent reference: docs/AGENTS.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
