import subprocess

url2 = "https://rr1---sn-4g5lznl7.googlevideo.com/videoplayback?expire=1794260668&ei=nCLyarDoB7mvw-APy8n1oAE&ip=176.41.43.122&id=0fa1a96f7a32e781&itag=18&source=contrib_service_geo_ugc&begin=0&requiressl=yes&xpc=EghoqJzIP3oBAQ==&rms=su,su&sc=yes&susc=gugc&app=fife&ic=1061&eaua=Aaz2Nyfyfhw&pcm2=yes&mime=video/mp4&vprv=1&rqh=1&dur=20.758&lmt=1726182677316980&cpn=4FjXvRtmqaKNcqAq&txp=0000224&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,susc,app,ic,eaua,pcm2,mime,vprv,rqh,dur,lmt&sig=AE0s2JYwRQIhAPRLMiBzAYHcQIIEgrK99J9CfsmBZRCE-M1rAsqncLUMAiA77R2TeVJhMirvWJahANCurRbzD0Xnfnbpgt_tQK_DEg==&redirect_counter=1&cm2rm=sn-nv4zd7l&rrc=191&req_id=884f62b3719936e2&cms_redirect=yes&cmsv=e&met=1794253468,&mh=rv&mm=34&mn=sn-4g5lznl7&ms=ltu&mt=1794253061&mv=m&mvi=1&pl=19&lsparams=met,mh,mm,mn,ms,mv,mvi,pl,rms,sc&lsig=APaTxxMwRgIhAPkBpebSyZk_8Ta_zebF6A_tMbiI5PZyUxSpKVrOO3O_AiEA16GzWl8Bl1eH35ftzTDEXg3GBfFOyMAQRBmuS52eJ2Q%3D"

res = subprocess.run([
    "curl.exe", "-s", "-L",
    "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "-H", "Referer: https://www.google.com/",
    "-o", "assets/videos/salon-lazer-uygulama.mp4",
    url2
])
print("Curl return code for video 2:", res.returncode)
