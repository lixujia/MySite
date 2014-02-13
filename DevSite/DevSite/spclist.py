from django.template.loader import get_template
from django.template import Context

from django.http import HttpResponse
from DevSite.models import SavedMainInfo
from DevSite.models import SavedExternInfo

def show_man_list(request):
    record_lst = []
    
    for record in SavedMainInfo.objects.all():
        dic = {}

        dic["vendor"]  = record.vendor
        dic["product"] = record.product
        dic["sn"]      = record.sn
        dic["hver"]    = record.hver
        dic["pdate"]   = record.pdate
        dic["mac"]     = record.mac
        dic["batch"]   = record.batch  

        record_lst.append(dic)
            
    t = get_template("csv-main.html")
    c = {"title":"CSV MainInfo",
         "record_lst":record_lst}

    html = t.render(Context(c))

    return HttpResponse(html)

def show_extend_list(request):
    record_lst = []
    
    for record in SavedExternInfo.objects.all():
        dic = {}

        dic["vendor"]  = record.vendor
        dic["product"] = record.product
        dic["sn"]      = record.sn
        dic["hver"]    = record.hver
        dic["pdate"]   = record.pdate
        dic["batch"]   = record.batch  

        record_lst.append(dic)
            
    t = get_template("csv-extend.html")
    c = {"title":"CSV ExtendInfo",
         "record_lst":record_lst}

    html = t.render(Context(c))

    return HttpResponse(html)


def show_csv(request,url):
    if 'main' == url:
        return show_man_list(request)
    elif 'extend' == url:
        return show_extend_list(request)
    else:
        return HttpResponse("ERROR!")
