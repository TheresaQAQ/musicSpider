import requests, os, json, re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

class Music:
    def __init__(self, id):

        # 获取歌曲详细信息
        url = 'https://api.imjad.cn/cloudmusic/?type=detail&id={id}'.format(
            id=id)
        req = requests.get(url,headers=headers).text
        dic = json.loads(req)['songs'][0]

        self.id = id
        self.name = self.remove(dic['name'])  # 歌曲名称
        self.singer = self.remove(dic['ar'][0]['name'])  # 歌手名称
        self.album = self.remove(dic['al']['name'])  # 所属专辑
        self.picurl = self.remove(dic['al']['picUrl'])  # 封面地址

        self.detail = {
            'name':self.name,
            'singer':self.singer,
            'id':self.id
        }

    # 移除名称里的正斜杠
    def remove(self, string):
        b = string.split('/')
        c = ''
        for i in b:
            c += i

        return c
    
    #下载方法
    def download(self):
        url = 'https://api.imjad.cn/cloudmusic/?type=id&id={id}'.format(id=self.id)
        req = requests.get(url, headers=headers).text
        dic = json.loads(req)['data'][0]
        url = dic['url']  # 歌曲地址

        file_name = 'cache\{name}-{singer}.mp3'.format(name=self.name, singer=self.singer)
        # 判断文件是否存在
        if os.path.exists(file_name) != True:
            content = requests.get(url).content
            with open(file_name, 'wb') as f:
                f.write(content)


#搜索
class Search:
    def __init__(self, type='', keyword=''):
        self.songs = []
        self.playlists = []
        self.type = type
        self.keyword = keyword

    def run(self):
        if self.type == '单曲':
            return self.music(keyword=self.keyword)
        elif self.type == '歌单':
            return self.playlist(keyword=self.keyword)

    # 移除名称里的正斜杠
    def remove(self, string):
        b = string.split('/')
        c = ''
        for i in b:
            c += i

        return c

    #搜索单曲
    def music(self, keyword, num=30):
        self.songs = []
        url = 'https://v1.alapi.cn/api/music/search?limit={num}&type=1&keyword={keyword}'.format(num=num, keyword=keyword)
        req = requests.get(url,headers=headers).text
        data = json.loads(req)
        if data['code'] == 200:
            data = data['data']['songs']
            for i in data:
                song = {}
                song['name'] = i['name']  # 名字
                song['id'] = i['id']  # ID
                song['singer'] = i["artists"][0]['name']  # 歌手名
                song['album'] = i['album']['name']  # 专辑名
                self.songs.append(song)
        # 使用另一个API
        else:
            print('API错误')
            data = {
                's': keyword,
                'type': 1,
                'limit': num
            }
            html = requests.post('http://music.163.com/api/search/pc', data,headers=headers)
            data = json.loads(html.text)['result']['songs']
            self.songs = []
            for i in data:
                song = {}
                song['name'] = i['name']  # 名字
                song['id'] = i['id']  # ID
                song['singer'] = i["artists"][0]['name']  # 歌手名
                self.songs.append(song)

        return self.songs

    #搜索歌单
    def playlist(self,keyword,num=30):
        self.playlists = []
        url = 'https://v1.alapi.cn/api/music/search?limit={num}&type=1000&keyword={keyword}'.format(num=num, keyword=keyword)
        req = requests.get(url,headers=headers).text
        # 如果第一个请求响应正常
        if json.loads(req)['code'] == 200:
            data = json.loads(req)['data']['playlists']
            for i in data:
                playlist = {}
                playlist['name'] = i['name']  # 名字
                playlist['id'] = i['id']  # ID
                self.playlists.append(playlist)

        # 如果第一个请求响应失败，使用第二个API
        else:
            print('API错误')
            data = {
                's': keyword,
                'type': 1000,
                'limit': num
            }
            html = requests.post('http://music.163.com/api/search/pc', data,headers=headers)
            data = json.loads(html.text)['result']['playlists']
            self.playlistss = []
            for i in data:
                playlist = {}
                playlist['name'] = i['name']  # 名字
                playlist['id'] = i['id']  # ID
                self.playlists.append(playlist)

        return self.playlists

def find_id_in_playlist(id):
    url = 'https://api.imjad.cn/cloudmusic/?type=playlist&id={0}'.format(id)
    req = requests.get(url,headers=headers).text
    dic = json.loads(req)['playlist']['tracks']
    musics = []
    for i in dic:
        s = {}
        s['name'] = i['name']
        s['id'] = i['id']
        s['singer'] = i['ar'][0]['name']
        musics.append(s)
    dic = json.loads(req)['playlist']['trackIds']
    ids = []
    for i in range(10,len(dic)):
        ids.append(str(dic[i]['id']))
    return musics,ids