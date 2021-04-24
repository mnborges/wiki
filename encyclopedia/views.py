import re
from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def item(request, title):
    if(util.get_entry(title)):
        return render(request, "encyclopedia/item.html", {
            "title": title,
            "item": util.get_entry(title)
        })
    else: return HttpResponse("Not Found.......")

def search(request):
    q = request.GET["q"]
    if(util.get_entry(q)):
        return item(request,q)
    else: 
        s = r'.*'+q+r'.*'
        all = '\n'.join(util.list_entries())
        result = re.findall(s,all,re.I)
        return render(request,"encyclopedia/search.html", {
            "term": q,
            "entries": result
        })