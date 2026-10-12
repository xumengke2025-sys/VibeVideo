// The only clock. No text or narration is burned into the film.
export const FILM={duration:60,fps:24,width:1080,height:1920,cuts:[7,16,25,36,46,54]};
export const SHOTS=[
 {id:'ambition',start:0,end:7,meaning:'一滴墨唤出年轻将军与古老金字塔',action:'落墨→人物显影→视线指向远方',camera:'近景轻退，前景与远景不同速度',join:'人物墨尾续为海上航路'},
 {id:'crossing',start:7,end:16,meaning:'跨海远征',action:'航线生长→舰船追随→沙漠从航线末端浮现',camera:'由船舷拉开以见路径',join:'海面墨线接为沙地行军路线'},
 {id:'victory',start:16,end:25,meaning:'军阵推进，陆上胜利',action:'列兵行进→结阵→硝烟越过画面',camera:'沿行军方向斜移，在军阵接触时停住',join:'硝烟加浓，吞入海战'},
 {id:'fleet-lost',start:25,end:36,meaning:'海上受击，归路断裂',action:'舰队建立→三次火光→浓墨烟柱与断裂航路',camera:'缓进靠近受击舰，爆炸时短促振动',join:'墨烟退为拓印的黑墨'},
 {id:'knowledge',start:36,end:46,meaning:'学者绘图与石碑发现，留下记录',action:'石碑从墨中显影→卷纸展开→羽笔描摹古迹',camera:'从石碑退到观察者与纸页',join:'纸页弧线转为归船尾迹'},
 {id:'departure',start:46,end:54,meaning:'人离去，远征消散',action:'船远去→人物与旗帜散墨→沙漠留下',camera:'静观小船缩小，前景消退',join:'断裂墨线消散，古迹留存'},
 {id:'memory',start:54,end:60,meaning:'征服消失，历史的痕迹长存',action:'军队已空→石碑淡影与金字塔留下→末帧安静停留',camera:'轻退后停住',join:'结束在纸色，保留2秒凝视'}
];
export const SOUND_EVENTS=[{t:.7,type:'drop'},{t:7.2,type:'brush'},{t:16.1,type:'brush'},{t:22,type:'distant-drum'},{t:26.6,type:'cannon'},{t:29.3,type:'cannon'},{t:32.1,type:'cannon'},{t:36.4,type:'paper'},{t:39.4,type:'brush'},{t:43,type:'pen'},{t:46.1,type:'sea'},{t:54.4,type:'bell'}];
