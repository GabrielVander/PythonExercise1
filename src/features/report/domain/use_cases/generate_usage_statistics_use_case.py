from src.features.report.domain.entities.data_usage_statistics import DataUsageStatistics
from src.features.report.domain.entities.user_data_usage import UserDataUsage


class GenerateUsageStatisticsUseCase:

    # noinspection PyMethodMayBeStatic
    async def execute(self, user_usages: list[UserDataUsage]) -> DataUsageStatistics:
        return DataUsageStatistics(user_usages=user_usages)
