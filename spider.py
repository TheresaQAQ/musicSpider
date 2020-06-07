import requests, os, json, re


class Music:
    def __init__(self, id):

        # 获取歌曲详细信息
        url = 'https://api.imjad.cn/cloudmusic/?type=detail&id={id}'.format(
            id=id)
        req = requests.get(url).text
        dic = json.loads(req)['songs'][0]

        self.name = self.remove(dic['name'])  # 歌曲名称
        self.singer = self.remove(dic['ar'][0]['name'])  # 歌手名称
        self.album = self.remove(dic['al']['name'])  # 所属专辑
        self.picurl = self.remove(dic['al']['picUrl'])  # 封面地址

        # 获取歌曲信息
        url = 'https://api.imjad.cn/cloudmusic/?type=id&id={id}'.format(id=id)
        req = requests.get(url).text
        dic = json.loads(req)['data'][0]
        self.url = dic['url']  # 歌曲地址

        self.details ={
            'name' : self.name,
            'singer': self.singer,
            'album' : self.album,
            'picurl' : self.picurl,
            'url' : self.url
        }
    # 移除名称里的正斜杠
    def remove(self, string):
        b = string.split('/')
        c = ''
        for i in b:
            c += i

        return c
    
    #下载方法
    def download(self, type='cache'):
        if type == 'cache':
            file_name = 'cache\{name}-{singer}.zqj'.format(name=self.name, singer=self.singer)
            # 判断文件是否存在
            if os.path.exists(file_name) != True:
                content = requests.get(self.url).content
                with open(file_name, 'wb') as f:
                    f.write(content)
        else:
            file_name = 'download\{name}-{singer}.mp3'.format(name=self.name, singer=self.singer)
            # 判断文件是否存在
            if os.path.exists(file_name) != True:
                content = requests.get(self.url).content
                with open(file_name, 'wb') as f:
                    f.write(content)
                print('下载成功:）')
            else:
                print('文件已存在！')


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
        req = requests.get(url).text
        data = json.loads(req)['data']['songs']
        for i in data:
            song = {}
            song['name'] = self.remove(i['name'])  # 名字
            song['id'] = i['id']  # ID
            song['singer'] = i["artists"][0]['name']  # 歌手名
            song['album'] = i['album']['name']  # 专辑名
            self.songs.append(song)

        req = requests.get(url).text
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
            html = requests.post('http://music.163.com/api/search/pc', data)
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
        req = requests.get(url).text
        data = json.loads(req)['data']['playlists']
        for i in data:
            playlist = {}
            playlist['name'] = i['name']  # 名字
            playlist['id'] = i['id']  # ID
            self.playlists.append(playlist)

        return self.playlists


def find_id_in_playlist(id):
    url = 'https://api.imjad.cn/cloudmusic/?type=playlist&id={0}'.format(id)
    req = requests.get(url).text
    dic = json.loads(req)['playlist']['trackIds']
    musics = []
    for i in dic:
        musics.append(str(i['id']))
    return musics