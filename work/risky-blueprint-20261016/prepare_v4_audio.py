from pathlib import Path
r=Path(__file__).resolve().parent
original=(r/'v3/make_audio.py').read_text(encoding='utf-8')
head=original[:original.index('chords=')]
tail=original[original.index('music += accents'):]
score=r'''# A quiet, deliberate 120 BPM score. Picture and score share event contacts.
def felt(note,length=1.5):
    t=ts(length);f=freq(note)
    sig=(np.sin(2*np.pi*f*t+1.3*np.sin(2*np.pi*f*2*t)*np.exp(-t*7))
         +.18*np.sin(2*np.pi*f*3*t)*np.exp(-t*9))
    return sig*env(t,.004,3.4)*np.minimum((length-t)/.12,1)*.14

def mallet(note,length=.8):
    t=ts(length);f=freq(note)
    return (np.sin(2*np.pi*f*t)+.2*np.sin(2*np.pi*f*3.97*t)*np.exp(-t*10))*env(t,.002,6)*.14

chords=[[50,57,62,65,76],[46,53,58,62,69],[48,55,60,65,74],[45,52,57,62,69],
        [50,57,62,65,76],[46,53,58,62,69],[48,55,60,64,74],[45,52,57,62,69],
        [46,53,58,62,69],[50,57,62,65,76]]
levels=[.36,.48,.56,.40,.42,.30,.68,.80,.52,.32]
for bar,notes in enumerate(chords):
    at=bar*8;level=levels[bar]
    # Rich sustain with an eight-second phrase. Keep transients clearly distinct.
    add(music,at,pad(notes[1:],min(8.6,80-at)),gain=1.4*level,kind='phrase-harmony')
    motif=[notes[2]+12,notes[3]+12,notes[1]+12,notes[2]+12]
    for j,offset in enumerate([0,2,4,6]):
        add(music,at+offset,felt(motif[j],1.85),gain=.75*level,pan=[-.2,.15,-.12,.2][j],kind='theme')
    for beat in range(16):
        when=at+beat*.5
        # Solid half-time pulse; avoid the previous constant busy dance beat.
        if beat%4==0:
            add(music,when,kick(),gain=.25*level,kind='pulse')
            add(music,when,bass(notes[0]-12,1.4),gain=.55*level,kind='bass')
        if beat%4==2:add(music,when,snare(),gain=.11*level,pan=.12,kind='soft-rim')
        if 48<=when<64:
            add(music,when,hat(),gain=.17*level,pan=(-.15 if beat%2 else .15),kind='clock')
            if beat%2:add(music,when,mallet(notes[1+beat%3]+12),gain=.33*level,pan=(-.22 if beat%4==1 else .22),kind='counterpoint')
        elif beat%2==0 and 8<=when<72:
            add(music,when,hat(),gain=.07*level,pan=.1,kind='quiet-clock')

# Beat-aligned stereo echoes from the tonal bed; no off-grid 0.19s delays.
for delay,gain in [(.25,.10),(.5,.06),(.75,.025)]:
    k=round(delay*SR);music[k:]+=music[:-k,::-1].copy()*gain

# Deliberate breath before lock, assumption-change, and archive contact.
for anchor in [10,18,36,44,52,62,64,68,75]:
    a,b=round((anchor-.18)*SR),round(anchor*SR)
    u=np.linspace(0,1,b-a)
    music[a:b]*=(1-.82*np.sin(u*np.pi/2)**2)[:,None]

for event in score['events']:
    at=event['at'];eid=event['id'];kind=event['sound']
    if kind=='lock':
        t=ts(.18)
        metal=(np.sin(2*np.pi*970*t)+.27*np.sin(2*np.pi*2340*t))*env(t,.0015,35)*.12
        add(fx,at,metal,gain=.65,kind='contact',event=eid)
        add(accents,at,mallet(event['note']),gain=.6,kind='contact-tone',event=eid)
    elif kind=='scan':
        t=ts(.8);noise=rng.normal(0,1,len(t));smooth=np.convolve(noise,np.ones(31)/31,mode='same')
        add(fx,at-.8,smooth*np.sin(np.pi*t/.8)**2*.045,kind='scan-approach')
        add(accents,at,felt(event['note'],1),gain=.6,kind='scan-arrival',event=eid)
    elif kind=='resolve':
        add(accents,at,pad([50,57,62,65,76],4.8),gain=1.8,kind='resolve-chord',event=eid)
        add(accents,at,felt(74,2),gain=.8,kind='resolve-note',event=eid)
    else:
        add(accents,at,mallet(event['note']+12),gain=.75 if kind=='drop' else .55,kind='action-note',event=eid)
        if kind in ['drop','bell']:add(accents,at,kick(),gain=.30 if kind=='drop' else .15,kind='action-pulse',event=eid)

# Three anticipation notes lead into the new-hypothesis contact on beat 104.
for i,note in enumerate([62,65,69]):
    add(music,50.5+i*.5,mallet(note+12),gain=.25+i*.12,pan=-.2+i*.2,kind='assumption-pickup')

'''
(r/'v4/make_audio.py').write_text(head+score+tail,encoding='utf-8')
print('Wrote V4 phrase score and shared event contacts')
