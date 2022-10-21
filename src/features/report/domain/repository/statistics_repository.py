from __future__ import annotations

import abc
import dataclasses

from src.features.report.domain.entities.data_usage_statistics import DataUsageStatistics


class StatisticsRepository(abc.ABC):

    @abc.abstractmethod
    async def save(self, statistics: DataUsageStatistics) -> None | StatisticsRepositoryFailure:
        pass  # pragma nocover


@dataclasses.dataclass(frozen=True, kw_only=True)
class StatisticsRepositoryFailure(abc.ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class StatisticsRepositoryUnableToSaveFailure(StatisticsRepositoryFailure):
    pass
