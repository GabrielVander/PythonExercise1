from collections.abc import Generator

import decoy
import pytest

from src.features.report.domain.entities.data_usage_statistics import DataUsageStatistics
from src.features.report.domain.entities.user_data_usage import UserDataUsage
from src.features.report.domain.use_cases.fetch_user_usage_use_case import FetchUserUsageUseCase
from src.features.report.domain.use_cases.generate_usage_statistics_use_case import GenerateUsageStatisticsUseCase
from src.features.report.domain.use_cases.save_usage_statistics_use_case import SaveUsageStatisticsUseCase
from src.features.report.report_controller import ReportController


class TestReportController:
    _decoy: decoy.Decoy
    _dummy_fetch_user_usage_use_case: FetchUserUsageUseCase
    _dummy_generate_usage_statistics_use_case: GenerateUsageStatisticsUseCase
    _dummy_save_usage_statistics_use_case: SaveUsageStatisticsUseCase
    _controller: ReportController

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self) -> Generator[None, None, None]:
        # Set Up
        self._decoy = decoy.Decoy()
        self._dummy_fetch_user_usage_use_case = self._decoy.mock(cls=FetchUserUsageUseCase)
        self._dummy_generate_usage_statistics_use_case = self._decoy.mock(cls=GenerateUsageStatisticsUseCase)
        self._dummy_save_usage_statistics_use_case = self._decoy.mock(cls=SaveUsageStatisticsUseCase)
        self._controller = ReportController(
            fetch_user_usage_use_case=self._dummy_fetch_user_usage_use_case,
            generate_usage_statistics_use_case=self._dummy_generate_usage_statistics_use_case,
            save_usage_statistics_use_case=self._dummy_save_usage_statistics_use_case,
        )

        yield

        # Tear Down
        self._decoy.reset()

    @pytest.mark.asyncio
    async def test_should_call_use_cases_correctly_and_in_order(self) -> None:
        dummy_user_usages: list[UserDataUsage] = self._decoy.mock(cls=list[UserDataUsage])
        dummy_statistics: DataUsageStatistics = self._decoy.mock(cls=DataUsageStatistics)

        self._decoy.when(
            await self._dummy_fetch_user_usage_use_case.execute()
        ).then_return(dummy_user_usages)

        self._decoy.when(
            await self._dummy_generate_usage_statistics_use_case.execute(dummy_user_usages)
        ).then_return(dummy_statistics)

        await self._controller.run()

        self._decoy.verify(
            await self._dummy_save_usage_statistics_use_case.execute(dummy_statistics)
        )
