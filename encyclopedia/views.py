from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random
import re

markdowner = Markdown()
def convertToMarkdown(title):
    content=util.get_entry(title)
    if content==None:
        return None
    else:

        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request, title):
    content =convertToMarkdown(title)
    if content is None:
        # If the content is not found, render the error page with the title
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "message": "Error, The requested page was not found."
        })
    else:
        # If the content is found, render the entry page with the content
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
def search(request):
    query = request.POST.get('q')
    if query is None or query == '':
        # No query provided
        return render(request, "encyclopedia/error.html", {
            "message": "No query provided."
        })
    elif util.get_entry(query) is not None and request.method == "POST":
        # Exact match found
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": convertToMarkdown(query)
        })
    elif request.method == "POST":
        # Partial matches
        sub_query = []
        all_entries = util.list_entries()
        for entry in all_entries:
            if query.lower() in entry.lower():
                sub_query.append(entry)
        if sub_query:
            return render(request, "encyclopedia/sub_search.html", {
                "sub_query": sub_query
            })
        else:
            # No matches found
            return render(request, "encyclopedia/error.html", {
                "message": "No title or entry found matching the query."
            })

    else:
        print("no title or entry found.")
        return render(request, "encyclopedia/error.html", {
            "massage": "no title or entry found."
        })
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        titleexist=util.get_entry(title)
        if titleexist is None:
            content=("#"+title+"\n"+content)
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": convertToMarkdown(title)
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "title": title,
                "massage": "Error, The requested page already exists."
            })
        
        
def randm(request):
    title = random.choice(util.list_entries())
    
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": convertToMarkdown(title)
        })
def edit(request):
    if request.method == "POST":
        title = request.POST.get('entry_title')
        content=convertToMarkdown(title)

       
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
def save_edit(request):
    if request.method=="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": convertToMarkdown(title)
        })
    
            
        
   