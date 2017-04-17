from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render_to_response
from datetime import datetime, timedelta
import httplib, urllib
import xml.etree.ElementTree as ET

# Create your views here.

def principal(request):
    members = [
            {"name": "Alejandra Prieto", "id": 12108950, "hours": 0, "number": '310 2979521'},
            {"name": "Andres del Rio", "id": 12109014, "hours": 0, "number": '316 5536752'},
            {"name": "Ivan David", "id": 11945700, "hours": 0, "number": '311 6724936'},
            # {"name": "Andres Pulido", "id": 12022031, "hours": 0, "number": '+33 7 69016977'},
            # {"name": "Parzifal D'Leon", "id": 11926499, "hours": 0, "number": '312 4182262'},
            {"name": "Yesid Ortiz", "id": 11679382, "hours": 0, "number": '316 3458730'},
            {"name": "Luis Salinas", "id": 12011890, "hours": 0, "number": '301 3365150'},
            {"name": "Juan Torres", "id": 11915856, "hours": 0, "number": '301 4360087'},
            {"name": "Carlos Arenas", "id": 11349307, "hours": 0, "number": '314 3271566'},
        ]

    holidays = [
            datetime.strptime('20170109', '%Y%m%d'), #Epiphany
            datetime.strptime('20170320', '%Y%m%d'), #St Josephs Day
            datetime.strptime('20170413', '%Y%m%d'), #Maundy Thursday
            datetime.strptime('20170414', '%Y%m%d'), #Good Friday
            datetime.strptime('20170501', '%Y%m%d'), #Labour Day
            datetime.strptime('20170529', '%Y%m%d'), #Ascension Day
            datetime.strptime('20170619', '%Y%m%d'), #Corpus Christi
            datetime.strptime('20170626', '%Y%m%d'), #Sacred Heart
            datetime.strptime('20170703', '%Y%m%d'), #Saint Peter and Saint Paul
            datetime.strptime('20170720', '%Y%m%d'), #Declaration of Independenc
            datetime.strptime('20170807', '%Y%m%d'), #Battle of Boyaca
            datetime.strptime('20170815', '%Y%m%d'), #Assumption Day
            datetime.strptime('20171016', '%Y%m%d'), #Columbus Day
            datetime.strptime('20171106', '%Y%m%d'), #All Saints Day
            datetime.strptime('20171113', '%Y%m%d'), #Independece of Cartagena
            datetime.strptime('20171208', '%Y%m%d'), #Immaculate Conception
            datetime.strptime('20171225', '%Y%m%d'), #Christmas
        ]

    templ = get_template("index.html")

    #careful differentiating between HTTPConnection and HTTPSConnection
    conn = httplib.HTTPSConnection("zemogatime.basecamphq.com")
    conn.connect()
    headers = {"Authorization": "Y2FybG9zLmFyZW5hc0B6ZW1vZ2EuY29tOlJvYm90Um9jazEwNiE=", }

    current_time = datetime.now()

    #Check the report for the day before
    the_date = current_time + timedelta(days=-1)

    #Check if the date is monday. From the documentation: Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
    if current_time.weekday() == 0:
        the_date = current_time + timedelta(days=-3)

    #Check if the current date is a holiday
    for holiday in holidays:
        next_day_after_holiday = holiday + timedelta(days=+1)
        #If today is the same day after a holiday
        if current_time.strftime('%Y%m%d') == next_day_after_holiday.strftime('%Y%m%d'):
            if holiday.weekday() == 0:
                the_date = current_time + timedelta(days=-4) #substract -4 days if the holiday was on monday
            elif holiday.weekday() == 6:
                the_date = current_time + timedelta(days=-3) #If sunday substract to check for friday's date
            else:
                the_date = current_time + timedelta(days=-2) #substract 2 days (-1 day of the holiday -1 day for the date of the review)

    #timeFormated = the_date.strftime('%Y%m%d') #<yyyy><mm><dd>
    timeFormated = "20170412"

    #params = urllib.urlencode({'from': timeFormated})
    path = '/time_entries/report.xml?from=' + timeFormated
    print path
    conn.request('GET', path, {}, headers)
    response = conn.getresponse()

    print "STATUS: " + str(response.status) + " - REASON: " + response.reason

    if response.status == httplib.OK:
        print "SUCCESS: Request succesfull!"
        #print response.read()

        xml = ET.fromstring(response.read())
        for time_entry in xml.findall('time-entry'):
            name = time_entry.find('person-name').text
            person_id = time_entry.find('person-id').text
            hours = time_entry.find('hours').text
            #print(name, person_id, hours)

            for person in members:
                if str(person['id']) == person_id:
                    #print (name, person_id, hours)
                    new_hours = person['hours'] + float(hours)
                    person['hours'] = new_hours
    else:
        print "ERROR: Something went wrong with the request"

    #Useful to have just in case
    #user_names = (members['name'] for person in members) #Get all the user names from a list of dictionaries

    html = templ.render({"fecha": the_date, "lista": members})
    return HttpResponse(html)
