from django.http import JsonResponse, HttpResponseBadRequest
from . import TrieManager


def recommendations(request):
    print(request.GET)
    if "query" in request.GET:
        return JsonResponse(
            TrieManager.get_recommendations(request.GET['query'],
                                            request.GET.get('cache')))
    else:
        return HttpResponseBadRequest(
            "This is a bad request. DO NOT ATTEMPT TO CALL THE API DIRECTLY")
