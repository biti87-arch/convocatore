"""Legge i due libri delle evocazioni (txt/) e scrive esterni.json ed elementali.json."""
import re,json,os
R=os.path.dirname(os.path.abspath(__file__))
ROM=['I','II','III','IV','V','VI','VII','VIII','IX']
FIELDS=['Tipo di esterno','Sensi','Statistiche','Caratteristiche','Abilità','Talenti','CA','PF','Tiri Salvezza','Attacchi','Immunità','Resistenze','RD','RI','Debolezze','Aura','Linguaggi']
def slug(s):
    s=s.lower()
    for a,b in [('à','a'),('è','e'),('é','e'),('ì','i'),('ò','o'),('ù','u'),("'",''),('’','')]: s=s.replace(a,b)
    return re.sub(r'[^a-z0-9]+','_',s).strip('_')
def num(s):
    m=re.search(r'[-+−]?\d+',s.replace('−','-')); return int(m.group()) if m else None
def parse(fname,hdr_re,libro):
    L=[l.strip() for l in open(os.path.join(R,'txt',fname),encoding='utf8').read().split('\n')]
    L=[l for l in L if l]
    grade=None; heads={}; GRUPPI=('Primordiali','Secondari','Esoterici')
    grp={i:l for i,l in enumerate(L) if l in GRUPPI}
    for i,l in enumerate(L):
        m=re.match(hdr_re,l)
        if m: heads[i]=ROM.index(m.group(1).upper())+1
    idx=[i for i,l in enumerate(L) if l.startswith('Tipo di esterno:')]
    out=[];ids=set()
    for k,i in enumerate(idx):
        nome=L[i-2]; descr=L[i-1]
        g=max((v for h,v in heads.items() if h<i-2),default=None) if heads else None
        g=[v for h,v in sorted(heads.items()) if h<i-2][-1]
        end=idx[k+1]-2 if k+1<len(idx) else len(L)
        body=L[i:end]
        # drop trailing grade headers / group headings
        gg=[v for h,v in sorted(grp.items()) if h<i-2]
        e={'gruppo':gg[-1] if gg else None,'id':None,'nome':nome,'libro':libro,'grado':g,'descr':descr,'campi':{},'magiche':[],'speciali':[]}
        mode=None
        for l in body:
            if re.match(hdr_re,l) or re.match(r'^GS [\d½]',l) or l in GRUPPI: continue
            fm=re.match(r'^('+'|'.join(map(re.escape,FIELDS))+r'):\s*(.*)$',l)
            if l.startswith('BMC:'):
                m=re.match(r'BMC:\s*(.*?)\s+DMC:\s*(.*)$',l); e['campi']['BMC']=m.group(1); e['campi']['DMC']=m.group(2); mode=None; continue
            if l.startswith('Capacità magiche'):
                mode='mag'; rest=l.split(':',1)[1].strip() if ':' in l else ''
                if rest: e['magiche'].append(rest)
                continue
            if l.startswith('Capacità e attacchi speciali') or l.startswith('Capacità speciali'): mode='spec'; continue
            if fm and mode is None: e['campi'][fm.group(1)]=fm.group(2); continue
            if fm and mode: e['campi'][fm.group(1)]=fm.group(2); mode=None if fm.group(1) in FIELDS else mode; continue
            if mode=='mag': e['magiche'].append(l)
            elif mode=='spec': e['speciali'].append(re.sub(r'^[\*•]\s*','',l))
            else: e.setdefault('altro',[]).append(l)
        c=e['campi']
        e['pf']=num(c.get('PF','')); e['dv']=num(re.search(r'\((\d+) DV',c.get('PF','')).group(1)) if re.search(r'\((\d+) DV',c.get('PF','')) else None
        tm=re.search(r'Taglia (\w+)',c.get('Statistiche','')); e['taglia']=tm.group(1).capitalize() if tm else None
        e['tipo']=c.get('Tipo di esterno','')
        e['ca']=num(c.get('CA',''))
        ts=c.get('Tiri Salvezza','')
        e['ts']={k:num(re.search(k+r'\s*([+\-−]?\d+)',ts).group(1)) if re.search(k+r'\s*([+\-−]?\d+)',ts) else None for k in ['Tempra','Riflessi','Volontà']}
        sid=slug(nome); 
        if sid in ids: sid=sid+'_'+str(g)
        ids.add(sid); e['id']=sid
        out.append(e)
    return out
es=parse('Libro_evocazioni_v2.5.txt',r'^Evoca esterno ([IVX]+)$','evocazioni')
el=parse('Libro_Evocazioni_Elementali_v1.txt',r'^EVOCA ELEMENTALE ([IVX]+)$','elementali')
for n,d in [('esterni.json',es),('elementali.json',el)]:
    json.dump(d,open(os.path.join(R,n),'w',encoding='utf8'),ensure_ascii=False,indent=1)
    print(n,len(d),{g:sum(1 for x in d if x['grado']==g) for g in range(1,10)})
    bad=[x['nome'] for x in d if not x['pf'] or not x['dv'] or not x['taglia'] or x['ca'] is None or 'Attacchi' not in x['campi']]
    print(' incompleti:',bad[:10], len(bad))
    print(' altro:',[(x['nome'],x['altro'][:2]) for x in d if x.get('altro')][:6])
