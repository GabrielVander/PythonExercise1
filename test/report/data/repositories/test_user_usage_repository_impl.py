import typing
from collections.abc import Generator

import decoy
import pytest

from src.features.report.data.data_sources.file_data_source import (
    FileDataSource, FileDataSourceFileContent, FileDataSourceFileModel,
)
from src.features.report.data.repositories.user_usage_repository_impl import UserUsageRepositoryImpl
from src.features.report.domain.entities.megabytes_unit import MegabytesUnit
from src.features.report.domain.entities.user_data_usage import UserDataUsage
from src.features.report.domain.entities.username import Username
from src.features.report.domain.repository.user_usage_repository import (
    UserUsageRepositoryFailure,
    UserUsageRepositoryUnableToFetchFailure,
)


class TestUserUsageRepositoryImpl:
    _decoy: decoy.Decoy
    _dummy_file_data_source: FileDataSource
    _repository: UserUsageRepositoryImpl

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self) -> Generator[None, None, None]:
        # Set Up
        self._decoy = decoy.Decoy()
        self._dummy_file_data_source = self._decoy.mock(cls=FileDataSource)
        self._repository = UserUsageRepositoryImpl(
            file_data_source=self._dummy_file_data_source
        )

        yield

        # Tear Down
        self._decoy.reset()

    # noinspection DuplicatedCode
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'file_content, expected_user_usages',
        [
            ('', []),
            ('\n\n\n\n', []),
            ('alexandre       456123789\n',
             [UserDataUsage(
                 username=Username(value='alexandre'),
                 usage=MegabytesUnit(value=434.99)
             )]),
            ('anderson        1245698456\n',
             [UserDataUsage(
                 username=Username(value='anderson'),
                 usage=MegabytesUnit(value=1187.99)
             )]),
            ('antonio        123456456\n',
             [UserDataUsage(
                 username=Username(value='antonio'),
                 usage=MegabytesUnit(value=117.74)
             )]),
            ('carlos          91257581\n',
             [UserDataUsage(
                 username=Username(value='carlos'),
                 usage=MegabytesUnit(value=87.03)
             )]),
            ('cesar           987458\n',
             [UserDataUsage(
                 username=Username(value='cesar'),
                 usage=MegabytesUnit(value=0.94)
             )]),
            ('rosemary        789456125\n',
             [UserDataUsage(
                 username=Username(value='rosemary'),
                 usage=MegabytesUnit(value=752.88)
             )]),
            ('alexandre       456123789\nanderson        1245698456\nantonio         123456456\ncarlos          '
             '91257581\ncesar           987458\nrosemary        789456125',
             [
                 UserDataUsage(
                     username=Username(value='alexandre'),
                     usage=MegabytesUnit(value=434.99)
                 ),
                 UserDataUsage(
                     username=Username(value='anderson'),
                     usage=MegabytesUnit(value=1187.99)
                 ),
                 UserDataUsage(
                     username=Username(value='antonio'),
                     usage=MegabytesUnit(value=117.74)
                 ),
                 UserDataUsage(
                     username=Username(value='carlos'),
                     usage=MegabytesUnit(value=87.03)
                 ),
                 UserDataUsage(
                     username=Username(value='cesar'),
                     usage=MegabytesUnit(value=0.94)
                 ),
                 UserDataUsage(
                     username=Username(value='rosemary'),
                     usage=MegabytesUnit(value=752.88)
                 )
             ]),
            (
                'alexandre       456123789\n\nanderson        1245698456\n\nantonio         123456456\n\ncarlos       '
                '   91257581\n\ncesar           987458\n\nrosemary        789456125',
                [
                    UserDataUsage(
                        username=Username(value='alexandre'),
                        usage=MegabytesUnit(value=434.99)
                    ),
                    UserDataUsage(
                        username=Username(value='anderson'),
                        usage=MegabytesUnit(value=1187.99)
                    ),
                    UserDataUsage(
                        username=Username(value='antonio'),
                        usage=MegabytesUnit(value=117.74)
                    ),
                    UserDataUsage(
                        username=Username(value='carlos'),
                        usage=MegabytesUnit(value=87.03)
                    ),
                    UserDataUsage(
                        username=Username(value='cesar'),
                        usage=MegabytesUnit(value=0.94)
                    ),
                    UserDataUsage(
                        username=Username(value='rosemary'),
                        usage=MegabytesUnit(value=752.88)
                    )
                ]),
        ]
    )
    async def test_should_return_correct_user_usages(
        self,
        file_content: str,
        expected_user_usages: list[UserDataUsage]
    ) -> None:
        model: FileDataSourceFileModel = self._map_content_to_file_model(file_content)

        self._decoy.when(
            await self._dummy_file_data_source.read_user_report_file()
        ).then_return(model)

        result: list[UserDataUsage] | UserUsageRepositoryFailure = await self._repository.fetch()

        assert not isinstance(result, UserUsageRepositoryFailure)
        user_usages: list[UserDataUsage] = typing.cast(list[UserDataUsage], result)
        assert user_usages == expected_user_usages

    # noinspection SpellCheckingInspection
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'file_content',
        [
            'alexandre       4a56123789\n',
            'alexandreeeeeeeeeeeeeeeeeeeeeeeeeeee       456123789\n',
            'a' * 500,
            'a' * 15,
        ]
    )
    async def test_should_return_unable_to_read_failure_if_parsing_error_occurs(self, file_content: str) -> None:
        model: FileDataSourceFileModel = self._map_content_to_file_model(file_content)

        self._decoy.when(
            await self._dummy_file_data_source.read_user_report_file()
        ).then_return(model)

        result: list[UserDataUsage] | UserUsageRepositoryFailure = await self._repository.fetch()

        assert isinstance(result, UserUsageRepositoryFailure)
        assert isinstance(result, UserUsageRepositoryUnableToFetchFailure)

    @pytest.mark.asyncio
    async def test_should_return_unable_to_read_failure_if_file_not_found_error_occurs(self) -> None:
        self._decoy.when(
            await self._dummy_file_data_source.read_user_report_file()
        ).then_raise(FileNotFoundError())

        result: list[UserDataUsage] | UserUsageRepositoryFailure = await self._repository.fetch()

        assert isinstance(result, UserUsageRepositoryFailure)
        assert isinstance(result, UserUsageRepositoryUnableToFetchFailure)

    @staticmethod
    def _map_content_to_file_model(content: str) -> FileDataSourceFileModel:
        return FileDataSourceFileModel(
            name='wisdom',
            extension='txt',
            content=FileDataSourceFileContent(value=content)
        )
