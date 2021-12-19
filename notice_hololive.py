##########################################################
# Hololive Live Stream Notification                      #
# https://qiita.com/k0gane_p/items/4796d0e80097f93af656  #
##########################################################
import time
import requests
import json
import copy
from datetime import datetime, timedelta, timezone

class Holo_live:
    #配信者のチャンネルID, 配信者名, アイコン画像のURLのリスト
    Hololive = {
        "UCp6993wxpyDPHUpavwDFqgg": [
            "ときのそら",
            "https://yt3.ggpht.com/a/AATXAJzGvZJuJ92qM5WcfBcDZqPFSj_CGIEYp9VFmA=s288-c-k-c0xffffffff-no-rj-mo"
        ],
        "UC1uv2Oq6kNxgATlCiez59hw": [
            "常闇トワ",
            "https://yt3.ggpht.com/a/AATXAJxqyp7DhLSSrSYRc5HaLcq5QvJvRp3jDnxTeA=s288-c-k-c0xffffffff-no-rj-mo"
        ],
        "UCa9Y57gfeY0Zro_noHRVrnw": [
            "姫森ルーナ",
            "https://yt3.ggpht.com/a/AATXAJzzirDjRJkofWVeoE6gVjodJ0VXaJhy4b_CLg=s288-c-k-c0xffffffff-no-rj-mo"
        ]

    }  
    #ホロライブ配信開始
    webhook_url_Hololive = 'https://discord.com/api/webhooks/922085339819044894/uoYC-z5Q2zXTA_J5-UklW8WlSb4ECpCwgUKGNRBpioq32HTo0r4pGyQQGWetSg_TUGLt' 
    #ホロライブ配信予定
    webhook_url_Hololive_yotei = 'https://discord.com/api/webhooks/922085778333507604/UvJ9tIiBRxUSbPL14YWe2PZwycRV_nMXAZ3GOHJ3N8qXGCHf24-cMpgFzPlislkC9kqY' 
    #配信予定のデータを格納
    broadcast_data = {} 

    YOUTUBE_API_KEY = ["AIzaSyC45K7Ldj3l9Rjoub4QaedDC3atwYN9Ze8"]
    def dataformat_for_python(at_time):
        at_year = int(at_time[0:4])
        at_month = int(at_time[5:7])
        at_day = int(at_time[8:10])
        at_hour = int(at_time[11:13])
        at_minute = int(at_time[14:16])
        at_second = int(at_time[17:19])
        return datetime(at_year, at_month, at_day, at_hour, at_minute, at_second)

    def replace_JST(s):
        a = s.split("-")
        u = a[2].split(" ")
        t = u[1].split(":")
        time = [int(a[0]), int(a[1]), int(u[0]), int(t[0]), int(t[1]), int(t[2])]
        if(time[3] >= 15):
            time[2] += 1
            time[3] = time[3] + 9 - 24
        else:
            time[3] += 9
        return (str(time[0]) + "/" + str(time[1]).zfill(2) + "/" + str(time[2]).zfill(2) + " " + str(time[3]).zfill(2) + "-" + str(time[4]).zfill(2) + "-" + str(time[5]).zfill(2))

    def post_to_discord(userId, videoId):
        #配信URL
        haishin_url = "https://www.youtube.com/watch?v=" + videoId
        #Discordに投稿される文章
        content = "配信中！\n" + haishin_url
        main_content = {
            #配信者名, アイコン, 文章
            "username": Hololive[userId][0],
            "avatar_url": Hololive[userId][1],
            "content": content
        }
        requests.post(webhook_url_Hololive, main_content) #Discordに送信
        broadcast_data.pop(videoId)

    def get_information():
        tmp = copy.copy(broadcast_data)
        #現在どのYouTube APIを使っているかを記録
        api_now = 0
        for idol in Hololive:
            api_link = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + idol + "&key=" + YOUTUBE_API_KEY[api_now] + "&eventType=upcoming&type=video"
            #apiを1つずらす
            api_now = (api_now + 1) % len(YOUTUBE_API_KEY)
            aaa = requests.get(api_link)
            v_data = json.loads(aaa.text)
            try:
                #各配信予定動画データに関して
                for item in v_data['items']:
                    broadcast_data[item['id']['videoId']] = {'channelId':item['snippet']['channelId']} 
                for video in broadcast_data:
                    try:
                        #既にbroadcast_dataにstarttimeがあるかチェック
                        a = broadcast_data[video]['starttime']
                    except KeyError:
                        aaaa = requests.get("https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id=" + video + "&key=" + YOUTUBE_API_KEY[api_now])
                        api_now = (api_now + 1) % len(YOUTUBE_API_KEY) 
                        vd = json.loads(aaaa.text)
                        print(vd)
                        broadcast_data[video]['starttime'] = vd['items'][0]['liveStreamingDetails']['scheduledStartTime']
            except KeyError: 
                #配信予定がなくて403が出た
                continue
        for vi in broadcast_data:
            if(not(vi in tmp)):
                print(broadcast_data[vi])
                try:
                    post_broadcast_schedule(broadcast_data[vi]['channelId'], vi, broadcast_data[vi]['starttime'])
                except KeyError:
                    continue

    def check_schedule(now_time, broadcast_data):
        for bd in list(broadcast_data):
            try:
                # RFC 3339形式 => datetime
                #配信スタート時間をdatetime型で保管
                sd_time = datetime.strptime(broadcast_data[bd]['starttime'], '%Y-%m-%dT%H:%M:%SZ') 
                sd_time += timedelta(hours=9)
                #今の方が配信開始時刻よりも後だったら
                if(now_time >= sd_time):
                    post_to_discord(broadcast_data[bd]['channelId'], bd)
            except KeyError:
                continue

    def post_broadcast_schedule(userId, videoId, starttime):
        st = starttime.replace('T', ' ')
        sst = st.replace('Z', '')
        ssst = replace_JST(sst)
        haishin_url = "https://www.youtube.com/watch?v=" + videoId
        #Discordに投稿される文章
        content = ssst + "に配信予定！\n" + haishin_url
        main_content = {
            "username": Hololive[userId][0],
            "avatar_url": Hololive[userId][1],
            "content": content
        }
        #Discordに送信

        requests.post(webhook_url_Hololive_yotei, main_content)
    while True:

        now_time = datetime.now() + timedelta(hours=9)
        if((now_time.minute == 0) and (now_time.hour % 2 == 0)):
            get_information()
        check_schedule(now_time, broadcast_data)
        time.sleep(60)

        
