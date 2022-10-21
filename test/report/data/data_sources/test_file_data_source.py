import pathlib

import pytest

from constants import PROJECT_ROOT
from src.features.report.data.data_sources.file_data_source import (
    FileDataSource,
    FileDataSourceFileContent,
    FileDataSourceFileModel,
)


class TestFileDataSource:

    @pytest.mark.asyncio
    async def test_read_user_report_file_should_read_file_correctly(self) -> None:
        data_source: FileDataSource = FileDataSource(
            input_file_name='test_users.txt',
            input_folder_path=PROJECT_ROOT.joinpath(pathlib.Path('test/report/data/data_sources/assets'))
        )

        result: FileDataSourceFileModel = await data_source.read_user_report_file()

        assert result.name == 'test_users.txt'
        assert result.extension == 'txt'
        assert result.content == FileDataSourceFileContent(
            value='alexandre       456123789\n\nanderson        1245698456\n\nantonio         123456456\n\ncarlos     '
                  '     91257581\n\ncesar           987458\n\nrosemary        789456125'
        )
