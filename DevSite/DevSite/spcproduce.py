from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from DevSite.models import MainInfo
from DevSite.models import MainInfoSn
from DevSite.models import SavedMainInfo
from DevSite.models import SavedExternInfo
import os
import time

import xml.etree.ElementTree as etree

def spc_produce_save_maininfo(xml):
    root = etree.fromstring(xml)
    main = root.find("main")
    dic = {}

    for name in ["vendorid","productid","sn","hw","producedate","mac","producebatch"]:
        item = main.find(name)
        if None != item:
            dic[name] = item.text
        else:
            dic[name] = ''

    record = SavedMainInfo.objects.filter(vendor = dic["vendorid"],
                                          product = dic["productid"],
                                          sn = dic["sn"],
                                          hver = dic["hw"],
                                          pdate = dic["producedate"],
                                          mac = dic["mac"],
                                          batch = dic["producebatch"])

    if 0 != len(record):
        return True
    else:
        record = SavedMainInfo(vendor = dic["vendorid"],  
                               product = dic["productid"],
                               sn = dic["sn"],            
                               hver = dic["hw"],          
                               pdate = dic["producedate"],
                               mac = dic["mac"],          
                               batch = dic["producebatch"])
        record.save()

        sn = dic["sn"]
        num = int(sn[8:12])

        mainsn = MainInfoSn.objects.filter(device = "mainboard")[0]
        mainsn.number = num + 1
        mainsn.save()
        
    main = MainInfo.objects.all()[0]
    main.mac += 1
    main.save()
    
    return True

def spc_produce_save_extendinfo(xml):
    root = etree.fromstring(xml)
    extend = root.find("extend")
    dic = {}
    
    for name in ["vendorid","productid","sn","hw","producedate","producebatch"]:
        item = extend.find(name)
        if None != item:
            dic[name] = item.text
        else:
            dic[name] = ''

    record = SavedExternInfo.objects.filter(vendor = dic["vendorid"],
                                          product = dic["productid"],
                                          sn = dic["sn"],
                                          hver = dic["hw"],
                                          pdate = dic["producedate"],
                                          batch = dic["producebatch"])

    if 0 != len(record):
        return True
    else:
        record = SavedExternInfo(vendor = dic["vendorid"],  
                               product = dic["productid"],
                               sn = dic["sn"],            
                               hver = dic["hw"],          
                               pdate = dic["producedate"],
                               batch = dic["producebatch"])
        record.save()

        sn = dic["sn"]
        num = int(sn[8:12])

        mainsn = MainInfoSn.objects.filter(device = "extendboard")[0]
        mainsn.number = num + 1
        mainsn.save()
        
    return True

        
def spc_produce_post(xml):
    root = etree.fromstring(xml)

    cmd = root.find('cmd')
    if None == cmd:
        return False

    if "setmaininfo" == cmd.text.strip():
        main = root.find('main')
        if None == main:
            return False
        
        return spc_produce_save_maininfo(xml)
    elif "setextendinfo" == cmd.text.strip():
        extend = root.find('extend')
        if None == extend:
            return False

        return spc_produce_save_extendinfo(xml)
    else:
        return False

def sn_calculate_check(sn):
    if 12 != len(sn):
        return None

    bmap = sn.encode("utf-8")

    c2 = bmap[0] + bmap[2] + bmap[4] + bmap[6] + bmap[8] + bmap[10]
    c1 = (bmap[1] + bmap[3] + bmap[5] + bmap[7] + bmap[9] + bmap[11]) * 3
    c3 = (c1 + c2) % 10

    return "{}".format((10 - c3) % 10)
    
