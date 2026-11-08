import fs from 'fs';
import {feature} from 'topojson-client';
import {geoCentroid} from 'd3-geo';
const topo=JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-50m.json'));
const fc=feature(topo,topo.objects.countries);
const W=1500,H=700,lat0=80,lat1=-58;
const F=JSON.parse(fs.readFileSync('../fatf.json'));const ids=[...Object.keys(F.black),...Object.keys(F.grey),F.scenario_counterparty.iso];
const out={};
for(const f of fc.features){ if(ids.includes(f.id)){const [lo,la]=geoCentroid(f);out[f.id]=[+((lo+170)/360*W).toFixed(1),+((lat0-la)/(lat0-lat1)*H).toFixed(1),f.properties.name];}}
fs.writeFileSync('../cent.json',JSON.stringify(out));console.log(Object.keys(out).length);
