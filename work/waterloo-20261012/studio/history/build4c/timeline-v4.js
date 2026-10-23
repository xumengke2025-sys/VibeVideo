export const DURATION=60,FPS=24;
export const EVENTS=[{t:11,kind:'cannon',duration:.12},{t:25.6,kind:'volley',duration:.13},{t:46.2,kind:'volley',duration:.14}];
export const SHOTS=[
 {id:'eagle-reveal',start:0,end:8,reads:'军鹰与旗帜→旗手→无边军阵',camera:'从鹰旗局部拉开；同源近层稍快于军阵'},
 {id:'cannon',start:8,end:15,reads:'完整炮组→11秒单次炮击→长烟幕',camera:'低位炮组；开火短停，后摇向烟幕'},
 {id:'cavalry',start:15,end:24,reads:'完整骑手与马→简化队列推进→军阵规模',subjectId:'horse',worldPath:'x=-35→110px',cameraPath:'x=-10→70px',screenRegion:'下部，完整马匹；右侧行进留白'},
 {id:'resistance',start:24,end:32,reads:'守军横列→25.6秒一次齐射→烟幕截断推进',camera:'拉开与横列停机；烟幕缓慢发展'},
 {id:'last-advance',start:32,end:45.55,reads:'法国军鹰→整齐阵列前进→旗手与压力',camera:'旗手轻微推进；40秒切近景手持旗杆'},
 {id:'break',start:45.55,end:54,reads:'短暂寂静→46.2秒决定性齐射→军阵在烟中散退',camera:'齐射停机，随后拉开看到反向运动'},
 {id:'dusk',start:54,end:60,reads:'同一旗手与低垂军旗→远方破碎队列→背光暗下',camera:'缓慢拉开，保留军鹰母题'}
];
export const shotAt=t=>SHOTS.find(s=>t>=s.start&&t<s.end)||SHOTS.at(-1);
