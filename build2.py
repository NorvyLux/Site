import random,math,re,json
cent=json.load(open('cent.json'))
FATF=json.load(open('fatf.json',encoding='utf-8'))
BLACK=list(FATF['black']);GREY=list(FATF['grey'])
_md=open('mapdata.js').read();_dots=json.loads(re.search(r'MAPDOTS=(\[.*?\]);',_md).group(1))
from collections import Counter as _C
_cnt=_C(d[2] for d in _dots)
SMALL=[k for k in cent if _cnt.get(k,0)<=4]
src=open('film.html',encoding='utf-8').read()
head=src[:src.index('<!-- 1. constat -->')]
def sec(id_):
    a=src.index(f'id="{id_}"'); a=src.rindex('<section',0,a); b=src.index('</section>',a)+len('</section>'); return src[a:b]
def retime(block,s,e,extra=''):
    block=re.sub(r'data-s="[\d.]+" data-e="[\d.]+"',f'data-s="{s}" data-e="{e}"',block,count=1)
    block=re.sub(r'<p data-at="0.8">.*?</p>','',block,count=1)
    return block
OPEN=retime(sec('s-open'),7,13).replace('Ouvrez un dossier en quelques clics.','Un dossier ouvert en quelques clics.')
INV=retime(sec('s-inv'),59,65).replace('data-cut="1"','').replace('<small data-at="0.2">Temps et facturation</small><h2 data-at="0.4">Le temps saisi devient une facture.</h2>','<small data-at="0.2">Facturation</small><h2 data-at="0.4">Du temps saisi à la facture.</h2>')
WEEK=retime(sec('s-week'),65,69.5).replace('<h2 data-at="0.4">Toutes vos échéances au même endroit.</h2>','<h2 data-at="0.4">Synchronisé avec Outlook.</h2>')
DASH=retime(sec('s-dash'),69.5,74)
END=sec('end') if 'id="end"' in src else None
a=src.index('<!-- 8. fin -->');b=src.index('</section>',a)+10
END=src[a:b].replace('data-s="45.5" data-e="52"','data-s="74" data-e="80"')

def unify(b,chip=None,at=None):
    b=b.replace('class="scene bg-light"','class="scene tech"').replace(' data-cfo="1"','').replace(' data-cut="1"','')
    b=b.replace('<div class="cap">','<div class="tcap">')
    if chip:
        b=b.replace('</section>',f'  <div class="okban" data-at="{at}">{chip}</div>\n</section>')
    return b
OPEN=unify(OPEN,'✓ Dossier créé',4.6)
INV=unify(INV,'✓ Facture réglée',5.3)
WEEK=unify(WEEK.replace('<h2 data-at="0.4">Synchronisé avec Outlook.</h2>','<h2 data-at="0.4">Toutes vos échéances<br>au même endroit.</h2>'),'✓ Synchronisé avec Outlook',3.4)
DASH=unify(DASH)
END=END.replace('class="scene bg-dark end"','class="scene tech end"')

# --- silhouette mesh
random.seed(7)
def inside(x,y):
    if ((x-320)/86)**2+((y-225)/106)**2<=1: return True
    if 325<=y<=410 and 290<=x<=350: return True
    if 410<=y<=790 and abs(x-320)<=40+235*((y-410)/390)**0.45: return True
    return False
pts=[]
tries=0
while len(pts)<70 and tries<200000:
    tries+=1
    x,y=random.uniform(60,580),random.uniform(130,760)
    if inside(x,y) and all((x-a)**2+(y-b)**2>34**2 for a,b in pts): pts.append((x,y))
edges=set()
for i,(x,y) in enumerate(pts):
    near=sorted(range(len(pts)),key=lambda j:(pts[j][0]-x)**2+(pts[j][1]-y)**2)[1:4]
    for j in near: edges.add(tuple(sorted((i,j))))
mesh=''.join(f'<line class="mline" x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[j][0]:.0f}" y2="{pts[j][1]:.0f}" data-y="{max(pts[i][1],pts[j][1]):.0f}"/>' for i,j in edges)
mesh+=''.join(f'<circle class="mpt" cx="{x:.0f}" cy="{y:.0f}" r="3.2" data-y="{y:.0f}"/>' for x,y in pts)


CATS=['Presse internationale','Presse régionale','Sites officiels','Décisions de justice','Blogs spécialisés']
LANGS=['FR','EN','DE','ES','IT','NL','PT','AR','ZH','PL']
random.seed(3)
cols=''
for c in range(3):
    cards=''
    for k in range(10):
        cat=CATS[(c*3+k)%5]; lg=LANGS[(c*4+k*3)%10]
        w1=random.randint(70,95); w2=random.randint(45,80); w3=random.randint(55,90)
        cards+=f'<div class="art"><div class="th"><svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="#A9B9F2" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="4" width="15" height="16" rx="2"/><path d="M18 8h3v10a2 2 0 01-2 2M6 8h9M6 12h9M6 16h6"/></svg></div><div class="tx"><div class="tags"><span class="cat">{cat}</span><span class="lg">{lg}</span></div><i style="width:{w1}%"></i><i style="width:{w2}%"></i><i class="s" style="width:{w3}%"></i></div><span class="ck"></span></div>'
    cols+=f'<div class="col" data-c="{c}">{cards}{cards}</div>'
MEDIA=f'''<section class="scene tech" data-s="45" data-e="52" id="s-media">
  <div class="tcap"><small data-at="0.2">Médias défavorables</small><h2 data-at="0.4">La presse du monde entier,<br>passée au crible.</h2>
    <div class="msrc" data-at="1.0"><span>Plusieurs langues</span><span>Presse, sites officiels, décisions de justice</span></div></div>
  <div class="wall" data-at="0.3"><div class="cols">{cols}</div><div id="mscan"></div><div class="fadeT"></div><div class="fadeB"></div></div>
  <div class="okban" data-at="5.4" style="left:120px;right:auto">✓ Aucune information défavorable</div>
</section>'''

NAMES=[('Helix Holdings S.à r.l.','Société'),('A. Keller','Bénéficiaire effectif'),('P. Durand','Bénéficiaire effectif'),('M. Rossi','Bénéficiaire effectif')]
rows=''
for i,(n,ty) in enumerate(NAMES):
    t0=1.0+i*0.8
    rows+=f'<div class="nrow" data-at="{0.5+i*0.15}" data-t0="{t0}"><div><b>{n}</b><span>{ty}</span></div><div class="nst"><i class="sp"></i><div class="meter"><i></i></div><em>0 correspondance</em></div></div>'
random.seed(11)
LS=[('UE','Union européenne'),('ONU','Nations unies'),('UK','Royaume-Uni'),('US','États-Unis')]
lcols=''
for k,(code,name) in enumerate(LS):
    ent=''
    for j in range(16):
        ent+=f'<div class="ent"><span class="ref">{code}-{random.randint(1000,9999)}</span><i style="width:{random.randint(45,90)}%"></i><i class="s" style="width:{random.randint(30,70)}%"></i></div>'
    lcols+=f'<div class="lcol" data-k="{k}"><div class="lh" data-lok="{4.6+k*0.25}"><span>{name}</span><i></i></div><div class="lstream"><div class="lin">{ent}{ent}</div></div></div>'
