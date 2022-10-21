from collections.abc import Generator

import decoy
import pytest

from src.features.report.domain.entities.user_data_usage import UserDataUsage
from src.features.report.domain.repository.user_usage_repository import (
    UserUsageRepositoryUnableToFetchFailure,
    UserUsageRepository,
)
from src.features.report.domain.use_cases.fetch_user_usage_use_case import (
    FetchUserUsageFailure,
    FetchUserUsageUseCase,
    NoDataFailure,
)


class TestFetchUserUsageUseCase:
    _decoy: decoy.Decoy
    _dummy_repository: UserUsageRepository
    _use_case: FetchUserUsageUseCase

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self) -> Generator[None, None, None]:
        # Set Up
        self._decoy = decoy.Decoy()
        self._dummy_repository = self._decoy.mock(cls=UserUsageRepository)
        self._use_case = FetchUserUsageUseCase(
            user_usage_repository=self._dummy_repository
        )

        yield

        # Tear Down
        self._decoy.reset()

    @pytest.mark.asyncio
    async def test_should_return_no_data_failure(self) -> None:
        self._decoy.when(
            await self._dummy_repository.fetch()
        ).then_return(UserUsageRepositoryUnableToFetchFailure())

        result: list[UserDataUsage] | FetchUserUsageFailure = await self._use_case.execute()

        assert isinstance(result, FetchUserUsageFailure)
        assert isinstance(result, NoDataFailure)

    @pytest.mark.asyncio
    async def test_should_call_repository_correctly(self) -> None:
        dummy_user_data_list: list[UserDataUsage] = self._decoy.mock(cls=list[UserDataUsage])

        self._decoy.when(
            await self._dummy_repository.fetch()
        ).then_return(dummy_user_data_list)

        result: list[UserDataUsage] | FetchUserUsageFailure = await self._use_case.execute()

        assert result is dummy_user_data_list
