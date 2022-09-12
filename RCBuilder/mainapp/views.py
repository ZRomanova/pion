from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView, View
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import is_safe_url, urlunquote
from django.db.models import Q

from datetime import datetime, timedelta

from django.contrib import messages

from .models import News, newsitemlist, Subscription
from .forms import SubscriptionForms, MainFormForms

class UnSubscriptionView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('mail'):
            created = Subscription.objects.get(
                mail=request.GET.get('mail')
            )
            messages.add_message(request, messages.INFO, 'Подписка отменена')
            created.delete()

        return HttpResponseRedirect('/')

class InfoView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = MainFormForms(request.POST, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Сообщение отправлено')


        next = request.META.get('HTTP_REFERER')
        if next:
            next = urlunquote(next)  # HTTP_REFERER may be encoded.
        return HttpResponseRedirect(next)


class SubscriptionView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = SubscriptionForms(request.POST, request.FILES or None)
        if request.method == "POST" and form.is_valid():

            created = Subscription.objects.get_or_create(
                mail=form.cleaned_data['mail']
            )
            if created:
                messages.add_message(request, messages.INFO, 'Вы успешно подписаны')
            else:
                messages.add_message(request, messages.INFO, 'Вы уже подписаны')

        else:
            print(form.errors)

        next = request.META.get('HTTP_REFERER')
        if next:
            next = urlunquote(next)  # HTTP_REFERER may be encoded.

        return HttpResponseRedirect(next)


class ManualView(View):
    def get(self, request, *args, **kwargs):
        mainForm = MainFormForms()
        form = SubscriptionForms()


        if not 'page' in kwargs:
            return render(request, 'manual.html', {'formSub': form, 'mainForm': mainForm})
        else:
            if kwargs['page'] == "1":
                return render(request, 'manual1.html', {'formSub': form, 'mainForm': mainForm, 'page_number': kwargs['page']})
            elif kwargs['page'] == "2":
                return render(request, 'manual2.html', {'formSub': form, 'mainForm': mainForm, 'page_number': kwargs['page']})
            elif kwargs['page'] == "3":
                return render(request, 'manual3.html', {'formSub': form, 'mainForm': mainForm, 'page_number': kwargs['page']})
            elif kwargs['page'] == "4":
                return render(request, 'manual4.html', {'formSub': form, 'mainForm': mainForm, 'page_number': kwargs['page']})
            elif kwargs['page'] == "5":
                return render(request, 'manual5.html', {'formSub': form, 'mainForm': mainForm, 'page_number': kwargs['page']})
            elif kwargs['page'] == "6":
                return render(request, 'manual6.html', {'formSub': form, 'mainForm': mainForm, 'page_number': kwargs['page']})
            elif kwargs['page'] == "7":
                return render(request, 'manual7.html', {'formSub': form, 'mainForm': mainForm, 'page_number': kwargs['page']})
            else:
                return render(request, 'manual.html', {'formSub': form, 'mainForm': mainForm})



class BaseView(View):
    def get(self, request, *args, **kwargs):
        mainForm = MainFormForms()
        form = SubscriptionForms()
        search_name = False
        if request.GET.get('main_form'):
            search_name = True

        return render(request, 'base.html', {'formSub': form, 'mainForm': mainForm, 'main_form':search_name})

class NawsView(ListView):
    def dispatch(self, request, *args, **kwargs):

        catlist = newsitemlist.objects.category_list('newscat')
        self.model = News
        form = SubscriptionForms()

        search_name = ''
        search_date = ''

        if request.GET.get('search_name'):
            search_name = request.GET.get('search_name')

        if request.GET.get('month'):
            search_date = request.GET.get('month')


        if 'slug' in kwargs:
            if request.GET.get('month'):
                self.queryset = self.model._base_manager.filter(Q(category__slug=kwargs['slug'])&Q(name__icontains=search_name)&Q(create__month=search_date))
            else:
                self.queryset = self.model._base_manager.filter(Q(category__slug=kwargs['slug'])&Q(name__icontains=search_name))

            self.extra_context = {'catlist': catlist, 'search_name':search_name, 'razItem': kwargs['slug'], 'formSub': form}
        else:
            if request.GET.get('month'):
                self.queryset = self.model._base_manager.filter(Q(name__icontains=search_name)&Q(name__icontains=search_name)&Q(create__month=search_date))
            else:
                self.queryset = self.model._base_manager.filter(Q(name__icontains=search_name)&Q(name__icontains=search_name))

            self.extra_context = {'catlist': catlist, 'search_name':search_name, 'formSub': form}

        self.paginate_by = 4
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'news'
    template_name = 'news.html'
    slug_url_kwarg = 'slug'


class NewsDetailView(DetailView):

    def dispatch(self, request, *args, **kwargs):
        catlist = newsitemlist.objects.category_list('newscat')
        self.model = News
        form = SubscriptionForms()

        self.queryset = self.model._base_manager.all()
        self.extra_context = {'catlist': catlist, 'formSub': form}
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'news_detail'
    template_name = 'details_news.html'
    slug_url_kwarg = 'slug'