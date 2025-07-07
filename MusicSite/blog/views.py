from django.shortcuts import render, get_object_or_404, redirect
from .models import Song, Singer, Comment
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
import time

def song_list(request):
    songs = Song.objects.all().order_by('id')
    paginator = Paginator(songs, 10) #分页器，每页10个
    page = request.GET.get('page', 1) # 请求默认第一页
    songs_page = paginator.get_page(page) # 获取当前页数据
    return render(request, 'blog/song_list.html', {'songs': songs_page, 'paginator': paginator}) # 渲染

def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk) #获取指定主键的歌曲，不存在则返回404
    comments = song.comments.order_by('-created_at') # 按照创建时间倒序排列
    if request.method == 'POST': #post请求，提交新评论
        content = request.POST.get('content', '').strip() #获取评论内容
        if content: # 内容不为空
            Comment.objects.create(song=song, comment_content=content) # 创建评论
        return redirect('song_detail', pk=pk) # 重定向
    return render(request, 'blog/song_detail.html', {'song': song, 'comments': comments})

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk) 
    song_pk = comment.song.pk  # 保存歌曲主键
    comment.delete() # 删除评论
    return redirect('song_detail', pk=song_pk) # 重定向回来

def singer_list(request):
    singers = Singer.objects.all().order_by('id')
    paginator = Paginator(singers, 10)
    page = request.GET.get('page', 1)
    singers_page = paginator.get_page(page)
    return render(request, 'blog/singer_list.html', {'singers': singers_page, 'paginator': paginator})

def singer_detail(request, pk):
    singer = get_object_or_404(Singer, pk=pk)
    songs = singer.songs.all()
    return render(request, 'blog/singer_detail.html', {'singer': singer, 'songs': songs})

def search(request):
    return render(request, 'blog/search.html')

# def search_results(request):
#     keyword = request.GET.get('q', '').strip()
#     search_type = request.GET.get('type', 'song')
#     start_time = time.time()
#     results = []
#     if keyword:
#         if search_type == 'song':
#             results = Song.objects.filter(name__icontains=keyword)
#         else:
#             results = Singer.objects.filter(name__icontains=keyword)
#     paginator = Paginator(results, 10)
#     page = request.GET.get('page', 1)
#     results_page = paginator.get_page(page)
#     elapsed = round(time.time() - start_time, 3)
#     return render(request, 'blog/search_results.html', {
#         'results': results_page,
#         'paginator': paginator,
#         'keyword': keyword,
#         'search_type': search_type,
#         'count': paginator.count,
#         'elapsed': elapsed
#     })
def search_results(request):
    keyword = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'song')
    start_time = time.time()
    results = []
    if keyword:
        if search_type == 'song':
            # 歌曲名、歌手名、歌词都能搜索
            results = Song.objects.filter(  # Q() 用于支持多字段或关系的复合查询。
                Q(name__icontains=keyword) |
                Q(singer__name__icontains=keyword) |
                Q(lyric__icontains=keyword)
            ).distinct()
        else:
            # 歌手名、简介都能搜索
            results = Singer.objects.filter(
                Q(name__icontains=keyword) |
                Q(intro__icontains=keyword)
            ).distinct()
    paginator = Paginator(results, 10)
    page = request.GET.get('page', 1)
    results_page = paginator.get_page(page)
    elapsed = round(time.time() - start_time, 3)
    return render(request, 'blog/search_results.html', {
        'results': results_page,
        'paginator': paginator,
        'keyword': keyword,
        'search_type': search_type,
        'count': paginator.count,
        'elapsed': elapsed
    })