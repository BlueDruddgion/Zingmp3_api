# ***Zingmp3***
Zingmp3 - A tool crawl data from [`zingmp3.vn`](https://zingmp3.vn/) or [`mp3.zing.vn`](https://mp3.zing.vn/) (use api).

[![Capture.png](https://i.postimg.cc/Nf6Hx9nL/Capture.png)](https://postimg.cc/CzK5h1SV)

[![Capture.png](https://i.postimg.cc/C5HxbDKg/Capture.png)](https://postimg.cc/Fkzv4YcW)
## ***Installation***
 - **Language**: Python3.x
 
 - **Module**: requests, colorama
    ```
    pip install -r requirements.txt
    ``` 
    
## ***Options***
  - `-c` or `--cookies`: Add cookies to auth
  - `-q` or `--quality` : Set quality want to download like ( 128,320,lossless for 'bai-hat' ) or ( 360,480,720,1080 for 'video' )
  - `-j` or `json` : Show json of info media. 
  - `-s` or `--save` : Path to save file downloaded.
  - `-l` or `--only-lyric` : Download only lyric.
  - `-m` or `--only-media` : Download only media.
  - Default will download all media and lyric.
  - All the example in Usage.
 
## ***All URL Supported***
- **url media**
    ```
    https://zingmp3.vn/video-clip/.../<id>.html
    https://zingmp3.vn/bai-hat/.../<id>.html
    https://zingmp3.vn/playlist/.../<id>.html
    https://zingmp3.vn/album/.../<id>.html
    https://zingmp3.vn/embed/.../<id>.html
    ```
- **url artist's profile type 1**
    ```
    https://zingmp3.vn/nghe-si/<name_artist>/video
    https://zingmp3.vn/nghe-si/<name_artist>/playlist
    https://zingmp3.vn/nghe-si/<name_artist>/bai-hat
    https://zingmp3.vn/nghe-si/<name_artist>/album
    ```
- **url artist's profile type 2**
    ```
    https://zingmp3.vn/<name_artist>/bai-hat
    https://zingmp3.vn/<name_artist>/playlist
    https://zingmp3.vn/<name_artist>/video
    https://zingmp3.vn/<name_artist>/album
    ```
- **url #ZINGCHART**
    ```
    https://zingmp3.vn/zing-chart/bai-hat.html
    https://zingmp3.vn/zing-chart/video.html
    https://zingmp3.vn/zing-chart-tuan/bai-hat-Viet-Nam/<id>.html
    https://zingmp3.vn/zing-chart-tuan/video-US-UK/<id>.html
    ```
- **url new release**
    ```
    https://zingmp3.vn/top-new-release/index.html
    ```
 
## ***How to get cookies.txt for login***
 If you want to use your account VIP to download quality like lossless ....
 
 1. Download extension from chrome store [`cookies.txt`](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg)
 2. Go to page [`zingmp3`](https://zingmp3.vn/)
 3. Click to icon cookies.txt just download
 4. Click to `click here` and save file cookies.txt
 5. Get cookies.txt then put it to them same path with tool, then run
 
 Sometime cookies will die, Pls follow the steps above to update the new cookies.
  
 If you don't set cookies, tool will download default quality like 128 ...
## ***Usage***
[![Capture.png](https://i.postimg.cc/9XBjGGMF/Capture.png)](https://postimg.cc/K44Vb3Bd)
 - **Install module**
    ```
    pip install -r requirements.txt
    ```
 - **Run**
    ```
    python zingmp3.py https://zingmp3.vn/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html
    ``` 
 - **Download with cookies**
  
    ```
    python zingmp3.py -c cookies.txt https://zingmp3.vn/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html
    ```
 - **Set quality want download**
 
    No cookies
    ```
    python zingmp3.py -q lossless https://zingmp3.vn/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html
    ```
    
    with cookies
    ```
    python zingmp3.py -c cookies.txt -q lossless https://zingmp3.vn/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html
    ```
    
    Video
    ```
    python zingmp3.py -q 1080 https://zingmp3.vn/video-clip/Em-Gi-Oi-Jack-K-ICM/ZWAEFWIF.html
    ```
    
 - **Show json of info media**
     ```
     python zingmp3.py -j https://zingmp3.vn/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html
     ```
   ```json
    {
        "err": 0,
        "msg": "Success",
        "data": {
            "id": "ZWBI0DFI",
            "title": "Khóc Cùng Em",
            "artists": [
                {
                    "id": "IWZ98609",
                    "name": "Mr Siro",
                    "link": "/nghe-si/Mr-Siro",
                    "cover": "https://photo-zmp3.zadn.vn/cover_artist/a/6/2/1/a62188a5db16a4ce31c80fd5420edb92.jpg",
                    "thumbnail": "https://photo-resize-zmp3.zadn.vn/w240_r1x1_jpeg/avatars/e/1/1/2/e1120261421cfec7513423222b0ca94c.jpg",
                    "spotlight": true,
                    "follow": 279349,
                    "oa_link": "/mrsiro"
                },
                {
                    "id": "IW6Z8BZB",
                    "name": "Gray",
                    "link": "/nghe-si/Gray-Moi",
                    "cover": "//static-zmp3.zadn.vn/dev/skins/zmp3-v5.2/images/default_cover.png",
                    "thumbnail": "https://photo-resize-zmp3.zadn.vn/w240_r1x1_jpeg/avatars/1/f/d/8/1fd885b98a30c0e981508d3c49c9ce17.jpg",
                    "spotlight": false,
                    "follow": 94
                },
                {
                    "id": "IW6Z8BZC",
                    "name": "Wind",
                    "link": "/nghe-si/Wind-Moi",
                    "cover": "//static-zmp3.zadn.vn/dev/skins/zmp3-v5.2/images/default_cover.png",
                    "thumbnail": "https://photo-resize-zmp3.zadn.vn/w240_r1x1_jpeg/avatars/c/2/9/7/c2974a4c3621ba90cfee7b97a48f83a0.jpg",
                    "spotlight": false,
                    "follow": 99
                }
            ],
            "artists_names": "Mr Siro, Gray, Wind",
            "raw_id": 1079491953,
            "alias": "Khoc-Cung-Em-Mr-Siro-Gray-Wind",
            "is_zma": false,
            "link": "/bai-hat/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html",
            "thumbnail": "https://photo-resize-zmp3.zadn.vn/w94_r1x1_jpeg/cover/a/c/7/3/ac735f3acd59d62b611d9b0712a4ff75.jpg",
            "isOffical": true,
            "user_name": "",
            "mv_link": "/video-clip/Khoc-Cung-Em-Mr-Siro-Gray-Wind/ZWBI0DFI.html",
            "zing_choise": false,
            "allow_audio_ads": true,
            "thumbnail_medium": "https://photo-resize-zmp3.zadn.vn/w240_r1x1_jpeg/cover/a/c/7/3/ac735f3acd59d62b611d9b0712a4ff75.jpg",
            "lyric": "https://static-zmp3.zadn.vn/lyrics/6/f/7/f/6f7ff7c5f438782a40ea3815ced608ba.lrc",
            "listen": 18094864,
            "status_name": "Hiển thị",
            "status_code": 1,
            "created_at": 1582166894,
            "released_at": 1582203600,
            "privacy": "public",
            "streaming_status": 1,
            "isVN": true,
            "duration": 236,
            "public_status": 0,
            "is_worldwide": true,
            "username": "",
            "userid": 384,
            "genres": [
                {
                    "id": "IWZ9Z08I",
                    "name": "Việt Nam",
                    "alias": "viet-nam",
                    "link": "/the-loai-album/Viet-Nam/IWZ9Z08I.html"
                },
                {
                    "id": "IWZ9Z088",
                    "name": "Nhạc Trẻ",
                    "alias": "nhac-tre",
                    "link": "/the-loai-album/Nhac-Tre/IWZ9Z088.html"
                },
                {
                    "id": "IWZ97FCD",
                    "name": "V-Pop",
                    "alias": "v-pop",
                    "link": "/the-loai-album/V-Pop/IWZ97FCD.html"
                }
            ],
            "album": {
                "raw_id": 1295448593,
                "id": "ZF90UA9I",
                "link": "/album/Khoc-Cung-Em-Single-Mr-Siro-Gray-Wind/ZF90UA9I.html",
                "title": "Khóc Cùng Em (Single)",
                "isoffical": true,
                "play_item_mode": 0,
                "isalbum": true,
                "is_single": true,
                "is_shuffle": false,
                "isPR": false,
                "release_date": "2020",
                "artists_names": "Mr Siro, Gray, Wind",
                "artists": [
                    {
                        "name": "Mr Siro",
                        "link": "/nghe-si/Mr-Siro",
                        "id": "IWZ98609",
                        "spotlight": true
                    },
                    {
                        "name": " Gray",
                        "link": "/nghe-si/Gray-Moi",
                        "id": "IW6Z8BZB",
                        "spotlight": false
                    },
                    {
                        "name": " Wind",
                        "link": "/nghe-si/Wind-Moi",
                        "id": "IW6Z8BZC",
                        "spotlight": false
                    }
                ],
                "subType": 0,
                "thumbnail": "https://photo-resize-zmp3.zadn.vn/w165_r1x1_jpeg/cover/a/c/7/3/ac735f3acd59d62b611d9b0712a4ff75.jpg",
                "thumbnail_medium": "https://photo-resize-zmp3.zadn.vn/w480_r1x1_jpeg/cover/a/c/7/3/ac735f3acd59d62b611d9b0712a4ff75.jpg",
                "listen": 0,
                "privacy": "public",
                "uid": "IWZ9ZW00",
                "user_name": ""
            },
            "composers": [
                {
                    "id": "IWZ98609",
                    "name": "Mr Siro",
                    "link": "/nghe-si/Mr-Siro",
                    "cover": "https://photo-zmp3.zadn.vn/cover_artist/a/6/2/1/a62188a5db16a4ce31c80fd5420edb92.jpg",
                    "thumbnail": "https://photo-resize-zmp3.zadn.vn/w240_r1x1_jpeg/avatars/e/1/1/2/e1120261421cfec7513423222b0ca94c.jpg",
                    "spotlight": true,
                    "follow": 279349,
                    "oa_link": "/mrsiro"
                }
            ],
            "content_owner": {
                "id": 7,
                "name": "Zing"
            },
            "lyrics": [
                {
                    "id": "IWCZAU88",
                    "content": "Cuộc gọi đến, và như mọi khi\n<br>Là lặng nghe em khóc\n<br>I try so very hard to listen your story\n<br>But you don’t know it hurts me so bad\n<br>Cầu trời chóng ấm\n<br>Đêm đông buốt giá kia sẽ bớt lạnh\n<br>Đôi tay giấu ác mộng dọa dẫm\n<br>Hy vọng càng mong manh\n<br>Vùi chôn tổn thương\n<br>Tội con tim này đơn phương\n<br>Chờ đợi một người\n<br>Dù biết chẳng có cơ hội\n<br>Điều gì nhẫn tâm hơn sự im lặng?\n<br>Muộn phiền người trút lên đôi vai này\n<br>Rồi ngày mai còn cần anh không?\n<br>Một vòng tròn tối tăm không ra lối\n<br>Đó là những gì mà anh \n<br>Phải kìm nén tất cả đau đớn, tủi thân\n<br>Để bên em\n<br>Làm gì để ngần ấy vết dao khép lại\n<br>Để giấu đi bao nỗi đau trĩu nặng\n<br>Sợ ngày nào nếu tim vỡ trăm mảnh\n<br>Chỉ còn lại vài nhịp mong manh\n<br>Chuyện tình về trái tim sắp gục ngã\n<br>Bên hai trái tim hạnh phúc\n<br>Họa thành bức tranh về tình yêu\n<br>Trong đó mờ tên anh\n<br>\n<br>I don’t know why\n<br>I need you so bad\n<br>Em luôn xa con tim này\n<br>Vì em không yêu sao có thể hiểu \n<br>Mình như đường thẳng song song vậy\n<br>Vì chưa từng có làm sao thiếu\n<br>Phải lặng lẽ ở bên\n<br>Tàn sức thương một người không lối thoát\n<br>Chờ đợi một người\n<br>Dù biết chẳng có cơ hội\n<br>Điều gì nhẫn tâm hơn sự im lặng?\n<br>Muộn phiền người trút lên đôi vai này\n<br>Rồi ngày mai còn cần anh không?\n<br>Một vòng tròn tối tăm không ra lối\n<br>Đó là những gì mà anh \n<br>Phải kìm nén tất cả đau đớn, tủi thân\n<br>Để bên em\n<br>Làm gì để ngần ấy vết dao khép lại\n<br>Để giấu đi bao nỗi đau trĩu nặng\n<br>Sợ ngày nào nếu tim vỡ trăm mảnh\n<br>Chỉ còn lại vài nhịp mong manh\n<br>Chuyện tình về trái tim sắp gục ngã\n<br>Bên hai trái tim hạnh phúc\n<br>Họa thành bức tranh về tình yêu\n<br>Trong đó mờ tên anh\n<br>\n<br>Mùa đông và nỗi nhớ tựa như tri kỷ\n<br>Nghìn năm không rời\n<br>Lạnh môi tay khẽ run từng đêm một mình\n<br>Vì nhớ bóng hình\n<br>Giờ em nghĩ đến ai\n<br>Mà môi không ngừng cười\n<br>Please don’t do it any more!\n<br>Chờ đợi một người\n<br>Dù biết chẳng có cơ hội\n<br>Điều gì nhẫn tâm hơn sự im lặng?\n<br>Muộn phiền người trút lên đôi vai này\n<br>Rồi ngày mai còn cần anh không?\n<br>Một vòng tròn tối tăm không ra lối\n<br>Đó là những gì mà anh \n<br>Phải kìm nén tất cả đau đớn, tủi thân\n<br>Để bên em\n<br>Làm gì để ngần ấy vết dao khép lại\n<br>Để giấu đi bao nỗi đau trĩu nặng\n<br>Sợ ngày nào nếu tim vỡ trăm mảnh\n<br>Chỉ còn lại vài nhịp mong manh\n<br>Chuyện tình về trái tim sắp gục ngã\n<br>Bên hai trái tim hạnh phúc\n<br>Họa thành bức tranh về tình yêu\n<br>Trong đó mờ tên anh\n<br>Cuộc gọi đến, và như mọi khi\n<br>Là lặng nghe em khóc\n<br>I try so very hard to listen your story\n<br>But you don’t know it hurts me so bad",
                    "username": "mp3",
                    "order": 1
                }
            ],
            "total_comment": 2721,
            "like": 999771,
            "streaming": {
                "default": {
                    "128": "//mp3-s1-zmp3.zadn.vn/45d6357d2b3ac2649b2b/4421039131854997609?authen=exp=1584071828~acl=/45d6357d2b3ac2649b2b/*~hmac=b6dfe6d32a65061fa31646780a29ae59",
                    "320": ""
                },
                "err": 0,
                "msg": "Success"
            }
        },
        "timestamp": 1583899963132
    }
    ```

## ***Note***
- All file downloaded in folder DOWNLOAD at the same path
- If there's an error or problem, please write issue out here
 [`zingmp3 issues`](https://github.com/hatienl0i261299/Zingmp3_api/issues)
- FB: 100011734236090
