from django.urls import path

from .views import BaseView, NawsView, NewsDetailView, SubscriptionView, UnSubscriptionView, InfoView

urlpatterns = [
 path('', BaseView.as_view(), name="base"),
 path('news/', NawsView.as_view(), name="news"),

 path('news/<str:slug>/', NawsView.as_view(), name="news"),
 path('subscription/', SubscriptionView.as_view(), name="subscription"),
 path('unsubscription/', UnSubscriptionView.as_view(), name="unsubscription"),

 path('info_form/', InfoView.as_view(), name="info_form"),


 path('news/item/<str:slug>/', NewsDetailView.as_view(), name="news")
]
