import os
import urllib.request

video1_url = "https://rr3---sn-4g5e6nze.googlevideo.com/videoplayback?expire=1794260659&ei=kyLyaoTwAY-qw-AP57PScA&ip=176.41.43.122&id=e80895ac48f47ae0&itag=18&source=contrib_service_geo_ugc&begin=0&requiressl=yes&xpc=EghoqJzIP3oBAQ==&rms=su,su&sc=yes&susc=gugc&app=fife&ic=1061&eaua=Aaz2Nyfyfhw&pcm2=yes&mime=video/mp4&vprv=1&rqh=1&dur=18.250&lmt=1726205072709225&cpn=YcSDl1-XqUo1AArp&txp=0000224&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,susc,app,ic,eaua,pcm2,mime,vprv,rqh,dur,lmt&sig=AE0s2JYwRQIhAPfbxLq5YOdTjd1OJ7UQQga2hd3ANaR3udVpLJ-VboSZAiBfI7CrvUEfBF5C4O1iwd6ryIj8ooNTsEZAOaq8v3znbQ==&redirect_counter=1&cm2rm=sn-nv4z67z&rrc=191&req_id=cf119709ce3a36e2&cms_redirect=yes&cmsv=e&met=1794253459,&mh=Oc&mm=34&mn=sn-4g5e6nze&ms=ltu&mt=1794253061&mv=m&mvi=3&pl=19&lsparams=met,mh,mm,mn,ms,mv,mvi,pl,rms,sc&lsig=APaTxxMwRQIhAOFNF5bKZRptqTb-Zo8GzECa-Ulqbpq4_ShFK3cY3StkAiAuZxDNqva4DmlQJOP8ZSL_p-Ykqf1k-9hXAF_l155SiQ%3D%3D"
video2_url = "https://rr1---sn-4g5lznl7.googlevideo.com/videoplayback?expire=1794260668&ei=nCLyarDoB7mvw-APy8n1oAE&ip=176.41.43.122&id=0fa1a96f7a32e781&itag=18&source=contrib_service_geo_ugc&begin=0&requiressl=yes&xpc=EghoqJzIP3oBAQ==&rms=su,su&sc=yes&susc=gugc&app=fife&ic=1061&eaua=Aaz2Nyfyfhw&pcm2=yes&mime=video/mp4&vprv=1&rqh=1&dur=20.758&lmt=1726182677316980&cpn=4FjXvRtmqaKNcqAq&txp=0000224&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,susc,app,ic,eaua,pcm2,mime,vprv,rqh,dur,lmt&sig=AE0s2JYwRQIhAPRLMiBzAYHcQIIEgrK99J9CfsmBZRCE-M1rAsqncLUMAiA77R2TeVJhMirvWJahANCurRbzD0Xnfnbpgt_tQK_DEg==&redirect_counter=1&cm2rm=sn-nv4zd7l&rrc=191&req_id=884f62b3719936e2&cms_redirect=yes&cmsv=e&met=1794253468,&mh=rv&mm=34&mn=sn-4g5lznl7&ms=ltu&mt=1794253061&mv=m&mvi=1&pl=19&lsparams=met,mh,mm,mn,ms,mv,mvi,pl,rms,sc&lsig=APaTxxMwRgIhAPkBpebSyZk_8Ta_zebF6A_tMbiI5PZyUxSpKVrOO3O_AiEA16GzWl8Bl1eH35ftzTDEXg3GBfFOyMAQRBmuS52eJ2Q%3D"

os.makedirs("assets/videos", exist_ok=True)

print("Downloading video 1 (cilt-bakimi-uygulama.mp4)...")
req1 = urllib.request.Request(video1_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req1, timeout=30) as resp, open("assets/videos/cilt-bakimi-uygulama.mp4", "wb") as f:
    f.write(resp.read())
print("Video 1 saved, size:", os.path.getsize("assets/videos/cilt-bakimi-uygulama.mp4"))

print("Downloading video 2 (salon-tanitim.mp4)...")
req2 = urllib.request.Request(video2_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req2, timeout=30) as resp, open("assets/videos/salon-tanitim.mp4", "wb") as f:
    f.write(resp.read())
print("Video 2 saved, size:", os.path.getsize("assets/videos/salon-tanitim.mp4"))
