from ccm.views import *
from django.urls import path

urlpatterns = [
    path('get-mikoa/', GetMikoa.as_view(), name='get-mikoa'),
    path('assign-representative/', AddWilayaRepresentativeView.as_view(), name='add-representative-to-wilaya'),
    path('representatives/', RepresentativeListView.as_view(), name='representative-list'),
    path('save-objectives/', ObjectiveCreateView.as_view(), name='save_objectives'),
    path('user-objectives/<uuid:representative_id>/',ObjectiveListView.as_view(), name='get_user_objectives'),
    path('save-targets/', TargetCreateView.as_view(), name="add_objective_targets"),
    path('objective-targets/<uuid:objective_id>/', TargetListView.as_view(), name="get_objective_targets"),
    path('save-indicators/', IndicatorCreateView.as_view(), name="add_target_indicators"),
    path('target-indicators/<uuid:target_id>/', IndicatorListView.as_view(), name="get_target_indicators"),
    path('save-activities/', ActivityCreateView.as_view(), name='add_target_activitis'),
    path('indicator-activities/<uuid:indicator_id>/', ActivityListView.as_view(), name='get_indicator_activities'),
]