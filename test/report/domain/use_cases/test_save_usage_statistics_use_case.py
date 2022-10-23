from collections.abc import Generator

import decoy
import pytest

from src.features.report.domain.entities.data_usage_statistics import DataUsageStatistics
from src.features.report.domain.entities.megabytes_unit import MegabytesUnit
from src.features.report.domain.entities.user_data_usage import UserDataUsage
from src.features.report.domain.entities.username import Username
from src.features.report.domain.repository.statistics_repository import (
    StatisticsRepository,
    StatisticsRepositoryUnableToSaveFailure,
)
from src.features.report.domain.use_cases.save_usage_statistics_use_case import (
    SaveUsageStatisticsFailure,
    SaveUsageStatisticsUnableToSaveFailure, SaveUsageStatisticsUseCase,
)


class TestSaveUsageStatisticsUseCase:
    _decoy: decoy.Decoy
    _dummy_repository: StatisticsRepository
    _use_case: SaveUsageStatisticsUseCase

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self) -> Generator[None, None, None]:
        # Set Up
        self._decoy = decoy.Decoy()
        self._dummy_repository = self._decoy.mock(cls=StatisticsRepository)
        self._use_case = SaveUsageStatisticsUseCase(statistics_repository=self._dummy_repository)

        yield

        # Tear Down
        self._decoy.reset()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'statistics',
        [
            DataUsageStatistics(user_usages=[]),
            DataUsageStatistics(
                user_usages=[
                    UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=62.0)),
                    UserDataUsage(username=Username(value='path'), usage=MegabytesUnit(value=38.0)),
                    UserDataUsage(username=Username(value='miss'), usage=MegabytesUnit(value=900.0)),
                ]
            ),
        ]
    )
    async def test_should_call_repository_correctly(self, statistics: DataUsageStatistics) -> None:
        result: None | SaveUsageStatisticsFailure = await self._use_case.execute(statistics)

        assert result is None

        self._decoy.verify(
            await self._dummy_repository.save(statistics)
        )

    @pytest.mark.asyncio
    async def test_should_return_unable_to_save_failure(self) -> None:
        dummy_statistics: DataUsageStatistics = self._decoy.mock(cls=DataUsageStatistics)

        self._decoy.when(
            await self._dummy_repository.save(dummy_statistics)
        ).then_return(StatisticsRepositoryUnableToSaveFailure())

        result: None | SaveUsageStatisticsFailure = await self._use_case.execute(dummy_statistics)

        assert isinstance(result, SaveUsageStatisticsFailure)
        assert isinstance(result, SaveUsageStatisticsUnableToSaveFailure)
