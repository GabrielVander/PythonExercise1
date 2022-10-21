import dataclasses

from src.features.report.domain.entities.individual_usage import IndividualUsage
from src.features.report.domain.entities.megabytes_unit import MegabytesUnit
from src.features.report.domain.entities.user_data_usage import UserDataUsage


@dataclasses.dataclass(frozen=True, kw_only=True)
class DataUsageStatistics:
    user_usages: list[UserDataUsage]
    total_usage: MegabytesUnit = dataclasses.field(init=False, default=MegabytesUnit(value=0))
    individual_usages: list[IndividualUsage] = dataclasses.field(init=False, default_factory=list)

    def __post_init__(self):
        self._set_total_usage()
        self._set_individual_usages()

    def _set_total_usage(self):
        total_usage: int = self._calculate_total_usage()
        object.__setattr__(self, 'total_usage', MegabytesUnit(value=float(total_usage)))

    def _calculate_total_usage(self) -> int:
        total: int = 0

        for usage in self.user_usages:
            usage_as_int: int = int(usage.usage.value)

            total += usage_as_int

        return total

    def _set_individual_usages(self):
        individual_usages: list[IndividualUsage] = self._build_individual_usages()
        object.__setattr__(self, 'individual_usages', individual_usages)

    def _build_individual_usages(self):
        individual_usages: list[IndividualUsage] = []
        for user_usage in self.user_usages:
            total_usage: float = float(self.total_usage.value)
            user_usage_value: float = float(user_usage.usage.value)

            overall_percentage: float = self._calculate_overall_percentage(total_usage, user_usage_value)
            rounded_overall_percentage: float = round(overall_percentage, 2)

            individual_usages.append(
                IndividualUsage(usage=user_usage, overall_percentage=rounded_overall_percentage * 100)
            )
        return individual_usages

    @staticmethod
    def _calculate_overall_percentage(total_usage: float, user_usage_value: float) -> float:
        return user_usage_value / total_usage if total_usage != 0 else 0
