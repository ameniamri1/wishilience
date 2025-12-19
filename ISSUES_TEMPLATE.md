# GitHub Issues à Créer

Copie-colle ces issues dans ton repository GitHub :

---

## TASK-01: Setup Project Structure
**Description:**
Initialize the project repository with proper directory structure and basic files.

**Acceptance Criteria:**
- [ ] Create folder structure (src/, tests/, kubernetes/, etc.)
- [ ] Add .gitignore
- [ ] Create README.md skeleton
- [ ] Setup requirements.txt

**Labels:** `setup`, `priority:high`

---

## TASK-02: Implement REST API Endpoints
**Description:**
Develop the FastAPI application with health check and chaos engineering endpoints.

**Acceptance Criteria:**
- [ ] Implement `/health` endpoint
- [ ] Implement `/chaos/burn-cpu` endpoint
- [ ] Implement `/chaos/leak-memory` endpoint
- [ ] Implement `/chaos/terminate` endpoint
- [ ] Add structured logging
- [ ] Code under 150 lines

**Labels:** `backend`, `priority:high`

---

## TASK-03: Add Unit Tests
**Description:**
Create comprehensive unit tests for all API endpoints.

**Acceptance Criteria:**
- [ ] Test all endpoints with pytest
- [ ] Achieve >90% code coverage
- [ ] Add test documentation

**Labels:** `testing`, `priority:high`

---

## TASK-04: Containerize with Docker
**Description:**
Create Dockerfile and docker-compose.yml for local development.

**Acceptance Criteria:**
- [ ] Multi-stage Dockerfile
- [ ] Docker image < 200MB
- [ ] docker-compose with API, Prometheus, Grafana
- [ ] Health checks in Dockerfile

**Labels:** `docker`, `priority:high`

---

## TASK-05: Configure CI/CD Pipeline
**Description:**
Setup GitHub Actions workflow for automated testing, building, and deployment.

**Acceptance Criteria:**
- [ ] Test job with pytest
- [ ] SAST job (Bandit + Trivy)
- [ ] Build and push Docker image
- [ ] DAST job (OWASP ZAP)
- [ ] All jobs passing

**Labels:** `ci-cd`, `priority:critical`

---

## TASK-06: Implement Observability
**Description:**
Add metrics, structured logs, and tracing to the application.

**Acceptance Criteria:**
- [ ] Prometheus metrics endpoint
- [ ] JSON structured logging
- [ ] OpenTelemetry tracing
- [ ] Custom metrics for chaos events

**Labels:** `observability`, `priority:high`

---

## TASK-07: Add Security Scans
**Description:**
Integrate SAST and DAST security scanning in CI/CD pipeline.

**Acceptance Criteria:**
- [ ] Bandit SAST scan
- [ ] Trivy vulnerability scan
- [ ] OWASP ZAP DAST scan
- [ ] Document findings

**Labels:** `security`, `priority:critical`

---

## TASK-08: Setup Kubernetes Deployment
**Description:**
Create Kubernetes manifests for deployment, service, and HPA.

**Acceptance Criteria:**
- [ ] Deployment with resource limits
- [ ] Service (LoadBalancer)
- [ ] HPA configuration
- [ ] Liveness/readiness probes
- [ ] Successfully deploy to minikube

**Labels:** `kubernetes`, `priority:high`

---

## TASK-09: Final Documentation
**Description:**
Complete README, create final report, and prepare presentation.

**Acceptance Criteria:**
- [ ] Comprehensive README.md
- [ ] Final report (1-2 pages)
- [ ] Architecture diagram
- [ ] Presentation slides
- [ ] Demo script

**Labels:** `documentation`, `priority:high`

---

## Instructions pour créer les issues :

1. Va sur ton repository GitHub
2. Clique sur "Issues" → "New Issue"
3. Copie-colle le contenu de chaque issue ci-dessus
4. Ajoute les labels appropriés
5. Assigne-toi l'issue
6. Crée l'issue

## Instructions pour les Pull Requests :

Pour chaque TASK, crée une branche :
```bash
git checkout -b feature/task-01-setup
# Travaille sur la tâche
git add .
git commit -m "feat: setup project structure (closes #1)"
git push origin feature/task-01-setup
# Crée la PR sur GitHub et lie-la à l'issue avec "closes #1"
```
