"""
Wishilience - Chaos Engineering API for Kubernetes Self-Healing Demo
Author: DevOps Student
Version: 1.0.0
"""

from fastapi import FastAPI, Response, BackgroundTasks
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
import logging
import json
import sys
import time
import threading
from typing import Dict

# ===== CONFIGURATION =====
app = FastAPI(title="Wishilience", version="1.0.0")

# OpenTelemetry Setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)

# Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus Metrics
chaos_counter = Counter('chaos_injections_total', 'Total chaos scenarios triggered', ['type'])
request_duration = Histogram('request_duration_seconds', 'Request duration')
crash_counter = Counter('app_crashes_total', 'Total application crashes')

# ===== HELPER FUNCTIONS =====
def log_event(level: str, event: str, **kwargs):
    """Structured JSON logging"""
    log_data = {
        "timestamp": time.time(),
        "level": level,
        "event": event,
        **kwargs
    }
    logger.info(json.dumps(log_data))

def cpu_burn():
    """CPU intensive task"""
    log_event("warning", "chaos_injection", type="cpu_burn", status="started")
    end_time = time.time() + 30
    while time.time() < end_time:
        _ = sum([i**2 for i in range(10000)])
    log_event("info", "chaos_injection", type="cpu_burn", status="completed")

def memory_leak():
    """Progressive memory leak"""
    log_event("warning", "chaos_injection", type="memory_leak", status="started")
    leak = []
    for _ in range(50):
        leak.append([0] * 1024 * 1024)  # Allocate ~8MB per iteration
        time.sleep(0.1)
    log_event("critical", "chaos_injection", type="memory_leak", status="oom_imminent")

# ===== ENDPOINTS =====
@app.get("/health")
async def health_check():
    """Kubernetes Liveness Probe endpoint"""
    with tracer.start_as_current_span("health_check"):
        log_event("info", "health_check", status="healthy")
        return {"status": "healthy", "timestamp": time.time()}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/chaos/burn-cpu")
async def trigger_cpu_burn(background_tasks: BackgroundTasks):
    """Trigger CPU intensive task to test HPA"""
    with tracer.start_as_current_span("chaos_cpu_burn"):
        chaos_counter.labels(type='cpu_burn').inc()
        background_tasks.add_task(cpu_burn)
        return {
            "status": "chaos_injected",
            "type": "cpu_burn",
            "duration_seconds": 30,
            "message": "CPU load spike initiated. Watch HPA scale!"
        }

@app.post("/chaos/leak-memory")
async def trigger_memory_leak(background_tasks: BackgroundTasks):
    """Trigger memory leak to test OOMKilled behavior"""
    with tracer.start_as_current_span("chaos_memory_leak"):
        chaos_counter.labels(type='memory_leak').inc()
        background_tasks.add_task(memory_leak)
        return {
            "status": "chaos_injected",
            "type": "memory_leak",
            "message": "Memory leak initiated. Pod will OOMKill soon!"
        }

@app.post("/chaos/terminate")
async def trigger_termination():
    """Force application crash to test pod restart"""
    with tracer.start_as_current_span("chaos_terminate"):
        chaos_counter.labels(type='terminate').inc()
        crash_counter.inc()
        log_event("critical", "chaos_injection", type="terminate", message="Application terminating NOW!")
        
        def shutdown():
            time.sleep(1)
            sys.exit(1)
        
        threading.Thread(target=shutdown).start()
        return {
            "status": "chaos_injected",
            "type": "terminate",
            "message": "Application will terminate in 1 second. Watch K8s restart!"
        }

@app.get("/")
async def root():
    """API information"""
    return {
        "service": "Wishilience",
        "version": "1.0.0",
        "description": "Chaos Engineering API for K8s Self-Healing Demo",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "chaos_cpu": "POST /chaos/burn-cpu",
            "chaos_memory": "POST /chaos/leak-memory",
            "chaos_terminate": "POST /chaos/terminate"
        }
    }

if __name__ == "__main__":
    import uvicorn
    log_event("info", "app_startup", message="Wishilience starting...")
    # Binding to 0.0.0.0 is required for containerized apps to accept external traffic
    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec B104
