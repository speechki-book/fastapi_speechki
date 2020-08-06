from fastapi_speechki.pagination import AbstractLimitOffsetPagination
from clickhouse_utils.client import ChExecutorClient
from starlette.requests import Request
from typing import Union
import asyncio


class OffsetLimitClickHousePagination(AbstractLimitOffsetPagination):
    def __init__(
            self,
            request: Request,
            client: ChExecutorClient,
            offset: int = 0,
            limit: int = 100,
    ):
        super().__init__(request, client, offset, limit)

    async def get_count(self, **kwargs) -> int:
        """

        :param kwargs:
        :return: number of found records
        """

        self.count = await self.client.get_count(**kwargs)
        return self.count

    def get_next_url(self) -> Union[str, None]:
        """

        :return: URL for next "page" of paginated results.
        """

        if self.offset + self.limit >= self.count:
            return None

        return str(
            self.request.url.include_query_params(
                limit=self.limit, offset=self.offset + self.limit
            )
        )

    def get_previous_url(self) -> Union[str, None]:
        """

        :return: URL for previous "page" of paginated results.
        """

        if self.offset <= 0:
            return None

        if self.offset - self.limit <= 0:
            return str(self.request.url.remove_query_params(keys=["offset"]))

        return str(
            self.request.url.include_query_params(
                limit=self.limit, offset=self.offset - self.limit
            )
        )

    async def get_list(self, **kwargs):
        """

        :param kwargs:
            - table: str,
            - filter_params: Optional[dict] = None,
            - pagination: Optional[dict] = None,
            - fields: Optional[List[str]] = None,
            - ordering Optional[List[str]] = None,
        :return:
        """
        self.list = await self.client.get_list(
            pagination=self.pagination_dict, **kwargs
        )
        return self.list

    async def paginate(self, **kwargs):
        """

        :param kwargs:
        :return: object that should be returned as a response
        """

        count, list_result = await asyncio.gather(
            self.get_count(**kwargs), self.get_list(**kwargs)
        )
        return {
            "count": count,
            "next": self.get_next_url(),
            "previous": self.get_previous_url(),
            "result": list_result,
        }
