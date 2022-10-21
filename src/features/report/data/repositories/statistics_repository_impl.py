from src.features.report.data.data_sources.file_data_source import FileDataSource, FileDataSourceFileContent
from src.features.report.domain.entities.data_usage_statistics import DataUsageStatistics
from src.features.report.domain.entities.individual_usage import IndividualUsage
from src.features.report.domain.entities.megabytes_unit import MegabytesUnit
from src.features.report.domain.repository.statistics_repository import (
    StatisticsRepository,
    StatisticsRepositoryFailure,
)


class StatisticsRepositoryImpl(StatisticsRepository):
    _number_width: int = 5
    _username_width: int = 20
    _amount_width: int = 15
    _percentage_width: int = 30

    _file_data_source: FileDataSource

    def __init__(self, file_data_source: FileDataSource) -> None:
        self._file_data_source = file_data_source

    async def save(self, statistics: DataUsageStatistics) -> None | StatisticsRepositoryFailure:
        await self._file_data_source.save_report_output_file(
            FileDataSourceFileContent(value=self._build_report_str(statistics))
        )

        return None

    def _build_report_str(self, statistics: DataUsageStatistics) -> str:
        lines: list[str] = [
            self._build_report_header(),
            self._build_usage_display_table(statistics.individual_usages),
            self._build_trailer(statistics.total_usage),
        ]

        return '\n'.join(lines)

    def _build_usage_display_table(self, individual_usages: list[IndividualUsage]) -> str:
        lines: list[str] = [
            f'{"#".center(self._number_width)}{"Username".center(self._username_width)}'
            f'{"Amount Used".center(self._amount_width)}{"Overall Percentage".center(self._percentage_width)}',
            '',
            '',
            *self._build_individual_usages(individual_usages),
            '',
            '',
        ]

        return '\n'.join(lines)

    @staticmethod
    def _build_report_header() -> str:
        lines: list[str] = [
            'MARVEL Inc.               Disk space usage by user',
            '',
            '-' * 50,
            '',
        ]

        return '\n'.join(lines)

    def _build_individual_usages(self, individual_usages: list[IndividualUsage]) -> list[str]:
        lines: list[str] = []

        for i, usage in enumerate(individual_usages):
            lines.append(
                f'{str(i + 1).center(self._number_width)}{usage.usage.username.value.center(self._username_width)}'
                f'{(str(usage.usage.usage.value) + "MB").center(self._amount_width)}'
                f'{(str(usage.overall_percentage) + "%").center(self._percentage_width)}'
            )

        return lines

    @staticmethod
    def _build_trailer(total_usage: MegabytesUnit) -> str:
        return f'Total Occupied Space: {total_usage.value}MB'
