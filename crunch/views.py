from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from dataop import get_city_wise_acquisition_rate_of_a_category
import json

def get_health_by_category():
    pass

@csrf_exempt
def get_by_category(request):
    if request.method == 'GET':
        cat = request.GET['cat']
        print cat
        rdict = get_city_wise_acquisition_rate_of_a_category(cat)
        # print rdict
        rdict = json.dumps(rdict)
        print rdict
        return JsonResponse('')

def index(request):
    return redirect("/view-by-category/")

def view_by_location(request):
    return render(request, 'crunch/location.html', {
            'foo': 'bar',
        })

def view_by_category(request):
    return render(request, 'crunch/category.html', {
            'foo': 'bar',
        })