# fastapi_speechki
===
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Introduction
------------
Utils for FastAPI


* **Permission**: Permission class and Permission dependency class

```python
from fastapi import APIRouter, Depends
from fastapi_speechki import permissions
router = APIRouter()


@router.get(
    "/api/v1/test/",
    tags=["test.v1"],
    dependencies=[
        Depends(
            permissions.OrPermissionsDependency(
                [permissions.AbstractPermission]
            )
        )
    ],
)
async def test_handler():
    return {"detail": "Hello World!"}
```

* **Pagination**: Pagination for ClickHouse

```python
from fastapi import APIRouter, Depends
from fastapi_speechki.clickhouse.pagination import OffsetLimitClickHousePagination


router = APIRouter()


@router.get(
    "/api/v1/test/",
    tags=["test.v1"],
)
async def test_handler(pagination: OffsetLimitClickHousePagination = Depends()):
    result = await pagination.paginate()
    return result
```

Installation
------------
   `$ pip install git+https://github.com/speechki-book/fastapi_speechki.git`


Dependencies
------------

1. FastAPI
2. https://github.com/speechki-book/clickhouse_utils.git
