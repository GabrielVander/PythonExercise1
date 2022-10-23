import asyncio

from constants import PROJECT_ROOT
from src.features.report.data.data_sources.file_data_source import FileDataSource
from src.features.report.data.repositories.statistics_repository_impl import StatisticsRepositoryImpl
from src.features.report.data.repositories.user_usage_repository_impl import UserUsageRepositoryImpl
from src.features.report.domain.repository.statistics_repository import StatisticsRepository
from src.features.report.domain.repository.user_usage_repository import UserUsageRepository
from src.features.report.domain.use_cases.fetch_user_usage_use_case import FetchUserUsageUseCase
from src.features.report.domain.use_cases.generate_usage_statistics_use_case import GenerateUsageStatisticsUseCase
from src.features.report.domain.use_cases.save_usage_statistics_use_case import SaveUsageStatisticsUseCase
from src.features.report.report_controller import ReportController


def reports_application() -> None:
    file_data_source: FileDataSource = FileDataSource(
        input_file_name='users.txt',
        input_folder_path=PROJECT_ROOT.joinpath('file_input'),
        output_file_name='report.txt',
        output_folder_path=PROJECT_ROOT.joinpath('file_output')
    )
    statistics_repository: StatisticsRepository = StatisticsRepositoryImpl(file_data_source=file_data_source)
    user_usage_repository: UserUsageRepository = UserUsageRepositoryImpl(file_data_source=file_data_source)
    fetch_user_usage_use_case: FetchUserUsageUseCase = FetchUserUsageUseCase(
        user_usage_repository=user_usage_repository
    )
    generate_usage_statistics_use_case: GenerateUsageStatisticsUseCase = GenerateUsageStatisticsUseCase()
    save_usage_statistics_use_case: SaveUsageStatisticsUseCase = SaveUsageStatisticsUseCase(
        statistics_repository=statistics_repository
    )
    controller: ReportController = ReportController(
        fetch_user_usage_use_case=fetch_user_usage_use_case,
        generate_usage_statistics_use_case=generate_usage_statistics_use_case,
        save_usage_statistics_use_case=save_usage_statistics_use_case,
    )

    asyncio.run(controller.run())


if __name__ == '__main__':
    reports_application()
