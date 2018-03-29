class DBClientResponseError(Exception):
    """Error when trying to retrieve data from downstream database"""
    pass


class NoResultsFoundError(Exception):
    """Error when no results found"""
    pass
