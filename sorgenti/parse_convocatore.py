"""Legge txt/Convocatore_v2.4_FINALE.txt e scrive convocatore.json
(tabella dell'eidolon, privilegi, forme, evoluzioni con meccaniche, doti, archetipi).
Le MECCANICHE delle evoluzioni sono codificate qui sotto (MECC): il testo viene sempre dal manuale."""
import re,json,os
R=os.path.dirname(os.path.abspath(__file__))
L=[l.strip() for l in open(os.path.join(R,'txt','Convocatore_v2.4_FINALE.txt'),encoding='utf8').read().split('\n')]
L=[l for l in L if l]
def slug(s):
    s=s.lower()
    for a,b in [('à','a'),('è','e'),('é','e'),('ì','i'),('ò','o'),('ù','u'),("'",''),('’',''),('[',''),(']','')]: s=s.replace(a,b)
    return re.sub(r'[^a-z0-9]+','_',s).strip('_')
N=lambda s:int(s.replace('+','').replace('°','').split('/')[0])
# --- tabella eidolon
c=L.index('Tabella dell’eidolon'); cells=L[c+13:c+13+240]
tab=[]
for i in range(20):
    r=cells[i*12:(i+1)*12]
    tab.append({'liv':N(r[0]),'dv':int(r[1]),'att':int(r[2]),'ba':N(r[3]),'baArmi':r[4],'tsB':N(r[5]),'tsS':N(r[6]),'pab':int(r[7]),'tal':int(r[8]),'arm':N(r[9]),'forDes':N(r[10]),'pe':int(r[11])})
# --- tabella convocatore (BAB, TS)
c=L.index('Tabella del convocatore'); cells=L[c+7:c+7+120]
conv=[]
for i in range(20):
    r=cells[i*6:(i+1)*6]; conv.append({'liv':N(r[0]),'bab':N(r[1]),'t':N(r[2]),'r':N(r[3]),'v':N(r[4]),'priv':r[5]})
# --- testi dei privilegi (dal blocco 'Privilegi di classe' fino a 'Incantesimi da convocatore')
def blocco(start,stop,titoli):
    a=L.index(start); b=L.index(stop,a); out={}; cur=None
    for l in L[a+1:b]:
        if l in titoli: cur=l; out[cur]=[]
        elif cur: out[cur].append(l)
    return out
priv_tit=[l for l in L[L.index('Privilegi di classe',100):L.index('Incantesimi da convocatore')] if len(l)<60 and not l.endswith('.')]
privilegi=blocco('Privilegi di classe','Incantesimi da convocatore',priv_tit)
pe_tit=['Punti evoluzione','Etica','Guarigione limitata','Rituale protettivo','Scurovisione','Comunicazione','Oggetti magici','Legame arcano','Riduzione del danno','Eludere','Aumento di caratteristica','Devozione','Multiattacco','Eludere migliorato']
a=L.index('Privilegi dell’eidolon',L.index('Tabella dell’eidolon')+250)
privE={}; cur=None
for l in L[a+1:L.index('Forme degli eidolon')]:
    if l in pe_tit: cur=l; privE[cur]=[]
    elif cur: privE[cur].append(l)
