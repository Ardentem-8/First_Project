from django.urls import path, include
import blog.views as views

urlpatterns = [
    path('', views.song_list, name='song_list'), # 歌曲列表页
   #path('song/<int:id>/', views.song_detail, name='song_detail'), # pk是django的最佳写法
    path('song/<int:pk>/', views.song_detail, name='song_detail'), # 歌曲详情页
    path('singers/', views.singer_list, name='singer_list'),  # 歌手列表页
    path('singer/<int:pk>/', views.singer_detail, name='singer_detail'),  # 歌手详情页
    path('search/', views.search, name='search'), # 搜索列表页
    path('search/results/', views.search_results, name='search_results'),# 搜索详情页
    
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'), # 评论功能实现
]