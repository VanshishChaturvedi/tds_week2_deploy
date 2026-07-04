import time
import uuid
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# 1. Strict CORS Policy
allowed_origins = [
    "https://dash-piwtbc.example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# 2. Required Middleware for Headers
@app.middleware("http")
async def custom_headers_middleware(request: Request, call_next):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response

# 3. The Metrics Endpoint
@app.get("/stats")
async def calculate_stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        nums = [int(v.strip()) for v in values.split(",") if v.strip()]
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "Invalid input. Only integers are allowed."})

    if not nums:
        return JSONResponse(status_code=400, content={"error": "No valid numbers provided."})

    count = len(nums)
    total_sum = sum(nums)
    min_val = min(nums)
    max_val = max(nums)
    mean_val = total_sum / count

    return {
        "email": "24f2003215@ds.study.iitm.ac.in", # <-- PUT YOUR EXACT EMAIL HERE
        "count": count,
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "mean": mean_val
    }
