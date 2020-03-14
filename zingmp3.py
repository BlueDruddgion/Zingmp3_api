from setup import *


class authentication():
    def __init__(self, path_cookies='', username='', password=''):
        self._path_cookies = path_cookies
        self._username = username
        self._password = password
        self._headers = HEADERS
        self.session = session

    def auth_with_cookies(self):
        file = open(self._path_cookies, 'r', encoding='utf-8')
        cookies = {}
        out = ''
        for line in file:
            line = line.strip()
            if '#' not in line:
                item = re.findall(r'[0-9]\s(.*)', line)
                if item:
                    item = item[0].split('\t')
                    if len(item) == 1:
                        cookies[item[0]] = ''
                        out += "%s=''; " % item[0]
                    else:
                        cookies[item[0]] = item[1]
        self.session.cookies.update(cookies)
        res = self.session.get(url='https://accounts.zingmp3.vn/account/userprofile', headers={
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/85.0.134 Chrome/79.0.3945.134 Safari/537.36",
            "sec-fetch-site": "same-site",
            'sec-fetch-mode': "cors",
            'referer': "https://zingmp3.vn/",
        })
        info = res.json()
        name = try_get(info, lambda x: x.get('data').get('info').get('name'))
        if not name:
            sys.stdout.write(
                fc + sd + "\n[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "Cookies die, pls try again.\n")
            sys.exit(0)
        return True


class extractZingMp3(ProgressBar):
    def __init__(self, *args, **kwargs):
        self._url = kwargs.get('url')
        self._show_json_info = kwargs.get('show_json_info')
        self._down_lyric = kwargs.get('down_lyric')
        self._down_media = kwargs.get('down_media')
        self._is_login = kwargs.get('is_login')
        self._quality = kwargs.get('quality')
        self._path_save = kwargs.get('path_save') or os.getcwd()
        self._headers = HEADERS
        self._regex_url = '''(?x)^
        ((http[s]?|fpt):)\/?\/(www\.|m\.|)
        (?P<site>
            (?:(zingmp3\.vn)|   
            (mp3\.zing\.vn))
        )\/                                                           # check domain (zingmp3 and mp3.zing.vn)
        (   
            (?P<type>bai-hat|album|video-clip|playlist|embed)\/       # get type (bai-hat, album,video-clip, playlist)
            (?P<slug>.*?)\/                                           # get slug of media
            (?P<id>.*?)(?:$|\W)                                       # get id of media
            |                                                         # if not media url, url is artist's profile url or chart url
            (?:nghe-si\/|)(?P<name>.*?)\/                             # get name artits or get name chart
            (?P<slug_name>.*?)(?:$|\.|\/(?P<id_name>.*?)(?:$|\W))     # get artist's slug or get chart slug
        )
        '''

        '''
        
            All url test
            
            {
                "url":"https://zingmp3.vn/zing-chart/bai-hat.html",
                "note":"url chart to get top bai-hat in zing"
            }
            
            {
                "url":"https://zingmp3.vn/zing-chart-tuan/bai-hat-US-UK/IWZ9Z0BW.html",
                "note":"url chart to get top bai-hat in zing"
            }
            
            {
                "url":"https://zingmp3.vn/top-new-release/index.html",
                "note":"top bai-hat new release"
            }
            
            {
                "url":"https://zingmp3.vn/video-clip/Tim-Ve-Loi-Ru-New-Version-Thanh-Hung-Various-Artists/ZW6ZOIZ7.html",
                "note":"video clip (label max is 480p)"
            }
            
            {
                "url":"https://zingmp3.vn/video-clip/Yeu-Nhieu-Ghen-Nhieu-Thanh-Hung/ZWB087B9.html",
                "note":"video clip (label max is 1080p)"
            }
            
            {
                "url":[
                    "https://zingmp3.vn/nghe-si/Huong-Giang-Idol/bai-hat",
                    "https://zingmp3.vn/nghe-si/Huong-Giang-Idol/album",
                    "https://zingmp3.vn/nghe-si/Huong-Giang-Idol/video",
                ],
                "note":"artist's profile type 1"
            }
            
            {
                "url":[
                    "https://zingmp3.vn/Mr-Siro/bai-hat",
                    "https://zingmp3.vn/Mr-Siro/playlist",
                    "https://zingmp3.vn/Mr-Siro/video"
                ],
                "note":"artist's profile type 2"
            }
            
            {
                "url":"https://zingmp3.vn/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html",
                "note":"bai hat"            
            }
            
            {
                "url":"https://zingmp3.vn/album/Khoc-Cung-Em-Single-Mr-Siro-Gray-Wind/ZF90UA9I.html",
                "note":"album"
            }
            
            {
                "url":"https://zingmp3.vn/playlist/Sofm-s-playlist/IWE606EA.html",
                "note":"playlist"
            }
            
        '''

        self.default_http = 'https://zingmp3.vn/'
        self._api_video = """http://api.mp3.zing.vn/api/mobile/video/getvideoinfo?requestdata={"id":"%s"}"""
        self._type_supported = ['bai-hat', 'album', 'video-clip', 'playlist', 'embed']

    def run(self):
        item = re.search(self._regex_url, self._url)
        if not item:
            return 'Invalid url.'
        video_id = item.group('id')
        type = item.group('type')
        name = item.group('name')
        slug = item.group('slug')
        if type in self._type_supported:
            return self.real_extract_media(type, video_id, slug)
        elif name:
            return self.real_extract_list_media(item, name)
        else:
            sys.stdout.write(fg + '[' + fr + '*' + fg + '] : Invalid url.\n')
        return

    def real_extract_list_media(self, item, name):
        slug_name = item.group('slug_name')
        list_name_api = {
            'bai-hat': "/song/get-list",  # get artist's bai-hat
            "playlist": "/playlist/get-list",  # get artist's playlist
            "album": "/playlist/get-list",  # get artist's album
            "video": "/video/get-list",  # get artist's video or artist's MV
            'zing-chart': {  # get top realtime in zing
                'name': '/chart-realtime/get-detail',  # name api of realtime chart
                'bai-hat': 'song',  # get top bai-hat
                'index': 'song',  # get top bai-hat
                'video': 'video',  # get top video
            },
            'zing-chart-tuan': {  # get chart tuan in zing
                'name': '/chart/get-chart',  # name api of chart tuan
            },
            'top-new-release': {  # get new release
                'name': '/chart/get-chart-new-release'  # name api of new release
            }
        }
        if name == 'zing-chart' or name == 'zing-chart-tuan' or name == 'top-new-release':
            if name == 'zing-chart':
                api = self.get_api(
                    name_api=list_name_api.get(name).get('name'),
                    type=list_name_api.get(name).get(slug_name)
                )
            elif name == 'zing-chart-tuan':
                api = self.get_api(
                    name_api=list_name_api.get(name).get('name'),
                    video_id=item.group('id_name')
                )
            else:
                api = self.get_api(
                    name_api=list_name_api.get(name).get('name'),
                    new_release=True
                )
            f = get_req(url=api, headers=self._headers, type='json')
            if f.get('msg').lower() != 'success':
                sys.stdout.write(fg + '[' + fr + '*' + fg + f'] : {self._url} data null.\n')
                return
            if self._show_json_info:
                print(json.dumps(f, indent=4, ensure_ascii=False))
                return
            datas = try_get(f, lambda x: x['data']['items'])
            for data in datas:
                self.real_extract_media(
                    type=search_regex(r'(?x)\/(.*?)\/', data.get('link')),
                    video_id=data.get('id'),
                )
            return
        name_api = list_name_api.get(slug_name) or None
        if not name_api:
            sys.stdout.write(fg + '[' + fr + '*' + fg + '] : Invalid url.\n')
            return
        content = get_req(url="https://mp3.zing.vn/nghe-si/" + name, headers=self._headers, type='text')
        id_artist = search_regex(r'''(?x)
                                \<a.*?tracking=\"\_frombox=artist_artistfollow\"
                                    \s+data-id=\"(?P<id_artist>.*?)\"
                                    \s+data-type=\"(?P<data_type>.*?)\"
                                    \s+data-name=\"(?P<data_name>.*?)\".*?\>
                                    ''', content, group="id_artist")
        api = self.get_api(name_api=name_api, video_id=id_artist)

        start = 0
        count = 30
        while True:
            f = get_req(url=api, headers=self._headers, type='json', params={
                'type': 'artist',
                'start': start,
                'count': count,
                'sort': 'hot',
            })
            if self._show_json_info:
                print(json.dumps(f, ensure_ascii=False, indent=4))
                return
            if f.get('msg').lower() != 'success':
                sys.stdout.write(fg + '[' + fr + '*' + fg + '] : Data playlist null.\n')
                return
            datas = try_get(f, lambda x: x['data']['items'])

            for data in datas:
                self.real_extract_media(
                    type=search_regex(r'(?x)\/(.*?)\/', data.get('link')),
                    video_id=data.get('id'),
                )
            total = is_int(try_get(f, lambda x: x['data']['total']))
            start += count

            if total <= start:
                break
        return

    def real_extract_media(self, type, video_id, slug=None):
        if type == 'video-clip':
            _json = get_req(url=self._api_video % (video_id), headers=self._headers, type='json')
            data = _json.get('source') or None
            if not data:
                sys.stdout.write(fg + '[' + fr + '*' + fg + f"] : {self._url} don't have video.\n")
                return
            f = _json
        else:
            name_api = ''
            if type == 'album' or type == 'playlist':
                name_api = '/playlist/get-playlist-detail'
            elif type == 'bai-hat':
                name_api = '/song/get-song-info'
            elif type == 'embed':
                if slug and slug == 'song':
                    name_api = '/song/get-song-info'
            else:
                sys.stdout.write(fg + '[' + fr + '*' + fg + f"] : {self._url} invalid.\n")
                return

            api = self.get_api(name_api, video_id)
            data = get_req(url=api, headers=self._headers, type='json')

            if type == 'bai-hat' and self._is_login:
                # get 123 and 320 and lossless
                api2 = self.get_api(name_api='/download/get-streamings', video_id=video_id)
                res = session.get(url=api2, headers=self._headers)
                data2 = res.json()
                if not data or not data2:
                    return "null"
                data['data']['streaming']['default'] = data2.get('data')

            f = data

        if self._show_json_info:
            print(json.dumps(f, ensure_ascii=False, indent=4))
            return
        return self.start_download(f)

    def start_download(self, f):
        if not f:
            return
        msg = f.get('msg')
        if msg and msg.lower() != 'success':
            sys.stdout.write(fg + '[' + fr + '*' + fg + '] : Data null.\n')
            return
        data = f.get('data')

        def get_best_label_video(source):
            """
            - Get best label of source
            :param source: {
                label: url.
            }
            Ex: {
                    360p:      https://.....
                    720p:      https://.....
                    1080p:     https://.....
                } or
                {
                    128:       https://.....
                    320:       https://.....
                    lossless:  https://.....
                }
            :return: url and label and ext
            """
            keys = list(source.keys())
            while True:
                if not keys:
                    break
                label_best = keys[-1]
                try:
                    if self._quality:
                        url = source[self._quality]
                        if url:
                            ext = search_regex(r'(?x).*\.(\w+)', url)
                            if ext not in KNOWN_EXTENSIONS:
                                ext = 'mp3'
                            return url, self._quality, ext
                    else:
                        # if not quality => get best quality of video
                        url = source[label_best]
                        if url:
                            ext = search_regex(r'(?x).*\.(\w+)', url)
                            if ext not in KNOWN_EXTENSIONS:
                                ext = 'mp3'
                            return url, label_best, ext
                except:
                    pass
                keys.remove(label_best)
            sys.stdout.write(
                fg + '[' + fc + '*' + fg + f'''] : Quality {self._quality} don't have in this media, just have {
                list(source.keys())
                }.\n''')
            return None, None, None

        def down_media():
            """
            - Download media.
            :return:
            """
            url, label_best, ext = get_best_label_video(sources)
            if not url:
                sys.stdout.write(fg + '[' + fr + '*' + fg + f"] : {title} don't have media.\n")
                return
            if not url.startswith('http') or not url.startswith('https'):
                url = 'https:' + url
            sys.stdout.write(fg + '[' + fc + '*' + fg + f'] : Downloading {title} - {label_best} .\n')
            down = Downloader(url=url)
            down.download(
                filepath='%s/%s_%s.%s' % (path_download, title, label_best, ext),
                callback=self.show_progress
            )
            sys.stdout.write('\n')
            return

        def down_lyric():
            """
            - Download lyric
            :return:
            """
            sys.stdout.write(fg + '[' + fc + '*' + fg + f'] : Downloading {title} - Lyric .\n')
            if lyric:
                if is_url(lyric):
                    fname = filename_from_url(lyric)
                    if fname.split('.')[-1] != 'lrc':
                        sys.stdout.write(fg + '[' + fr + '*' + fg + f'] : Error when download lyric.')
                        return
                    down = Downloader(url=lyric)
                    down.download(
                        filepath=f"{path_download}/{title}.{fname.split('.')[-1]}",
                        callback=self.show_progress
                    )
                else:
                    with io.open(f"{path_download}/{title}.lrc", 'w', encoding='utf-8-sig') as f:
                        f.write(lyric)
                    sys.stdout.write(fg + '[' + fc + '*' + fg + '] : Done.\n')
            else:
                sys.stdout.write(fg + '[' + fr + '*' + fg + f"] : {title} dont't have Lyric .")
            sys.stdout.write('\n')
            return

        title = f.get('title') or data.get('title') or data.get('alias')
        sys.stdout.write(fg + '[' + fc + '*' + fg + f'] :   {title} .\n')
        title = removeCharacter_filename(title)

        if not data:  # video-clip
            # title = f.get('title')
            # title = removeCharacter_filename(title)
            source = try_get(f, lambda x: x['source'])
            url, label_best, ext = get_best_label_video(source)
            if not url:
                sys.stdout.write(fg + '[' + fr + '*' + fg + f"] : {title} don't have video.\n\n")
                time.sleep(5)
                return
            sys.stdout.write(fg + '[' + fc + '*' + fg + f'] : Downloading {title} .\n')
            path_download = os.path.join(self._path_save, 'DOWNLOAD')
            if not os.path.exists(path=path_download):
                os.mkdir(path_download)
            if not url.startswith('http') or not url.startswith('https'):
                url = 'https:' + url
            down = Downloader(url=url)
            down.download(
                filepath='%s/%s_%s.mp4' % (path_download, title, label_best),
                callback=self.show_progress
            )
            sys.stdout.write('\n\n')
            return

        lyric = data.get('lyric') or try_get(data, lambda x: x['lyrics'][0]['content'])
        sources = try_get(data, lambda x: x['streaming']['default'])

        if not sources:
            song_items = try_get(data, lambda x: x['song']['items'])
            if not song_items:
                sys.stdout.write(fg + '[' + fr + '*' + fg + f"] : {try_get(data, lambda x: x['streaming']['msg'])}.\n")
            else:
                for song in song_items:
                    self.real_extract_media(
                        type=search_regex(r'(?x)\/(.*?)\/', song.get('link')),
                        video_id=song.get('id'),
                    )
        else:
            path_download = os.path.join(self._path_save, 'DOWNLOAD')
            if not os.path.exists(path=path_download):
                os.mkdir(path_download)
            if self._down_lyric is True and self._down_media is False:
                down_lyric()
            elif self._down_lyric is False and self._down_media is True:
                down_media()
            else:
                down_media()
                down_lyric()
        sys.stdout.write('\n\n')
        return

    def get_api(self, name_api, video_id='', type='', new_release=False):
        API_KEY = '38e8643fb0dc04e8d65b99994d3dafff'
        SECRET_KEY = b'10a01dcf33762d3a204cb96429918ff6'
        if not name_api:
            return

        def get_hash256(string):
            return hashlib.sha256(string.encode('utf-8')).hexdigest()

        def get_hmac512(string):
            return hmac.new(SECRET_KEY, string.encode('utf-8'), hashlib.sha512).hexdigest()

        def get_request_path(data):
            def mapping(key, value):
                return quote(key) + "=" + quote(value)

            data = [mapping(k, v) for k, v in data.items()]
            data = "&".join(data)
            return data

        def get_api_by_id(id):
            url = f"https://zingmp3.vn/api{name_api}?id={id}&"
            time = str(int(datetime.datetime.now().timestamp()))
            sha256 = get_hash256(f"ctime={time}id={id}")

            data = {
                'ctime': time,
                'api_key': API_KEY,
                'sig': get_hmac512(f"{name_api}{sha256}")
            }
            return url + get_request_path(data)

        def get_api_chart(type):
            url = f"https://zingmp3.vn/api{name_api}?type={type}&"
            time = str(int(datetime.datetime.now().timestamp()))
            sha256 = get_hash256(f"ctime={time}")

            data = {
                'ctime': time,
                'api_key': API_KEY,
                'sig': get_hmac512(f"{name_api}{sha256}")
            }
            return url + get_request_path(data)

        def get_api_new_release():
            url = f"https://zingmp3.vn/api{name_api}?"
            time = str(int(datetime.datetime.now().timestamp()))
            sha256 = get_hash256(f"ctime={time}")

            data = {
                'ctime': time,
                'api_key': API_KEY,
                'sig': get_hmac512(f"{name_api}{sha256}")
            }
            return url + get_request_path(data)

        def get_api_download(id):
            url = f"https://download.zingmp3.vn/api{name_api}?id={id}&"
            time = str(int(datetime.datetime.now().timestamp()))
            sha256 = get_hash256(f"ctime={time}id={id}")

            data = {
                'ctime': time,
                'api_key': API_KEY,
                'sig': get_hmac512(f"{name_api}{sha256}")
            }
            return url + get_request_path(data)

        if 'download' in name_api:
            return get_api_download(id=video_id)

        if video_id:
            return get_api_by_id(video_id)
        if type:
            return get_api_chart(type)
        if new_release == True:
            return get_api_new_release()
        return


def main(argv):
    parser = argparse.ArgumentParser(description='Zingmp3 - A tool crawl data from zingmp3.vn .')
    parser.add_argument('url', type=str, help='Url.')

    authen = parser.add_argument_group('Authentication')
    authen.add_argument('-c', '--cookies', dest='path_cookies', type=str, help='Cookies for authenticate with.',
                        metavar='')

    opts = parser.add_argument_group("Options")
    opts.add_argument('-q', '--quality', type=str, help='Set quality want to download.', dest='quality', metavar='')
    opts.add_argument('-s', '--save', type=str, default=os.getcwd(), help='Path to save', dest='path_save', metavar='')
    opts.add_argument('-j', '--json', default=False, action='store_true', help="Show json of info media.",
                      dest='show_json_info')
    opts.add_argument('-l', '--only-lyric', default=False, action='store_true', help='Download only lyric.',
                      dest='down_lyric')
    opts.add_argument('-m', '--only-media', default=False, action='store_true', help='Download only media.',
                      dest='down_media')

    args = parser.parse_args()
    status_auth = False
    if args.path_cookies:
        auth = authentication(path_cookies=args.path_cookies)
        status_auth = auth.auth_with_cookies()
        if status_auth:
            sys.stdout.write(fg + '[' + fc + '*' + fg + '] : Login oki.\n')
        else:
            sys.stdout.write(fg + '[' + fc + '*' + fg + '] : Login false.\n')
    extract = extractZingMp3(
        url=args.url,
        path_save=args.path_save,
        show_json_info=args.show_json_info,
        down_lyric=args.down_lyric,
        down_media=args.down_media,
        is_login=status_auth,
        quality=args.quality
    )
    extract.run()


if __name__ == '__main__':
    try:
        if sys.stdin.isatty():
            main(sys.argv)
        else:
            argv = sys.stdin.read().split(' ')
            main(argv)
    except KeyboardInterrupt:
        sys.stdout.write(
            fc + sd + "\n[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "User Interrupted..\n")
        sys.exit(0)
