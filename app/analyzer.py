import google.generativeai as genai
from app.dependencies import get_gemini_api_key
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)
genai.configure(api_key=get_gemini_api_key())

# Initialize the model with error handling
try:
    model = genai.GenerativeModel("gemini-1.5-pro")  # Updated model name
    logger.info("Gemini model initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini model: {str(e)}")
    raise RuntimeError("Failed to initialize AI model")

async def generate_market_report(sector: str, data: str, detailed: bool = False) -> str:
    prompt = f"""
Create a comprehensive markdown report analyzing the current trade opportunities and market trends in the "{sector}" sector in India.

Report Structure:
1. ## {sector.capitalize()} Sector Analysis - India
2. ### Current Trends (bullet points)
3. ### Trade Opportunities (numbered list)
4. ### Risk Factors (bullet points)
5. ### Recommended Actions (bullet points)

Use the following context:
{data}

Additional Instructions:
- Be concise but informative
- Focus on actionable insights
- Highlight both opportunities and risks
- Use Indian market context specifically
- Format strictly in markdown
    """
    try:
        logger.info(f"Generating report for {sector} sector")
        
        # Add error handling for the API call
        response = await model.generate_content_async(prompt)
        
        if not response.text:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service returned empty response"
            )
            
        return response.text
        
    except Exception as e:
        logger.error(f"AI generation failed for {sector}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI generation failed: {str(e)}"
        )