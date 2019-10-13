class SessionData(object):
    """Creating the singleton session object

    Arguments:
        object {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SessionData, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.long_term_forecast = dict()

    def isLongTermForecastCached(self):
        return True
