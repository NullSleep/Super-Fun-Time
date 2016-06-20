from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
import httplib, urllib

# Create your views here.

usuarios = [
    "Alejandra Prieto",
    "Andre del Rio",
    "Ivan David",
    "Andres Pulido",
    "Parzifal D'Leon",
    "Yesid Ortiz",
    "Luis Salinas",
    "Oscar Robayo",
    "Juan Torres",
    "Carlos Arenas",
    ]

def principal(request):
    templ = get_template("index.html")

    #careful differentiating between HTTPConnection and HTTPSConnection
    conn = httplib.HTTPSConnection("zemogatime.basecamphq.com")
    conn.connect()
    headers = {"Authorization": "Y2FybG9zLmFyZW5hc0B6ZW1vZ2EuY29tOlJvYm90Um9jazEwNiE=", }
    params = urllib.urlencode({'from': 20160405, 'to': 20160405})
    conn.request('GET', '/time_entries/report.xml?=', params, headers)

    response = conn.getresponse()

    print response.status
    print response.reason

    if response.status == httplib.OK:
        print response.read()
    else:
        print "Something went wrong"


    c = Context({"lista": usuarios})
    html = templ.render(c)
    return HttpResponse(html)
