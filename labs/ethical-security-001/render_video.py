"""Palm92 evidence film: original silent motion graphics, Pillow and FFmpeg."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, math, json
ROOT=Path(__file__).resolve().parent
W,H,FPS=1080,1920,15
OUT=ROOT/'Palm92_Find_Fix_Prove.mp4'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
scenes=[
 ('FROM HEADLINE','TO EVIDENCE',['Palm92 Ethical Security Lab 001','An original local training exercise'],5),
 ('THE WEAKNESS','3 RECORDS EXPOSED',['An unsafe SQL query returned','all three fictional records.'],6),
 ('THE FIX','BIND THE INPUT',['A parameterized query treats','the input as data.'],6),
 ('THE RETEST','0 RECORDS EXPOSED',['The same injection input now','returns no matching records.'],6),
 ('VERIFIED RESULT','7 CHECKS PASSED',['Normal lookups still work.','The execution evidence is saved.'],6),
 ('PALM92 INTELLIGENCE','FIND. FIX. PROVE.',['AI investigates. Humans decide.','Code and evidence on GitHub'],7),
]
DURATION=sum(s[3] for s in scenes)
bg=Image.new('RGB',(W,H)); px=bg.load()
for y in range(H):
 for x in range(W):
  g=max(0,1-math.hypot((x-900)/1200,(y-1100)/1400))
  px[x,y]=(int(5+g*8),int(13+g*16),int(34+g*38))

def text(d,xy,s,size=52,fill='white',bold=False,center=False):
 f=ImageFont.truetype(BOLD if bold else FONT,size)
 if center: xy=(xy[0]-d.textbbox((0,0),s,font=f)[2]/2,xy[1])
 d.text(xy,s,font=f,fill=fill)

p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT)],stdin=subprocess.PIPE)
frame=0
for idx,(label,title,lines,seconds) in enumerate(scenes):
 for j in range(seconds*FPS):
  t=j/FPS; im=bg.copy(); d=ImageDraw.Draw(im)
  for k in range(8):
   yy=int(330+k*180+math.sin(t*.7+k)*20)
   d.line((60,yy,1020,yy-90),fill=(12,40,66),width=2)
  text(d,(70,90),'PALM',82,bold=True);text(d,(324,90),'92',82,fill='#FFD44D',bold=True)
  text(d,(75,195),'I N T E L L I G E N C E',31)
  d.rounded_rectangle((70,320,1010,405),radius=25,fill='#193459')
  text(d,(540,340),label,36,fill='#4DE7FF',bold=True,center=True)
  # Heading sized to fit safely inside the vertical frame.
  size=72
  while ImageDraw.Draw(im).textbbox((0,0),title,font=ImageFont.truetype(BOLD,size))[2]>940: size-=2
  text(d,(540,510),title,size,fill='#FFD44D' if idx in (1,4) else '#4DE7FF',bold=True,center=True)
  # Three fictional records visually reveal the before and after result.
  if idx in (1,3):
   for k,name in enumerate(['Fictional Alice record','Fictional Bob record','Fictional apostrophe record']):
    yy=760+k*145
    d.rounded_rectangle((90,yy,990,yy+110),radius=22,fill='#173457',outline='#3BDDEE',width=2)
    text(d,(125,yy+30),name,37)
    if idx==3:
     d.rectangle((90,yy,990,yy+110),fill='#0C1B32')
     text(d,(540,yy+32),'NO MATCH',36,fill='#65EDBB',bold=True,center=True)
  elif idx==4:
   text(d,(540,760),'7 / 7',180,fill='#FFD44D',bold=True,center=True)
   for k in range(7):
    x=150+k*115; d.ellipse((x,1080,x+70,1150),fill='#65EDBB' if t>.2*k else '#193459')
  else:
   cx,cy=540,940; pulse=int(8*math.sin(t*2))
   d.ellipse((cx-180-pulse,cy-180-pulse,cx+180+pulse,cy+180+pulse),outline='#39DDF8',width=7)
   d.line([(440,950),(510,1020),(660,845)],fill='#FFD44D',width=25)
  for k,line in enumerate(lines): text(d,(540,1280+k*85),line,43,center=True)
  text(d,(540,1580),'OFFLINE LAB  |  FICTIONAL DATA',33,fill='#B7D3E8',center=True)
  text(d,(540,1640),'NO EXTERNAL TARGETS',33,fill='#B7D3E8',center=True)
  text(d,(540,1740),f'{idx+1:02d} / 06',31,fill='#FFD44D',center=True)
  d.rectangle((70,1830,1010,1840),fill='#173457')
  d.rectangle((70,1830,70+int(940*frame/(DURATION*FPS-1)),1840),fill='#4DE7FF')
  p.stdin.write(im.tobytes()); frame+=1
p.stdin.close()
if p.wait(): raise SystemExit('FFmpeg render failed')
print(OUT)
