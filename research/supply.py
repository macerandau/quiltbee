import json, time, urllib.parse, urllib.request, statistics, sys, datetime
terms = [l.strip() for l in open('terms.txt') if l.strip()]
rows=[]
for t in terms:
    url="https://itunes.apple.com/search?"+urllib.parse.urlencode({'term':t,'entity':'software','country':'us','limit':50})
    for attempt in range(4):
        try:
            d=json.load(urllib.request.urlopen(url,timeout=20)); break
        except Exception as e:
            time.sleep(5*(attempt+1)); d={'results':[]}
    res=d.get('results',[])
    rc=[r.get('userRatingCount',0) for r in res]
    rc_sorted=sorted(rc,reverse=True)
    top5=rc_sorted[:5]
    stale=0; now=datetime.datetime.now(datetime.timezone.utc)
    for r in res[:10]:
        try:
            dt=datetime.datetime.fromisoformat(r['currentVersionReleaseDate'].replace('Z','+00:00'))
            if (now-dt).days>365: stale+=1
        except Exception: pass
    top=sorted(res,key=lambda r:r.get('userRatingCount',0),reverse=True)[:3]
    topnames="; ".join(f"{r['trackName'][:28]} ({r.get('userRatingCount',0)}★{r.get('averageUserRating',0):.1f} {r.get('formattedPrice','')})" for r in top)
    rows.append((t,len(res),sum(top5),rc_sorted[0] if rc_sorted else 0, int(statistics.median(rc)) if rc else 0, sum(1 for x in rc if x>=1000), stale, topnames))
    time.sleep(3.2)
json.dump(rows,open('supply.json','w'))
print(f"{'term':32} {'n':>3} {'top5sum':>8} {'max':>7} {'med':>5} {'>=1k':>4} {'stale10':>7}  top3")
for r in sorted(rows,key=lambda r:r[2]):
    print(f"{r[0]:32} {r[1]:3} {r[2]:8} {r[3]:7} {r[4]:5} {r[5]:4} {r[6]:7}  {r[7]}")
