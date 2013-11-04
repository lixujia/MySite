from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.conf import settings
import os

def static_file_page_itemlist(subpath):
    wildcard = ["txt","pdf","doc","docx","bin","hex","c","h","Makefile"]
    path = os.path.join(settings.STATIC_ROOT,subpath)

    lst = []

    for item in os.listdir(path):
        full_path = os.path.join(path,item)

        page_item = {"filename":item}

        if os.path.isdir(full_path):
            page_item["url"] = os.path.join('/files',subpath,item)
            page_item["type"] = 0
        else:
            page_item["url"] = os.path.join('/site_media',subpath,item)
            suffix = item.split('.')[-1]
            if suffix in wildcard:
                page_item["type"] = wildcard.index(suffix) + 1
            else:
                page_item["type"] = len(wildcard) + 1

        lst.append(page_item)

    return lst

def static_file_page(request,url):
    item_list = static_file_page_itemlist(url)

    t = get_template("static-file-page.html")
    c = {"title":"file:" + url,
         "filelist":item_list}
    html = t.render(Context(c))

    return HttpResponse(html)

