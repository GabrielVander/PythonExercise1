from collections.abc import Generator

import decoy
import pytest

from src.features.report.data.data_sources.file_data_source import FileDataSource, FileDataSourceFileContent
from src.features.report.data.repositories.statistics_repository_impl import StatisticsRepositoryImpl
from src.features.report.domain.entities.data_usage_statistics import DataUsageStatistics
from src.features.report.domain.entities.megabytes_unit import MegabytesUnit
from src.features.report.domain.entities.user_data_usage import UserDataUsage
from src.features.report.domain.entities.username import Username


class TestStatisticsRepositoryImpl:
    _decoy: decoy.Decoy
    _dummy_file_data_source: FileDataSource
    _repository: StatisticsRepositoryImpl

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self) -> Generator[None, None, None]:
        # Set Up
        self._decoy = decoy.Decoy()
        self._dummy_file_data_source = self._decoy.mock(cls=FileDataSource)
        self._repository = StatisticsRepositoryImpl(
            file_data_source=self._dummy_file_data_source
        )

        yield

        # Tear Down
        self._decoy.reset()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'statistics, expected_non_static_lines',
        [
            (DataUsageStatistics(user_usages=[]), ['Total Occupied Space: 0.0MB']),
            (DataUsageStatistics(
                user_usages=[UserDataUsage(
                    username=Username(value='screw'), usage=MegabytesUnit(
                        value=738.59
                    )
                )]
            ), ['1', 'screw', '738.59MB', '100.0%', 'Total Occupied Space: 738.59MB']),
        ]
    )
    async def test_should_build_file_content_correctly(
        self,
        statistics: DataUsageStatistics,
        expected_non_static_lines: list[str]
    ) -> None:
        file_content_captor = decoy.matchers.Captor()

        await self._repository.save(statistics)

        self._decoy.verify(
            await self._dummy_file_data_source.save_report_output_file(file_content_captor)
        )

        file_content: FileDataSourceFileContent = file_content_captor.value
        raw_content: str = file_content.value

        assert 'MARVEL Inc.' in raw_content
        assert 'Disk space usage by user' in raw_content
        assert '#' in raw_content
        assert 'Username' in raw_content
        assert 'Amount Used' in raw_content
        assert 'Overall Percentage' in raw_content

        for line in expected_non_static_lines:
            assert line in raw_content