SANC=f'''<section class="scene tech" data-s="30" data-e="36.5" id="s-sanc">
  <div class="tcap"><small data-at="0.2">Listes de sanctions</small><h2 data-at="0.4">Chaque nom comparé<br>aux listes officielles.</h2></div>
  <div class="names">{rows}</div>
  <div class="lpanel" data-at="0.3"><div class="lcols">{lcols}</div><div class="cmpband"></div></div>
  <div class="okban" data-at="5.3" style="left:120px;right:auto">✓ 0 correspondance sur 4 listes</div>
</section>'''

VIG='''<section class="scene tech" data-s="52" data-e="59" id="s-vig">
  <div class="tcap"><small data-at="0.2">Niveau de vigilance</small><h2 data-at="0.4">La vigilance et le suivi,<br>proposés automatiquement.</h2></div>
  <div class="gauge" data-at="0.5">
    <svg viewBox="0 0 600 340" width="600" height="340">
      <path d="M60 300 A240 240 0 0 1 180 92" stroke="#1F9D63" stroke-width="34" fill="none"/>
      <path d="M186 89 A240 240 0 0 1 414 89" stroke="#E7A529" stroke-width="34" fill="none"/>
      <path d="M420 92 A240 240 0 0 1 540 300" stroke="#D9534A" stroke-width="34" fill="none"/>
      <g id="needle" transform="rotate(-90 300 300)"><line x1="300" y1="300" x2="300" y2="98" stroke="#fff" stroke-width="8" stroke-linecap="round"/><circle cx="300" cy="300" r="20" fill="#fff"/></g>
    </svg>
    <div class="glabels"><span>Simplifiée</span><span>Standard</span><span>Renforcée</span></div>
    <div class="gres" data-at="3.3">Vigilance renforcée proposée</div>
  </div>
  <div class="factors" data-at="0.6">
    <div class="fr" data-at="0.9"><i class="am"></i><b>Personne politiquement exposée</b><span>1 correspondance</span></div>
    <div class="fr" data-at="1.3"><i class="am"></i><b>Pays liés au client</b><span>1 en liste grise GAFI</span></div>
    <div class="fr" data-at="1.7"><i class="gr"></i><b>Listes de sanctions</b><span>Aucune correspondance</span></div>
    <div class="fr" data-at="2.1"><i class="gr"></i><b>Médias défavorables</b><span>Aucune information</span></div>
  </div>
  <div class="plan" data-at="3.6">
    <div class="ph">Plan de suivi proposé</div>
    <div class="tlx"><div class="tline"><i id="tlfill"></i></div>
      <div class="tn" style="left:0%" data-at="4.0"><span class="dot ok"></span><b>Aujourd'hui</b><em>Ouverture du dossier</em></div>
      <div class="tn" style="left:50%" data-at="4.4"><span class="dot"></span><b>Mai 2027</b><em>Revue KYC</em></div>
      <div class="tn" style="left:100%" data-at="4.8"><span class="dot"></span><b>Nov. 2027</b><em>Revue complète</em></div>
    </div>
    <div class="cont" data-at="5.0"><span class="pulse"></span>Surveillance continue des listes et des médias</div>
    <div class="pact" data-at="5.6"><span class="vbtn" data-press="6.3">Valider le plan</span></div>
  </div>
</section>'''

NODES=[('h','Helix Holdings S.à r.l.','LU','c',1320,170,0.6,None,''),
 ('o','Orion Capital SA','BE','c',1060,390,1.4,'h','50 %'),('n','Nordlicht GmbH','DE','c',1580,390,1.6,'h','50 %'),
 ('a','Atlas Trust','CH','c',1060,610,2.4,'o','100 %'),('k','A. Keller','','p',1390,610,2.6,'n','50 %'),('s','Silver Bay Ltd','AE','c',1730,610,2.8,'n','50 %'),
 ('d','P. Durand','','p',1060,830,3.4,'a','100 %'),('r','M. Rossi','','p',1730,830,3.6,'s','100 %')]
P={n[0]:n for n in NODES}
edges='';labs='';nodes=''
for key,name,cc,kind,x,y,t0,par,pct in NODES:
    if par:
        px,py=P[par][4],P[par][5]+46
        cy=y-46; my=(py+cy)/2
        d=f'M{px} {py} V{my} H{x} V{cy}'
        L=abs(cy-py)+abs(x-px)
        edges+=f'<path class="oe" d="{d}" data-t0="{t0-0.4}" data-len="{L:.0f}" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"/>'
        labs+=f'<span class="opct" style="left:{x}px;top:{(my+cy)/2-16:.0f}px" data-at="{t0}">{pct}</span>'
    if kind=='c':
        nodes+=f'<div class="on co" style="left:{x}px;top:{y}px" data-at="{t0}"><b>{name}</b><span class="cc">{cc}</span></div>'
    else:
        nodes+=f'<div class="on pe" data-k="{key}" style="left:{x}px;top:{y}px" data-at="{t0}"><span class="av"></span><b>{name}</b></div>'
ORGS=f'''<section class="scene tech" data-s="22.5" data-e="30" id="s-org">
  <div class="tcap"><small data-at="0.2">Organigramme de détention</small><h2 data-at="0.4">La chaîne de détention<br>reconstituée,<br>niveau par niveau.</h2></div>
  <div class="lvl" data-at="1.0"><span data-lv="0.6">Niveau 1</span><span data-lv="1.4">Niveau 2</span><span data-lv="2.4">Niveau 3</span><span data-lv="3.4">Niveau 4</span></div>
  <svg class="oedges" viewBox="0 0 1920 1080" width="1920" height="1080">{edges}</svg>
  {labs}{nodes}
  <div class="beres" data-at="4.6"><div class="bt">Bénéficiaires effectifs identifiés</div>
    <div class="bl"><span data-at="4.9"><b>P. Durand</b>50 %</span><span data-at="5.1"><b>A. Keller</b>25 %</span><span data-at="5.3"><b>M. Rossi</b>25 %</span></div></div>
</section>'''

RAIL='''<div id="rail"><span data-a="7" data-b="13">Dossier</span><span data-a="13" data-b="52">Contrôles AML</span><span data-a="52" data-b="59">Vigilance</span><span data-a="59" data-b="65">Facturation</span><span data-a="65" data-b="69.5">Agenda</span><span data-a="69.5" data-b="74">Pilotage</span></div>'''

