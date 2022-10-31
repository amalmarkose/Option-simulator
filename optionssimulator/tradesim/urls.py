from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alltrades', views.alltrades, name='alltrades'),
    path('archived', views.archived, name='archived'),
    path('trade/<int:id>/<str:strategy>/<str:expiry>', views.trade, name='trade'),
    path('inviewpush', views.inviewpush, name='inviewpush'),
    path('inviewupdate/<str:strategy>/<str:expiry>', views.inviewupdate, name='inviewupdate'),
    path('dashboardpush/<str:name>/<str:date>', views.dashboardpush, name='dashboardpush'),
    path('dashboardmodify/<str:maxprofit>/<str:maxloss>/<str:breakeven1>/<str:breakeven2>', views.dashboardmodify, name='dashboardmodify'),
    path('displaydatapush', views.displaydatapush, name='displaydatapush'),
    path('positionspush/<str:name>/<str:date>', views.positionspush, name='positionspush'),
    path('optionchainpush/<str:expiry>/<str:active>', views.optionchainpush, name='optionchainpush'),
    path('builderpush/<str:name>/<str:date>', views.builderpush, name='builderpush'),
    path('chartpush', views.chartpush, name='chartpush'),
    path('buildermodify/<str:token>/<str:bs>/<str:action>', views.buildermodify, name='buildermodify'),
    path('addtoposition', views.addtoposition, name='addtoposition'),
    path('positionmodify/<str:token>/<str:action>/<str:value>', views.positionmodify, name='positionmodify'),
    path('trademodify/<str:id>/<str:strategy>/<str:expiry>/<str:action>', views.trademodify, name='trademodify'),
    
]