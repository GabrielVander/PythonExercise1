import dataclasses

from src.features.report.domain.entities.megabytes_unit import MegabytesUnit
from src.features.report.domain.entities.username import Username


@dataclasses.dataclass(frozen=True, kw_only=True)
class UserDataUsage:
    username: Username
    usage: MegabytesUnit
