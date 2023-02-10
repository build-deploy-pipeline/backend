import jenkins
from config import Settings
from api.models.webapp import RequestBodyCreateWebApp
from .models import CreateJenkinsJobParameters


def TriggerJenkinsJob(request_body: RequestBodyCreateWebApp, settings: Settings):
    """생성을 jenkins에게 위임"""
    jenkins_client = jenkins.Jenkins(settings.jenkins_url, username=settings.jenkins_username, password=settings.jenkins_password)

    try:
        jenkins_job_name = getJenkinsJobByTemplateType(request_body.templateType)
    except IndexError:
        raise RuntimeError("유효하지 않은 템플릿type")

    jenkins_job_parameters = generateJenkinsJobParameters(request_body)
    triggerJenkinsJobOrRaiseException(jenkins_client, jenkins_job_name, jenkins_job_parameters.__dict__)


def triggerJenkinsJobOrRaiseException(jenkins_client, jenkins_job_name: str, jenkins_job_parameters: dict) -> int:
    """jenkins job 요청"""
    try:
        jenkins_queue_id: int = jenkins_client.build_job(
            jenkins_job_name,
            parameters=jenkins_job_parameters.__dict__,
            token=None
        )
        return jenkins_queue_id
    except jenkins.NotFoundException as e:
        raise RuntimeError("Jenkins job이 존재하지 않습니다.")
    except Exception as e:
        raise RuntimeError(e)


def generateJenkinsJobParameters(request_body):
    """젠킨스 잡 파라미터 생성"""
    return CreateJenkinsJobParameters(
        applicationName=request_body.applicationName,
        templateVersion=request_body.templateVersion,
        githubLink=request_body.githubLink,
        githubBranch=request_body.githubBranch
    )


def getJenkinsJobByTemplateType(template_type: str):
    """template타입에 따른 젠킨스 잡 조회"""
    jenkins_jobs = {
        "fastapi": "test/remote_trigger"
    }

    return jenkins_jobs[template_type]
