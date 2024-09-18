from django.http import JsonResponse

def handler404(request,exception):
    meesage=('Path not found')
    response=JsonResponse(data={'error':meesage})
    response.status_code=404
    return response



def handler500(request):
    meesage=('Internal server error')
    response=JsonResponse(data={'error':meesage})
    response.status_code=500
    return response
