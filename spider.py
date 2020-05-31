import requests, os, json, re


class Music:
    def __init__(self,id):

        #获取歌曲详细信息
        url = 'https://api.imjad.cn/cloudmusic/?type=detail&id={id}'.format(id=id)
        req = requests.get(url).text
        dic = json.loads(req)['songs'][0]

        self.name = dic['name'] #歌曲名称
        self.singer = dic['ar'][0]['name'] #歌手名称
        self.album = dic['al']['name'] #所属专辑
        self.picurl = dic['al']['picUrl'] #封面地址

        #获取歌曲信息
        url = 'https://api.imjad.cn/cloudmusic/?type=id&id={id}'.format(id=id)
        req = requests.get(url).text
        dic = json.loads(req)['data'][0]
        self.url = dic['url'] #歌曲地址
    
    #下载方法
    def download(self):
        file_name = '{name}-{singer}.mp3'.format(name=self.name, singer=self.singer)
        
        #判断文件是否存在
        if os.path.exists(file_name) != True:
            content = requests.get(self.url).content
            with open(file_name,'wb') as f:
                f.write(content)
            print('下载成功:）')
        else:
            print('文件已存在！')


#搜索
class Search:
    def __init__(self, type, keyword):
        self.songs = []
        self.playlists = []
        self.type = type
        self.keyword = keyword

    def run(self):
        if self.type == '单曲':
            return self.music(keyword=self.keyword)
        elif self.type == '歌单':
            return self.playlist(keyword=self.keyword)

    #搜索单曲
    def music(self, keyword, num=30):
        self.songs = []
        url = 'https://v1.alapi.cn/api/music/search?limit={num}&type=1&keyword={keyword}'.format(num=num, keyword=keyword)
        req = requests.get(url).text
        data = json.loads(req)['data']['songs']
        for i in data:
            song = {}
            song['name'] = i['name']  # 名字
            song['id'] = i['id']  # ID
            song['singer'] = i["artists"][0]['name']  # 歌手名
            song['album'] = i['album']['name']  # 专辑名
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


def playlist(id):
    url = 'https://api.imjad.cn/cloudmusic/?type=playlist&id={0}'.format(id)
    req = requests.get(url).text
    dic = json.loads(req)['playlist']['trackIds']
    musics = []
    for i in dic:
        musics.append(Music(str(i['id'])))
    
    for i in musics:
        i.download()
    



def a_music():
    pass



def main():
    print('请选择功能：\n1.单曲下载\n2.歌单下载\n3.单曲搜索\n4.歌单搜索')
    
    #获得用户输入信息
    while True:
        try:
            userinput = input('输入对应数字选择功能：')
            userinput = str(re.search('^(.*?)([1-4])(.*?)$',userinput).group(2)) #使用正则提取用户输入的信息
            break
        except AttributeError:
            print('输入信息不合法，请重新输入！')
    if userinput == '1':
        #单曲下载
        id = input('请输入歌曲ID:')
        music = Music(id) 
        music.download()
    elif userinput == '2':
        #歌单下载
        pass
    elif userinput == '3':
        #单曲搜索
        keyword = input('请输入歌曲名称: ')
        songs = Keyword()
        songs.music()
        print(songs)
    else:
        #歌单搜索
        pass

if __name__ == '__main__':
    a = Search(type='单曲',keyword='凉凉')
    b = a.run()
    print(b)