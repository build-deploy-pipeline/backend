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

    jenkins_job_parameters = CreateJenkinsJobParameters(
        applicationName=request_body.applicationName,
        templateVersion=request_body.templateVersion,
        githubLink=request_body.githubLink,
        githubBranch=request_body.githubBranch
    )

    try:
        jenkins_queue_id: int = jenkins_client.build_job(
            jenkins_job_name,
            parameters=jenkins_job_parameters.__dict__,
            token=None
        )
    except jenkins.NotFoundException as e:
        raise RuntimeError("Jenkins job이 존재하지 않습니다.")
    except Exception as e:
        print(e)
        raise RuntimeError(e)

    print(jenkins_queue_id)


def getJenkinsJobByTemplateType(template_type: str):
    """template타입에 따른 젠킨스 잡 조회"""
    jenkins_jobs = {
        "fastapi": "test/remote_trigger"
    }

    return jenkins_jobs[template_type]
