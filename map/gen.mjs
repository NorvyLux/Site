import fs from 'fs';
import {feature} from 'topojson-client';
import {geoContains,geoCentroid} from 'd3-geo';
const topo=JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-50m.json'));
const fc=feature(topo,topo.objects.countries);
const W=1500,H=700,step=13; // equirectangular, lat 80..-58
const lat0=80,lat1=-58;
const hl={'442':'LU','250':'FR','056':'BE','826':'GB','840':'US','276':'DE','756':'CH','784':'AE','643':'RU','156':'CN','076':'BR','710':'ZA','124':'CA','036':'AU','566':'NG','356':'IN'};
let dots=[];
for(let y=0;y<=H;y+=step){for(let x=0;x<=W;x+=step){
  const lon=-170+x/W*360, lat=lat0-(y/H)*(lat0-lat1);
  for(const f of fc.features){ if(geoContains(f,[lon,lat])){dots.push([x,y,f.id]);break;} }
}}
const pins={};
for(const f of fc.features){ if(hl[f.id]){const [lo,la]=geoCentroid(f);pins[hl[f.id]]=[ (lo+170)/360*W, (lat0-la)/(lat0-lat1)*H ];}}
pins['LU']=[ (6.13+170)/360*W,(lat0-49.6)/(lat0-lat1)*H ];
pins['FR']=[ (2.5+170)/360*W,(lat0-46.5)/(lat0-lat1)*H ];
pins['US']=[ (-98+170)/360*W,(lat0-39)/(lat0-lat1)*H ];
fs.writeFileSync('../mapdata.js','window.MAPDOTS='+JSON.stringify(dots)+';window.MAPPINS='+JSON.stringify(pins)+';window.MAPW='+W+';window.MAPH='+H+';');
console.log(dots.length,Object.keys(pins));
