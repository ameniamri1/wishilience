#!/bin/bash

# Script de vérification du projet Wishilience
# Usage: ./check_project.sh

echo "🔍 Vérification du projet Wishilience..."
echo "========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Compteur
total=0
passed=0

check_file() {
    total=$((total + 1))
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        passed=$((passed + 1))
    else
        echo -e "${RED}✗${NC} $1 ${RED}(MANQUANT)${NC}"
    fi
}

check_dir() {
    total=$((total + 1))
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        passed=$((passed + 1))
    else
        echo -e "${RED}✗${NC} $1/ ${RED}(MANQUANT)${NC}"
    fi
}

echo "📂 Structure des dossiers:"
check_dir "src"
check_dir "tests"
check_dir "kubernetes"
check_dir "kubernetes/monitoring"
check_dir ".github"
check_dir ".github/workflows"
check_dir "security"

echo ""
echo "📄 Fichiers principaux:"
check_file "src/app.py"
check_file "tests/test_api.py"
check_file "Dockerfile"
check_file "docker-compose.yml"
check_file "requirements.txt"
check_file ".gitignore"

echo ""
echo "☸️  Manifests Kubernetes:"
check_file "kubernetes/deployment.yaml"
check_file "kubernetes/service.yaml"
check_file "kubernetes/hpa.yaml"
check_file "kubernetes/monitoring/prometheus.yml"

echo ""
echo "🔄 CI/CD:"
check_file ".github/workflows/ci-cd.yml"

echo ""
echo "📚 Documentation:"
check_file "README.md"
check_file "REPORT.md"
check_file "PRESENTATION_GUIDE.md"
check_file "ISSUES_TEMPLATE.md"

echo ""
echo "========================================="
echo -e "Résultat: ${GREEN}${passed}${NC}/${total} fichiers présents"

if [ $passed -eq $total ]; then
    echo -e "${GREEN}✓ Projet complet !${NC}"
    echo ""
    echo "🚀 Prochaines étapes:"
    echo "1. Initialiser git: git init"
    echo "2. Premier commit: git add . && git commit -m 'feat: initial project setup'"
    echo "3. Créer repo GitHub et push"
    echo "4. Tester localement: python src/app.py"
    echo ""
else
    echo -e "${RED}✗ Il manque des fichiers${NC}"
fi

# Vérification des lignes de code
echo ""
echo "📊 Statistiques du code:"
if [ -f "src/app.py" ]; then
    lines=$(wc -l < src/app.py)
    echo "   API: $lines lignes"
    if [ $lines -le 150 ]; then
        echo -e "   ${GREEN}✓${NC} Sous la limite de 150 lignes"
    else
        echo -e "   ${RED}✗${NC} Dépasse la limite de 150 lignes"
    fi
fi

if [ -f "tests/test_api.py" ]; then
    tests=$(grep -c "^def test_" tests/test_api.py)
    echo "   Tests: $tests fonctions de test"
fi

echo ""
echo "💡 Conseil: Lis le fichier QUICKSTART.md pour commencer !"
