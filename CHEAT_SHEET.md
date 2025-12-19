# 🚀 WISHILIENCE - CHEAT SHEET

## ⚡ COMMANDES ESSENTIELLES

### 🔍 VÉRIFICATION
```bash
./check_project.sh                    # Vérifier structure projet
wc -l src/app.py                      # Compter lignes de code
pytest tests/ -v --cov=src            # Tests avec coverage
```

### 🐍 PYTHON LOCAL
```bash
# Installation
pip install -r requirements.txt

# Lancer l'API
python src/app.py                     # Port 8000

# Tests
pytest tests/ -v                      # Tests unitaires
pytest tests/ --cov=src               # Avec coverage
pytest tests/ -v --tb=short           # Moins verbose

# SAST
bandit -r src/ -f txt                 # Security scan
```

### 🐳 DOCKER
```bash
# Build
docker build -t wishilience:local .

# Run
docker run -p 8000:8000 wishilience:local
docker run -d --name wishilience -p 8000:8000 wishilience:local

# Logs
docker logs wishilience -f

# Stop/Remove
docker stop wishilience
docker rm wishilience

# Docker Compose
docker-compose up -d                  # Démarrer stack
docker-compose ps                     # Status services
docker-compose logs -f wishilience    # Logs API
docker-compose down                   # Arrêter tout
```

### ☸️ KUBERNETES (MINIKUBE)
```bash
# Setup
minikube start --cpus=4 --memory=4096
minikube addons enable metrics-server
minikube status

# Deploy
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml

# Ou tout d'un coup
kubectl apply -f kubernetes/

# Vérifier
kubectl get all                       # Tous les objets
kubectl get pods                      # Liste pods
kubectl get pods -w                   # Watch pods
kubectl get svc                       # Services
kubectl get hpa                       # HPA status
kubectl get hpa -w                    # Watch HPA

# Logs
kubectl logs -l app=wishilience       # Tous les pods
kubectl logs -l app=wishilience -f    # Follow logs
kubectl logs pod-name -f              # Pod spécifique

# Describe (debug)
kubectl describe pod pod-name
kubectl describe hpa wishilience-hpa
kubectl describe svc wishilience-service

# Events
kubectl get events --sort-by='.lastTimestamp'

# Metrics
kubectl top nodes                     # Métriques nœuds
kubectl top pods                      # Métriques pods

# Accès
minikube service wishilience-service --url
kubectl port-forward svc/wishilience-service 8080:80

# Cleanup
kubectl delete -f kubernetes/
minikube delete
```

### 🔥 CHAOS ENGINEERING
```bash
# Obtenir l'URL du service
SERVICE_URL=$(minikube service wishilience-service --url)
echo $SERVICE_URL

# Endpoints
curl $SERVICE_URL/health              # Health check
curl $SERVICE_URL/metrics             # Prometheus metrics
curl $SERVICE_URL/                    # API info

# DEMO 1: Self-Healing
curl -X POST $SERVICE_URL/chaos/terminate

# DEMO 2: Auto-Scaling
for i in {1..10}; do
  curl -X POST $SERVICE_URL/chaos/burn-cpu &
done

# DEMO 3: Memory Leak
curl -X POST $SERVICE_URL/chaos/leak-memory
```

### 📊 OBSERVABILITÉ
```bash
# Prometheus
kubectl port-forward svc/prometheus 9090:9090
# Ouvrir : http://localhost:9090
# Queries :
#   - chaos_injections_total
#   - app_crashes_total
#   - rate(chaos_injections_total[5m])

# Grafana (via docker-compose)
# http://localhost:3000
# Login: admin/admin

# Logs structurés
kubectl logs -l app=wishilience | jq .
```

### 🔐 SÉCURITÉ
```bash
# SAST - Bandit
pip install bandit
bandit -r src/ -f txt
bandit -r src/ -f json -o bandit-report.json

# Trivy - Filesystem
docker run --rm -v $(pwd):/app aquasec/trivy fs /app

# Trivy - Image
docker run --rm aquasec/trivy image wishilience:local

# DAST - OWASP ZAP (après avoir lancé l'API)
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://host.docker.internal:8000
```

### 🐙 GITHUB
```bash
# Setup
git init
git branch -M main
git add .
git commit -m "feat: initial project setup"
git remote add origin https://github.com/USERNAME/wishilience.git
git push -u origin main

# Workflow branches
git checkout -b feature/task-01-setup
# ... faire des changements ...
git add .
git commit -m "feat: setup project structure (closes #1)"
git push origin feature/task-01-setup
# Créer PR sur GitHub

# Voir status pipeline
gh run list                           # Avec GitHub CLI
# Ou sur : https://github.com/USERNAME/wishilience/actions
```

### 🎯 DÉMONSTRATIONS

#### DEMO 1 : Self-Healing (Terminal splitté)
```bash
# Terminal 1 (gauche)
kubectl get pods -w

# Terminal 2 (droite)
SERVICE_URL=$(minikube service wishilience-service --url)
curl -X POST $SERVICE_URL/chaos/terminate

# Observer : Pod Error → K8s restart → Running
```