PINS=[('LU',0,'c'),('BE',1,'b'),('CH',1,'b'),('AE',1,'b'),('FR',0,''),('DE',0,''),('GB',0,''),('US',0,''),('CA',0,''),('BR',0,''),('ZA',0,''),('NG',0,''),('RU',0,''),('IN',0,''),('CN',0,''),('AU',0,'')]
MAP=f'''<section class="scene tech" data-s="13" data-e="22.5" id="s-map">
  <div class="tcap"><small data-at="0.2">Contrôle AML</small><h2 data-at="0.4">Chaque pays lié au client,<br>comparé aux listes du GAFI.</h2></div>
  <svg class="map map2" viewBox="-20 -20 1540 740"><g id="dots"></g><g id="marks"></g><g id="arcs"></g><g id="pins"></g><line id="sweep" y1="-20" y2="720"/></svg>
  <div class="mlegend" data-at="3.0"><span><i style="background:#E5484D"></i>Liste noire GAFI</span><span><i style="background:#F5B83D"></i>Liste grise GAFI</span><em>Listes du {FATF['date_fr']}</em></div>
  <div class="cpanel" data-at="3.4"><div class="cph">Helix Holdings S.à r.l. <em>· pays liés</em></div><div class="crow" data-at="3.8"><span class="ccode">LU</span><div><b>Luxembourg</b><em>Siège · Helix Holdings</em></div><span class="cst ok">Hors listes</span></div><div class="crow" data-at="4.1"><span class="ccode">BE</span><div><b>Belgique</b><em>Orion Capital SA</em></div><span class="cst ok">Hors listes</span></div><div class="crow" data-at="4.4"><span class="ccode">DE</span><div><b>Allemagne</b><em>Nordlicht GmbH</em></div><span class="cst ok">Hors listes</span></div><div class="crow" data-at="4.7"><span class="ccode">CH</span><div><b>Suisse</b><em>Atlas Trust</em></div><span class="cst ok">Hors listes</span></div><div class="crow" data-at="5.0"><span class="ccode">AE</span><div><b>Émirats arabes unis</b><em>Silver Bay Ltd</em></div><span class="cst ok">Hors listes</span></div><div class="crow" data-at="5.3"><span class="ccode">FR</span><div><b>France</b><em>P. Durand · bénéficiaire</em></div><span class="cst ok">Hors listes</span></div><div class="crow crw" data-at="5.7"><span class="ccode">VN</span><div><b>Vietnam</b><em>Contrepartie</em></div><span class="cst gr">Liste grise GAFI</span></div></div>
  <div class="okban" data-at="6.6" style="background:#FFF0D1;color:#9A6400">1 pays lié en liste grise du GAFI</div>
</section>'''
SCAN=f'''<section class="scene tech" data-s="36.5" data-e="45" id="s-scan">
  <div class="frame" data-at="0.2">
    <span class="br tl"></span><span class="br tr"></span><span class="br bl"></span><span class="br brr"></span>
    <div class="idcard" data-at="0.2">
      <div class="idh"><span>Pièce d'identité</span><em>Lecture automatique</em></div>
      <div class="idb"><div class="phw"><svg viewBox="0 0 150 190" class="idph"><rect width="150" height="190" fill="#DCE3F5"/><circle cx="75" cy="78" r="38" fill="#9AA8CC"/><path d="M14 190 C18 140 46 124 75 124 C104 124 132 140 136 190 Z" fill="#9AA8CC"/>
<g id="lmk" fill="#2F5BD8" stroke="#2F5BD8" stroke-width="1"><line x1="58" y1="68" x2="92" y2="68" opacity=".7"/><line x1="58" y1="68" x2="75" y2="84" opacity=".7"/><line x1="92" y1="68" x2="75" y2="84" opacity=".7"/><line x1="75" y1="84" x2="64" y2="98" opacity=".7"/><line x1="75" y1="84" x2="86" y2="98" opacity=".7"/><line x1="64" y1="98" x2="75" y2="104" opacity=".7"/><line x1="86" y1="98" x2="75" y2="104" opacity=".7"/><line x1="58" y1="68" x2="50" y2="62" opacity=".7"/><line x1="92" y1="68" x2="100" y2="62" opacity=".7"/><line x1="50" y1="62" x2="75" y2="48" opacity=".7"/><line x1="100" y1="62" x2="75" y2="48" opacity=".7"/><line x1="50" y1="62" x2="46" y2="82" opacity=".7"/><line x1="100" y1="62" x2="104" y2="82" opacity=".7"/><line x1="46" y1="82" x2="60" y2="112" opacity=".7"/><line x1="104" y1="82" x2="90" y2="112" opacity=".7"/><line x1="60" y1="112" x2="75" y2="116" opacity=".7"/><line x1="90" y1="112" x2="75" y2="116" opacity=".7"/><line x1="64" y1="98" x2="60" y2="112" opacity=".7"/><line x1="86" y1="98" x2="90" y2="112" opacity=".7"/><circle cx="58" cy="68" r="2.6"/><circle cx="92" cy="68" r="2.6"/><circle cx="75" cy="84" r="2.6"/><circle cx="64" cy="98" r="2.6"/><circle cx="86" cy="98" r="2.6"/><circle cx="75" cy="104" r="2.6"/><circle cx="50" cy="62" r="2.6"/><circle cx="100" cy="62" r="2.6"/><circle cx="75" cy="48" r="2.6"/><circle cx="46" cy="82" r="2.6"/><circle cx="104" cy="82" r="2.6"/><circle cx="75" cy="116" r="2.6"/><circle cx="60" cy="112" r="2.6"/><circle cx="90" cy="112" r="2.6"/></g></svg><span class="fbox" id="fbox"></span></div>
        <div class="idf">
          <div class="fl" data-y="110"><small>Nom</small><b>KELLER</b></div>
          <div class="fl" data-y="170"><small>Prénom</small><b>Andreas</b></div>
          <div class="fl" data-y="230"><small>Date de naissance</small><b>14.03.1968</b></div>
          <div class="fl" data-y="290"><small>Expire le</small><b>12.04.2031</b></div>
        </div></div>
      <div class="mrz" data-y="390">ID&lt;&lt;&lt;KELLER&lt;&lt;ANDREAS&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;<br>6803148M3104127&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;0</div>
      <div id="idscan"></div>
    </div>
    <div class="idok" data-at="3.0">✓ Pièce lue et vérifiée</div>
    <svg class="idlink" viewBox="0 0 40 70"><path id="idl" d="M20 0 V70" stroke="#F5B83D" stroke-width="3" stroke-dasharray="6 6" fill="none"/></svg>
    <div class="pepc" data-at="3.7">
      <div class="phw sm"><svg viewBox="0 0 150 190" class="idph"><rect width="150" height="190" fill="#2A3768"/><circle cx="75" cy="78" r="38" fill="#7C89B3"/><path d="M14 190 C18 140 46 124 75 124 C104 124 132 140 136 190 Z" fill="#7C89B3"/></svg></div>
      <div class="pinfo"><small>Base PPE</small><b>Andreas Keller</b><span>Ancien maire · mandat 2014–2020</span><em>Né le 14.03.1968</em></div>
      <span class="mtag" data-at="4.4">Correspondance</span>
    </div>
    <span class="ftag" data-at="0.6">Analyse PPE</span>
  </div>
  <div class="tcap right"><small data-at="0.3">Personnes politiquement exposées</small><h2 data-at="0.5">Les profils sensibles<br>repérés pour vous.</h2>
    <div class="rcard" data-at="1.0">
      <div class="prog"><span>Comparaison aux bases PPE</span><div class="bar"><i id="pbar"></i></div></div>
      <div class="warn" data-at="4.4"><b>!</b> 1 correspondance à examiner</div>
      <div class="actrow" data-at="5.2"><span class="vbtn" data-press="6.2">Valider le client</span><span class="rec" data-at="6.6">✓ Décision enregistrée</span></div>
    </div>
  </div>
</section>'''

