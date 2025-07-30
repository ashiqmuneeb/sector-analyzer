from fastapi import FastAPI, Depends, Path, Request
from fastapi.responses import PlainTextResponse
from slowapi.middleware import SlowAPIMiddleware
from app.rate_limiter import limiter
from app.auth import authenticate_user
from app.fetcher import fetch_sector_news
from app.analyzer import generate_market_report
from app.session_manager import session_manager
from app.logger import logger
from fastapi.middleware.cors import CORSMiddleware
import re



app = FastAPI(
    title="Sector Market Analyzer API",
    description="API for analyzing Indian market sectors using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter

@app.middleware("http")
async def session_middleware(request: Request, call_next):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = session_manager.create_session(request)
    
    session_manager.update_session(session_id)
    response = await call_next(request)
    response.set_cookie(key="session_id", value=session_id)
    return response

@app.get(
    "/analyze/{sector}",
    response_class=PlainTextResponse,
    summary="Analyze a market sector",
    description="""Analyzes the specified market sector in India and returns a markdown report
    with current trends, trade opportunities, and risk factors.""",
    responses={
        200: {
            "content": {"text/markdown": {}},
            "description": "Markdown formatted market analysis report",
        },
        403: {"description": "Invalid API key"},
        429: {"description": "Rate limit exceeded"},
        422: {"description": "Validation error"},
    },
    tags=["Analysis"]
)
@limiter.limit("5/minute")
async def analyze_sector(
    request: Request,
    sector: str = Path(
        ...,
        min_length=3,
        max_length=30,
        pattern=r"^[a-zA-Z\-]+$",
        example="technology",
        description="Name of the sector to analyze (letters and hyphens only)"
    ),
    _: None = Depends(authenticate_user)
):
    try:
        logger.info(f"Analyzing sector: {sector}")
        session_id = request.cookies.get("session_id")
        session_data = session_manager.get_session(session_id)
        
        raw_data = await fetch_sector_news(sector)
        logger.debug(f"Raw data fetched: {raw_data[:100]}...")
        
        markdown_report = await generate_market_report(sector, raw_data)
        logger.info(f"Report generated for sector: {sector}")
        
        return markdown_report
    except Exception as e:
        logger.error(f"Error analyzing sector {sector}: {str(e)}", exc_info=True)
        return f"## Error\n\nSomething went wrong: {str(e)}"