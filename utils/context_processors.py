from usuarios.models import Usuario
from django.http import JsonResponse

def datos_usuario(request):
    if request.user.is_authenticated:
        try:
            usuario = Usuario.objects.filter(pk=request.user.id).first()
        
            return {'user':usuario}
        except Exception as e:
            print(e)
            return {'user':None}
    else:
        print('no utenticado')
        return {'user':None}


def verificarRol(request, roles):
    if request.user.is_authenticated:
        try:
            usuario = Usuario.objects.filter(pk=request.user.id).first()
            if usuario and usuario.rol in roles:
                return True
            return JsonResponse({'message': 'No tienes permisos'}, status=403)
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'message': 'Error en la verificación de rol'}, status=500)
    else:
        print('No autenticado')
        return JsonResponse({'message': 'No autenticado'}, status=401)