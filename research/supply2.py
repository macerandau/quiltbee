import json, time, urllib.parse, urllib.request, statistics, datetime, os
# term -> stems that must appear in name+description for a result to count as a real competitor
T = {
 "expiration date tracker": ["expir","pantry","food waste","best before"],
 "pantry expiration": ["expir","pantry","food waste"],
 "memorize lines": ["memoriz","rehears","script","lines"],
 "flock camera map": ["flock","alpr","license plate reader","surveillance camera map","deflock"],
 "alpr camera map": ["flock","alpr","license plate reader","surveillance"],
 "quilt design": ["quilt"],
 "quilt pattern designer": ["quilt"],
 "knitting row counter": ["knit","crochet","row counter"],
 "jet lag": ["jet lag","jetlag","circadian"],
 "jet lag planner": ["jet lag","jetlag","circadian"],
 "turbulence forecast": ["turbulence"],
 "turbulence": ["turbulence"],
 "volunteer hours tracker": ["volunteer"],
 "volunteer hours": ["volunteer"],
 "games attended tracker": ["attended","stadium","ballpark","games i've been","been to"],
 "sports games attended": ["attended","stadium","ballpark","been to"],
 "walk up song": ["walk-up","walk up","walkup"],
 "walk-up songs baseball": ["walk-up","walk up","walkup"],
 "pupillary distance": ["pupillary","pd measure","pupil"],
 "insect sound identifier": ["insect","cricket","bug"],
 "cricket sound identifier": ["insect","cricket","bug"],
 "pressed penny": ["pressed penn","elongated","penny"],
 "read bible aloud": ["bible"],
 "stud finder": ["stud"],
 "sign language learn": ["sign language","asl"],
 "kids piano lessons": ["piano"],
 "nutrient tracker not calories": ["micronutrient","vitamin","nutrient"],
 "days since quit": ["days since","quit","sober","streak"],
 "interval reminder every hour": ["interval","every hour","hourly","repeat"],
 "hum to find song": ["hum"],
 "child support payments log": ["child support","co-parent","custody"],
 "pet sitting": ["pet sit","dog sit","pet care"],
 "hoa management": ["hoa","homeowners association","condo"],
 "freelance tax calculator": ["freelance","self-employed","1099","quarterly tax"],
 "one line a day journal": ["one line","journal"],
 "digital detox": ["detox","screen time","focus","block"],
 "elderly simple phone": ["senior","elderly","big button"],
 "rubiks cube solver": ["rubik","cube"],
 "record screen off": ["screen off","background record"],
 "pocket door measure room temperature": ["temperature","thermometer"],
 "landscape yard design ai": ["landscap","yard","garden"],
 "garden planner": ["garden","landscap","yard"],
 "estate sale finder": ["estate sale"],
 "learn mahjong american": ["mahjong"],
 "vocal pitch trainer sing in tune": ["pitch","sing","vocal"],
 "cocktail from ingredients": ["cocktail","drink"],
 "medication expiration": ["expir"],
 "airplane offline entertainment": ["offline","airplane","flight mode"],
}
os.makedirs('raw',exist_ok=True)
rows=[]
for t,stems in T.items():
    fn='raw/'+t.replace(' ','_')+'.json'
    if os.path.exists(fn):
        d=json.load(open(fn))
    else:
        url="https://itunes.apple.com/search?"+urllib.parse.urlencode({'term':t,'entity':'software','country':'us','limit':100})
        d={'results':[]}
        for attempt in range(4):
            try:
                d=json.load(urllib.request.urlopen(url,timeout=25)); break
            except Exception: time.sleep(6*(attempt+1))
        json.dump(d,open(fn,'w')); time.sleep(3.2)
    res=d.get('results',[])
    rel=[r for r in res if any(s in (r.get('trackName','')+' '+r.get('description','')).lower() for s in stems)]
    rc=sorted([r.get('userRatingCount',0) for r in rel],reverse=True)
    now=datetime.datetime.now(datetime.timezone.utc)
    def age(r):
        try: return (now-datetime.datetime.fromisoformat(r['currentVersionReleaseDate'].replace('Z','+00:00'))).days
        except Exception: return -1
    top=sorted(rel,key=lambda r:r.get('userRatingCount',0),reverse=True)[:4]
    topnames="; ".join(f"{r['trackName'][:30]} ({r.get('userRatingCount',0)} ★{r.get('averageUserRating',0):.1f} {r.get('formattedPrice','')} upd {age(r)}d)" for r in top)
    rows.append((t,len(res),len(rel),sum(rc[:3]),rc[0] if rc else 0,sum(1 for x in rc if x>=1000),sum(1 for x in rc if x>=10000),topnames))
print(f"{'term':36} {'n':>3} {'rel':>3} {'top3':>7} {'max':>6} {'>=1k':>4} {'>=10k':>5}  top relevant apps")
for r in sorted(rows,key=lambda r:r[3]):
    print(f"{r[0]:36} {r[1]:3} {r[2]:3} {r[3]:7} {r[4]:6} {r[5]:4} {r[6]:5}  {r[7]}")
