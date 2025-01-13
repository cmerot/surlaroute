from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.core.schemas import (
    PageParams,
)


class ToursPageParams(PageParams):
    pass


ToursPageParamsDep = Annotated[ToursPageParams, Depends()]
