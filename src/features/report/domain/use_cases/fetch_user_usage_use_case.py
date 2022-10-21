from __future__ import annotations

import dataclasses
import typing

from src.features.report.domain.entities.user_data_usage import UserDataUsage
from src.features.report.domain.repository.user_usage_repository import UserUsageRepository, UserUsageRepositoryFailure


class FetchUserUsageUseCase:
    _user_usage_repository: UserUsageRepository

    def __init__(self, user_usage_repository: UserUsageRepository) -> None:
        self._user_usage_repository = user_usage_repository

    async def execute(self) -> list[UserDataUsage] | FetchUserUsageFailure:
        result: list[UserDataUsage] | UserUsageRepositoryFailure = await self._user_usage_repository.fetch()

        if isinstance(result, UserUsageRepositoryFailure):
            return NoDataFailure()

        user_data_usage: list[UserDataUsage] = typing.cast(list[UserDataUsage], result)

        return user_data_usage


@dataclasses.dataclass(frozen=True, kw_only=True)
class FetchUserUsageFailure:
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class NoDataFailure(FetchUserUsageFailure):
    pass
