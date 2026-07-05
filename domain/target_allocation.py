# =============================================================================
# File Name : domain/target_allocation.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Target Allocation Model
#
# Represents the desired portfolio allocation.
#
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TargetAllocation:

    allocations: dict[str, float] = field(default_factory=dict)

    tolerance: float = 5.0

    # -------------------------------------------------------------------------
    # Total Allocation
    # -------------------------------------------------------------------------

    @property
    def total(self) -> float:

        return round(

            sum(

                self.allocations.values()

            ),

            2

        )

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    def validate(self) -> bool:

        return abs(self.total - 100.0) <= 0.01

    # -------------------------------------------------------------------------
    # Target
    # -------------------------------------------------------------------------

    def target_for(

        self,

        asset: str

    ) -> float:

        return self.allocations.get(

            asset,

            0.0

        )