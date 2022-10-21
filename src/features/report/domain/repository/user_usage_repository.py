from __future__ import annotations

import abc
import dataclasses

from src.features.report.domain.entities.user_data_usage import UserDataUsage


class UserUsageRepository(abc.ABC):

    @abc.abstractmethod
    async def fetch(self) -> list[UserDataUsage] | UserUsageRepositoryFailure:
        pass  # pragma nocover


@dataclasses.dataclass(frozen=True, kw_only=True)
class UserUsageRepositoryFailure:
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class UserUsageRepositoryUnableToFetchFailure(UserUsageRepositoryFailure):
    pass
