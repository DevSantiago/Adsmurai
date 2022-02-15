import csv
import time
from datetime import datetime
from hashlib import sha256
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.api import FacebookAdsApi

def main(pixel_id, access_token):

    FacebookAdsApi.init(access_token=access_token)

    # Se lee el archivo, desde la segunda fila; teniendo en cuenta que la primer fila es el encabezado del csv. 
    # Se toma la fecha actual vs la fecha del evento.
    # Se resta la fecha actual - la fecha del evento. Esta arroja la diferencia entre días. Si es mayor a 7 o está entre 0 y 7 días, subirá la conversión.
    # Arroja la cantidad de filas o registros que no subió en caso que no esté dentro del rango de 7 días.
    # Se hashean cada uno de los campos que pide la API de Facebook.
    with open('/home/santiago/Documents/Adsmurai/example_Solutions - example_events_file - example_events_file.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        counter = 0
        counter_not_upload = 0
        time_today = datetime.today().strftime('%Y-%m-%d')
        time_today_timestamp = time.mktime(datetime.strptime(time_today, '%Y-%m-%d').timetuple())
        for row in csv_reader:
            if counter != 0:
                email1 = sha256(row[0].encode('utf-8')).hexdigest()
                email2 = sha256(row[1].encode('utf-8')).hexdigest()
                email3 = sha256(row[2].encode('utf-8')).hexdigest()
                phone = sha256(row[3].encode('utf-8')).hexdigest()
                madid = row[4]
                name = sha256(row[5].encode('utf-8')).hexdigest()
                zip_code = sha256(row[6].encode('utf-8')).hexdigest()
                country = sha256(row[7].encode('utf-8')).hexdigest()
                gender = sha256(row[8].encode('utf-8')).hexdigest()
                action = row[9]
                checkout = row[10]
                checkout_timestamp = time.mktime(datetime.strptime(checkout, '%Y-%m-%d').timetuple())
                price = row[11].replace('$', '').replace(',','.').replace('€', '')
                diff_days = round(int(float(time_today_timestamp)-float(checkout_timestamp))/(60*60*24))
            
                if diff_days > 0 and diff_days <= 7:
                    user_data = UserData(
                        email= [email1, email2, email3],
                        phone=phone,
                        #gender=[gender],
                        first_name=name,    
                        country_code=country,
                        zip_code=zip_code,                
                    )

                    custom_data = CustomData(
                        value=float(price),
                        currency='eur',
                        #madid=madid,
                    )

                    event = Event(
                        event_name=action,
                        event_time=int(checkout_timestamp),
                        user_data=user_data,
                        custom_data=custom_data,
                    )
                    
                    events = [event]

                    event_request = EventRequest(
                        events=events,
                        pixel_id=pixel_id,
                    )

                    try:
                        event_response = event_request.execute()
                    except (Exception) as error:
                        print('Algo ha ocurrido: '+ error)
                        

                    print(event_response)
                    print('OK')
                else:
                    counter_not_upload+=1
        
            counter += 1
        print('La cantidad de registros no subidos fue de: ', counter_not_upload)

            



if __name__ == '__main__':

    # Se declaran las variables para acceso a la API e ID del pixel asociado a la cuenta BM.
    access_token = 'EAAJdeeE7wfsBABH6aVGawuIXI19B64lkrkbrx9w62aIdOn7ZCukAJU6ZAmiNKOOfR4IRSXN8UAblsyuPp4RYuREG1kvIZCBZBqDZCPV9G5ez1qaTxb2XgpAsewLzIAxfaXe0fH6UjFeuwNHjBtZA2brAZAS93cL99r6pZCtTzxeCN90QnqcgMLsG6125xr5NXGMZD'
    pixel_id = '891865914813933'

    # Valida que exista o esté inicializado el pixel id y el access token
    if not (pixel_id and access_token):
        raise Exception('Validar que esté definido correctamente el pixel id: {pixel_id} y el access token: {access_token}.'.format(pixel_id, access_token)) 

    main(pixel_id, access_token)