# --- forme
FORME={
 'aberrante':{'nome':'Aberrante','vel':6,'tsBuoni':['t','r'],'base':['morso','massa_tentacolare','afferrare:massa_tentacolare','armatura_naturale_migliorata']},
 'amorfo':{'nome':'Amorfo','vel':6,'tsBuoni':['t','v'],'base':['massa_tentacolare','afferrare:massa_tentacolare'],'corpoInforme':True},
 'bipede':{'nome':'Bipede','vel':9,'tsBuoni':['t','v'],'base':['arti_braccia','arti_gambe','competenza_nelle_armi_semplici'],'scelta':['artigli','schianto']},
 'quadrupede':{'nome':'Quadrupede','vel':12,'tsBuoni':['t','r'],'base':['morso','afferrare:morso','arti_gambe','arti_gambe']},
 'serpentiforme':{'nome':'Serpentiforme','vel':6,'tsBuoni':['r','v'],'base':['morso','afferrare:morso','coda','colpo_di_coda','portata:colpo_di_coda']},
 'taurico':{'nome':'Taurico','vel':12,'tsBuoni':['t','v'],'base':['arti_braccia','arti_gambe','arti_gambe'],'scelta':['artigli','schianto'],'mediaCosta':2},
}
fi=L.index('Forme degli eidolon'); ftxt=L[fi:L.index('Evoluzioni',fi)]
for k,f in FORME.items():
    j=ftxt.index(f['nome']); f['taglia']=ftxt[j+1]; f['testoBase']=ftxt[j+4]
    assert str(f['vel'])+' m'==ftxt[j+2], (k,ftxt[j+2])