CARDS=src[src.index('<!-- cards layer'):src.index('<!-- 2. norvy -->')]
INTRO='''<section class="scene tech" data-s="0" data-e="3.5" data-out="1" id="s-prob">
  <div class="big" style="top:150px;font-size:54px" data-at="0.2">Dossiers, temps, factures, agenda, contrôles AML…</div>
  <div class="big" style="top:228px;font-size:54px;color:var(--peri)" data-at="1.2">…répartis entre plusieurs outils.</div>
</section>'''
INTRO2='''<section class="scene" data-s="0" data-e="7" id="s-hub" style="background:none">
  <div class="big" style="top:150px;font-size:58px" data-at="3.9">Tout est réuni dans Norvy.</div>
  <div class="hub" data-at="3.3">
    <div class="hubtop"><span class="lg"><b>n</b>norvy</span><span class="ttl">Tableau de bord</span></div>
    <div class="hubgrid">
      <div data-at="4.2"><span class="hi" style="background:#E6ECFB;color:#2F4A86">▤</span><b>Dossiers</b><em>42 actifs</em></div>
      <div data-at="4.4"><span class="hi" style="background:#DDF3E6;color:#16794A">€</span><b>Facturation</b><em>48 250 € ce mois</em></div>
      <div data-at="4.6"><span class="hi" style="background:#FFF0D1;color:#9A6400">◷</span><b>Agenda</b><em>2 audiences aujourd'hui</em></div>
      <div data-at="4.8"><span class="hi" style="background:#EDE6FB;color:#5B3BA8">✓</span><b>Contrôles AML</b><em>2 alertes à examiner</em></div>
    </div>
  </div>
</section>'''
CSS='''<style>
.tech{background:radial-gradient(1100px 700px at 60% 45%,#16245A 0%,#0B1230 65%)}
.tcap{position:absolute;left:120px;top:90px;z-index:3}
.tcap small{font-size:22px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--peri)}
.tcap h2{margin:14px 0 0;font-size:52px;line-height:1.1;letter-spacing:-.03em;color:#fff;font-weight:700}
.tcap.right{left:auto;right:130px;top:200px;width:760px}
.client{position:absolute;right:120px;top:110px;display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.07);border:1px solid rgba(169,185,242,.3);color:#fff;font-size:24px;font-weight:600;padding:14px 22px;border-radius:14px}
.client em{font-style:normal;color:#B9C2DC;font-weight:500}
.cdot{width:14px;height:14px;border-radius:50%;background:#7FA0FF;box-shadow:0 0 0 6px rgba(127,160,255,.25)}
.map{position:absolute;left:150px;top:270px;width:1620px;height:auto}
.map circle.d{fill:#A9B9F2}
.map.map2{left:60px;top:250px;width:1280px}
.mlegend{position:absolute;right:90px;top:935px;width:500px;flex-wrap:wrap;row-gap:6px;display:flex;gap:28px;align-items:center;color:#C9D1EA;font-size:19px}
.mlegend span{display:flex;align-items:center;gap:10px}.mlegend i{width:14px;height:14px;border-radius:50%;display:inline-block}
.mlegend em{font-style:normal;color:#8F9AB8;font-size:16px}
.cpanel{position:absolute;right:90px;top:150px;width:500px;background:rgba(255,255,255,.05);border:1px solid rgba(169,185,242,.25);border-radius:18px;padding:22px 22px 12px}
.cph{color:#fff;font-size:22px;font-weight:700;margin-bottom:14px}.cph em{font-style:normal;color:#8F9AB8;font-weight:500}
.crow{display:flex;align-items:center;gap:14px;padding:11px 0;border-top:1px solid rgba(169,185,242,.14)}
.crow .ccode{width:44px;height:30px;border-radius:7px;background:rgba(127,160,255,.16);color:#A9C4FF;font-weight:700;font-size:15px;display:flex;align-items:center;justify-content:center;flex:none}
.crow div{flex:1;display:flex;flex-direction:column}.crow b{color:#fff;font-size:19px;font-weight:600}.crow em{font-style:normal;color:#8F9AB8;font-size:15px}
.cst{font-size:14px;font-weight:700;padding:5px 10px;border-radius:999px;white-space:nowrap}.cst.ok{background:rgba(31,157,99,.18);color:#5FD49B}.cst.gr{background:#FFF0D1;color:#9A6400}
.crow.crw .ccode{background:rgba(245,184,61,.2);color:#F5B83D}

#sweep{stroke:#7FA0FF;stroke-width:3;filter:drop-shadow(0 0 12px #7FA0FF)}
.lists{position:absolute;left:120px;bottom:80px;display:flex;gap:14px}
.li{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);color:#E3E8F7;font-size:22px;font-weight:600;padding:12px 20px;border-radius:12px}
.li i{width:24px;height:24px;border-radius:50%;border:3px solid rgba(169,185,242,.35);border-top-color:#A9B9F2;position:relative}
.li.ok i{border:0;background:#1F9D63}
.li.ok i::after{content:"";position:absolute;left:8px;top:4px;width:6px;height:11px;border:solid #fff;border-width:0 3px 3px 0;transform:rotate(45deg)}
.okban{position:absolute;right:120px;bottom:84px;background:#DDF3E6;color:#16794A;font-size:24px;font-weight:700;padding:16px 24px;border-radius:12px}
.frame{position:absolute;left:170px;top:140px;width:640px;height:800px}
.frame .sil{width:640px;height:800px;display:block}
.grid line{stroke:rgba(169,185,242,.08);stroke-width:1}
.mline{stroke:#A9B9F2;stroke-width:1.3;opacity:0}
.mpt{fill:#C9D5FF;opacity:0}
.br{position:absolute;width:56px;height:56px;border-color:#7FA0FF;border-style:solid;border-width:0}
.br.tl{left:-14px;top:-14px;border-left-width:4px;border-top-width:4px}
.br.tr{right:-14px;top:-14px;border-right-width:4px;border-top-width:4px}
.br.bl{left:-14px;bottom:-14px;border-left-width:4px;border-bottom-width:4px}
.br.brr{right:-14px;bottom:-14px;border-right-width:4px;border-bottom-width:4px}
.idcard{position:absolute;left:0;top:0;width:640px;height:470px;border-radius:22px;background:linear-gradient(135deg,#F4F7FD,#E3E9F7);box-shadow:0 30px 80px -30px rgba(0,0,0,.6);overflow:hidden;color:#1B2440}
.idh{display:flex;justify-content:space-between;align-items:center;padding:20px 28px;background:#2F5BD8;color:#fff}.idh span{font-weight:700;font-size:20px;letter-spacing:.08em;text-transform:uppercase}.idh em{font-style:normal;font-size:15px;opacity:.85}
.idb{display:flex;gap:30px;padding:24px 28px 0}.phw{position:relative;width:150px;height:190px;border-radius:10px;overflow:hidden;flex:none}.idph{width:150px;height:190px;display:block}
.fbox{position:absolute;left:28px;top:30px;width:94px;height:104px;border:3px solid #2F5BD8;border-radius:8px;opacity:0}
.idf{display:flex;flex-direction:column;gap:10px;flex:1}.fl{position:relative;padding:4px 10px;border-radius:8px;border:2px solid transparent}.fl small{display:block;font-size:13px;color:#6B7798;text-transform:uppercase;letter-spacing:.06em}.fl b{font-size:22px;font-weight:700}
.fl.rd{border-color:#2F5BD8;background:rgba(47,91,216,.07)}
.mrz{position:absolute;left:20px;right:20px;bottom:18px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:17px;letter-spacing:.12em;color:#3A4566;padding:6px 8px;border-radius:8px;border:2px solid transparent;line-height:1.5}
.mrz.rd{border-color:#2F5BD8;background:rgba(47,91,216,.07)}
#idscan{position:absolute;left:0;right:0;height:4px;background:#7FA0FF;box-shadow:0 0 24px 8px rgba(127,160,255,.6);top:-10px}
.idok{position:absolute;left:0;top:492px;background:rgba(31,157,99,.18);color:#5FD49B;font-weight:700;font-size:19px;padding:8px 16px;border-radius:999px}
.idlink{position:absolute;left:300px;top:492px;width:40px;height:70px}
.pepc{position:absolute;left:0;top:572px;width:640px;display:flex;gap:24px;align-items:center;background:rgba(255,255,255,.06);border:2px solid rgba(169,185,242,.25);border-radius:20px;padding:20px 24px;color:#fff}
.pepc .phw.sm{width:96px;height:122px}.pepc .phw.sm .idph{width:96px;height:122px}
.pinfo{display:flex;flex-direction:column;gap:3px;flex:1}.pinfo small{color:#8F9AB8;font-size:14px;text-transform:uppercase;letter-spacing:.08em}.pinfo b{font-size:26px}.pinfo span{color:#C9D1EA;font-size:18px}.pinfo em{font-style:normal;color:#8F9AB8;font-size:16px}
.mtag{position:absolute;right:20px;top:20px;background:#FFF0D1;color:#9A6400;font-weight:700;font-size:15px;padding:6px 12px;border-radius:999px}
.pepc.hit{border-color:#F5B83D;box-shadow:0 0 0 6px rgba(245,184,61,.15)}
.ftag{position:absolute;left:0;top:-62px;font-size:20px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#7FA0FF}
.rcard{margin-top:56px;background:rgba(255,255,255,.06);border:1px solid rgba(169,185,242,.25);border-radius:20px;padding:30px}
.prog span{font-size:22px;color:#C9D1EA;font-weight:600}
.bar{margin-top:14px;height:12px;border-radius:6px;background:rgba(255,255,255,.1);overflow:hidden}
.bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#4F6CA8,#7FA0FF)}
.warn{margin-top:26px;display:flex;align-items:center;gap:14px;background:#FFF0D1;color:#9A6400;font-size:24px;font-weight:700;padding:16px 20px;border-radius:12px}
.warn b{display:inline-flex;width:30px;height:30px;border-radius:50%;background:#E7A529;color:#fff;align-items:center;justify-content:center;font-size:18px}
.actrow{margin-top:22px;display:flex;align-items:center;gap:22px}
.vbtn{display:inline-block;font-size:22px;font-weight:700;color:#fff;padding:16px 26px;border-radius:12px;background:#2F5BD8}
.rec{font-size:22px;color:#7FD3A6;font-weight:600}
.cap h2{font-size:58px}

/* coherence */
html,body{background:radial-gradient(1100px 700px at 60% 45%,#16245A 0%,#0B1230 65%)!important}
.okban{left:120px!important;right:auto!important;bottom:110px!important}
.tcap h2{font-size:52px!important}
.mock{top:56%!important}
.mock .app{box-shadow:0 50px 120px -30px rgba(0,0,0,.75)!important;border:1px solid rgba(255,255,255,.08)!important}
#rail{position:absolute;left:50%;bottom:34px;transform:translateX(-50%);display:flex;gap:10px;z-index:20;opacity:0}
#rail span{position:relative;font-size:16px;font-weight:600;color:rgba(201,209,234,.38);padding:0 6px 12px;letter-spacing:.02em;white-space:nowrap}
#rail span::after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;border-radius:2px;background:rgba(201,209,234,.15)}
#rail span i{position:absolute;left:0;bottom:0;height:3px;border-radius:2px;background:#7FA0FF;width:0}
#rail span.cur{color:#fff}#rail span.done{color:rgba(201,209,234,.7)}

.oedges{position:absolute;left:0;top:0;pointer-events:none}
.oe{fill:none;stroke:#7FA0FF;stroke-width:3}
.on{position:absolute;transform:translate(-50%,-50%)!important;display:flex;align-items:center;gap:12px;white-space:nowrap}
.on.co{background:#1A2649;border:2px solid rgba(127,160,255,.55);border-radius:14px;padding:18px 22px;color:#fff}
.on.co b{font-size:24px}.on .cc{font-size:15px;font-weight:700;color:#C9D5FF;background:rgba(127,160,255,.2);padding:3px 8px;border-radius:6px}
.on.pe{background:#2A2414;border:2px solid #E7A529;border-radius:999px;padding:12px 22px 12px 12px;color:#FFE2A8}
.on.pe b{font-size:24px}.av{width:36px;height:36px;border-radius:50%;background:#E7A529;position:relative}
.av::before{content:"";position:absolute;left:12px;top:6px;width:12px;height:12px;border-radius:50%;background:#2A2414}
.av::after{content:"";position:absolute;left:8px;top:20px;width:20px;height:11px;border-radius:10px 10px 3px 3px;background:#2A2414}
.on.pe.glow{box-shadow:0 0 0 6px rgba(231,165,41,.25),0 0 40px rgba(231,165,41,.55)}
.opct{position:absolute;transform:translateX(12px);font-size:19px;font-weight:700;color:#A9B9F2;background:#0F1830;padding:2px 8px;border-radius:6px}
.lvl{position:absolute;left:790px;top:150px;display:flex;flex-direction:column;gap:182px}
.lvl span{font-size:16px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgba(169,185,242,.35)}
.lvl span.on2{color:#7FA0FF}
.beres{position:absolute;left:120px;bottom:120px;width:620px;background:rgba(231,165,41,.1);border:1px solid rgba(231,165,41,.45);border-radius:18px;padding:24px 26px}
.beres .bt{color:#FFE2A8;font-size:22px;font-weight:700}
.beres .bl{display:flex;flex-direction:column;gap:10px;margin-top:16px}
.beres .bl span{display:flex;justify-content:space-between;color:#FFE2A8;font-size:22px}.beres .bl b{color:#fff}

.gauge{position:absolute;left:150px;top:420px;width:600px}
.glabels{display:flex;justify-content:space-between;margin-top:10px;color:#C9D1EA;font-size:22px;font-weight:600}
.gres{margin-top:26px;text-align:center;background:rgba(217,83,74,.16);border:1px solid rgba(217,83,74,.5);color:#FFB4AD;font-size:26px;font-weight:700;padding:16px;border-radius:14px}
.factors{position:absolute;right:120px;top:120px;width:900px;display:grid;grid-template-columns:1fr 1fr;gap:14px}
.fr{display:grid;grid-template-columns:auto 1fr;column-gap:14px;align-items:center;background:rgba(255,255,255,.06);border:1px solid rgba(169,185,242,.2);border-radius:14px;padding:16px 20px}
.fr i{grid-row:span 2;width:14px;height:14px;border-radius:50%}.fr i.am{background:#E7A529}.fr i.gr{background:#1F9D63}
.fr b{color:#fff;font-size:21px}.fr span{color:#8F9AB8;font-size:18px}
.plan{position:absolute;right:120px;top:420px;width:900px;background:rgba(255,255,255,.06);border:1px solid rgba(169,185,242,.25);border-radius:20px;padding:30px 40px 34px}
.ph{color:#fff;font-size:28px;font-weight:700}
.tlx{position:relative;height:150px;margin:34px 60px 0}
.tline{position:absolute;left:0;right:0;top:12px;height:4px;background:rgba(255,255,255,.12);border-radius:2px}.tline i{display:block;height:100%;width:0;background:#7FA0FF;border-radius:2px}
.tn{position:absolute;top:0;transform:translateX(-50%);text-align:center;width:220px;margin-left:-110px}
.tn .dot{display:block;margin:0 auto;width:28px;height:28px;border-radius:50%;background:#0F1830;border:4px solid #7FA0FF}.tn .dot.ok{background:#1F9D63;border-color:#1F9D63}
.tn b{display:block;margin-top:14px;color:#fff;font-size:22px}.tn em{display:block;font-style:normal;color:#8F9AB8;font-size:18px;margin-top:2px}
.cont{margin-top:6px;display:flex;align-items:center;gap:14px;color:#C9D5FF;font-size:22px;font-weight:600;background:rgba(127,160,255,.12);border-radius:12px;padding:14px 18px}
.pulse{width:14px;height:14px;border-radius:50%;background:#7FA0FF;box-shadow:0 0 0 0 rgba(127,160,255,.6)}
.pact{margin-top:22px}

html,body{background:radial-gradient(1200px 700px at 70% 30%,#1B2A55 0%,#0F1830 60%)}
.hub{position:absolute;left:50%;top:300px;width:1120px;margin-left:-560px;border-radius:24px;overflow:hidden;background:#F3F5F9;box-shadow:0 50px 120px -30px rgba(0,0,0,.7)}
.hubtop{display:flex;align-items:center;justify-content:space-between;background:#181C24;color:#fff;padding:20px 28px}
.hubtop .lg{display:flex;align-items:center;gap:12px;font-weight:700;font-size:28px;letter-spacing:-.03em}
.hubtop .lg b{display:inline-flex;width:40px;height:40px;border-radius:10px;background:#4F6CA8;align-items:center;justify-content:center;font-size:22px}
.hubtop .ttl{color:#9AA4BE;font-size:20px}
.hubgrid{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:28px}
.hubgrid>div{background:#fff;border:1px solid #E1E5EE;border-radius:16px;padding:26px;display:grid;grid-template-columns:auto 1fr;column-gap:18px;align-items:center}
.hubgrid .hi{grid-row:span 2;width:60px;height:60px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800}
.hubgrid b{font-size:28px;color:#131A2E;letter-spacing:-.02em}.hubgrid em{font-style:normal;color:#7A849E;font-size:20px;margin-top:2px}

.names{position:absolute;left:120px;top:380px;width:680px;display:flex;flex-direction:column;gap:16px}
.nrow{display:flex;align-items:center;justify-content:space-between;gap:20px;background:rgba(255,255,255,.06);border:1px solid rgba(169,185,242,.2);border-radius:14px;padding:18px 22px}
.nrow b{display:block;color:#fff;font-size:26px;font-weight:700}.nrow span{display:block;color:#8F9AB8;font-size:18px;margin-top:2px}
.nst{display:flex;align-items:center;gap:14px;flex:none}
.nst .sp{width:26px;height:26px;border-radius:50%;border:3px solid rgba(169,185,242,.35);border-top-color:#A9B9F2}
.meter{width:120px;height:10px;border-radius:5px;background:rgba(255,255,255,.1);overflow:hidden}.meter i{display:block;height:100%;width:0;background:#7FA0FF}
.nst em{font-style:normal;font-size:19px;font-weight:700;color:#7FD3A6;display:none}
.nrow.done .sp{border:0;background:#1F9D63;position:relative}
.nrow.done .sp::after{content:"";position:absolute;left:9px;top:5px;width:6px;height:11px;border:solid #fff;border-width:0 3px 3px 0;transform:rotate(45deg)}
.nrow.done .meter{display:none}.nrow.done em{display:inline}
.nrow.act{border-color:#7FA0FF;box-shadow:0 0 24px rgba(127,160,255,.35)}
.lpanel{position:absolute;right:110px;top:110px;width:960px;height:860px;border-radius:22px;overflow:hidden;background:rgba(255,255,255,.03);border:1px solid rgba(169,185,242,.15)}
.lcols{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding:18px;height:100%}
.lcol{display:flex;flex-direction:column;min-width:0}
.lh{display:flex;align-items:center;justify-content:space-between;gap:8px;color:#E3E8F7;font-size:19px;font-weight:700;padding:10px 12px;border-radius:10px;background:rgba(127,160,255,.12);margin-bottom:12px}
.lh i{flex:none;width:22px;height:22px;border-radius:50%;border:3px solid rgba(169,185,242,.35);border-top-color:#A9B9F2;position:relative}
.lh.ok i{border:0;background:#1F9D63}.lh.ok i::after{content:"";position:absolute;left:7px;top:4px;width:5px;height:10px;border:solid #fff;border-width:0 3px 3px 0;transform:rotate(45deg)}
.lstream{flex:1;overflow:hidden;position:relative}
.lin{will-change:transform}
.ent{height:74px;border-radius:10px;background:rgba(255,255,255,.05);margin-bottom:10px;padding:10px 12px}
.ent .ref{font-family:ui-monospace,Menlo,monospace;font-size:13px;color:#8F9AB8}
.ent i{display:block;height:10px;border-radius:5px;background:rgba(229,235,255,.32);margin-top:9px}.ent i.s{background:rgba(229,235,255,.16)}
.ent.hit{background:rgba(127,160,255,.22);box-shadow:inset 0 0 0 1px #7FA0FF}
.cmpband{position:absolute;left:0;right:0;top:470px;height:84px;border-top:2px solid rgba(127,160,255,.8);border-bottom:2px solid rgba(127,160,255,.8);background:rgba(127,160,255,.08);box-shadow:0 0 40px rgba(127,160,255,.35)}

.wall{position:absolute;right:110px;top:90px;width:980px;height:900px;overflow:hidden;border-radius:22px}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;height:100%}
.col{display:flex;flex-direction:column;gap:18px;will-change:transform}
.art{position:relative;display:flex;gap:14px;background:rgba(255,255,255,.06);border:1px solid rgba(169,185,242,.18);border-radius:14px;padding:16px;height:150px;flex:none}
.art .th{flex:none;width:64px;height:64px;border-radius:10px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#2A3A72,#1A2550)}
.art .tx{flex:1;min-width:0}
.art .tags{display:flex;gap:8px;margin-bottom:12px}
.art .cat{font-size:14px;font-weight:700;color:#C9D5FF;background:rgba(127,160,255,.16);padding:3px 10px;border-radius:999px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.art .lg{font-size:13px;font-weight:700;color:#8F9AB8;border:1px solid rgba(143,154,184,.4);padding:2px 8px;border-radius:6px}
.art i{display:block;height:13px;border-radius:6px;background:rgba(229,235,255,.42);margin-top:10px}
.art i.s{background:rgba(201,213,255,.16)}
.art .ck{position:absolute;right:14px;bottom:14px;width:26px;height:26px;border-radius:50%;background:#1F9D63;opacity:0}
.art .ck::after{content:"";position:absolute;left:9px;top:5px;width:6px;height:11px;border:solid #fff;border-width:0 3px 3px 0;transform:rotate(45deg)}
.art.hot{border-color:#7FA0FF;box-shadow:0 0 0 2px rgba(127,160,255,.35),0 0 30px rgba(127,160,255,.35)}
#mscan{position:absolute;left:0;right:0;height:4px;background:#7FA0FF;box-shadow:0 0 24px 6px rgba(127,160,255,.55);top:-10px}
.fadeT,.fadeB{position:absolute;left:0;right:0;height:120px;pointer-events:none}
.fadeT{top:0;background:linear-gradient(#0D1535,rgba(13,21,53,0))}.fadeB{bottom:0;background:linear-gradient(rgba(13,21,53,0),#0D1535)}
.msrc{margin-top:34px;display:flex;flex-direction:column;gap:12px;max-width:520px}
.msrc span{display:inline-block;align-self:flex-start;font-size:20px;color:#C9D1EA;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);padding:10px 16px;border-radius:10px}

</style>'''
JS=r'''<script>
(function(){
 var g=document.getElementById('dots'),h='';var BL=__BL__,GR=__GR__,CE=__CE__;
 MAPDOTS.forEach(function(d){var k=BL.indexOf(d[2])>=0?'b':(GR.indexOf(d[2])>=0?'g':'');h+='<circle class="d" cx="'+d[0]+'" cy="'+d[1]+'" r="3.4" data-x="'+d[0]+'" data-k="'+k+'"/>';});g.innerHTML=h;
 var mk='';Object.keys(CE).forEach(function(id){var c=CE[id],k=BL.indexOf(id)>=0?'b':'g';mk+='<circle class="mk" cx="'+c[0]+'" cy="'+c[1]+'" r="7" data-x="'+c[0]+'" data-k="'+k+'" fill="none" stroke-width="2.5"/>';});
 document.getElementById('marks').innerHTML=mk;
 var C=Object.assign({},MAPPINS,{VN:[CE['704'][0],CE['704'][1]]});var L=C.LU;
 var T=[['BE',0.3],['DE',0.6],['CH',0.9],['AE',1.2],['FR',1.5],['VN',1.9]];var ah='',ph='<g class="pin" data-t="0"><circle class="ring" cx="'+L[0]+'" cy="'+L[1]+'" r="0" fill="none" stroke="#7FA0FF" stroke-width="3"/><circle class="core" cx="'+L[0]+'" cy="'+L[1]+'" r="10" fill="#7FA0FF"/></g>';
 T.forEach(function(p){var c=C[p[0]],w=p[0]==='VN',col=w?'#F5B83D':'#7FA0FF';var dx=c[0]-L[0],dy=c[1]-L[1],dist=Math.sqrt(dx*dx+dy*dy);var lift=Math.max(40,dist*0.35);
   var mx=(L[0]+c[0])/2,my=Math.min(L[1],c[1])-lift;var len=Math.round(dist*1.4+60);
   ah+='<path class="arc" data-t="'+p[1]+'" data-len="'+len+'" d="M'+L[0]+' '+L[1]+' Q'+mx+' '+my+' '+c[0]+' '+c[1]+'" fill="none" stroke="'+col+'" stroke-width="'+(w?3.5:2.5)+'" stroke-dasharray="'+len+'" stroke-dashoffset="'+len+'"/>';
   ph+='<g class="pin" data-t="'+(p[1]+0.5)+'"><circle class="ring" cx="'+c[0]+'" cy="'+c[1]+'" r="0" fill="none" stroke="'+col+'" stroke-width="3"/><circle class="core" cx="'+c[0]+'" cy="'+c[1]+'" r="'+(w?9:6)+'" fill="'+col+'"/></g>';});
 document.getElementById('pins').innerHTML=ph;document.getElementById('arcs').innerHTML=ah;
})();
var _base=render;
render=function(t){_base(t);
 var m=document.getElementById('s-map'),lt=t-13;
 if(+m.style.opacity>0){
   var sx=(lt-0.6)/2.6*1500;
   m.querySelectorAll('circle.d').forEach(function(c){var x=+c.dataset.x,dd=sx-x,k=c.dataset.k;var o=lt<0.2?0:0.13,f='#A9B9F2';
     if(dd>0){o=dd<90?1:0.38;f=dd<90?'#E3EAFF':'#A9B9F2';if(k){f=k==='b'?'#E5484D':'#F5B83D';o=dd<90?1:0.95;}}c.style.opacity=o;c.style.fill=f;});
   m.querySelectorAll('circle.mk').forEach(function(c){var dd=sx-(+c.dataset.x),k=c.dataset.k;c.setAttribute('stroke',k==='b'?'#E5484D':'#F5B83D');c.style.opacity=dd>0?1:0;});
   var sw=document.getElementById('sweep');sw.setAttribute('x1',sx);sw.setAttribute('x2',sx);sw.style.opacity=(sx>-10&&sx<1520)?1:0;
   m.querySelectorAll('.arc').forEach(function(a){var p=Math.max(0,Math.min(1,(lt-3.8-(+a.dataset.t))/0.7));a.setAttribute('stroke-dashoffset',(+a.dataset.len)*(1-p));});
   m.querySelectorAll('.pin').forEach(function(p){var k=lt-3.6-(+p.dataset.t);var core=p.querySelector('.core'),ring=p.querySelector('.ring');core.style.opacity=k>0?1:0;
     var ph=k>0?((k%1.6)/1.6):0;ring.setAttribute('r',k>0?6+ph*34:0);ring.style.opacity=k>0?(1-ph):0;});
 }
 var sc=document.getElementById('s-scan'),st=t-36.5;
 if(+sc.style.opacity>0){
   var y=st<0.8?-10:(st<2.6?(st-0.8)/1.8*480:-10);var sl=document.getElementById('idscan');sl.style.top=y+'px';sl.style.opacity=(st>0.8&&st<2.6)?1:0;
   var maxy=st<0.8?-1:(st<2.6?y:999);
   sc.querySelectorAll('.idcard [data-y]').forEach(function(e){e.classList.toggle('rd',maxy>(+e.dataset.y)+10);});
   var fb=document.getElementById('fbox');var fk=Math.max(0,Math.min(1,(st-2.4)/0.5));fb.style.opacity=fk;fb.style.transform='scale('+(1.25-0.25*fk)+')';
   sc.querySelectorAll('#lmk > *').forEach(function(e,i){e.style.opacity=st>2.5+i*0.04?1:0;});
   var ld=document.getElementById('idl');ld.style.opacity=st>3.4?1:0;ld.setAttribute('stroke-dashoffset',-(st*30)%12);
   sc.querySelector('.pepc').classList.toggle('hit',st>=4.4);
   document.getElementById('pbar').style.width=(Math.max(0,Math.min(1,(st-1.4)/3.0))*100)+'%';
 }



 var rl=document.getElementById('rail');
 if(rl){rl.style.opacity=(t<6.6||t>73.6)?0:Math.min(1,(t-6.6)/0.5,(73.6-t)/0.4);
   rl.querySelectorAll('span').forEach(function(sp){if(!sp.querySelector('i'))sp.insertAdjacentHTML('beforeend','<i></i>');var a=+sp.dataset.a,b=+sp.dataset.b;
     sp.classList.toggle('cur',t>=a&&t<b);sp.classList.toggle('done',t>=b);sp.querySelector('i').style.width=(Math.max(0,Math.min(1,(t-a)/(b-a)))*100)+'%';});}
 var og=document.getElementById('s-org'),olt=t-22.5;
 if(og&&+og.style.opacity>0){
   og.querySelectorAll('.oe').forEach(function(e){var p=Math.max(0,Math.min(1,(olt-(+e.dataset.t0))/0.45));e.setAttribute('stroke-dashoffset',(+e.dataset.len)*(1-p));});
   og.querySelectorAll('.on.pe').forEach(function(n){n.classList.toggle('glow',olt>4.4);});
   og.querySelectorAll('.lvl span').forEach(function(l){l.classList.toggle('on2',olt>=+l.dataset.lv);});
 }
 var sn=document.getElementById('s-sanc'),sl=t-30;
 if(sn&&+sn.style.opacity>0){
   var EH=84,NN=16*EH;
   sn.querySelectorAll('.lcol').forEach(function(c){var k=+c.dataset.k;var off=((sl*(420+k*60)+k*150)%NN);var lin=c.querySelector('.lin');lin.style.transform='translateY('+(-off)+'px)';
     var stop=sl>4.6+k*0.25;if(stop){lin.style.transform='translateY('+(-((4.6+k*0.25)*(420+k*60)+k*150)%NN)+'px)';}
     c.querySelector('.lh').classList.toggle('ok',stop);
     c.querySelector('.lh i').style.transform=stop?'none':'rotate('+(sl*420)+'deg)';
     var cur=stop?(((4.6+k*0.25)*(420+k*60)+k*150)%NN):off;
     c.querySelectorAll('.ent').forEach(function(e,j){var y=58+j*EH-cur+37;e.classList.toggle('hit',!stop&&y>455&&y<555);});});
   sn.querySelectorAll('.nrow').forEach(function(r){var t0=+r.dataset.t0,k=sl-t0;r.classList.toggle('act',k>0&&k<1.2);r.classList.toggle('done',k>=1.2);
     r.querySelector('.sp').style.transform=(k<1.2)?'rotate('+(sl*420)+'deg)':'none';
     r.querySelector('.meter i').style.width=(k>0&&k<1.2)?(20+Math.abs(Math.sin(k*9))*45)+'%':'0';});
 }

 var vg=document.getElementById('s-vig'),vl=t-52;
 if(vg&&+vg.style.opacity>0){
   var p=Math.max(0,Math.min(1,(vl-1.0)/2.0)),e=1-Math.pow(1-p,3),ang=-90+e*150+Math.sin(p*Math.PI)*8*(1-p);
   document.getElementById('needle').setAttribute('transform','rotate('+ang+' 300 300)');
   document.getElementById('tlfill').style.width=(Math.max(0,Math.min(1,(vl-4.0)/1.0))*100)+'%';
   var pu=vg.querySelector('.pulse'),k=((vl*1.2)%1);pu.style.boxShadow='0 0 0 '+(k*14)+'px rgba(127,160,255,'+(0.6*(1-k))+')';
 }
 var md=document.getElementById('s-media'),ml=t-45;
 if(md&&+md.style.opacity>0){
   var P=168,N=10*P,sy=ml<0.8?-10:(((ml-0.8)%2.4)/2.4)*900;
   document.getElementById('mscan').style.top=sy+'px';
   md.querySelectorAll('.col').forEach(function(c){var ci=+c.dataset.c;var off=((ml*(55+ci*18)+ci*70)%N);c.style.transform='translateY('+(-off)+'px)';
     c.querySelectorAll('.art').forEach(function(a,k){var y=k*P-off+75;var d=sy-y;a.classList.toggle('hot',ml>0.8&&Math.abs(d)<70);a.querySelector('.ck').style.opacity=(ml>0.8&&d>70&&d<900)?1:0;});});
 }
};
</script>'''
JS=JS.replace('__BL__',json.dumps(BLACK)).replace('__GR__',json.dumps(GREY)).replace('__CE__',json.dumps({k:v[:2] for k,v in cent.items() if k in SMALL}))
# film JS core
core=src[src.index('<script>'):src.index('</script>')+9]
core=core.replace("var conv=ease((t-5.9)/1.6);","var conv=ease((t-2.4)/1.4);").replace("var appear=ease((t-0.8-k*0.25)/0.6);","var appear=ease((t-0.2-k*0.15)/0.5);").replace("c.style.opacity=appear*(1-ease((t-7.0)/0.8));","c.style.opacity=appear*(1-ease((t-3.4)/0.6));").replace("t<8.2?'visible':'hidden'","t<4.2?'visible':'hidden'")
CARDS=CARDS.replace('data-e="8.2"','data-e="4.2"')
body=head.replace('</head>',CSS+'<script src="mapdata.js"></script></head>')
html=body+INTRO+CARDS+INTRO2+'\n'+OPEN+'\n'+MAP+'\n'+ORGS+'\n'+SANC+'\n'+SCAN+'\n'+MEDIA+'\n'+VIG+'\n'+INV+'\n'+WEEK+'\n'+DASH+'\n'+END+'\n'+RAIL+'\n'+core+JS+'\n</body></html>'
open('film2.html','w',encoding='utf-8').write(html)
print('ok',len(html))
