from apiclient.discovery import build

service = build("customsearch", "v1",
               developerKey="** your developer key **")

res = service.cse().list(
    q='butterfly',
    cx=' ** your cx **',
    searchType='image',
    num=3,
    imgType='clipart',
    fileType='png',
    safe= 'off'
).execute()

if not 'items' in res:
    print 'No result !!\nres is: {}'.format(res)
else:
    for item in res['items']:
        print('{}:\n\t{}'.format(item['title'], item['link']))