ci=[i for i,l in enumerate(ftxt) if l.startswith('Corpo informe')][0]
corpoInforme=ftxt[ci+1]
tagliaPiccola=[l for l in ftxt if l.startswith('Taglia Piccola:')][0]
# --- evoluzioni: MECCANICHE
# att: attacco naturale {nome,dado,n,tipo p/s,forza} ; lv: livello minimo ; req: evoluzioni richieste ; multi: True|'2@10'|'2@7'|'ogni5'|'per:arti_braccia'|'per:coda' ;
# eff: effetti numerici ; scelta: parametro da scegliere (energia/attacco/abilita/caratteristica/effetto)
MECC={
 'addestrato':{'multi':True,'scelta':'abilita'},
 'afferrante':{'nota':'+4 alle manovre per iniziare o mantenere una lotta'},
 'anfibio':{},
 'apparato_natatorio':{'multi':True,'eff':{'nuotare':6}},
 'armatura_naturale_migliorata':{'multi':'2@10','eff':{'caNat':2}},
 'artigli':{'req':['arti_braccia'],'multi':'per:arti_braccia','att':{'nome':'Artiglio','dado':'1d4','n':2,'tipo':'p'}},
 'attacchi_magici_sop':{},
 'bonus_ai_tiri_salvezza':{'multi':True,'scelta':'effetto'},
 'cacciatore':{'req':['fiuto']},
 'cavalcatura':{'forme':['aberrante','quadrupede','serpentiforme']},
 'coda':{'multi':True},
 'coda_prensile':{'req':['coda']},
 'colpo_di_coda':{'req':['coda'],'multi':'per:coda','att':{'nome':'Colpo di coda','dado':'1d8','n':1,'tipo':'s'}},
 'competenza_nelle_armi_da_guerra':{'req':['competenza_nelle_armi_semplici']},
 'competenza_nelle_armi_semplici':{},
 'danno_naturale_migliorato':{'multi':True,'scelta':'attacco','reqAtt':True},
 'fiuto':{'sensi':'Fiuto 9 m'},
 'morso':{'att':{'nome':'Morso','dado':'1d6','n':1,'tipo':'p','forza':1.5}},
 'portata':{'multi':True,'scelta':'attacco','reqAtt':True},
 'presenza_innaturale':{},
 'pungiglione':{'req':['coda'],'multi':'per:coda','att':{'nome':'Pungiglione','dado':'1d6','n':1,'tipo':'p'}},
 'resistenza':{'multi':True,'scelta':'energia'},
 'sanguinamento':{'multi':True,'scelta':'attacco','reqAtt':True},
 'sbilanciare':{'req':['morso']},
 'scalare':{'eff':{'scalare':'meta'}},
 'schianto':{'req':['arti_braccia'],'multi':'per:arti_braccia','att':{'nome':'Schianto','dado':'1d8','n':1,'tipo':'p'}},
 'sguardo_ipnotico':{'cd':'car'},
 'slot_condiviso':{'multi':True},
 'spingere':{'multi':True,'scelta':'attacco','reqAtt':True},
 'tentacolo':{'multi':True,'att':{'nome':'Tentacolo','dado':'1d4','n':1,'tipo':'s'}},
 'tiri_salvezza_migliorati':{'multi':'2@10','eff':{'ts':1}},
 'trascinare':{'multi':True,'scelta':'attacco','reqAtt':True},
 'viscido':{'nota':'+4 Artista della fuga e +4 DMC per sfuggire alla lotta'},
 'vista_vitale':{},
 'afferrare':{'lv':7,'multi':True,'scelta':'attacco','reqAtt':True},
 'arti_braccia':{'multi':True},
 'arti_gambe':{'multi':True,'eff':{'vel':3}},
 'attacchi_energetici_sop':{'multi':True,'scelta':'energia'},
 'aumento_di_caratteristica':{'multi':'ogni5','scelta':'caratteristica','eff':{'car':2}},
 'aura_innaturale':{},
 'barriera_arcana':{'eff':{'barriera':True}},
 'chele':{'req':['arti_braccia'],'multi':'per:arti_braccia','att':{'nome':'Chela','dado':'1d6','n':2,'tipo':'p'}},
 'corna':{'att':{'nome':'Corna','dado':'1d10','n':1,'tipo':'p'}},
 'fortificazione':{'lv':4,'multi':'2@7'},
 'immunita_sop':{'multi':True,'scelta':'energia'},
 'magia_condivisa_mag':{},
 'massa_tentacolare':{'att':{'nome':'Massa tentacolare','dado':'1d8','n':1,'tipo':'s'}},
 'percezione_tellurica':{'lv':7,'sensi':'Percezione tellurica 9 m'},
 'sete_di_sangue':{'lv':7},
 'speroni':{'lv':4,'forme':['quadrupede']},
 'squarciare':{'lv':4,'req':['artigli','afferrare']},
 'squartare':{'lv':6,'req':['artigli']},
 'stritolare':{'req':['afferrare']},
 'talentuoso':{'multi':True},
 'testa':{'multi':True},
 'travolgere':{'cd':'for'},
 'veleno':{'lv':7,'reqUno':['morso','pungiglione'],'cd':'cos','extra':{'nome':'CD +2','costo':1}},
 'balzare':{'lv':7,'forme':['quadrupede']},
 'inghiottire':{'lv':9,'req':['afferrare','morso']},
 'levitazione':{'eff':{'volo':9}},
 'mente_aliena':{'lv':9,'cd':'car'},
 'percezione_cieca':{'lv':9,'sensi':'Percezione cieca 9 m'},
 'presenza_inquietante':{'lv':11,'cd':'car'},
 'ragnatela':{'lv':7,'cd':'cos'},
 'sacrificio_di_sangue_sop':{},
 'scavare':{'lv':7,'eff':{'scavare':'meta'}},
 'amorfo':{},
 'evanescenza_sop':{'lv':15},
 'guarigione':{'lv':11},
 'immunita_a_unenergia':{'lv':9,'multi':True,'scelta':'energia'},
 'porta_dimensionale_mag':{'lv':17},
 'resistenza_agli_incantesimi':{'lv':9},
 'soffio':{'lv':9,'cd':'cos','scelta':'energia','extra':{'nome':'soffio aggiuntivo (max 3/giorno)','costo':1,'max':2}},
 'taglia_superiore':{'lv':9,'taglia':True},
}
ei=L.index('Evoluzioni',fi); ee=L.index('Doti da convocatore',ei)
evo=[]; costo=None; cur=None
tit=set()
seg=L[ei+1:ee]
for i,l in enumerate(seg):
    m=re.match(r'Evoluzioni da (\d) punt',l)
    if m: costo=int(m.group(1)); continue
    if costo is None: continue
    if slug(l) in MECC and len(l)<45:
        cur={'id':slug(l),'nome':l,'costo':costo,'requisiti':'','testo':[],'speciale':''}; evo.append(cur); continue
    if cur is None: continue
    if l.startswith('Requisiti:'):
        cur['requisiti']=l[10:].strip()
    elif l.startswith('Speciale:'): cur['speciale']=l[9:].strip()
    else: cur['testo'].append(l)
