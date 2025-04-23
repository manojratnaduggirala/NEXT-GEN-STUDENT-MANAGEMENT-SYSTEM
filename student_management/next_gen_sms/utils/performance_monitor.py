from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import psutil
import time

app = FastAPI()

class PerformanceMetrics(BaseModel):
    response_time: float
    throughput: float 
    error_rate: float
    cpu_usage: float
    memory_usage: float

def get_system_metrics():
    """Collect real system performance metrics"""
    return {
        'cpu_usage': psutil.cpu_percent(),
        'memory_usage': psutil.virtual_memory().percent
    }

@app.get("/metrics")
async def get_metrics():
    """Endpoint to return performance metrics"""
    metrics = get_system_metrics()
    return {
        "response_time": 0.45,  # Simulated value
        "throughput": 1200,     # Simulated value
        "error_rate": 0.02,     # Simulated value
        "cpu_usage": metrics['cpu_usage'],
        "memory_usage": metrics['memory_usage']
    }

def start_monitor():
    """Start the performance monitoring server"""
    uvicorn.run(app, host="0.0.0.0", port=8001)