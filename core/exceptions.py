from __future__ import annotations


class PortfolioException(Exception):
    """Base exception."""


class ValidationError(PortfolioException):
    """Validation failed."""


class DatabaseError(PortfolioException):
    """Database operation failed."""


class RepositoryError(PortfolioException):
    """Repository operation failed."""


class ServiceError(PortfolioException):
    """Service operation failed."""


class NAVNotFoundError(PortfolioException):
    """NAV not available."""


class BenchmarkNotFoundError(PortfolioException):
    """Benchmark not found."""


class DuplicateInvestmentError(PortfolioException):
    """Duplicate investment detected."""


class InvalidTransactionError(PortfolioException):
    """Invalid transaction."""


class FundNotFoundError(PortfolioException):
    """Fund not found."""


class ConfigurationError(PortfolioException):
    """Configuration error."""


class APIError(PortfolioException):
    """External API failure."""