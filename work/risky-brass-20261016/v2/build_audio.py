from pathlib import Path
R=Path(__file__).parent
s=(R.parent/'v1'/'make_audio.py').read_text(encoding='utf-8').replace('24-second','80-second').replace('DURATION = 24','DURATION = 80').replace('sample-audio.wav','full-audio.wav')
a=s.index('# D minor /')
b=s.index('def contact(',a)
s=s[:a]+'''# Thirty composed bars: presentation, inquiry, trials, return and cadence.
# A continuous composition with changing voicings and density, not a looped sample.
progression = [(50,57,62,65),(46,58,62,65),(43,55,58,62),(45,57,61,64),
               (50,57,62,65),(48,55,60,64),(46,58,62,65),(45,57,61,64),
               (43,55,58,62),(50,57,62,65),(46,58,62,65),(45,57,61,64),
               (50,57,62,65),(43,55,58,62),(45,57,61,64),(50,57,62,65),
               (46,58,62,65),(43,55,58,62),(45,57,61,64),(50,57,62,65),
               (46,58,62,65),(48,55,60,64),(43,55,58,62),(45,57,61,64),
               (50,57,62,65),(46,58,62,65),(43,55,58,62),(45,57,61,64),
               (50,57,62,65),(38,50,57,62)]
phrases = [(74,77,76,74),(77,81,79,77),(79,77,74,70),(73,76,81,79),
           (77,74,69,74),(76,79,81,79),(77,82,81,77),(76,73,69,73)]
for bar,chord in enumerate(progression):
    origin=bar*4*BEAT
    section=0 if bar<8 else 1 if bar<12 else 2 if bar<21 else 3
    density=[.85,.74,.90,.72][section]
    add(note(chord[0],2.7,'bow'),origin,.030*density,-.13)
    pattern=[1,2,3,2,1,3,2,3] if bar%2==0 else [1,3,2,3,1,2,3,2]
    for step,degree in enumerate(pattern):
        if bar==29 and step>1:continue
        add(note(chord[degree],1.10),origin+step*BEAT/2,.047*density,-.34)
    phrase=phrases[(bar+section*2)%len(phrases)]
    for step,pitch in enumerate(phrase):
        if bar==29:continue
        # Rest in alternate phrases lets mechanical actions remain audible.
        if section==1 and step==2:continue
        pitch += -12 if bar in [10,11,24,25] else 0
        add(note(pitch,1.35),origin+step*BEAT,.043*density,.33)
    if bar>=12 and bar<21:
        add(note(chord[2]+12,2.4,'bow'),origin,.012,.16)
    if bar==29:
        for pitch in [38,50,57,62,65,74]:add(note(pitch,2.55),origin,.033,0)

''' +s[b:]
a=s.index('for when, strength, label in [')
b=s.index('# A light room response',a)
events=[(3.5,.07,'company-card'),(5.0,.07,'event-card'),(8.5,.06,'evidence-arrival'),(10.2,.035,'evidence-open'),(12,.04,'source-1-saved'),(12.8,.04,'source-2-saved'),(13.1,.045,'pending-card'),(18.3,.04,'guarantee-link'),(18.9,.04,'group-link'),(24.5,.06,'council-arrival'),(26.2,.035,'expert-card'),(28.6,.04,'opinion-return'),(29.1,.04,'question-return'),(34.35,.07,'case-arrives'),(35.45,.09,'clamp-closed'),(35.65,.09,'seal-contact'),(36.5,.04,'trial-1-dispatch'),(37.55,.04,'trial-2-dispatch'),(38.6,.04,'trial-3-dispatch'),(38.7,.05,'trial-1-dock'),(39.75,.05,'trial-2-dock'),(40.8,.05,'trial-3-dock'),(46.3,.055,'pressure-change'),(47.3,.035,'B-response'),(48.1,.035,'C-response'),(50.5,.055,'mitigation-assumption'),(59,.06,'recorder-arrival'),(59.7,.025,'record-line-1'),(61,.025,'record-line-2'),(62.3,.025,'record-line-3'),(65.7,.045,'bundle-loaded'),(72,.055,'return-arrival'),(73.5,.03,'review-1'),(73.8,.03,'review-2'),(74.1,.03,'review-3'),(75.6,.045,'pending-filed')]
s=s[:a]+'for when,strength,label in '+repr(events)+':\n    contact(when,strength,label)\n\n'+s[b:]
s=s.replace('if peak > .65:\n    mix *= .65/peak','if peak > 0:\n    mix *= .50/peak')
(R/'make_audio.py').write_text(s,encoding='utf-8')

