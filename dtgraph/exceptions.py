"""
DTGraph's exception definitions.
"""

class DTGraphException(Exception):
    """Base DTGraph exception class."""

class ParseError(DTGraphException):
    """Error in rule parsing."""

class CompileError(DTGraphException):
    """Error in rule compilation."""

class RunTimeError(DTGraphException):
    """Error in rule execution."""

class RuleInitializationError(DTGraphException):
    """Error in rule initialization."""

class TransformationActivationError(DTGraphException):
    """Error in transformation activation."""

class TransformationDeactivationError(DTGraphException):
    """Error in transformation deactivation."""

class TransformationDiagnosisError(DTGraphException):
    """Error in transformation diagnosis."""