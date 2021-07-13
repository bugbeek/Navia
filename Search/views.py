from django.db import models
from django.db.models.base import Model
from django.shortcuts import render
from .models import Medicine
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity,TrigramDistance
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models.functions import Greatest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



#using caching 
CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)



def home(request):
    """
    This is the default view.
    """

    return render(request,'home.html')


def getdetails(query = None):
    """
    Search algorithms to find results
    """
    if query:

        print("################## DATA COMING FROM DB ############################")

        #search vector with weight to different models
        vector = SearchVector('sku_name', weight='A') + SearchVector('manufacturer_name', weight='B') + SearchVector('salt_name', weight='C')

        new_query = SearchQuery(query)

        #ranking our results 
        details = Medicine.objects.annotate(rank=SearchRank(vector, new_query,weights=[0.2, 0.4, 0.6, 1])
        ).filter(rank__gte=0.3)


        if (not(details)):
                temp = True
                split_query = query.split(' ')
                print(split_query)
                print("in if")
                for i in split_query:
                    sku = Medicine.objects.filter(Q(sku_name__icontains = i))
                    manufacturer = Medicine.objects.filter(Q(manufacturer_name__icontains = i)) 
                    salt = Medicine.objects.filter(Q(salt_name__icontains = i))
                    details=  sku.union(salt,manufacturer)



    else:
        details = Medicine.objects.all()

    return details


def search(request):
    """
    search results view
    """
    query = request.GET['query']
    if cache.get(query):
        print("######### DATA COMING FROM CACHE ##################")
        details = cache.get(query)
    else:
        if query:
            details = getdetails(query)
            cache.set(query, details)
        else:
            details = getdetails()

    #pagination        
    page = request.GET.get('page',1)
    paginator = Paginator(details, 10) # 6 posts per page
    

    try:
        alldetails = paginator.page(page)
    except PageNotAnInteger:
        alldetails = paginator.page(1)
    except EmptyPage:
        alldetails = paginator.page(paginator.num_pages)

    context = {'alldetails': alldetails, 'query': query}
    return render(request, 'search.html' , context)