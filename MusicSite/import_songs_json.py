import os
import django
import json
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MusicSite.settings')
django.setup()

from blog.models import Song, Singer

# 清空所有歌曲和歌手
Song.objects.all().delete()
Singer.objects.all().delete()
with open('qqmusic_2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# 1. 先导入所有歌手（去重）
singer_map = {}
for item in data:
    singer_name = item.get('歌手名') or item.get('singer_name')
    singer_pic = item.get('歌手图片') or ''
    singer_intro = item.get('歌手简介') or ''
    singer_url = item.get('歌手原始URL') or ''
    if singer_name not in singer_map: # 去重操作
        singer_obj, _ = Singer.objects.get_or_create(
            name=singer_name,
            defaults={
                'image': singer_pic,
                'intro': singer_intro,
                'url': singer_url
            }
        )
        singer_map[singer_name] = singer_obj

# 2. 再导入所有歌曲（关联歌手）
count = 0 # 统计有多少歌import了
for item in data:
    song_name = (item.get('歌曲名') or item.get('song_name') or '').strip()
    singer_name = (item.get('歌手名') or item.get('singer_name') or '').strip()
    song_pic = item.get('歌曲图片') or ''
    lyric = item.get('歌词') or ''
    # 去除无关标签
    lyric = re.sub(r'\[.*?:.*?\]', '', lyric) 
    lyric = lyric.strip()
    # 过滤无歌词的纯音乐
    if '此歌曲为没有填词的纯音乐，请您欣赏' in lyric: 
        continue
    url = item.get('歌曲原始URL') or item.get('song_url') or ''
    singer_obj = singer_map.get(singer_name)
    if not song_name or not singer_obj:
        continue
    Song.objects.get_or_create(
        name=song_name,
        singer=singer_obj,
        defaults={
            'image': song_pic,
            'lyric': lyric,
            'url': url
        }
    )
    count += 1

print(count) # 过滤三个纯音乐，导入完成
print("导入完成！")