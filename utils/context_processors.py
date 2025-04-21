from usuarios.models import Usuario
def datos_usuario(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        
        usuario_id = request.user.id 
       
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            print(usuario)
            return {'usuario':usuario}
        except Exception as e:
            print(e)
            return {'usuario':None}
    else:
        print('no utenticado')
        return {'usuario':None}
   