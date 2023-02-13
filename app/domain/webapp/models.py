from dataclasses import dataclass, asdict
import json


@dataclass
class CreateJenkinsJobParameters:
    application_name: str
    # templateVersion: str
    github_link: str
    github_branch: str

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return json.dumps(self.__dict__)
