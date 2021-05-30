from django.db.models import F
from .models import newstats


class DemoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.num_exception = 0
        self.context_response = {
            "msg": {'warning': 'there is no more ink in the printer'},
        }
    
    def stats(self, os_info):
        if "Windows" in os_info:
            newstats.objects.all().update(win=F('win') + 1)
        elif "mac" in os_info:
            newstats.objects.all().update(mac=F('mac') + 1)
        elif "iPhone" in os_info:
            newstats.objects.all().update(iph=F('iph') + 1)
        elif "Android" in os_info:
            newstats.objects.all().update(android=F('android') + 1)
        else:
            newstats.objects.all().update(oth=F('oth') + 1)

    def __call__(self, request):
        print("hello world")
        print(request.path)
        print(request.headers['Accept-Language'])
        if 'admin' not in request.path:
            self.stats(request.META['HTTP_USER_AGENT'])
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print(f'view name: {view_func.__name__}')
        pass

    def process_exception(self, request, exception):
        self.num_exception += 1
        print(f'Exception count: {self.num_exception}')

    def process_template_response(self, request, response):
        response.context_data["new_data"] = self.context_response
        return response