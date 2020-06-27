import requests
import lxml.html as lh

CITIES = {'Sacramento', 'Eureka', 'Redding', 'Marysville', 'Oakland', 'San Luis Obispo', 'Fresno',
          'Los Angeles', 'San Bernardino', 'Bishop', 'Stockton', 'San Diego', 'Santa Ana', 'San', 'Santa', 'Los'}
CITIES_AB = {'San', 'Santa', 'Los'}


def scrape_caltrain_contact_page():
    result = []
    original_url = 'https://dot.ca.gov'

    url = f'{original_url}/contact-us'
    response = requests.get(url)
    doc = lh.fromstring(response.content)
    offices = doc.xpath('//tr')

    for office in range(1, len(offices)):
        each_location = {
            "office_name": None,
            "office_link": None,
            "office_address": None,
            "office_city": None,
            "office_state": None,
            "office_zip": None,
            "office_phone": None,
            "mail_address": None,
            "mail_pobox": None,
            "mail_city": None,
            "mail_state": None,
            "mail_zip": None,
            "mail_phone": None
        }
        href = offices[office].xpath(".//a/@href")
        if not href:
            break
        if len(href) == 1:
            href = original_url
        else:
            href = original_url + href[0]

        col = 0
        for data in offices[office].iterchildren():
            data = " ".join(data.text_content().split())
            data = data.split(' ')

            office_address = ''
            mail_address = ''
            mail_pobox = ''
            office_phone = ''
            mail_city = ''
            office_city = ''
            for d in range(len(data)):
                if not data[d]:
                    continue
                if data[d][-1] == ',':
                    data[d] = data[d][:-1]

                if col == 0:
                    office_name = data[0]
                    if data[1] != ':-':
                        office_name = office_name + ' ' + data[1]

                elif col == 2:
                    if data[d] in CITIES:
                        mail_city = data[d]
                    elif data[d] in CITIES_AB or mail_city and data[d] != 'CA' and data[d] != data[-1]:
                        mail_city = mail_city + ' ' + data[d]
                    if data[d] not in CITIES and data[d] != 'CA' and data[d] != data[-1] and not mail_city:
                        if data[d] == 'P.O.' or 'P.O.' in mail_pobox:
                            mail_pobox = mail_pobox + ' ' + data[d]
                        else:
                            mail_address = mail_address + ' ' + data[d]
                    if data[d] == 'CA':
                        each_location['mail_state'] = data[d]
                    if data[d] == data[-1]:
                        each_location['mail_zip'] = data[d]

                elif col == 1:
                    if data[d] in CITIES:
                        office_city = data[d]
                    elif data[d] in CITIES_AB or office_city and data[d] != 'CA' and data[d] != data[-1]:
                        office_city = office_city + ' ' + data[d]
                    if data[d] not in CITIES and data[d] != 'CA' and data[d] != data[-1] and not office_city:
                        office_address = office_address + ' ' + data[d]

                    if data[d] == 'CA':
                        each_location['office_state'] = data[d]
                    if data[d] == data[-1]:
                        each_location['office_zip'] = data[d]

                elif col == 3 and '(' in data[d] or '-' in data[d]:
                    if '(' and '-' in office_phone:
                        continue
                    office_phone = office_phone + ' ' + data[d]

                if office_address:
                    each_location['office_address'] = office_address.lstrip()
                if mail_address:
                    each_location['mail_address'] = mail_address.lstrip()
                if mail_pobox:
                    each_location['mail_pobox'] = mail_pobox.lstrip()
                if office_city:
                    each_location['office_city'] = office_city
                if mail_city:
                    each_location['mail_city'] = mail_city
                if office_phone:
                    office_phone = office_phone.lstrip()
                    for o in office_phone:
                        if o == '(' or o == ')':
                            office_phone = office_phone.replace(o, '')
                        if o == ' ':
                            office_phone = office_phone.replace(' ', '-')
                            break
                    each_location['office_phone'] = office_phone

                each_location['office_link'] = href

                each_location['office_name'] = office_name

            col += 1

        result.append(each_location)

    return result
