import requests
import json


class Connection:
    def __init__(self, url):
        self.url = url

    def get(self, data, size=None, next=None):
        try:
            url = self.url + data
            if size is not None and next is not None:
                url += f"?size={size}&next={next}"
            elif size is not None:
                url += f"?size={size}"
            elif next is not None:
                url += f"?next={next}"
            return json.loads(requests.get(url).text)
        except Exception as e:
            raise Exception(e)
