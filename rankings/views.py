from logging import getLogger

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse

import simplejson as json

from models import Score

LOGGER = getLogger('rankings.views')


@csrf_exempt
@require_http_methods(["GET", "POST"])
def handle_ranking_request(request):
    """
    Dispatcher for passing POST requests to updating handler
    and GET requests to retrieving handler.

    See handle_update for GET parameters and
    retrieve_ranking for POST parameters.
    """
    if request.method == 'POST':
        return handle_update(request)
    return retrieve_ranking(request)


def handle_update(request):
    """
    Creates new score record if no record for given username and metric exists,
    updates the value of the existing record otherwise.

    POST-Parameters:
        score data consisting of:
        - username: player ID, required
        - metric: score category name, requried
        - value: decimal score, will be stored with 5 digits precision, max length is 15 digits, required

    Returns:
        - 200 and 'score created'/'score updated'
        - 400 when invalid request
    """
    if not is_valid_update_request(request):
        LOGGER.error('Invalid update request with parameters %s', request.POST)
        return HttpResponseBadRequest()

    parameters = request.POST.dict()
    value = parameters.pop('value')
    key = parameters
    created = Score.update_or_create(value=value, **key)
    response_text = 'score ' + ('created' if created else 'updated')
    return HttpResponse(response_text)


def is_valid_update_request(request):
    if request.method != 'POST':
        return False
    if set(request.POST.keys()) != set(['username', 'metric', 'value']):
        return False
    try:
        float(request.POST['value'])
    except ValueError:
        return False
    return True


def retrieve_ranking(request):
    """
    Retrieves top x score records matching given parameters.

    GET-Parameters:
        - username: player ID, optional
        - metric: score category name, optional
        - limit: integer, max number of records to be returned, optional
                 defaults to 0 if not provided,
                 for 0 all matching score records are retrieved,
                 for negative limit, last 'limit' matching records are excluded

    Returns:
        - 200 and json with list of top 'limit' score records ordered by value, e.g.:
            'metric=metric1&limit=2' returns '[["username3", "metric1", 10], ["username1", "metric1", 3.5]]'
            'username=uid1' returns all scores for 'uid1': '[["uid1", "metric1", 3.5], ["uid1", "metric2", 0], ...]'
        - 400 when invalid request
    """
    if not is_valid_retrieve_request(request):
        LOGGER.error('Invalid retrieve request with parameters: %s', request.GET)
        return HttpResponseBadRequest()

    parameters = request.GET.dict()
    limit = int(parameters.pop('limit', 0))
    key = parameters
    ranking = Score.filter(limit=limit, **key)
    serialized_ranking = list(ranking.values_list('username', 'metric', 'value'))
    response_content = json.dumps(serialized_ranking, use_decimal=True)
    return HttpResponse(response_content)


def is_valid_retrieve_request(request):
    if request.method != 'GET':
        return False
    if len(set(request.GET.keys()) - set(['username', 'metric', 'limit'])):
        return False
    if 'limit' in request.GET:
        value = request.GET['limit']
        try:
            int(value)
        except ValueError:
            return False
    return True
