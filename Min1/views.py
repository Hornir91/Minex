from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from djgeojson.views import GeoJSONLayerView

from Min1.forms import MineForm, LoginForm, AddUserForm, ResetPasswordForm, NewsPostForm, CommentForm
from Min1.models import Mine, Category, NewsPost, Comment
from Min1.tokens import account_activation_token


class Dashboard(View):

    def get(self, request):
        news = NewsPost.objects.all()
        # for new in news:
        #     comments = new.comments.all()
        return render(request, 'dashboard.html', locals())


class MineCreate(View):

    def get(self, request):
        form = MineForm()
        return render(request, 'mine_create.html', locals())

    def post(self, request):
        form = MineForm(request.POST, request.FILES)

        if form.is_valid():
            lng = form.cleaned_data.get('lng')
            lat = form.cleaned_data.get('lat')
            m1 = Mine.objects.create(name=form.cleaned_data.get('name'), description=form.cleaned_data.get('description'),
                                     is_active=form.cleaned_data.get('is_active'), voivodeship=form.cleaned_data.get('voivodeship'),
                                     added_by=form.cleaned_data.get('added_by'), geom=Point(lng, lat), images=form.cleaned_data.get('image'))
            categories = form.cleaned_data.get('category')
            for category in categories:
                c1 = Category.objects.filter(name__contains=category)
                m1.category.add(c1[0].id)
            return redirect(reverse_lazy('dashboard'))
        else:
            return redirect(reverse_lazy('dashboard'))


class MineEdit(View):

    def get(self, request, id):
        mine = Mine.objects.get(pk=id)
        form = MineForm(initial={'name': mine.name, 'description': mine.description, 'is_active': mine.is_active,
                                 'voivodeship': mine.voivodeship, 'added_by': mine.added_by, 'lat': mine.geom.coords[1],
                                 'lng': mine.geom.coords[0]})
        return render(request, 'mine_edit.html', locals())

    def post(self, request, id):
        form = MineForm(request.POST, request.FILES)
        if form.is_valid():
            m1 = Mine.objects.get(pk=id)
            lng = form.cleaned_data.get('lng')
            lat = form.cleaned_data.get('lat')
            m1.geom = Point(lng, lat)
            m1.name = form.cleaned_data.get('name')
            m1.description = form.cleaned_data.get('description')
            m1.is_active = form.cleaned_data.get('is_active')
            m1.voivodeship = form.cleaned_data.get('voivodeship')
            m1.added_by = form.cleaned_data.get('added_by')
            m1.images = form.cleaned_data.get('image')
            m1.save()
            return redirect(reverse_lazy('dashboard'))
        else:
            return redirect(reverse_lazy('dashboard'))


class MineList(View):
    def get(self, request):
        mines = Mine.objects.all()
        return render(request, 'mine_list.html', locals())


class MapDisplay(View):
    def get(self, request):
        return render(request, 'map_display.html')


class MineDetails(View):
    def get(self, request, id):
        mine = Mine.objects.get(pk=id)
        return render(request, 'mine_details.html', locals())


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', locals())

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_login, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('dashboard'))
            else:
                return HttpResponse('<script>alert("Nieprawidłowe hasło");\
             window.location=""</script>')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('dashboard'))


class GeoJSONLayerMinePropertiesView(GeoJSONLayerView):
    model = Mine
    properties = ['name', 'description', 'images_url']


class Contact(View):
    def get(self, request):
        return render(request, 'contact.html')


class AddUser(View):

    def get(self, request):
        form = AddUserForm()
        return render(request, 'add_user.html', locals())

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            password_repeat = form.cleaned_data['password_repeat']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(username=user_name)
                form.add_error('user_name', 'Nazwa użytkownika zajęta')
                return render(request, 'add_user.html', {'form': form})
            except User.DoesNotExist:
                user = User.objects.create_user(username=user_name, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Aktywacja konta w serwisie.'
                message = render_to_string('activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email
                email_msg = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email_msg.send()
                return HttpResponse('Na podanego emaila został wysłany link aktywacyjny. Proszę postępować zgodnie '
                                    'z instrukcjami zawartymi we wiadomości.')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return HttpResponse('Dziękujemy za potwierdzenie wiadomości email. Twoje konto zostało aktywowane i możesz się '
                            'zalogować.')
    else:
        return HttpResponse('Link aktywacyjny jest niepoprawny!')


class ResetPassword(PermissionRequiredMixin, View):
    permission_required = 'auth.change_user'

    def get(self, request, id):
        form = ResetPasswordForm()
        return render(request, 'reset_password.html', locals())

    def post(self, request, id):
        user = User.objects.get(pk=id)
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_password']
            new_pass = form.cleaned_data['new_password']
            new_pass2 = form.cleaned_data['new_password2']

            if not user.check_password(f'{old_pass}'):
                response = HttpResponse("Podano niewłaściwe hasło")
                return response

            user.set_password(f'{new_pass}')
            user.save()
            return HttpResponse("Hasło zmienione")


class SearchView(View):

    def get(self, request):
        query = request.GET.get('q')
        search_result = Mine.objects.filter(name__icontains=query)
        return render(request, 'search_result.html', {'search_result': search_result})


class NewsPostCreate(View):

    def get(self, request):
        form = NewsPostForm()
        return render(request, 'news_post_create.html', locals())

    def post(self, request):
        form = NewsPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            n1 = NewsPost.objects.create(title=title, content=content)
        return redirect(reverse_lazy('dashboard'))


class NewsPostEdit(View):

    def get(self, request, id):
        post = NewsPost.objects.get(pk=id)
        form = NewsPostForm(initial={'title': post.title, 'content': post.content})
        return render(request, 'news_post_edit.html', locals())

    def post(self, request, id):
        post = NewsPost.objects.get(pk=id)
        form = NewsPostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data.get('title')
            post.content = form.cleaned_data.get('content')
            post.save()
        return redirect(reverse_lazy('dashboard'))


class NewsPostDelete(View):

    def get(self, request, id):
        post = NewsPost.objects.get(pk=id)
        post.delete()
        return redirect(reverse_lazy('dashboard'))


class NewsPostDetails(View):

    def get(self, request, id):
        new = NewsPost.objects.get(pk=id)
        comments = new.comments.all()
        form = CommentForm()
        return render(request, 'news_post_details.html', locals())

    def post(self, request, id):
        new = NewsPost.objects.get(pk=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            body = form.cleaned_data.get('body')
            # c = Comment.objects.create(content_type=new, object_id=id, user_name=user_name, body=body, content_type_id=9)
            c = Comment(content_object=new, user_name=user_name, body=body)
            c.save()
            return redirect(reverse_lazy('news-post-details', args=id))
