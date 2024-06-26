from ccm.views import *
from django.urls import path

urlpatterns = [
    path('get-mikoa/', GetMikoa.as_view(), name='get-mikoa'),
    path('assign-representative/', AddWilayaRepresentativeView.as_view(), name='add-representative-to-wilaya'),
    path('representatives/', RepresentativeListView.as_view(), name='representative-list'),
    path('save-objectives/', ObjectiveCreateView.as_view(), name='save_objectives'),
    path('user-objectives/<uuid:representative_id>/',ObjectiveListView.as_view(), name='get_user_objectives'),
]