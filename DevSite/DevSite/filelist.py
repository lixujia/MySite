from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.conf import settings
import os
import time

wildcard = ["txt","pdf","odt","doc","docx","bin","hex","c","h","Makefile",
            "py","sh","png","rpm","xml","exe"]

mimetype_icon = {
    "deb":"Mimetype-deb-icon.png",
    "c":"Mimetype-source-c-icon.png",
    "cpp":"Mimetype-source-cpp-icon.png",
    "h":"Mimetype-source-h-icon.png",
    "php":"Mimetype-source-php-icon.png",
    "py":"Mimetype-source-py-snake-icon.png",
    "7z":"Mimetypes-application-7zip-icon.png",
    "cab":"Mimetypes-application-vnd.ms-cab-compressed-icon.png",
    "bz2":"Mimetypes-application-x-bzip-icon.png",
    "tar":"Mimetypes-application-x-compressed-tar-icon.png",
    "gz":"Mimetypes-application-x-gzip-icon.png",
    "jar":"Mimetypes-application-x-jar-icon.png",
    "avi":"Mimetypes-avi-icon.png",
    "bin":"Mimetypes-bin-icon.png",
    "cd":"Mimetypes-blank-cd-icon.png",
    "bmp":"Mimetypes-bmp-icon.png",
    "png":"Mimetypes-bmp-icon.png",
    "jpg":"Mimetypes-bmp-icon.png",
    "pdf":"Mimetypes-gnome-mime-application-pdf-icon.png",
    "psd":"Mimetypes-image-x-psd-icon.png",
    "js":"Mimetypes-javascript-icon.png",
    "mp3":"Mimetypes-mp-3-icon.png",
    "rar":"Mimetypes-rar-icon.png",
    "wav":"Mimetypes-sound-icon.png",
    "text":"Mimetypes-text-plain-icon.png",
    "tex":"Mimetypes-text-x-bibtex-icon.png",
    "zip":"Mimetypes-zip-icon.png",
    "iso":"Mimetypes-blank-cd-icon.png",
    "doc":"libreoffice-oasis-text.png",
    "odt":"libreoffice-oasis-text.png",
    "rpm":"Mimetypes-rpm-icon24x24.png",
    "exe":"Mimetypes-application-x-executable24x24.png",
    "docx":"libreoffice-oasis-text.png",
    "sh":"Mimetypes-application-x-executable24x24.png",
    "xml":"Mimetypes-application-xml-icon24x24.png",
    "makefile":"Mimetypes-text-x-makefile-icon.png",
    }
    
def static_file_page_itemlist(subpath):
    path = os.path.join(settings.MEDIA_ROOT,"Files",subpath)

    lst = []

    for item in os.listdir(path):
        full_path = os.path.join(path,item)

        page_item = {"filename":item}

        if os.path.isdir(full_path):
            page_item["url"] = os.path.join('/files',subpath,item)
            page_item["type"] = 0
            page_item["icon"] = os.path.join('/static','icons','folder.png')
            page_item["size"] = ' '
        else:
            page_item["url"] = os.path.join('/static','Files',subpath,item)
            suffix = item.split('.')[-1]
            if suffix in wildcard:
                page_item["type"] = wildcard.index(suffix) + 1
            else:
                page_item["type"] = len(wildcard) + 1

            try:
                page_item["icon"] = os.path.join('/static','icons',mimetype_icon[suffix.lower()])
            except:
                page_item["icon"] = '/static/icons/clipping-unknow-icon24x24.png'

            s = os.stat(full_path).st_size
            if (s > (1 << 30)):
                page_item["size"] = "{:.2f}G".format(s / (1 << 30))
            elif (s > (1 << 20)):
                page_item["size"] = "{:.2f}M".format(s / (1 << 20))
            elif (s > (1 << 10)):
                page_item["size"] = "{:.2f}K".format(s / (1 << 10))
            else:
                page_item["size"] = "{}B".format(s)
            
        lt = time.localtime(os.stat(full_path).st_mtime)
        page_item["mtime"] = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(lt[0],lt[1],lt[2],
                                                                    lt[3],lt[4],lt[5])
        
        lst.append(page_item)

    return sorted(lst,key = lambda item: (item["type"],item["filename"]))

def static_file_page_pathlist(path):
    lst = [{"url":"/files","name":"files"},]

    prefix = "/files"
    
    for seg in path.split("/"):
        if "" == seg:
            continue

        lst.append({"url":prefix + "/" + seg,
                    "name":seg})

        prefix += "/" + seg

    return lst

def static_file_page(request,url):
    item_list = static_file_page_itemlist(url)
    path_list = static_file_page_pathlist(url)
    
    t = get_template("static-file-page.html")
    c = {"title":"file:" + url,
         "filelist":item_list,
         "pathlist":path_list,
         "jquery_path":"/static/jquery-ui-1.10.3/jquery-1.9.1.js",
         "jquery_ui_path":"/static/jquery-ui-1.10.3/ui/jquery-ui.js",
         "jquery_ui_css":"/static/jquery-ui-1.10.3/themes/base/jquery-ui.css"}
        
    html = t.render(Context(c))

    return HttpResponse(html)