for e in evo:
    e['testo']=' '.join(e['testo']); e.update(MECC[e['id']])
    # livello minimo dichiarato nei requisiti deve coincidere
    m=re.search(r'Convocatore di (\d+)° livello',e['requisiti']+' '+e['testo'][:60])
    if m and e['id']!='taglia_superiore': assert e.get('lv')==int(m.group(1)),(e['id'],m.group(1),e.get('lv'))
missing=set(MECC)-{e['id'] for e in evo}
assert not missing, missing
# --- doti
di=ee; de=L.index('Archetipi del convocatore',di)
doti=[]; cur=None
dseg=L[di+2:de]
for l in dseg:
    if len(l)<60 and not l.endswith('.') and not l.startswith('Requisiti'):
        nome=re.sub(r'\s*\[metaevocazione\]','',l)
        cur={'id':slug(nome),'nome':nome,'meta':'[metaevocazione]' in l,'requisiti':'','testo':''}; doti.append(cur)
    elif l.startswith('Requisiti:'): cur['requisiti']=l[10:].strip()
    else: cur['testo']=(cur['testo']+' '+l).strip()
# --- archetipi
ARCH=['Leader empireo','Profeta','Elementalista','Creativo','Controevocatore','Demonologo','Armonizzatore','Cavalca eidolon','Signore delle Schiere']
ai=de; ae=L.index('Custode grigio',ai) if 'Custode grigio' in L[ai:] else len(L)
aseg=L[ai+1:ae]
arch=[]; cur=None; pv=None
for k,l in enumerate(aseg):
    if l in ARCH:
        cur={'id':slug(l),'nome':l,'descr':aseg[k+1],'voci':[]}; arch.append(cur); pv=None; continue
    if cur is None or l==cur['descr']: continue
    if l.startswith('Privilegio di classe'):
        pv['diciture'].append(l); continue
    if re.match(r'^(Abilità di classe|Punti abilità per livello|Competenze offensive|Competenze difensive|Ricchezza iniziale|Allineamento):',l):
        cur['voci'].append({'nome':l.split(':')[0],'testo':l.split(':',1)[1].strip(),'diciture':[]}); pv=cur['voci'][-1]; continue
    if len(l)<50 and not l.endswith('.'):
        pv={'nome':l,'testo':'','diciture':[]}; cur['voci'].append(pv)
    else: pv['testo']=(pv['testo']+' '+l).strip()
for a in arch:
    tocca=[]
    for v in a['voci']:
        for d in v['diciture']:
            for part in re.split(r'Privilegio di classe (?:modificato|sostituito): ',d)[1:]:
                for x in re.split(r',| e ',part.rstrip('. ')):
                    n=re.sub(r'\s+(al|ai|all’)\s.*$|\s+a ciascun.*$|\s+all’\d.*$','',x.strip())
                    if n: tocca.append(n.strip())
    a['tocca']=sorted(set(tocca))
json.dump({'tabella':tab,'classe':conv,'privilegi':{k:' '.join(v) for k,v in privilegi.items()},'privilegiEidolon':{k:' '.join(v) for k,v in privE.items()},
  'forme':FORME,'corpoInforme':corpoInforme,'tagliaPiccola':tagliaPiccola,'evoluzioni':evo,'doti':doti,'archetipi':arch},
  open(os.path.join(R,'convocatore.json'),'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('evoluzioni',len(evo),{c:sum(1 for e in evo if e['costo']==c) for c in (1,2,3,4)},'doti',len(doti),'archetipi',[(a['nome'],a['tocca']) for a in arch])
print('privilegi',list(privilegi)[:40])
