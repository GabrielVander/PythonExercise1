from collections.abc import Generator

import decoy
import pytest

from src.features.report.domain.entities.data_usage_statistics import DataUsageStatistics
from src.features.report.domain.entities.individual_usage import IndividualUsage
from src.features.report.domain.entities.megabytes_unit import MegabytesUnit
from src.features.report.domain.entities.user_data_usage import UserDataUsage
from src.features.report.domain.entities.username import Username


class TestDataUsageStatistics:
    _decoy: decoy.Decoy

    @pytest.fixture(autouse=True)
    def set_up_and_tear_down(self) -> Generator[None, None, None]:
        # Set Up
        self._decoy = decoy.Decoy()

        yield

        # Tear Down
        self._decoy.reset()

    @pytest.mark.parametrize(
        'user_usages, expected_total',
        [
            ([], MegabytesUnit(value=0)),
            ([UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=0))],
             MegabytesUnit(value=0)),
            ([UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=62))],
             MegabytesUnit(value=62)),
            ([
                 UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=62)),
                 UserDataUsage(username=Username(value='path'), usage=MegabytesUnit(value=38)),
             ],
             MegabytesUnit(value=100)),
            ([
                 UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=62)),
                 UserDataUsage(username=Username(value='path'), usage=MegabytesUnit(value=38)),
                 UserDataUsage(username=Username(value='miss'), usage=MegabytesUnit(value=900)),
             ],
             MegabytesUnit(value=1000)),
            ([
                 UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=0)),
                 UserDataUsage(username=Username(value='path'), usage=MegabytesUnit(value=0)),
                 UserDataUsage(username=Username(value='miss'), usage=MegabytesUnit(value=0)),
             ],
             MegabytesUnit(value=0)),
        ]
    )
    def test_should_set_total_usage_correctly(
        self,
        user_usages: list[UserDataUsage],
        expected_total: MegabytesUnit
    ) -> None:
        statistics: DataUsageStatistics = DataUsageStatistics(user_usages=user_usages)

        assert statistics.total_usage == expected_total

    @pytest.mark.parametrize(
        'user_usages, expected_percentages',
        [
            ([], []),
            ([UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=0))], [0]),
            ([UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=62))], [100]),
            ([
                 UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=62)),
                 UserDataUsage(username=Username(value='path'), usage=MegabytesUnit(value=38)),
             ], [62, 38]),
            ([
                 UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=62)),
                 UserDataUsage(username=Username(value='path'), usage=MegabytesUnit(value=38)),
                 UserDataUsage(username=Username(value='miss'), usage=MegabytesUnit(value=900)),
             ], [6.2, 3.8, 90]),
            ([
                 UserDataUsage(username=Username(value='breathe'), usage=MegabytesUnit(value=0)),
                 UserDataUsage(username=Username(value='path'), usage=MegabytesUnit(value=0)),
                 UserDataUsage(username=Username(value='miss'), usage=MegabytesUnit(value=0)),
             ], [0, 0, 0]),
        ]
    )
    def test_should_calculate_usage_percentages_correctly(
        self,
        user_usages: list[UserDataUsage],
        expected_percentages: list[float]
    ) -> None:
        assert len(user_usages) == len(expected_percentages)

        statistics: DataUsageStatistics = DataUsageStatistics(user_usages=user_usages)
        individual_usages: list[IndividualUsage] = statistics.individual_usages

        for i, expected_percentage in enumerate(expected_percentages):
            individual_usage: IndividualUsage = individual_usages[i]

            assert individual_usage.overall_percentage == expected_percentage
