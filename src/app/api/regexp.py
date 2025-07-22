from fastapi import APIRouter
from src.app.schemas.regexp import RegexpPatternRequest, RegexpTextRequest
from src.app.service.regexp import ScriptTextAnalyzer

router = APIRouter(prefix="/regexp", tags=["regexp"])


@router.post("/extract_emails")
async def extract_emails(data: RegexpTextRequest):
    """
    Извлечь все email-адреса из текста скрипта.
    """
    emails = ScriptTextAnalyzer.extract_emails(data.text)
    return {"emails": emails}


@router.post("/extract_variables")
async def extract_variables(data: RegexpTextRequest):
    """
    Извлечь переменные вида {{variable}} из текста скрипта.
    """
    variables = ScriptTextAnalyzer.extract_variables(data.text)
    return {"variables": variables}


@router.post("/validate_pattern")
async def validate_pattern(data: RegexpPatternRequest):
    """
    Проверить, соответствует ли текст скрипта заданному регулярному выражению.
    """
    is_valid = ScriptTextAnalyzer.validate_script_pattern(
        data.text,
        data.pattern
        )
    return {"is_valid": is_valid}
