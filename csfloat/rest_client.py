import requests 
from typing import List,Dict
from csfloat.exceptions import CSFloatApiException
from csfloat.models import Result
from json import JSONDecodeError
import logging

class RestClient:
    def __init__(self,hostname:str, api_key: str,logger: logging.Logger = None):
        """
        Constructor for RestClient
        :param hostname: api hostname, eg csfloat.com/api/v1
        :param api_key: string used for authentication 
        :param logger: (optional) If your app has a logger, pass it in here.
        
        """

        self.url = f"https://{hostname}"
        self._api_key = api_key
        self._logger = logger or logging.getLogger(__name__)


    def _do(self, http_method : str, endpoint:str,ep_params: Dict = None, data: Dict = None) ->Result: 
        full_url = self.url + endpoint
        headers = {'Authorization': self._api_key}

        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))

        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url, 
                                    headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise CSFloatApiException("Request failed") from e
        
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise CSFloatApiException("Bad JSON in response") from e
        is_success = 299 >= response.status_code >= 200
        log_line = log_line_post.format(is_success, response.status_code, response.reason)

        if is_success: 
            self._logger.debug(msg=log_line)
            return Result(response.status_code,message=response.reason,data=data_out)
        
        self._logger.error(msg=log_line)
        raise CSFloatApiException(f"{response.status_code}: {response.reason}")
    
    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)
