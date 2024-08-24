from datetime import datetime

from django.http import HttpRequest, HttpResponse


def set_useragent_on_request_middleware(get_response):
    print("initial call")

    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware


class LimitRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_request = dict()

    def __call__(self, request: HttpRequest):
        ip_address = request.META["REMOTE_ADDR"]
        prev_time = self.last_request.get(ip_address)

        if prev_time:

            if datetime.now().timestamp() - prev_time < 3:
                self.last_request[ip_address] = datetime.now().timestamp()
                message = "Превышен лимит на количество запросов!"
                return HttpResponse(message, status=409)

        self.last_request[ip_address] = datetime.now().timestamp()
        return self.get_response(request)
