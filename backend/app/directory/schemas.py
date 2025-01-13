from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.core.schemas import (
    PageParams,
)


class DirectoryPageParams(PageParams):
    activity: str | None = None


DirectoryPageParamsDep = Annotated[DirectoryPageParams, Depends()]
