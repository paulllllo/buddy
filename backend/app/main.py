from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import create_tables
from app.routers import auth, companies, flows, stages, content_types, content_blocks, stage_templates, new_hires, onboarding
from app.middleware.rate_limit import rate_limit_onboarding_middleware

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Onboarding-as-a-Service (OaaS) Backend API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware for onboarding endpoints
app.middleware("http")(rate_limit_onboarding_middleware)

# Mount static files for local storage
app.mount("/files", StaticFiles(directory=settings.local_storage_path), name="files")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(companies.router, prefix="/api/companies", tags=["Companies"])
app.include_router(flows.router, prefix="/api/flows", tags=["Onboarding Flows"])
app.include_router(stages.router, prefix="/api/stages", tags=["Stages"])
app.include_router(content_types.router, prefix="/api/content-types", tags=["Content Types"])
app.include_router(content_blocks.router, prefix="/api/content-blocks", tags=["Content Blocks"])
app.include_router(stage_templates.router, prefix="/api/stage-templates", tags=["Stage Templates"])
app.include_router(new_hires.router, prefix="/api/new-hires", tags=["New Hires"])
app.include_router(onboarding.router, prefix="/api/onboarding", tags=["Onboarding Sessions"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    # Create database tables
    create_tables()
    
    # Seed content types and templates
    from app.services.content_type_service import ContentTypeService
    from app.services.stage_template_service import StageTemplateService
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Seed content types
        created_types = ContentTypeService.seed_content_types(db)
        if created_types:
            print(f"✅ Seeded {len(created_types)} content types")
        
        # Seed stage templates
        created_templates = StageTemplateService.seed_stage_templates(db)
        if created_templates:
            print(f"✅ Seeded {len(created_templates)} stage templates")
            
    except Exception as e:
        print(f"⚠️  Seeding error: {e}")
    finally:
        db.close()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Onboarding-as-a-Service API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 