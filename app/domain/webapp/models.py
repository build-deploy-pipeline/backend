from dataclasses import dataclass, asdict
import json


@dataclass
class CreateJenkinsJobParameters:
    applicationName: str
    # templateVersion: str
    githubLink: str
    githubBranch: str

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return json.dumps(self.__dict__)
