class DimensionError(Exception):
    """Raised when bad dimensions are passed"""
    pass

class ContentError(Exception):
    """Raised when cell content is bad"""
    pass

class UnitValueError(Exception):
    """Raised when a multi-char value is passed to
the unitCell class
"""
    pass
