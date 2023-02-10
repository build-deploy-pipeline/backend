from fastapi import APIRouter, Depends, HTTPException
from config import get_settings, Settings
import domain.webapp.service as webapp_service
from api.models.webapp import RequestBodyCreateWebApp


router = APIRouter(
    prefix="/webapp",
    tags=["webapp API"]
)


@router.post("/")
def createWebapp(request_body: RequestBodyCreateWebApp, settings: Settings = Depends(get_settings)):
    """webapp 생성"""
    try:
        webapp_service.TriggerJenkinsJob(request_body=request_body, settings=settings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
