from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

from .views import CaptchaAPIView,VerifyCaptchaAPIView

urlpatterns = [
    path(r"student_list/",view=views.index,name="app01_index"),
    path(r"login/",view=views.LoginAPIView.as_view(),name="LoginAPIView"),
    path(r"password/",view=views.PasswordMixinView.as_view(),name="PasswordMixinView"),
    path(r"import_csv/",view=views.import_csv,name="import_csv"),
    path(r"NotesAPIview/",view=views.NotesAPIview.as_view(),name="NotesAPIview"),  #当前登录用户作为user外键
    path(r"employee/",view=views.EmployeeView.as_view(),name="EmployeeView"),  #一对多外键序列化测试
    path(r"babyview/",view=views.BabyView.as_view(),name="BabyView"),  #多对多外键序列化测试
    path(r"article/list/mixin/",view=views.ArticleListMixin.as_view(),name="ArticleList"),  #genericAPIView，排序，过滤，搜索功能
    path(r"article/create/",view=views.ArticleCreate.as_view(),name="article_create"),  #genericAPIView，排序，过滤，搜索功能
    path(r"article/list/genericapiview/",view=views.ArticleListGenericAPIView.as_view(),name="ArticleListGenericAPIView"),  #genericAPIView，排序，过滤，搜索功能ArticleAPIView
    path(r"register/",view=views.UserRegisterAPIView.as_view(),name="UserRegisterAPIView"),  
    path(r'generate_captcha/', CaptchaAPIView.as_view(), name='generate_captcha'),
    path(r'verify_captcha/', VerifyCaptchaAPIView.as_view(), name='verify_captcha'),
]


router = DefaultRouter()  # 可以处理视图的路由器
router.register(r'student_viewset', views.StudentViewSet)  # 向路由器中注册视图集
router.register(r'image_viewset', views.ImagetestViewSet) 
router.register(r'student_pagination', views.StudentPaginationViewSet) 
urlpatterns += router.urls  # 将路由器中的所有路由信息追到到django的路由列表中