#### DEMO 2 : Auto-Scaling (Terminal splitté)
```bash
# Terminal 1 (gauche)
kubectl get hpa wishilience-hpa -w

# Terminal 2 (droite)
SERVICE_URL=$(minikube service wishilience-service --url)
for i in {1..10}; do
  curl -X POST $SERVICE_URL/chaos/burn-cpu &
done

# Observer : CPU 10% → 85%, Replicas 2 → 7
```

#### DEMO 3 : Logs + Metrics
```bash
# Terminal 1 : Logs
kubectl logs -l app=wishilience -f | jq .

# Terminal 2 : Déclencher événement
curl -X POST $SERVICE_URL/chaos/terminate

# Terminal 3 : Prometheus
kubectl port-forward svc/prometheus 9090:9090
# Query : chaos_injections_total
```

---

## 🛠️ TROUBLESHOOTING

### Problème : HPA affiche <unknown>
```bash
# Vérifier metrics-server
kubectl get pods -n kube-system | grep metrics-server

# Activer si absent
minikube addons enable metrics-server

# Attendre 1-2 minutes
kubectl top nodes
```

### Problème : Pods stuck in Pending
```bash
# Vérifier ressources
kubectl describe pod pod-name

# Redémarrer minikube avec plus de ressources
minikube delete
minikube start --cpus=4 --memory=4096
```

### Problème : Docker build échoue
```bash
# Vérifier Docker daemon
docker ps

# Nettoyer Docker
docker system prune -a

# Rebuild sans cache
docker build --no-cache -t wishilience:local .
```

### Problème : Tests échouent
```bash
# Vérifier dépendances
pip install -r requirements.txt

# Vérifier Python version
python --version  # Doit être 3.11+

# Run tests verbose
pytest tests/ -v -s
```

### Problème : CI/CD échoue
```bash
# Vérifier secrets GitHub
# Settings → Secrets → DOCKER_USERNAME & DOCKER_PASSWORD

# Vérifier logs du workflow
# Actions → Click workflow → Click job → Voir erreur
```

---

## 📝 COMMANDES DE PRÉSENTATION

### Setup avant présentation (10 min avant)
```bash
# 1. Démarrer minikube
minikube start --cpus=4 --memory=4096
minikube addons enable metrics-server

# 2. Déployer l'app
kubectl apply -f kubernetes/

# 3. Attendre que tout soit prêt
kubectl get pods -w  # Attendre 3/3 Running

# 4. Ouvrir 4 terminaux
# Terminal 1 : kubectl get pods -w
# Terminal 2 : kubectl get hpa -w
# Terminal 3 : kubectl logs -l app=wishilience -f
# Terminal 4 : Commandes démo

# 5. Préparer variable
SERVICE_URL=$(minikube service wishilience-service --url)
echo $SERVICE_URL  # Copier pour les démos
```

### Pendant la présentation
```bash
# Slide 1-2 : Intro (30s)
# Slide 3 : Architecture (1 min)

# DEMO 1 : Self-Healing (3 min)
curl -X POST $SERVICE_URL/chaos/terminate
# → Pointer Terminal 1 (pods) et Terminal 3 (logs)

# DEMO 2 : Auto-Scaling (2 min)
for i in {1..10}; do curl -X POST $SERVICE_URL/chaos/burn-cpu & done
# → Pointer Terminal 2 (hpa)

# Slide 4 : Features (1 min)
# Montrer GitHub Actions (déjà ouvert dans navigateur)
# Montrer Docker Hub (déjà ouvert dans navigateur)

# Slide 5 : Lessons Learned (1 min)
# Q&A (reste du temps)
```

---

## 🎯 RACCOURCIS UTILES

```bash
# Alias pratiques (ajouter dans ~/.bashrc)
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kgh='kubectl get hpa'
alias kl='kubectl logs'
alias kd='kubectl describe'

# Variables d'environnement
export SERVICE_URL=$(minikube service wishilience-service --url)
export KUBE_EDITOR="nano"  # Ou vim, code, etc.
```

---

## 📚 LIENS RAPIDES

- **GitHub Repo :** https://github.com/USERNAME/wishilience
- **Docker Hub :** https://hub.docker.com/r/USERNAME/wishilience
- **CI/CD Pipeline :** https://github.com/USERNAME/wishilience/actions
- **Local API :** http://localhost:8000
- **Prometheus :** http://localhost:9090
- **Grafana :** http://localhost:3000

---

## ✅ CHECKLIST PRÉ-PRÉSENTATION

- [ ] Minikube démarré avec metrics-server
- [ ] App déployée, 3 pods Running
- [ ] HPA configuré et fonctionnel
- [ ] 4 terminaux ouverts et labellisés
- [ ] Variable SERVICE_URL définie
- [ ] GitHub Actions ouvert dans navigateur
- [ ] Docker Hub ouvert dans navigateur
- [ ] Slides/notes prêtes
- [ ] Screenshots de backup disponibles
- [ ] Laptop chargé à 100%
- [ ] Plan B préparé (si démo échoue)

---

**🚀 Bonne chance ! Tu vas déchirer ! 💪**
