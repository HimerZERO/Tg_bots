from config_data.config import Url
import requests
import logging

logger = logging.getLogger(__name__)


def GetCatsLink(cat_api: Url, http_cat: Url) -> str:
    cat_response: requests.Response = requests.get(cat_api.path)
    if cat_response.status_code == 200:
        return cat_response.json()[0]['url']

    return http_cat.to(str(cat_response.status_code))
