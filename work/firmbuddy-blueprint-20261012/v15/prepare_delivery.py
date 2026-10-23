from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'v14/verify_delivery.py').read_text(encoding='utf-8').replace('v14-burden-journey','v15-human-mechanism').replace('V14','V15')
s=s.replace('times=[5,11,16,20.3,21,21.7,28,33,39.5,40.2,40.9,51.1,51.8,52.5,65.1,65.8,66.5,75.5,76.2,76.9,81.9,82.6,83.3,89.5]','times=[4,10.4,14,18.4,19.2,20.8,24,30,35.2,38.4,44.8,48,51.2,54.4,59.2,60.8,64,67.2,72,76,79.2,81.6,86.4,89.6]')
s=s.replace('[21.6,40.8,52.4,66.4,76.8,83.2]','[20.8,38.4,54.4,64,79.2,85.6]')
(R/'verify_delivery.py').write_text(s,encoding='utf-8')
print('Final verification prepared')
