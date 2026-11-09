import subprocess

url = "https://rr3---sn-4g5e6nze.googlevideo.com/videoplayback?expire=1794260659&ei=kyLyaoTwAY-qw-AP57PScA&ip=176.41.43.122&id=e80895ac48f47ae0&itag=18&source=contrib_service_geo_ugc&begin=0&requiressl=yes&xpc=EghoqJzIP3oBAQ==&rms=su,su&sc=yes&susc=gugc&app=fife&ic=1061&eaua=Aaz2Nyfyfhw&pcm2=yes&mime=video/mp4&vprv=1&rqh=1&dur=18.250&lmt=1726205072709225&cpn=YcSDl1-XqUo1AArp&txp=0000224&sparams=expire,ei,ip,id,itag,source,requiressl,xpc,susc,app,ic,eaua,pcm2,mime,vprv,rqh,dur,lmt&sig=AE0s2JYwRQIhAPfbxLq5YOdTjd1OJ7UQQga2hd3ANaR3udVpLJ-VboSZAiBfI7CrvUEfBF5C4O1iwd6ryIj8ooNTsEZAOaq8v3znbQ==&redirect_counter=1&cm2rm=sn-nv4z67z&rrc=191&req_id=cf119709ce3a36e2&cms_redirect=yes&cmsv=e&met=1794253459,&mh=Oc&mm=34&mn=sn-4g5e6nze&ms=ltu&mt=1794253061&mv=m&mvi=3&pl=19&lsparams=met,mh,mm,mn,ms,mv,mvi,pl,rms,sc&lsig=APaTxxMwRQIhAOFNF5bKZRptqTb-Zo8GzECa-Ulqbpq4_ShFK3cY3StkAiAuZxDNqva4DmlQJOP8ZSL_p-Ykqf1k-9hXAF_l155SiQ%3D%3D"

res = subprocess.run([
    "curl.exe", "-s", "-L",
    "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "-H", "Referer: https://www.google.com/",
    "-o", "assets/videos/cilt-bakimi-uygulama.mp4",
    url
])
print("Curl return code:", res.returncode)
