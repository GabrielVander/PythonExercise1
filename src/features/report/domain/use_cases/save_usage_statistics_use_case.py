from __future__ import annotations

import abc
import dataclasses

from src.features.report.domain.entities.data_usage_statistics import DataUsageStatistics
from src.features.report.domain.repository.statistics_repository import (
    StatisticsRepository,
    StatisticsRepositoryFailure,
)


class SaveUsageStatisticsUseCase:
    _statistics_repository: StatisticsRepository

    def __init__(self, statistics_repository: StatisticsRepository) -> None:
        self._statistics_repository = statistics_repository

    async def execute(self, statistics: DataUsageStatistics) -> None | SaveUsageStatisticsFailure:
        save_result: None | StatisticsRepositoryFailure = await self._statistics_repository.save(
            statistics
        )

        if save_result is not None:
            return SaveUsageStatisticsUnableToSaveFailure()

        return None


@dataclasses.dataclass(frozen=True, kw_only=True)
class SaveUsageStatisticsFailure(abc.ABC):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class SaveUsageStatisticsUnableToSaveFailure(SaveUsageStatisticsFailure):
    pass
