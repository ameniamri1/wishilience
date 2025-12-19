# 🚀 QUICKSTART - Wishilience

## 📋 Prérequis

Avant de commencer, assure-toi d'avoir installé :

- [ ] Python 3.11+
- [ ] Git
- [ ] Docker & Docker Compose
- [ ] kubectl
- [ ] minikube (ou kind)
- [ ] Un compte GitHub
- [ ] Un compte Docker Hub

---

## ⚡ DÉMARRAGE RAPIDE (5 minutes)

### Étape 1 : Vérifier le projet

```bash
# Vérifier que tous les fichiers sont présents
./check_project.sh

# Tu devrais voir: ✓ Projet complet ! (22/22 fichiers)
```

### Étape 2 : Tester l'API localement

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'API
python src/app.py

# Dans un autre terminal, tester :
curl http://localhost:8000/health
curl http://localhost:8000/
curl -X POST http://localhost:8000/chaos/burn-cpu
```

**Résultat attendu :** 
```json
{"status": "healthy", "timestamp": 1703001234.56}
```

### Étape 3 : Tester avec Docker

```bash
# Build l'image
docker build -t wishilience:local .

# Run le container
docker run -p 8000:8000 wishilience:local

# Tester
curl http://localhost:8000/health
```

### Étape 4 : Tester avec Docker Compose

```bash
# Démarrer toute la stack
docker-compose up -d

# Vérifier les services
docker-compose ps

# Accéder aux services :
# - API:        http://localhost:8000
# - Prometheus: http://localhost:9090
# - Grafana:    http://localhost:3000 (admin/admin)

# Voir les logs
docker-compose logs -f wishilience

# Arrêter
docker-compose down
```

---

## 🐙 SETUP GITHUB (15 minutes)

### Étape 1 : Créer le repository

1. Va sur https://github.com/new
2. Nom : `wishilience`
3. Description : `Chaos Engineering API for Kubernetes Self-Healing Demo`
4. Public ✓
5. **NE PAS** cocher "Add README" (on a déjà tout)
6. Créer le repository

### Étape 2 : Push le code

```bash
# Initialiser git
git init
git branch -M main

# Ajouter les fichiers
git add .
git commit -m "feat: initial project setup with complete DevOps stack"

# Connecter au repository GitHub
git remote add origin https://github.com/TON_USERNAME/wishilience.git

# Push
git push -u origin main
```

### Étape 3 : Créer les GitHub Issues

1. Va sur ton repo → Issues → New Issue
2. Copie-colle les 9 issues depuis `ISSUES_TEMPLATE.md`
3. Pour chaque issue :
   - Titre : ex. "TASK-01: Setup Project Structure"
   - Description : copie depuis le template
   - Labels : `setup`, `priority:high`, etc.
   - Assign to : toi-même

**Les 9 issues à créer :**
- TASK-01: Setup Project Structure ✅ (déjà fait)
- TASK-02: Implement REST API Endpoints ✅ (déjà fait)
- TASK-03: Add Unit Tests ✅ (déjà fait)
- TASK-04: Containerize with Docker ✅ (déjà fait)
- TASK-05: Configure CI/CD Pipeline (à faire)
- TASK-06: Implement Observability ✅ (déjà fait)
- TASK-07: Add Security Scans (à faire)
- TASK-08: Setup Kubernetes Deployment (à faire)
- TASK-09: Final Documentation (à faire)

### Étape 4 : Setup Docker Hub Secrets

1. Va sur ton repo → Settings → Secrets and variables → Actions
2. New repository secret :
   - Name : `DOCKER_USERNAME`
   - Value : ton username Docker Hub
3. New repository secret :
   - Name : `DOCKER_PASSWORD`
   - Value : ton token Docker Hub (créer sur https://hub.docker.com/settings/security)

---

## 🔄 WORKFLOW CI/CD (5 minutes)

### Activer GitHub Actions

```bash
# Le fichier .github/workflows/ci-cd.yml est déjà créé
# Il va se déclencher automatiquement au prochain push