def spc_produce_get(request):
    main = MainInfo.objects.all()[0]

    vendor,product,hver,batch = main.vendor,main.product,main.hver,main.batch
    mac = "6e:80:{:02x}:{:02x}:{:02x}:{:02x}".format((main.mac >> 24) & 0xFF,
                                                     (main.mac >> 16) & 0xFF,
                                                     (main.mac >> 8)  & 0xFF,
                                                     (main.mac + 1)       & 0xFF)

    lt = time.localtime()

    mainsnobj = MainInfoSn.objects.get(device = "mainboard")
    extendsnobj = MainInfoSn.objects.get(device = "extendboard")

    sn = "20204501{:04d}".format(mainsnobj.number)
    mainsn = sn + sn_calculate_check(sn)
    sn = "20204601{:04d}".format(extendsnobj.number)
    extendsn = sn + sn_calculate_check(sn)
    
    timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(lt.tm_year,lt.tm_mon,lt.tm_mday,
                                                            lt.tm_hour,lt.tm_min,lt.tm_sec)
    maininfo = '''
<spc>
  <cmd>setmaininfo</cmd>
  <main>
    <vendorid>{vendor}</vendorid>
    <productid>{product}</productid>
    <sn>{sn}</sn>
    <hw>{hver}</hw>
    <producedate>{time}</producedate>
    <producebatch>{batch}</producebatch>
    <mac>{mac}</mac>
  </main>
</spc>'''.format(vendor = vendor,product = product,
                 sn = mainsn,hver = hver,
                 time = timestamp,batch = batch,
                 mac = mac)

    extendinfo = '''
<spc>
  <cmd>setextendinfo</cmd>
  <extend>
    <vendorid>{vendor}</vendorid>
    <productid>{product}</productid>
    <sn>{sn}</sn>
    <hw>{hver}</hw>
    <producedate>{time}</producedate>
    <producebatch>{batch}</producebatch>
  </extend>
</spc>'''.format(vendor = vendor,product = product,sn = extendsn,hver = hver,
                 time = timestamp,batch = batch)
        
    t = get_template("xml-display.html")
    c = {"title":"maininfo",
         "main_xml":maininfo,
         "extend_xml":extendinfo}
        
    html = t.render(Context(c))
    
    return HttpResponse(html)

def spc_produce_post(request):
    main_xml = request.POST.get("main")
    extend_xml = request.POST.get("extend")

    ret1 = spc_produce_save_maininfo(main_xml)
    ret2 = spc_produce_save_extendinfo(extend_xml)

    if ret1 and ret2:
        return HttpResponse("OK!")
    else:
        return HttpResponse("Failure!")
    

def spc_produce(request):
    if request.method == 'POST':
        return spc_produce_post(request)
    else:
        return spc_produce_get(request)

def hwt_produce_xml():
    main = MainInfo.objects.all()[0]

    vendor,product,hver,batch = main.vendor,main.product,main.hver,main.batch
    mac = "6e:80:{:02x}:{:02x}:{:02x}:{:02x}".format((main.mac >> 24) & 0xFF,
                                                     (main.mac >> 16) & 0xFF,
                                                     (main.mac >> 8)  & 0xFF,
                                                     (main.mac + 1)       & 0xFF)

    lt = time.localtime()

    mainsnobj = MainInfoSn.objects.get(device = "mainboard")
    extendsnobj = MainInfoSn.objects.get(device = "extendboard")

    sn = "20204501{:04d}".format(mainsnobj.number)
    mainsn = sn + sn_calculate_check(sn)
    sn = "20204601{:04d}".format(extendsnobj.number)
    extendsn = sn + sn_calculate_check(sn)
    
    timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(lt.tm_year,lt.tm_mon,
                                                                   lt.tm_mday,lt.tm_hour,
                                                                   lt.tm_min,lt.tm_sec)
    iedinfo = '''<?xml version="1.0" encoding="utf-8"?>
<ied>
  <main>
    <mac>{mac}</mac>
    <vendorid>{vendor}</vendorid>
    <productid>{product}</productid>
    <sn>{mainsn}</sn>
    <hw>{hver}</hw>
    <producedate>{time}</producedate>
    <producebatch>{batch}</producebatch>
  </main>
  <extend>
    <vendorid>{vendor}</vendorid>
    <productid>{product}</productid>
    <sn>{extendsn}</sn>
    <hw>{hver}</hw>
    <producedate>{time}</producedate>
    <producebatch>{batch}</producebatch>
  </extend>
</ied>
'''.format(vendor = vendor,product = product,
           mainsn = mainsn,hver = hver,
           time = timestamp,batch = batch,
           mac = mac,extendsn = extendsn)
    
    return iedinfo
    
def hwt_produce_get(request):
    iedinfo = hwt_produce_xml()
    
    t = get_template("hwtproduce.html")
    c = {"title":"HWT IED info",
         "ied_info":iedinfo}
        
    html = t.render(Context(c))
    
    return HttpResponse(html)

def hwt_produce_post(request):
    xml = request.POST.get("main")

    ret1 = spc_produce_save_maininfo(xml)
    ret2 = spc_produce_save_extendinfo(xml)

    if ret1 and ret2:
        return HttpResponse("OK!")
    else:
        return HttpResponse("Failure!")

        
def hwt_produce(request):
    if request.method == "POST":
        return hwt_produce_post(request)
    else:
        return hwt_produce_get(request)
    

def hwt_ied_info_xml(request):
    if request.method == "POST":
        return HttpResponse("OK")

    iedinfo = hwt_produce_xml()
    return HttpResponse(iedinfo)
