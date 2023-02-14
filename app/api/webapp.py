from fastapi import APIRouter, Depends, HTTPException
from config import get_settings, Settings
import domain.webapp.service as webapp_service
from api.models.webapp import RequestBodyCreateWebApp
import custom_exception

router = APIRouter(
    prefix="/webapp",
    tags=["webapp API"]
)


@router.post("/")
def createWebapp(request_body: RequestBodyCreateWebApp, settings: Settings = Depends(get_settings)):
    """webapp 생성"""
    try:
        webapp_service.TriggerJenkinsJob(request_body=request_body, settings=settings)
    except custom_exception.NotFoundTemplate as e:
        raise HTTPException(status_code=400, detail=str(e))
    except custom_exception.JenkinsError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
