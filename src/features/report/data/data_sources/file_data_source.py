from __future__ import annotations

import dataclasses
import pathlib


class FileDataSource:
    _input_file_name: str
    _output_file_name: str
    _input_folder_path: pathlib.Path
    _output_folder_path: pathlib.Path
    _input_file_path: pathlib.Path
    _output_file_path: pathlib.Path

    def __init__(
        self,
        input_file_name: str,
        input_folder_path: pathlib.Path,
        output_file_name: str,
        output_folder_path: pathlib.Path
    ) -> None:
        self._input_file_name = input_file_name
        self._output_file_name = output_file_name
        self._input_folder_path = input_folder_path
        self._output_folder_path = output_folder_path
        self._input_file_path = self._input_folder_path.joinpath(pathlib.Path(self._input_file_name))
        self._output_file_path = self._output_folder_path.joinpath(pathlib.Path(self._output_file_name))

    async def read_user_report_file(self) -> FileDataSourceFileModel:
        content: str = ''

        with self._input_file_path.open('r', encoding='utf-8') as file:
            for line in file.read():
                content += line

        return FileDataSourceFileModel(
            extension='txt',
            name=self._input_file_name,
            content=FileDataSourceFileContent(value=content)
        )

    async def save_report_output_file(self, file_content: FileDataSourceFileContent) -> None:
        with self._output_file_path.open('w', encoding='utf-8') as file:
            file.write(file_content.value)


@dataclasses.dataclass(frozen=True, kw_only=True)
class FileDataSourceFileModel:
    name: str
    extension: str
    content: FileDataSourceFileContent


@dataclasses.dataclass(frozen=True, kw_only=True)
class FileDataSourceFileContent:
    value: str
