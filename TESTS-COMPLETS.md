# 🧪 TESTS COMPLETS - WISHILIENCE

## ✅ SECTION 1 : API LOCALE

### Test 1 : Démarrer l'API
Lance l'application Python localement.
```powershell
cd C:\Users\MSI\OneDrive\Desktop\wishilience
1. Installer dépendances : `pip install -r requirements.txt`
2. Lancer l'API : `python src/app.py`
```
**Attendu :** `Uvicorn running on http://0.0.0.0:8000`

### Test 2 : Endpoints API
Teste les 3 endpoints principaux.
```powershell
# Dans un 2ème terminal
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing
Invoke-WebRequest -Uri "http://localhost:8000/metrics" -UseBasicParsing
```
**Attendu :** StatusCode 200 pour les 3

**Arrête l'API :** Ctrl+C dans le 1er terminal

**Score Section 1 : 2/ 2**

---

## ✅ SECTION 2 : DOCKER

### Test 3 : Build Docker
Construit l'image Docker.
```powershell
docker build -t ameniamri1/wishilience:test .
```
**Attendu :** `naming to docker.io/ameniamri1/wishilience:test`

### Test 4 : Run Docker
Lance le container.
```powershell
docker run -d --name wishilience-test -p 8001:8000 ameniamri1/wishilience:test
```
**Attendu :** ID du container (long hash)

### Test 5 : Tester container
Vérifie que l'API fonctionne dans Docker.
```powershell
Invoke-WebRequest -Uri "http://localhost:8001/health" -UseBasicParsing
docker logs wishilience-test --tail=20
```
**Attendu :** StatusCode 200 + logs JSON

### Test 6 : Cleanup Docker
Supprime le container et l'image de test.
```powershell
docker stop wishilience-test
docker rm wishilience-test
docker rmi ameniamri1/wishilience:test
```
**Attendu :** Confirmations de suppression

**Score Section 2 : 4 / 4**

---

## ✅ SECTION 3 : DOCKER COMPOSE

### Test 7 : Démarrer stack
Lance API + Prometheus + Grafana.
```powershell
docker-compose up -d
```
**Attendu :** `Creating wishilience ... done` (3 services)

### Test 8 : Vérifier services
Liste les services actifs.
```powershell
docker-compose ps
```
**Attendu :** 3 services "Up"

### Test 9 : Tester services web
Ouvre dans le navigateur :
- http://localhost:8000/health
- http://localhost:9090
- http://localhost:3000 (admin/admin)

**Attendu :** Les 3 pages chargent

### Test 10 : Métriques Prometheus
Cherche les métriques de chaos.
1. Ouvre http://localhost:9090
2. Va dans "Graph"
3. Tape : `chaos_injections_total`
4. Clique "Execute"

**Attendu :** Métrique visible (valeur 0 OK)

### Test 11 : Cleanup Compose
Arrête tous les services.
```powershell
docker-compose down
```
**Attendu :** `Removing wishilience ... done` (3 services)

**Score Section 3 : 5/ 5**

---

## ✅ SECTION 4 : KUBERNETES

### Test 12 : Vérifier Minikube
Vérifie que minikube tourne.
```powershell
minikube status
```
**Attendu :** `minikube: Running, kubelet: Running, apiserver: Running`

**Si pas Running :**
```powershell
minikube start --cpus=4 --memory=4096
```

### Test 13 : État global
Vérifie tous les objets K8s.
```powershell
kubectl get all
```
**Attendu :** 3 pods Running, 1 service, 1 deployment 3/3, 1 HPA

### Test 14 : Détails pods
Liste les pods individuellement.
```powershell
kubectl get pods
```
**Attendu :** 3 pods avec READY 1/1, STATUS Running

### Test 15 : API sur K8s
Teste l'API déployée.
```powershell
minikube service wishilience-service --url
# Copie l'URL puis :
Invoke-WebRequest -Uri "http://127.0.0.1:51549/health" -UseBasicParsing
```
**Attendu :** StatusCode 200

### Test 16 : Logs pods
Affiche les logs des pods.
```powershell
kubectl logs -l app=wishilience --tail=20
```
**Attendu :** Logs JSON structurés

### Test 17 : HPA status
Vérifie l'autoscaler.
```powershell
kubectl get hpa
```
**Attendu :** HPA avec TARGETS (% CPU/Memory), MINPODS 2, MAXPODS 10

### Test 18 : Metrics server
Vérifie les métriques système.
```powershell
kubectl top nodes
kubectl top pods
```
**Attendu :** CPU et Memory affichés (pas "error")

**Score Section 4 : 7 / 7**

---

## ✅ SECTION 5 : DÉMOS CHAOS

### Test 19 : Self-Healing
Démontre le redémarrage automatique.
```powershell
# Terminal 1 :
kubectl get pods -w

# Terminal 2 :
kubectl delete pod wishilience-b75fb8b48-f4drt
```
**Attendu :** Pod Terminating → Nouveau pod créé → Running en ~8s

