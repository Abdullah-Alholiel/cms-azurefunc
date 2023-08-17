import logging, requests,json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    text = req.params.get('text')
    name = req.params.get('name')

    books= get_books(text)
    
 
    return func.HttpResponse(
        json.dumps(books),
        mimetype="application/json",
    ) 
        


def get_books(text):
    url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
    r = requests.get(url)
    if r.status_code == 200:
        answer = r.json()
        result_list = []
        for item in answer.get('items', [])[:5]:
            volume_info = item.get('volumeInfo', {})
            result_dict = {
                'title': volume_info.get('title'),
                'subtitle': volume_info.get('subtitle', ''),
                'description': volume_info.get('description', ''),
                'count': volume_info.get('pageCount', 0),
                'categories': volume_info.get('categories', []),
                'rating': volume_info.get('averageRating', 0),
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                'preview': volume_info.get('previewLink', ''),
            }
            result_list.append(result_dict)
        return  {"books":result_dict}