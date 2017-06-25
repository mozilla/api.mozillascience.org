from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_protect


@csrf_protect
@api_view(['GET'])
@permission_classes([AllowAny])
def bootstrap(request):
    user_content = {}
    user = request.user

    user_content['authenticated'] = user.is_authenticated()
    if user_content['authenticated']:
        user_content['first_name'] = user.first_name
        user_content['last_name'] = user.last_name
        user_content['email'] = user.email

    content = {'user': user_content}
    return Response(content)
