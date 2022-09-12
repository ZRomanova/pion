from django.urls import path

from .views import BaseView, NawsView, NewsDetailView, SubscriptionView, UnSubscriptionView, InfoView, ManualView

urlpatterns = [
 path('', BaseView.as_view(), name="base"),
 path('news/', NawsView.as_view(), name="news"),

 path('news/<str:slug>/', NawsView.as_view(), name="news"),
 path('subscription/', SubscriptionView.as_view(), name="subscription"),
 path('unsubscription/', UnSubscriptionView.as_view(), name="unsubscription"),

 path('info_form/', InfoView.as_view(), name="info_form"),

 path('manual/', ManualView.as_view(), name="manual"),
 path('manual/<str:page>/', ManualView.as_view(), name="manual_page"),

 path('news/item/<str:slug>/', NewsDetailView.as_view(), name="news")
]
