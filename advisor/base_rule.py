# =============================================================================
# File Name : advisor/base_rule.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Base Advisor Rule
#
# =============================================================================

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseRule(ABC):

    @abstractmethod
    def evaluate(
        self,
        portfolio
    ) -> list:

        """
        Returns list of recommendations.

        """

        raise NotImplementedError