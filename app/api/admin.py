import time

from fastapi import APIRouter, Query

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/simulate-error")
def simulate_error():
    raise RuntimeError("Intentional simulated server error")


@router.post("/simulate-latency")
def simulate_latency(seconds: float = Query(default=1.0, ge=0, le=30)):
    time.sleep(seconds)
    return {"status": "ok", "delay_seconds": seconds}
