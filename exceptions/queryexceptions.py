class InvalidInputQuery(Exception):
    pass


class InvalidInputParameter(Exception):
    """Error when input query parameter does not exist"""
    pass


class InvalidInputParameterCombination(Exception):
    """Error when input query parameters collide, e.g. sort and random"""
    pass


class InvalidInputParameterValue(Exception):
    """Error when input query parameter value is invalid"""
    pass


class InvalidQueryResponse(Exception):
    pass
