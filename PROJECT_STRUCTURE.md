# 📁 Structure du Projet Wishilience

```
wishilience/
├── .github/
│   └── workflows/
│       └── ci-cd.yml                 ✅ Pipeline CI/CD complet
│
├── src/
│   └── app.py                        ✅ API principale (149 lignes)
│
├── tests/
│   └── test_api.py                   ✅ Tests unitaires
│
├── kubernetes/
│   ├── deployment.yaml               ✅ Deployment K8s
│   ├── service.yaml                  ✅ Service LoadBalancer
│   ├── hpa.yaml                      ✅ Horizontal Pod Autoscaler
│   └── monitoring/
│       └── prometheus.yml            ✅ Config Prometheus
│
├── security/
│   └── (rapports de scan ici)
│
├── Dockerfile                        ✅ Multi-stage build
├── docker-compose.yml                ✅ Stack locale (API+Prometheus+Grafana)
├── requirements.txt                  ✅ Dépendances Python
├── .gitignore                        ✅ Fichiers à ignorer
│
├── README.md                         ✅ Documentation complète
├── REPORT.md                         ✅ Rapport final (1-2 pages)
├── PRESENTATION_GUIDE.md             ✅ Guide présentation 10 min
└── ISSUES_TEMPLATE.md                ✅ Template GitHub Issues
```

## ✅ Fichiers Créés

Vérifions que tout est présent :
