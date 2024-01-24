"""
DTGraph's exception definitions.
"""

class DTGraphException(Exception):
    """Base DTGraph exceptions class."""

class ParseError(DTGraphException):
    """Errors in rule parsing."""

class CompileError(DTGraphException):
    """Errors in rule compilation."""

class RunTimeError(DTGraphException):
    """Errors in rule execution."""