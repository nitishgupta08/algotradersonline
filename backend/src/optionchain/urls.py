from django.urls import path
from .views import option_data, get_ltp, get_nifty, get_nifty_histo

urlpatterns = [
    path('api/options_data/', option_data, name='option_data'),
    path('api/get_ltp/', get_ltp, name='get_ltp'),
    path('api/get_nifty/', get_nifty, name='get_nifty'),
    path('api/get_nifty_histo/', get_nifty_histo, name='get_nifty_histo'),

]
