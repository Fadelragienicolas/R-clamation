from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
# Create your views here.


# #fonction inscription
# def Inscription(request):

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         pwd = request.POST.get('pwd')
#         c_pwd = request.POST.get('c_pwd')

#         #verrification des champs
#         if not username or not email or not pwd or not c_pwd :
#             messages.error(request, 'Tous les champs sont obligatoire')
#             return redirect('inscription')
        
#         #verrification nom utilisateur
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Ce nom utilisateur existe déja')
#             return redirect('inscription')

#         #verification mot de passe 
#         if pwd != c_pwd :
#             messages.error(request, 'Mot de passe nom identique')
#             return redirect('inscription')

#         #verification si email existe deja
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Cet email existe déja")
#             return redirect('inscription')
        
#         #Creation de l'utilisateur
#         user = User.objects.create_user(username=username, email=email, password=pwd)
#         user.save()
#         messages.success(request, 'Compte créé avec success ! Vous pouvez vous connecter.')

#         return redirect('connexion')
#     return render(request, 'register.html')


# Debut fonction Connecion
def Connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = authenticate(request, username = username, password = pwd)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
          messages.error(request, 'Nom utilisateur ou mot de passe invalide')
    return render(request, 'login.html')


    

# Debut fonction deconnecion
def Deconnexion(request):
    logout(request)
    return redirect('presentation_app')



