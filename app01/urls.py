from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path(r"student_list/",view=views.index,name="app01_index"),
    # path(r"student_apiview/", views.StudentViewSet.as_view({"get":"list"}),name="app01_apiview")
]


router = DefaultRouter()  # 可以处理视图的路由器
router.register(r'student_viewset', views.StudentViewSet)  # 向路由器中注册视图集
router.register(r'image_viewset', views.ImagetestViewSet) 
router.register(r'student_pagination', views.StudentPaginationViewSet) 
urlpatterns += router.urls  # 将路由器中的所有路由信息追到到django的路由列表中
