from pydantic import BaseModel, Field


class RequestBodyCreateWebApp(BaseModel):
    """웹앱 생성 요청"""
    applicationName: str = "demo_application"
    templateType: str = "fastapi"
    # templateVersion: str = "0.1"
    githubLink: str = "https://github.com/build-deploy-pipeline/argo-manifest-nginx-sample.git"
    githubBranch: str = "main"

    class Config:
        anystr_strip_whitespace = True