from mfl_response import MFLLoginResponse, MFLRostersResponse, MFLPlayersResponse, MFLLeagueResponse, MFLLiveScoringResponse, MFLPlayerScoresResponse
import requests

### MFLRequest ###############################################################

class MFLRequestUrl:
    """A non-data descriptor that returns a formatted MFL login request URL string"""
    def __get__(self, obj, type):
        if obj.request_base_type == "login":
            host = "api.myfantasyleague.com"
        else:
            host = obj.host
        return f"{obj.protocol}://{host}/{obj.default_year}/{obj.request_base_type}" 

class MFLRequest:
    """Class to manage MFL requests""" 
    protocol=""
    host=""
    default_year=""
    user_cookie=""
    request_url = MFLRequestUrl()

    def make_request(self):
        print(self.request_url)
        print(self.request_params)
        return requests.post(url=self.request_url, data=self.request_params, cookies={'MFL_USER_ID' : self.user_cookie})

##############################################################################

#### MFLExportRequest ########################################################

class MFLExportRequest(MFLRequest):
    """Class to manage MFL export requests"""
    request_base_type = "export"
    pass

##############################################################################

#### MFLRostersRequest #######################################################

class MFLRostersRequestParams:
    """A non-data descriptor that returns MFL rosters request params as a dictionary"""
    def __get__(self, obj, type):
        params = {'TYPE' : obj.request_type, 'L' : obj.league_id}
        if obj.franchise is not None:
            params['FRANCHISE'] = obj.franchise
        if obj.week is not None:
            params['W'] = obj.week
        params['JSON'] = obj.json
        return params

class MFLRostersRequest(MFLExportRequest):
    """Class to manage MFL rosters request"""
    request_type = "rosters"
    request_params = MFLRostersRequestParams()

    def __init__(self, league_id: str, franchise: str=None, week: int=None):
        self.league_id = league_id
        self.franchise = franchise
        self.week = week
        self.json = 1

    def make_request(self):
        response = super().make_request()
        return MFLRostersResponse(response)

##############################################################################

#### MFLPlayersRequest #######################################################

class MFLPlayersRequestParams:
    """A non-data descriptor that returns MFL players request params as a dictionary"""
    def __get__(self, obj, type):
        params = {'TYPE' : obj.request_type}
        if obj.league_id is not None:
            params['L'] = obj.league_id
        if obj.details:
            params['DETAILS'] = 1
        if obj.since is not None:
            params['SINCE'] = obj.since
        if obj.players is not None:
            params['PLAYERS'] = obj.players
        params['JSON'] = obj.json
        return params

class MFLPlayersRequest(MFLExportRequest):
    """Class to manage MFL players request"""
    request_type = "players"
    request_params = MFLPlayersRequestParams()

    def __init__(self, league_id: str=None, details: bool=False, since: int=None, players: str=None):
        self.league_id = league_id
        self.details = details
        self.since = since
        self.players = players
        self.json = 1

    def make_request(self):
        response = super().make_request()
        return MFLPlayersResponse(response)

##############################################################################

#### MFLLeagueRequest ########################################################

class MFLLeagueRequestParams:
    """A non-data descriptor that returns MFL league request params as a dictionary"""
    def __get__(self, obj, type):
        params = {'TYPE' : obj.request_type, 'L' : obj.league_id, 'JSON' : obj.json}
        return params

class MFLLeagueRequest(MFLExportRequest):
    """Class to manage MFL league request"""
    request_type = "league"
    request_params = MFLLeagueRequestParams()

    def __init__(self, league_id: str):
        self.league_id = league_id
        self.json = 1

    def make_request(self):
        response = super().make_request()
        return MFLLeagueResponse(response)

##############################################################################

#### MFLLiveScoringRequest ###################################################

class MFLLiveScoringRequestParams:
    """A non-data descriptor that returns MFL live scoring request params as a dictionary"""
    def __get__(self, obj, type):
        params = {'TYPE' : obj.request_type, 'L' : obj.league_id}
        if obj.week is not None:
            params['W'] = obj.week
        if obj.details:
            params['DETAILS'] = 1
        params['JSON'] = obj.json
        return params

class MFLLiveScoringRequest(MFLExportRequest):
    """Class to manage MFL live scoring request"""
    request_type = "liveScoring"
    request_params = MFLLiveScoringRequestParams()

    def __init__(self, league_id: str, week: int=None, details: bool=False):
        self.league_id = league_id
        self.week = week
        self.details = details
        self.json = 1

    def make_request(self):
        response = super().make_request()
        return MFLLiveScoringResponse(response)

##############################################################################

#### MFLPlayerScoresRequest ##################################################

class MFLPlayerScoresRequestParams:
    """A non-data descriptor that returns MFL player scores request params as a dictionary"""
    def __get__(self, obj, type):
        params = {'TYPE' : obj.request_type, 'L' : obj.league_id}
        if obj.week is not None:
            params['W'] = obj.week
        #if obj.year is not None:
        #    params['YEAR'] = obj.year
        if obj.players is not None:
            params['PLAYERS'] = obj.players
        if obj.status is not None:
            params['STATUS'] = obj.status
        if obj.rules:
            params['RULES'] = 1
        if obj.count is not None:
            params['COUNT'] = obj.count
        params['JSON'] = obj.json
        return params

class MFLPlayerScoresRequest(MFLExportRequest):
    """Class to manage MFL player scores request"""
    request_type = "playerScores"
    request_params = MFLPlayerScoresRequestParams()

    def __init__(self, league_id: str, week: int=None, year: int=None, players: str=None, status: str=None, rules: bool=False, count: int=None):
        self.league_id = league_id
        self.week = week
        self.year = year # TO DO ignored, MFLRequest.default_year always used
        self.players = players
        self.status = status
        self.rules = rules
        self.count = count
        self.json = 1

    def make_request(self):
        response = super().make_request()
        return MFLPlayerScoresResponse(response)

##############################################################################

### MFLLoginRequest ##########################################################

class MFLLoginRequestParams:
    """A non-data descriptor that returns MFL login request params as a dictionary"""
    def __get__(self, obj, type):
        return {'USERNAME' : obj.username, 'PASSWORD' : obj.password, 'XML' : 1}

class MFLLoginRequest(MFLRequest):
    """Class to manage MFL login requests"""
    request_base_type = "login"
    request_params = MFLLoginRequestParams()

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def make_request(self):
        response = super().make_request()
        return MFLLoginResponse(response)

##############################################################################

