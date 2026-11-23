import {useEffect,useState} from 'react';
type Metrics={resources:number;average_quality:number;validation_runs:number;invalid_runs:number};
type Resource={id:string;resourceType:string;quality_score:number;created_at:string};
const API=import.meta.env.VITE_API_URL||'http://localhost:8000';
export default function App(){
 const [metrics,setMetrics]=useState<Metrics>({resources:0,average_quality:0,validation_runs:0,invalid_runs:0});
 const [resources,setResources]=useState<Resource[]>([]);
 const [status,setStatus]=useState('Connecting to API…');
 useEffect(()=>{Promise.all([fetch(`${API}/api/v1/metrics`).then(r=>{if(!r.ok)throw Error();return r.json()}),fetch(`${API}/api/v1/resources`).then(r=>r.json())]).then(([m,rows])=>{setMetrics(m);setResources(rows);setStatus('Live API connected')}).catch(()=>setStatus('API unavailable — start the API service'))},[]);
 return <main><header><div><p className="eyebrow">HEALTH DATA ENGINEERING</p><h1>FHIR Quality Console</h1><p className="sub">R4 resource validation and data-quality monitoring</p></div><span className="status">● {status}</span></header>
 <section className="cards"><article><small>INGESTED RESOURCES</small><strong>{metrics.resources}</strong><span>Stored synthetic FHIR resources</span></article><article><small>AVERAGE QUALITY</small><strong>{metrics.average_quality}%</strong><span>Weighted quality score</span></article><article><small>VALIDATION RUNS</small><strong>{metrics.validation_runs}</strong><span>Total validation checks</span></article><article><small>INVALID RUNS</small><strong>{metrics.invalid_runs}</strong><span>Runs with errors</span></article></section>
 <section className="panel"><div className="panelhead"><div><h2>Resource inventory</h2><p>Most recently ingested resources</p></div><span>FHIR R4</span></div><table><thead><tr><th>Resource ID</th><th>Type</th><th>Quality</th><th>Created</th></tr></thead><tbody>{resources.map(r=><tr key={r.id}><td>{r.id}</td><td><span className="tag">{r.resourceType}</span></td><td>{r.quality_score}%</td><td>{new Date(r.created_at).toLocaleString()}</td></tr>)}{resources.length===0&&<tr><td colSpan={4} className="empty">No resources yet. Load synthetic samples using the API.</td></tr>}</tbody></table></section><footer>Demo environment · Synthetic data only · Not for clinical use</footer></main>
}