### Test 20 : Vérifier remplacement
Confirme le nouveau pod.
```powershell
kubectl get pods
```
**Attendu :** 1 pod avec AGE récent (~1min), 2 pods avec AGE ancien

### Test 21 : CPU Burn (optionnel)
Génère charge CPU pour HPA.
```powershell
$SERVICE_URL = (minikube service wishilience-service --url)
Invoke-WebRequest -Uri "$SERVICE_URL/chaos/burn-cpu" -Method POST -UseBasicParsing
kubectl top pods
```
**Attendu :** CPU augmente sur les pods

### Test 22 : Événements K8s
Liste les événements récents.
```powershell
kubectl get events --sort-by='.lastTimestamp' | Select-Object -Last 20
```
**Attendu :** Événements "Killing", "Created", "Started"

**Score Section 5 : __ / 4**

---

## ✅ SECTION 6 : CI/CD GITHUB

### Test 23 : Repo GitHub
Vérifie que le code est en ligne.
- Ouvre : `https://github.com/ameniamri1/wishilience`
- Vérifie : Tous les fichiers présents, README s'affiche

**Attendu :** Repo accessible avec tous les fichiers

### Test 24 : GitHub Actions
Vérifie le pipeline CI/CD.
- Ouvre : `https://github.com/ameniamri1/wishilience/actions`
- Vérifie : Au moins 1 workflow run

**Attendu :** Pipeline vert ✅ ou en cours 🟡 (pas rouge ❌)

### Test 25 : Secrets GitHub
Vérifie la configuration des secrets.
- Ouvre : `https://github.com/ameniamri1/wishilience/settings/secrets/actions`
- Vérifie : DOCKER_USERNAME et DOCKER_PASSWORD existent

**Attendu :** 2 secrets configurés

### Test 26 : Docker Hub
Vérifie l'image publiée.
- Ouvre : `https://hub.docker.com/r/ameniamri1/wishilience`
- Vérifie : Image existe avec tags

**Attendu :** Image visible avec tag "latest"

**Score Section 6 : __ / 4**

---

## ✅ SECTION 7 : DOCUMENTATION

### Test 27 : Fichiers MD
Liste tous les fichiers Markdown.
```powershell
cd C:\Users\MSI\OneDrive\Desktop\wishilience
Get-ChildItem -Filter *.md
```
**Attendu :** 8-9 fichiers .md listés

### Test 28 : README valide
Vérifie que les commandes fonctionnent.
- Ouvre README.md
- Teste 2-3 commandes aléatoires

**Attendu :** Commandes s'exécutent sans erreur

**Score Section 7 : __ / 2**

---

## ✅ SECTION 8 : SCRIPTS

### Test 29 : Script de vérification
Vérifie la structure du projet.
```powershell
.\check_project.sh
```
**Attendu :** `✓ Projet complet ! (22/22 fichiers)`

### Test 30 : Vérification finale
Lance le check complet avec stats.
```powershell
.\FINAL_CHECK.sh
```
**Attendu :** `✓ PROJET COMPLET ET PRÊT ! Total attendu : 90-100%`

**Score Section 8 : __ / 2**

---

## 📊 RÉSULTATS FINAUX

```
Section 1 - API Locale      : __ / 2
Section 2 - Docker          : __ / 4
Section 3 - Docker Compose  : __ / 5
Section 4 - Kubernetes      : __ / 7
Section 5 - Démos Chaos     : __ / 4
Section 6 - CI/CD GitHub    : __ / 4
Section 7 - Documentation   : __ / 2
Section 8 - Scripts         : __ / 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL                       : __ / 30
```

**Interprétation :**
- **28-30** : 🏆 Parfait
- **24-27** : ✅ Très bien
- **20-23** : ⚠️ Quelques ajustements
- **< 20** : ❌ Corrections nécessaires

---

## 🆘 TROUBLESHOOTING

**Si test échoue, note :**
```
❌ Test XX : [titre]
Erreur : [message]
```

**Solutions rapides :**
- **ModuleNotFoundError** → `pip install -r requirements.txt`
- **Docker daemon not running** → Lance Docker Desktop
- **Minikube not running** → `minikube start --cpus=4 --memory=4096`
- **HPA shows <unknown>** → `minikube addons enable metrics-server` puis attends 2 min
- **Port already in use** → Change le port ou tue le processus

---

## 📝 NOTES

**Durée totale estimée :** 45 minutes

**Ordre recommandé :**
1. Sections 1-3 : Tests locaux (15 min)
2. Section 4 : Kubernetes (15 min)
3. Section 5 : Démos (10 min)
4. Sections 6-8 : Vérifications (5 min)

**Conseils :**
- Fais les tests dans l'ordre
- Note ton score après chaque section
- Si un test échoue, passe au suivant et reviens après
- Garde 2 terminaux PowerShell ouverts

**Bon courage ! 🚀**