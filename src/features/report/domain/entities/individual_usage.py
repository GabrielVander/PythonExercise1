import dataclasses

from src.features.report.domain.entities.user_data_usage import UserDataUsage


@dataclasses.dataclass(frozen=True, kw_only=True)
class IndividualUsage:
    usage: UserDataUsage
    overall_percentage: float