# Teste en faisant un petit changement
echo "# Test CI/CD" >> README.md
git add README.md
git commit -m "test: trigger CI/CD pipeline"
git push

# Va sur GitHub → Actions
# Tu devrais voir le pipeline tourner ! 🎉
```

**Ce que le pipeline fait :**
1. ✅ Run tests (pytest)
2. ✅ SAST scan (Bandit + Trivy)
3. ✅ Build Docker image
4. ✅ Push to Docker Hub
5. ✅ DAST scan (OWASP ZAP)

---

## ☸️ KUBERNETES DEPLOYMENT (20 minutes)

### Étape 1 : Setup Minikube

```bash
# Démarrer minikube avec ressources suffisantes
minikube start --cpus=4 --memory=4096

# Activer le metrics-server (OBLIGATOIRE pour HPA)
minikube addons enable metrics-server

# Vérifier
kubectl get nodes
kubectl top nodes
```

### Étape 2 : Mettre à jour les manifests

```bash
# Remplace YOUR_DOCKERHUB_USERNAME par ton username
sed -i 's/YOUR_DOCKERHUB_USERNAME/ton_vrai_username/g' kubernetes/deployment.yaml

# Vérifie le changement
grep "image:" kubernetes/deployment.yaml
```

### Étape 3 : Déployer l'application

```bash
# Appliquer tous les manifests
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml

# Vérifier le déploiement
kubectl get all
kubectl get hpa

# Attendre que les pods soient Ready (30-60 secondes)
kubectl get pods -w
# Ctrl+C quand tu vois 3/3 Running
```

### Étape 4 : Accéder à l'application

```bash
# Obtenir l'URL du service
minikube service wishilience-service --url

# Ou utiliser port-forward
kubectl port-forward svc/wishilience-service 8080:80

# Tester
curl http://localhost:8080/health
```

---

## 🔥 DÉMOS CHAOS ENGINEERING

### DEMO 1 : Self-Healing (Pod Restart)

```bash
# Terminal 1 : Watch les pods
kubectl get pods -w

# Terminal 2 : Trigger un crash
SERVICE_URL=$(minikube service wishilience-service --url)
curl -X POST $SERVICE_URL/chaos/terminate

# Observe dans Terminal 1 :
# - Pod passe de Running → Error
# - Kubernetes le redémarre automatiquement
# - Nouveau pod devient Running en ~15 secondes
```

**🎯 Ce que ça démontre :** 
- Liveness probe détecte le crash
- Kubernetes redémarre automatiquement le pod
- Zero downtime grâce aux replicas

### DEMO 2 : Auto-Scaling (HPA)

```bash
# Terminal 1 : Watch le HPA
kubectl get hpa wishilience-hpa -w

# Terminal 2 : Générer de la charge CPU
SERVICE_URL=$(minikube service wishilience-service --url)
for i in {1..10}; do
  curl -X POST $SERVICE_URL/chaos/burn-cpu &
done

# Observe dans Terminal 1 :
# - CPU monte : 10% → 85%
# - HPA scale : 2 pods → 7 pods
# - Scale up prend ~30-45 secondes
```

**🎯 Ce que ça démontre :**
- HPA détecte la charge CPU
- Scale automatique de 2 à 10 pods
- Distribution de charge

### DEMO 3 : Memory Leak (OOMKilled)

```bash
# Watch les pods
kubectl get pods -w

# Trigger memory leak
curl -X POST $SERVICE_URL/chaos/leak-memory

# Le pod sera OOMKilled après ~5 secondes
# Kubernetes le redémarre automatiquement
```

---

## 📊 OBSERVABILITÉ

### Prometheus

```bash
# Port-forward Prometheus
kubectl port-forward -n default svc/prometheus 9090:9090

# Accéder : http://localhost:9090

