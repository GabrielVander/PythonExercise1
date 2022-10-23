import pathlib

import pytest

from constants import PROJECT_ROOT
from src.features.report.data.data_sources.file_data_source import (
    FileDataSource,
    FileDataSourceFileContent,
    FileDataSourceFileModel,
)


class TestFileDataSource:
    _assets_directory: pathlib.Path = PROJECT_ROOT.joinpath(pathlib.Path('test/report/data/data_sources/assets'))

    @pytest.mark.asyncio
    async def test_read_user_report_file_should_read_file_correctly(self) -> None:
        data_source: FileDataSource = FileDataSource(
            input_file_name='test_users.txt',
            input_folder_path=self._assets_directory,
            output_file_name='',
            output_folder_path=pathlib.Path()
        )

        result: FileDataSourceFileModel = await data_source.read_user_report_file()

        assert result.name == 'test_users.txt'
        assert result.extension == 'txt'
        assert result.content == FileDataSourceFileContent(
            value='alexandre       456123789\n\nanderson        1245698456\n\nantonio         123456456\n\ncarlos     '
                  '     91257581\n\ncesar           987458\n\nrosemary        789456125'
        )

    @pytest.mark.asyncio
    async def test_save_report_output_file_should_save_file_correctly(self) -> None:
        expected_output_path: pathlib.Path = PROJECT_ROOT.joinpath(
            pathlib.Path(
                'test/report/data/data_sources/assets/output_test.txt'
            )
        )
        data_source: FileDataSource = FileDataSource(
            input_file_name='',
            input_folder_path=pathlib.Path(),
            output_file_name='output_test.txt',
            output_folder_path=self._assets_directory,
        )

        await data_source.save_report_output_file(FileDataSourceFileContent(value='Hello Test\n\nHello Back'))

        assert expected_output_path.exists()
        assert expected_output_path.is_file()

        with expected_output_path.open('r', encoding='utf-8') as file:
            content: str = file.read()

            assert content == 'Hello Test\n\nHello Back'
