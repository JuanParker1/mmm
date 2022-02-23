import os


class Credential:
    def __init__(self, api_key: str, secret_key: str, phrase: str or None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.phrase = phrase

    @classmethod
    def load_from_env(cls):
        api_key = os.environ.get('API_KEY', None)
        if api_key is None:
            raise RuntimeError('API_KEY未配置')
        secret_key = os.environ.get('SECRET_KEY', None)
        if secret_key is None:
            raise RuntimeError('SECRET_KEY未配置')
        phrase = os.environ.get('PHRASE', None)
        return cls(api_key, secret_key, phrase)
