from collections.abc import Generator

import decoy
import pytest

from src.features.report.domain.entities.data_usage_statistics import DataUsageStatistics
from src.features.report.domain.entities.megabytes_unit import MegabytesUnit
from src.features.report.domain.entities.user_data_usage import UserDataUsage
from src.features.report.domain.entities.username import Username
from src.features.report.domain.use_cases.generate_usage_statistics_use_case import GenerateUsageStatisticsUseCase


class TestGenerateUsageStatisticsUseCase:
    _decoy: decoy.Decoy
    _use_case: GenerateUsageStatisticsUseCase

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self) -> Generator[None, None, None]:
        # Set Up
        self._decoy = decoy.Decoy()
        self._use_case = GenerateUsageStatisticsUseCase()

        yield

        # Tear Down
        self._decoy.reset()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'user_usages',
        [
            [],
            [
                UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=62.0)),
                UserDataUsage(username=Username(value='path'), usage=MegabytesUnit(value=38.0)),
                UserDataUsage(username=Username(value='miss'), usage=MegabytesUnit(value=900.0)),
            ],
        ]
    )
    async def test_should_return_a_statistics_object(self, user_usages: list[UserDataUsage]) -> None:
        result: DataUsageStatistics = await self._use_case.execute(user_usages)

        assert isinstance(result, DataUsageStatistics)
        assert result.user_usages is user_usages
