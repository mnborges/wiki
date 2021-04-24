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
    else: return HttpResponse("Not Found")