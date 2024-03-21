### IMPORT PACCHETTI E FUNZIONI
import quickstart as q
import pandas as pd
import mysql_helper as ms
#warnings
import warnings
warnings.filterwarnings("ignore")
#time
import time
import random
#remove html code
import re
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

#set constant variables for the called functions
path = 'C://Users//Administrator//Desktop//Scripts//Google Calendar//v0//'
time_min = "2023-06-01T00:00:01Z"
time_max = "2024-01-01T00:00:00Z"
num_eventi = 2500

# lettura del file contenente le mail
my_file = open(path + "list_email.txt", "r")
data = my_file.read()
mail_list = data.replace('\n', '').split(",")

#lista parole da controllare
lista_check = ['ferie', 'ooo', 'out of office', 
'maternit', 'paternit', 'mutua', 'malattia', 'permesso']

#create dataframe
df = pd.DataFrame(columns=['mail', 'evento', 'inizio', 'fine', 'attendees', 'description'])

lista_mail = []
lista_titolo_evento = []
lista_start = []
lista_end = []
lista_attendees = []
lista_descrizione = []
#lista_event_creator = []


for mail in mail_list:
    time.sleep(random.randint(1,3))
    print(mail)
    events = q.main(mail, num_eventi, time_min, time_max) #Qui chiamo la funzione all'interno di quickstart
    for event in events:
        try: 
            ### volte rompe le palle su event['summary'], magari non tutti gli eventi hanno un titolo (?)
            ### PRIMA PROVA A SCARICARE  IL TITOLO !!!!!!!!! ######
            lista_titolo_evento.append(event['summary'])
            lista_mail.append(mail)
            lista_start.append(event['start'].get('dateTime', event['start'].get('date')))
            lista_end.append(event['end'].get('dateTime', event['end'].get('date')))
            ### lista_event_creator.append(event['creator'].get('email')) ##si pianta
            if mail == 'c_0dkmfbtn14jbs818avke0cjagc@group.calendar.google.com':
                #prima recupero il primo partecipante (che è il trainer)
                try:
                    lista_attendees.append(event['attendees'][0].get('email'))
                except:
                    lista_attendees.append('no attendees')
                #poi recupero la descrizione dell'evento
                try:
                    descrizione_evento = str(event['description'])
                    #descrizione_evento = remove_tags(descrizione_evento) #qui tolgo il codice html per renderlo leggibile
                    descrizione_evento = descrizione_evento
                    lista_descrizione.append(descrizione_evento)
                except:
                    lista_descrizione.append('_')
            else:
                lista_attendees.append('_')
                lista_descrizione.append('_')
        except:                                    
            continue

df.mail = lista_mail
df.evento = lista_titolo_evento
df.inizio = lista_start
df.fine = lista_end
df.attendees = lista_attendees
df.description = lista_descrizione
### df.event = lista_event_creator

df.evento = df.evento.str.lower()

df['filtro'] = pd.Series()
for i in range(len(df)):
    #tolgo gli eventi solo dai calendari non training@visualitics (ciò che non rientra nella lista lista_check)
    if df.mail[i] != 'c_0dkmfbtn14jbs818avke0cjagc@group.calendar.google.com':
        for check in lista_check:
            if check in df.evento[i]:
                df['filtro'][i] = "True"
    else:
        df['filtro'][i] = "True" 
           
df.dropna(inplace=True)
df.drop('filtro', axis=1, inplace=True)

#export to csv
print(df)
df.to_csv(path + 'data_2023_s2.csv', index=False)

###############################################################àà
# DB MySQL details
import config 
server = config.server
port = config.port
username_DB = config.username_DB
password_DB = config.password_DB
database = config.database   
    
# Connect to mysql and check if the specify DB already exists; if not, creates it
# try:
cnx = ms.mysql_connector(server, port, database, username_DB, password_DB)
cursor = cnx.cursor()
    #logging.info('Successfully connected to {0} (DB: {1}) as {2}'.format(server, database, username_DB))
    
# except Exception as ex:
    # logging.exception(ex)
    # raise
        
# try:
cursor.execute("USE {}".format(database))
engine = ms.mysql_engine(server, port, database, username_DB, password_DB)

df.to_sql(name="ds_planning_2023_s2", con=engine, if_exists = 'replace', index=False)
        