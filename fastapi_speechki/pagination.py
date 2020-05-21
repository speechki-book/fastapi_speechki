from starlette.requests import Request
from typing import Union, Dict, Any


class AbstractLimitOffsetPagination(object):
    def __init__(
        self,
        request: Request,
        client: Any,
        offset: int = 0,
        limit: int = 100,
    ):
        self.request = request
        self.offset = offset
        self.limit = limit
        self.pagination_dict = {"limit": limit, "offset": offset}
        self.count = None
        self.list = []
        self.client = client

    async def get_count(self, **kwargs) -> int:
        raise NotImplementedError

    def get_next_url(self) -> Union[str, None]:
        raise NotImplementedError

    def get_previous_url(self) -> Union[str, None]:
        raise NotImplementedError

    async def get_list(self, **kwargs):
        raise NotImplementedError

    async def paginate(
        self, query: str, response_class, **kwargs
    ) -> Dict[str, Union[str, int, list]]:
        """

        :param query: query to click house
        :param response_class: serializer which return data
        :param kwargs:
        :return: object that should be returned as a response
        """

        raise NotImplementedError
