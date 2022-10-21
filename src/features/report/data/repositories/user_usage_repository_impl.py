from src.features.report.data.data_sources.file_data_source import FileDataSource, FileDataSourceFileModel
from src.features.report.domain.entities.megabytes_unit import MegabytesUnit
from src.features.report.domain.entities.user_data_usage import UserDataUsage
from src.features.report.domain.entities.username import Username
from src.features.report.domain.repository.user_usage_repository import (
    UserUsageRepository,
    UserUsageRepositoryFailure,
    UserUsageRepositoryUnableToFetchFailure,
)


class UserUsageRepositoryImpl(UserUsageRepository):
    _file_data_source: FileDataSource

    def __init__(self, file_data_source: FileDataSource) -> None:
        self._file_data_source = file_data_source

    async def fetch(self) -> list[UserDataUsage] | UserUsageRepositoryFailure:
        try:
            return await self._fetch_from_file()
        except (ValueError, FileNotFoundError):
            return UserUsageRepositoryUnableToFetchFailure()

    async def _fetch_from_file(self):
        result: FileDataSourceFileModel = await self._file_data_source.read_user_report_file()
        user_usages: list[UserDataUsage] = self._parse_content(result)

        return user_usages

    def _parse_content(self, result: FileDataSourceFileModel) -> list[UserDataUsage]:
        user_usages: list[UserDataUsage] = []

        for line in result.content.value.split('\n'):
            if len(line) <= 14:
                continue

            user_usages.append(self._as_user_data_usage(line))

        return user_usages

    def _as_user_data_usage(self, line: str) -> UserDataUsage:
        return UserDataUsage(
            username=self._as_username(line[:14]), usage=self._as_megabytes(
                line[15:]
            )
        )

    def _as_megabytes(self, bytes_str: str) -> MegabytesUnit:
        conversion_constant: int = 1048576

        bytes_as_float: float = float(bytes_str)
        precise_megabytes_value: float = bytes_as_float / conversion_constant
        megabytes_value_up_to_two_decimals: float = self._to_two_decimals(precise_megabytes_value)

        return MegabytesUnit(value=megabytes_value_up_to_two_decimals)

    @staticmethod
    def _as_username(username_str: str) -> Username:
        stripped_username: str = username_str.strip()

        return Username(value=stripped_username)

    @staticmethod
    def _to_two_decimals(value: float) -> float:
        # value_as_str_with_two_decimals = f'{value:.2f}'
        #
        # return float(value_as_str_with_two_decimals)

        return round(value, 2)