# Requêtes utiles :
# - chaos_injections_total
# - app_crashes_total
# - rate(chaos_injections_total[5m])
```

### Logs

```bash
# Voir les logs de tous les pods
kubectl logs -l app=wishilience --tail=50 -f

# Logs d'un pod spécifique
kubectl logs wishilience-xxxxx-yyyyy -f

# Format : JSON structuré
# Exemple :
# {"timestamp": 1703001234, "level": "critical", "event": "chaos_injection"}
```

### Métriques

```bash
# Voir les métriques des pods
kubectl top pods

# Voir les événements
kubectl get events --sort-by='.lastTimestamp'

# Détails du HPA
kubectl describe hpa wishilience-hpa
```

---

## 🎓 CHECKLIST AVANT PRÉSENTATION

### Tests Fonctionnels
- [ ] API démarre localement : `python src/app.py`
- [ ] Tests passent : `pytest tests/ -v`
- [ ] Docker build réussit : `docker build -t test .`
- [ ] Pipeline CI/CD est vert sur GitHub
- [ ] Image publiée sur Docker Hub

### Déploiement Kubernetes
- [ ] Minikube démarré et metrics-server actif
- [ ] 3 pods tournent : `kubectl get pods`
- [ ] HPA configuré : `kubectl get hpa`
- [ ] Service accessible : `curl` fonctionne

### Démos
- [ ] Self-healing testé 3 fois (succès à chaque fois)
- [ ] Auto-scaling testé 2 fois (scale visible)
- [ ] Logs visibles et structurés
- [ ] Métriques accessibles dans Prometheus

### Documentation
- [ ] README à jour avec ton username
- [ ] REPORT complété avec screenshots
- [ ] PRESENTATION_GUIDE lu 2 fois
- [ ] Réponses préparées pour 5 questions possibles

---

## 🐛 TROUBLESHOOTING

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### "Cannot connect to Docker daemon"
```bash
sudo systemctl start docker
# Ou : sudo service docker start
```

### "minikube: command not found"
```bash
# Installer minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### "HPA shows <unknown> for CPU"
```bash
# Vérifier metrics-server
kubectl get pods -n kube-system | grep metrics-server

# Si absent, l'activer
minikube addons enable metrics-server

# Attendre 1-2 minutes
kubectl top nodes
```

### "Pods stuck in Pending"
```bash
# Vérifier les ressources
kubectl describe pod <pod-name>

# Si problème de ressources
minikube delete
minikube start --cpus=4 --memory=4096
```

### "Pipeline CI/CD échoue"
```bash
# Vérifier les secrets Docker Hub
# GitHub → Settings → Secrets → DOCKER_USERNAME et DOCKER_PASSWORD

# Vérifier les logs du job
# GitHub → Actions → Click sur le workflow → Click sur le job en erreur
```

---

## 🎯 PROCHAINES ÉTAPES

1. **Aujourd'hui :**
   - ✅ Setup GitHub (15 min)
   - ✅ Tester localement (5 min)
   - ✅ Premier push et CI/CD (10 min)

2. **Cette semaine :**
   - Déployer sur Kubernetes
   - Faire les 2 démos chaos
   - Prendre screenshots pour le rapport
   - Créer les PRs et demander reviews

3. **La semaine prochaine :**
   - Finaliser le rapport
   - Préparer la présentation
   - Dry run des démos 3 fois

---

## 💬 BESOIN D'AIDE ?

Si tu es bloqué :
1. Relis ce QUICKSTART
2. Check le README.md pour plus de détails
3. Regarde les logs : `kubectl logs`, `docker logs`
4. Vérifie GitHub Actions pour le CI/CD
5. Demande-moi ! 🤝

---

## 🎉 TU ES PRÊT !

Tout est en place pour un projet DevOps de qualité professionnelle !

**Commence par :**
```bash
./check_project.sh
python src/app.py
```

**Bon courage ! 🚀**
