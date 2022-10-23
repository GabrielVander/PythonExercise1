from src.features.report.domain.entities.data_usage_statistics import DataUsageStatistics
from src.features.report.domain.entities.user_data_usage import UserDataUsage
from src.features.report.domain.use_cases.fetch_user_usage_use_case import FetchUserUsageFailure, FetchUserUsageUseCase
from src.features.report.domain.use_cases.generate_usage_statistics_use_case import GenerateUsageStatisticsUseCase
from src.features.report.domain.use_cases.save_usage_statistics_use_case import (
    SaveUsageStatisticsFailure,
    SaveUsageStatisticsUseCase,
)


class ReportController:
    _fetch_user_usage_use_case: FetchUserUsageUseCase
    _generate_usage_statistics_use_case: GenerateUsageStatisticsUseCase
    _save_usage_statistics_use_case: SaveUsageStatisticsUseCase

    def __init__(
        self,
        fetch_user_usage_use_case: FetchUserUsageUseCase,
        generate_usage_statistics_use_case: GenerateUsageStatisticsUseCase,
        save_usage_statistics_use_case: SaveUsageStatisticsUseCase
    ) -> None:
        self._fetch_user_usage_use_case = fetch_user_usage_use_case
        self._generate_usage_statistics_use_case = generate_usage_statistics_use_case
        self._save_usage_statistics_use_case = save_usage_statistics_use_case

    async def run(self) -> None:
        user_usages: list[UserDataUsage] | FetchUserUsageFailure = await self._fetch_user_usage_use_case.execute()

        if isinstance(user_usages, FetchUserUsageFailure):
            print('Unable To Fetch User Usage')
            return

        statistics: DataUsageStatistics = await self._generate_usage_statistics_use_case.execute(user_usages)
        save_result: None | SaveUsageStatisticsFailure = await self._save_usage_statistics_use_case.execute(statistics)

        if isinstance(save_result, SaveUsageStatisticsFailure):
            print('Unable To Save Output File')
            return
