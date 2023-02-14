from fastapi import APIRouter, Depends, HTTPException
from config import get_settings, Settings
import domain.webapp.service as webapp_service
from api.models.webapp import RequestBodyCreateWebApp
import custom_exception
from log import get_logger


router = APIRouter(
    prefix="/webapp",
    tags=["webapp API"]
)
logger = get_logger()


@router.post("/")
def createWebapp(request_body: RequestBodyCreateWebApp, settings: Settings = Depends(get_settings)):
    """webapp 생성"""
    logger.debug(f"[webapp 생성 파라미터] {request_body.json()}")
    try:
        webapp_service.TriggerJenkinsJob(request_body=request_body, settings=settings)
    except custom_exception.NotFoundTemplate as e:
        logger.error(f"[webapp 생성 오류] 템플릿이 없습니다: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except custom_exception.JenkinsError as e:
        logger.error(f"[webapp 생성 오류] 젠킨스 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"[webapp 생성 오류] 기타 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))
