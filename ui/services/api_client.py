import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, Timeout
from urllib3.util.retry import Retry


class APIError(Exception):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.details = details


class APIClient:
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.3, status_forcelist=(500, 502, 504))
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def post(self, path: str, json=None):
        url = self._url(path)
        try:
            resp = self.session.post(url, json=json, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except ConnectionError as e:
            # Connection refused / not reachable
            raise APIError(f"Não foi possível conectar-se à API em {self.base_url}: {e}")
        except Timeout as e:
            raise APIError(f"Tempo de conexão esgotado ao contatar a API em {self.base_url}: {e}")
        except requests.RequestException as e:
            # try to extract response body for a friendlier error
            details = None
            resp = getattr(e, 'response', None)
            if resp is not None:
                try:
                    details = resp.json()
                except Exception:
                    details = {'text': resp.text}
            raise APIError(str(e), details=details)

    def get(self, path: str, params=None):
        url = self._url(path)
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except ConnectionError as e:
            raise APIError(f"Não foi possível conectar-se à API em {self.base_url}: {e}")
        except Timeout as e:
            raise APIError(f"Tempo de conexão esgotado ao contatar a API em {self.base_url}: {e}")
        except requests.RequestException as e:
            details = None
            resp = getattr(e, 'response', None)
            if resp is not None:
                try:
                    details = resp.json()
                except Exception:
                    details = {'text': resp.text}
            raise APIError(str(e), details=details)
