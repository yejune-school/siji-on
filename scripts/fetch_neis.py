import os,json,re,sys
from datetime import date,timedelta
import requests
from bs4 import BeautifulSoup
KEY=os.getenv("NEIS_API_KEY")
if not KEY: sys.exit("NEIS_API_KEY secret is missing")
BASE="https://open.neis.go.kr/hub"; ATPT="D10"; NAME="시지중학교"; OUT="data"; os.makedirs(OUT,exist_ok=True); s=requests.Session()
def rows(service,p):
 p={"KEY":KEY,"Type":"json","pIndex":1,"pSize":1000,**p}; r=s.get(f"{BASE}/{service}",params=p,timeout=30); r.raise_for_status(); d=r.json(); return d.get(service,[{},{}])[1].get("row",[]) if service in d and len(d[service])>1 else []
def save(n,x):
 with open(f"{OUT}/{n}","w",encoding="utf-8") as f: json.dump(x,f,ensure_ascii=False,indent=2)
def main():
 info=rows("schoolInfo",{"SCHUL_NM":NAME})
 if not info: raise RuntimeError("학교를 찾지 못했습니다.")
 code=info[0]["SD_SCHUL_CODE"]; t=date.today(); a=(t-timedelta(days=7)).strftime("%Y%m%d"); b=(t+timedelta(days=35)).strftime("%Y%m%d")
 meals=rows("mealServiceDietInfo",{"ATPT_OFCDC_SC_CODE":ATPT,"SD_SCHUL_CODE":code,"MLSV_FROM_YMD":a,"MLSV_TO_YMD":b}); save("meal.json",[{"date":x.get("MLSV_YMD",""),"mealType":x.get("MMEAL_SC_NM",""),"menu":re.sub(r"<br\\s*/?>","<br>",x.get("DDISH_NM",""))} for x in meals])
 sch=rows("SchoolSchedule",{"ATPT_OFCDC_SC_CODE":ATPT,"SD_SCHUL_CODE":code,"AA_FROM_YMD":a,"AA_TO_YMD":b}); save("schedule.json",[{"date":x.get("AA_YMD",""),"name":x.get("EVENT_NM",""),"content":x.get("EVENT_CNTNT","")} for x in sch])
 save("timetable.json",[])
 news=[]; u="https://siji.dge.ms.kr/sijim/main.do"
 try:
  soup=BeautifulSoup(s.get(u,timeout=20).text,"html.parser")
  from urllib.parse import urljoin
  for x in soup.find_all("a",href=True):
   title=" ".join(x.get_text(" ",strip=True).split())
   if title and any(k in title for k in ["공지","소식","알림","가정통신문","행사"]): news.append({"title":title,"url":urljoin(u,x["href"])})
 except Exception as e: print("news warning",e)
 seen=set(); news=[x for x in news if not(x["url"] in seen or seen.add(x["url"]))]; save("news.json",news[:50])
if __name__=="__main__": main()
