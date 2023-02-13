class NotFoundTemplate(Exception):
    """템플릿이 존재하지 않음"""
    def __int__(self):
        self.code = 100
        self.message = "유효하지 않은 템플릿"
        super.__init__(f"[error code: {self.code}], error message: {self.message}")


class JenkinsOtherError(Exception):
    """젠킨스 실행 오류"""
    def __int__(self):
        self.code = 101
        self.message = "젠킨스 기타 에러"
        super.__init__(f"[error code: {self.code}], error message: {self.message}")
