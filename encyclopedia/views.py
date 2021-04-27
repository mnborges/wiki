import re
import random
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from . import util
import markdown2


#index page with list of all existing entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
#view for individual encyclopedia entries
def item(request, title):
    if(util.get_entry(title)):
        item = (util.get_entry(title))
        return render(request, "encyclopedia/item.html", {
            "title": title,
            "item": item
        })
    else: #ERROR CODE_0 page does not exist
        return render(request, "encyclopedia/error.html", {
            "error_code": '0'
        })
    
#function to return search results
def search(request):
    q = request.GET["q"] #receives the term the user searched for
    if(util.get_entry(q)): #if query matches a existing entry, user is taken to the entry page
        return item(request,q)
    else: 
        s = r'.*'+q+r'.*' #regular expression pattern to be searched in each existing entry, pattern matches words that have the user input
        all = '\n'.join(util.list_entries()) #create a unique string with all the existing words separated by newline
        result = re.findall(s,all,re.I) #get a list with every word the regex pattern matched in the string with entries - re.I case makes it case insensitive 
        return render(request,"encyclopedia/search.html", { #render search page with query and list of results
            "term": q, 
            "entries": result
        })
#view to add new entries to the encyclopedia, newpage.html has textareas for title and content
def newpage (request):
    if request.method=="POST": #if the request method is POST it means the user pressed the submit button with the filled form
        title = request.POST["title"] #user input for the title of the page
        content = request.POST["content"] #user input for the content of the page
        if util.get_entry(title): #checks if the title already exists in the wiki
            return render(request, "encyclopedia/error.html", {
                "existing_page": title,
                "error_code": '1'
            })
        else:
            util.save_entry(title,content)
            return item(request,title) #redirects user to the page created
    return render(request, "encyclopedia/newpage.html",{#request method is GET, meaning the user clicked a link to create a new page
        "page_title": '', #textareas for the title and content are blank so the user can fill the and submit the form to create a new page
        "page_content": '',
        "page_url": "newpage"
    })
#view to edit an existing term in the wiki
def edit(request, title):
    if request.method=="POST":
        new_content = request.POST["content"] #user input for the content of the page
        util.save_entry(title,new_content) 
        """
            ADD SOME SERVER-SIDE VALIDATION
        """
        return item(request,title)
    else:
        if(util.get_entry(title)): #checks if the term exists in the wiki
            return render(request, "encyclopedia/newpage.html",{ #renders the same page used to submit a new entry
                "page_title": title, #but pre-populates the textareas with the title and content of the entry the user wants to edit
                "page_content": util.get_entry(title),
                "page_url": "edit"
            })
        else: 
            return render(request, "encyclopedia/error.html", {
                "error_code": '2'
            })
def randpage(request):
    return item(request,random.choice(util.list_entries())) #returns random item from the entries' list
    
