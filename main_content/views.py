from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render_to_response
from datetime import datetime, timedelta
import httplib, urllib
import xml.etree.ElementTree as ET

# Create your views here.

def principal(request):

    usuarios = [
            {"name": "Alejandra Prieto", "id": 12108950, "hours": 0},
            {"name": "Andres del Rio", "id": 12109014, "hours": 0},
            {"name": "Luis Roca", "id": 12105586, "hours": 0},
            {"name": "Ivan David", "id": 11945700, "hours": 0},
            {"name": "Andres Pulido", "id": 12022031, "hours": 0},
            {"name": "Parzifal D'Leon", "id": 11926499, "hours": 0},
            {"name": "Yesid Ortiz", "id": 11679382, "hours": 0},
            {"name": "Luis Salinas", "id": 12011890, "hours": 0},
            {"name": "Oscar Robayo", "id": 11696911, "hours": 0},
            {"name": "Juan Torres", "id": 11915856, "hours": 0},
            {"name": "Carlos Arenas", "id": 11349307, "hours": 0},
        ]

    templ = get_template("index.html")

    #careful differentiating between HTTPConnection and HTTPSConnection
    conn = httplib.HTTPSConnection("zemogatime.basecamphq.com")
    conn.connect()
    headers = {"Authorization": "Y2FybG9zLmFyZW5hc0B6ZW1vZ2EuY29tOlJvYm90Um9jazEwNiE=", }

    current_time = datetime.now()
    the_date = current_time + timedelta(days=-1)

    #From the documentation: Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
    if current_time.weekday() == 0:
        the_date = current_time + timedelta(days=-3)

    timeFormated = the_date.strftime('%Y%m%d')

    #params = urllib.urlencode({'from': timeFormated})
    path = '/time_entries/report.xml?from=' + timeFormated
    print path
    conn.request('GET', path, {}, headers)
    response = conn.getresponse()

    print "STATUS: " + str(response.status) + " - REASON: " + response.reason

    if response.status == httplib.OK:
        print "Request succesfull!"
        #print response.read()

        xml = ET.fromstring(response.read())
        for time_entry in xml.findall('time-entry'):
            name = time_entry.find('person-name').text
            person_id = time_entry.find('person-id').text
            hours = time_entry.find('hours').text
            #print(name, person_id, hours)

            for person in usuarios:
                if str(person['id']) == person_id:
                    #print (name, person_id, hours)
                    new_hours = person['hours'] + float(hours)
                    person['hours'] = new_hours
    else:
        print "Something went wrog with the request"

    #user_names = (person['name'] for person in usuarios) #Get all the user names from a list of dictionaries

    html = templ.render({"fecha": the_date, "lista": usuarios})
    return HttpResponse(html)
