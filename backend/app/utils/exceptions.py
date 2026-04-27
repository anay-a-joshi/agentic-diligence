class DiligenceAIException(Exception):
    """Base exception for the app."""


class FilingNotFoundError(DiligenceAIException):
    pass


class AgentExecutionError(DiligenceAIException):
    pass
