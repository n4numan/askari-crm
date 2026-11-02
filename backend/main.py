
from fastapi import FastAPI
from routes.leads import router as leads_router
from routes.tutors import router as tutors_router
from routes.demos import router as demos_router
from routes.follow_ups import router as follow_ups_router
from routes.tuitions import router as tuitions_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Askari Academy CRM API",
    description="Home Tuition Lead Management System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9000",
        "http://127.0.0.1:9000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads_router)
app.include_router(tutors_router)
app.include_router(demos_router)
app.include_router(follow_ups_router)
app.include_router(tuitions_router)



@app.get("/")
def home():
    return {
        "message": "Askari Academy CRM Backend is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
