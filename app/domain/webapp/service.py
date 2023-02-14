import jenkins
from config import Settings
from api.models.webapp import RequestBodyCreateWebApp
from .models import CreateJenkinsJobParameters
import custom_exception

def TriggerJenkinsJob(request_body: RequestBodyCreateWebApp, settings: Settings):
    """생성을 jenkins에게 위임"""
    jenkins_client = jenkins.Jenkins(settings.jenkins_url, username=settings.jenkins_username, password=settings.jenkins_password)

    try:
        jenkins_job_name = getJenkinsJobByTemplateType(request_body.templateType)
    except IndexError:
        raise custom_exception.NotFoundTemplate("템플릿이 없습니다.")

    jenkins_job_parameters = generateJenkinsJobParameters(request_body)
    triggerJenkinsJobOrRaiseException(jenkins_client, jenkins_job_name, jenkins_job_parameters.__dict__)


def triggerJenkinsJobOrRaiseException(jenkins_client, jenkins_job_name: str, jenkins_job_parameters: dict) -> int:
    """jenkins job 요청"""
    try:
        jenkins_queue_id: int = jenkins_client.build_job(
            jenkins_job_name,
            parameters=jenkins_job_parameters,
            token=None
        )
        return jenkins_queue_id
    except jenkins.NotFoundException as e:
        raise RuntimeError("Jenkins job이 존재하지 않습니다.")
    except Exception as e:
        raise custom_exception.JenkinsError("jenkins 기타 에러가 발생했습니다.")


def generateJenkinsJobParameters(request_body):
    """젠킨스 잡 파라미터 생성"""
    return CreateJenkinsJobParameters(
        application_name=request_body.applicationName,
        # templateVersion=request_body.templateVersion,
        github_link=request_body.githubLink,
        github_branch=request_body.githubBranch
    )


def getJenkinsJobByTemplateType(template_type: str):
    """template타입에 따른 젠킨스 잡 조회"""
    jenkins_jobs = {
        "fastapi": "create_webapp/fastapi"
    }

    return jenkins_jobs[template_type]
