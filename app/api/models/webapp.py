from pydantic import BaseModel


class RequestBodyCreateWebApp(BaseModel):
    """웹앱 생성 요청"""
    applicationName: str
    templateType: str
    templateVersion: str
    githubLink: str
    githubBranch: str
