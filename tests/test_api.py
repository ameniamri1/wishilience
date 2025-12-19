"""
Unit tests for Wishilience API
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint returns 200"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint():
    """Test root endpoint returns service info"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Wishilience"

def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "chaos_injections_total" in response.text

def test_cpu_burn_endpoint():
    """Test CPU burn chaos scenario"""
    response = client.post("/chaos/burn-cpu")
    assert response.status_code == 200
    assert response.json()["type"] == "cpu_burn"

def test_memory_leak_endpoint():
    """Test memory leak chaos scenario"""
    response = client.post("/chaos/leak-memory")
    assert response.status_code == 200
    assert response.json()["type"] == "memory_leak"

def test_terminate_endpoint():
    """Test termination chaos scenario"""
    response = client.post("/chaos/terminate")
    assert response.status_code == 200
    assert response.json()["type"] == "terminate"
