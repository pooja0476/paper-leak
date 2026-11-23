import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { LayoutDashboard, AlertTriangle, FolderSearch, MapPinned, ChartNoAxesCombined, ShieldCheck, Settings, Search, Bell, ChevronDown, Menu, X, ExternalLink, FileText, Image as ImageIcon, UserRound, Plus, Filter, ArrowUpRight, Activity, LogOut, CheckCircle2, CircleHelp, Eye } from 'lucide-react';
import './style.css';


const seedAlerts = [
 {id:'PLS-1042',exam:'NEET Sample Examination',source:'Telegram · @exam_updates',date:'22 Nov 2026 · 10:45 AM',risk:'High',score:87,status:'Pending',center:'Not assigned',reason:'OCR text has strong overlap with the authorised reference paper.',evidence:['paper-photo.jpg','extracted-text.txt'],link:'https://t.me/example/1042'},
 {id:'PLS-1039',exam:'State Board Mathematics',source:'Telegram · @study_materials',date:'22 Nov 2026 · 09:18 AM',risk:'Medium',score:64,status:'Under Review',center:'North Zone · review needed',reason:'Post claims to contain a paper; OCR match is partial.',evidence:['scan.pdf','ocr-output.txt'],link:'https://t.me/example/1039'},
 {id:'PLS-1035',exam:'Engineering Entrance Mock',source:'Public web submission',date:'21 Nov 2026 · 06:22 PM',risk:'Low',score:31,status:'Dismissed',center:'Not assigned',reason:'The file appears to be a previously published practice paper.',evidence:['submitted-file.pdf'],link:''},
 {id:'PLS-1028',exam:'State Board Physics',source:'Telegram · @paper_watch',date:'21 Nov 2026 · 01:05 PM',risk:'High',score:91,status:'Verified',center:'Center 028 · investigation ongoing',reason:'Multiple matching sections and consistent source references; manually reviewed.',evidence:['image-1.png','image-2.png','ocr-report.txt'],link:'https://t.me/example/1028'},
 {id:'PLS-1022',exam:'University Semester Exam',source:'Anonymous report',date:'20 Nov 2026 · 11:30 AM',risk:'Medium',score:58,status:'Pending',center:'Not assigned',reason:'Anonymous report includes a document claimed to be an exam paper.',evidence:['report-attachment.pdf'],link:''}
];
const centerRows = [
 {id:'CTR-028',name:'Center 028 · North Zone',exam:'State Board Physics',risk:'High',score:82,avg:'78 → 91',top:'4% → 18%',note:'Large changes in average marks and top-score share; review recommended.'},
 {id:'CTR-114',name:'Center 114 · Central Zone',exam:'NEET Sample Examination',risk:'Medium',score:66,avg:'72 → 79',top:'8% → 13%',note:'Moderate deviation from previous results; needs contextual review.'},
 {id:'CTR-209',name:'Center 209 · South Zone',exam:'University Semester Exam',risk:'Low',score:29,avg:'64 → 67',top:'6% → 7%',note:'Minor changes within expected range.'}
];
const historyRows = [
 {center:'Center 028',exam:'State Board Physics',year:'2025',avg:78,top:4},{center:'Center 028',exam:'State Board Physics',year:'2026',avg:91,top:18},
 {center:'Center 114',exam:'NEET Sample Examination',year:'2025',avg:72,top:8},{center:'Center 114',exam:'NEET Sample Examination',year:'2026',avg:79,top:13},
 {center:'Center 209',exam:'University Semester Exam',year:'2025',avg:64,top:6},{center:'Center 209',exam:'University Semester Exam',year:'2026',avg:67,top:7}
];
const nav = [
 {id:'dashboard',label:'Overview',icon:LayoutDashboard},{id:'alerts',label:'Leak Alerts',icon:AlertTriangle},{id:'cases',label:'Investigations',icon:FolderSearch},
 {id:'centers',label:'Center Analysis',icon:MapPinned},{id:'history',label:'Historical Data',icon:ChartNoAxesCombined},{id:'settings',label:'Admin Settings',icon:Settings}
];
const statusList=['Pending','Under Review','Verified','Dismissed','Closed'];
function Badge({children,kind=''}) { return <span className={`badge ${kind||String(children).toLowerCase().replaceAll(' ','-')}`}>{children}</span>; }
function App() {
 const [page,setPage]=useState('dashboard');
 const [alerts,setAlerts]=useState(()=>{try{return JSON.parse(localStorage.getItem('pls-alerts'))||seedAlerts;}catch{return seedAlerts;}});
 const [cases,setCases]=useState(()=>{try{return JSON.parse(localStorage.getItem('pls-cases'))||{};}catch{return {};}});
 const [active,setActive]=useState(null); const [search,setSearch]=useState(''); const [riskFilter,setRiskFilter]=useState('All risks'); const [statusFilter,setStatusFilter]=useState('All statuses'); const [note,setNote]=useState(''); const [toast,setToast]=useState(''); const [logged,setLogged]=useState(false); const [loginUser,setLoginUser]=useState(''); const [loginPass,setLoginPass]=useState(''); const [sidebarOpen,setSidebarOpen]=useState(false);
 const persistAlerts=(arr)=>{setAlerts(arr);localStorage.setItem('pls-alerts',JSON.stringify(arr));};
 const persistCases=(obj)=>{setCases(obj);localStorage.setItem('pls-cases',JSON.stringify(obj));};
 const filtered=useMemo(()=>alerts.filter(a=>`${a.id} ${a.exam} ${a.source} ${a.center} ${a.status}`.toLowerCase().includes(search.toLowerCase())&&(riskFilter==='All risks'||a.risk===riskFilter)&&(statusFilter==='All statuses'||a.status===statusFilter)),[alerts,search,riskFilter,statusFilter]);
 const stats={total:alerts.length,high:alerts.filter(a=>a.risk==='High').length,centers:centerRows.filter(c=>c.risk==='High').length,open:alerts.filter(a=>['Pending','Under Review'].includes(a.status)).length};
 const notify=(msg)=>{setToast(msg);setTimeout(()=>setToast(''),2800);};
 const changeStatus=(id,newStatus)=>{const updated=alerts.map(a=>a.id===id?{...a,status:newStatus}:a);persistAlerts(updated);const prev=cases[id]||{notes:[],history:[]};persistCases({...cases,[id]:{...prev,history:[...(prev.history||[]),{from:alerts.find(a=>a.id===id)?.status,to:newStatus,at:new Date().toLocaleString(),by:'Demo Admin'}]}});notify(`Case ${id} updated to ${newStatus}`);};
 const addNote=(id)=>{if(!note.trim())return;const prev=cases[id]||{notes:[],history:[]};persistCases({...cases,[id]:{...prev,notes:[...(prev.notes||[]),{text:note.trim(),at:new Date().toLocaleString(),by:'Demo Admin'}]}});setNote('');notify('Investigation note saved');};
 const openCase=(alert)=>{setActive(alert);setNote('');};
 const demoLogin=(e)=>{e.preventDefault();if(loginUser.trim()&&loginPass.trim()){setLogged(true);notify('Signed in to prototype');}else notify('Enter a username and password');};
 if(!logged) return <div className="login-shell"><div className="login-card"><div className="brand-mark"><ShieldCheck size={30}/></div><div className="eyebrow">EXAM INTEGRITY PLATFORM</div><h1>Paper Leak<br/>Sentinel</h1><p className="muted">Secure administration and investigation workspace</p><form onSubmit={demoLogin}><label>Admin username<input value={loginUser} onChange={e=>setLoginUser(e.target.value)} placeholder="Enter username" autoComplete="username"/></label><label>Password<input type="password" value={loginPass} onChange={e=>setLoginPass(e.target.value)} placeholder="Enter password" autoComplete="current-password"/></label><button className="primary full">Sign in <ArrowUpRight size={17}/></button></form><p className="login-hint"><CircleHelp size={14}/> Prototype login accepts any non-empty username and password.</p><div className="login-footer">DEMO UI · NOT CONNECTED TO REAL AUTHENTICATION</div></div></div>;
 const title=nav.find(n=>n.id===page)?.label||'Overview';
 return <div className="app">
  <aside className={`sidebar ${sidebarOpen?'open':''}`}><div className="brand"><div className="brand-mark"><ShieldCheck size={23}/></div><div><b>Paper Leak</b><span>Sentinel</span></div><button className="mobile-close" onClick={()=>setSidebarOpen(false)}><X/></button></div><div className="workspace-label">WORKSPACE</div><nav>{nav.map(n=>{const Icon=n.icon;return <button key={n.id} className={`nav-item ${page===n.id?'active':''}`} onClick={()=>{setPage(n.id);setSidebarOpen(false);}}><Icon size={18}/><span>{n.label}</span>{n.id==='alerts'&&stats.open>0&&<small>{stats.open}</small>}</button>;})}</nav><div className="sidebar-bottom"><div className="secure-label"><span className="pulse-dot"/> Prototype environment</div><div className="user-box"><div className="avatar">DA</div><div><b>Demo Admin</b><small>Administrator</small></div><button title="Sign out" onClick={()=>setLogged(false)}><LogOut size={16}/></button></div></div></aside>
  <main className="main"><header className="topbar"><button className="mobile-menu" onClick={()=>setSidebarOpen(true)}><Menu/></button><div className="crumb"><span>Paper Leak Sentinel</span><span className="slash">/</span><b>{title}</b></div><div className="top-actions"><span className="demo-pill">DEMO DATA</span><button className="icon-button" title="Notifications"><Bell size={18}/><i/></button><div className="top-user"><div className="avatar small">DA</div><span>Admin</span><ChevronDown size={15}/></div></div></header>
  <div className="content">
   {page==='dashboard'&&<><div className="page-heading"><div><div className="eyebrow">COMMAND CENTER</div><h1>Good afternoon, Admin</h1><p>Here is an overview of current alerts and investigations.</p></div><button className="outline" onClick={()=>setPage('alerts')}><Eye size={16}/> Review alerts</button></div><div className="stat-grid"><Stat icon={AlertTriangle} label="Total possible leaks" value={stats.total} color="blue" sub="All recorded alerts"/><Stat icon={Activity} label="High-risk alerts" value={stats.high} color="red" sub="Prioritise verification"/><Stat icon={MapPinned} label="Centers flagged" value={stats.centers} color="amber" sub="Needs human review"/><Stat icon={FolderSearch} label="Open investigations" value={stats.open} color="green" sub="Pending or under review"/></div><div className="dashboard-grid"><div className="panel"><div className="panel-head"><div><h2>Recent leak alerts</h2><p>Latest suspicious items received</p></div><button className="text-button" onClick={()=>setPage('alerts')}>View all <ArrowUpRight size={15}/></button></div><AlertTable items={alerts.slice(0,4)} onOpen={openCase}/></div><div className="panel"><div className="panel-head"><div><h2>Center risk overview</h2><p>Illustrative model outputs</p></div><button className="text-button" onClick={()=>setPage('centers')}>Details <ArrowUpRight size={15}/></button></div><div className="risk-bars">{centerRows.map(c=><div className="risk-row" key={c.id}><div className="risk-row-label"><b>{c.name.split(' · ')[0]}</b><Badge kind={c.risk}>{c.risk}</Badge></div><div className="bar-bg"><div className={`bar ${c.risk.toLowerCase()}`} style={{width:`${c.score}%`}}/></div><span className="risk-number">{c.score}</span></div>)}</div><div className="notice"><ShieldCheck size={17}/><span>Risk scores are leads for review—not proof of wrongdoing.</span></div></div></div><div className="panel activity-panel"><div className="panel-head"><div><h2>Recent activity</h2><p>Latest case updates</p></div></div><ActivityList alerts={alerts.slice(0,5)}/></div></>}
   {page==='alerts'&&<><div className="page-heading"><div><div className="eyebrow">DETECTION FEED</div><h1>Leak Alerts</h1><p>Review suspicious posts and evidence submitted by detection modules.</p></div><div className="heading-actions"><button className="outline" onClick={()=>{setSearch('');setRiskFilter('All risks');setStatusFilter('All statuses');}}><Filter size={16}/> Reset filters</button></div></div><div className="panel"><div className="filters"><div className="searchbox"><Search size={17}/><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search alert, exam, source or center…"/></div><select value={riskFilter} onChange={e=>setRiskFilter(e.target.value)}><option>All risks</option><option>High</option><option>Medium</option><option>Low</option></select><select value={statusFilter} onChange={e=>setStatusFilter(e.target.value)}><option>All statuses</option>{statusList.map(s=><option key={s}>{s}</option>)}</select></div><AlertTable items={filtered} onOpen={openCase}/><div className="table-foot">Showing {filtered.length} of {alerts.length} alerts · Demo records</div></div></>}
   {page==='cases'&&<><div className="page-heading"><div><div className="eyebrow">CASE WORKSPACE</div><h1>Investigations</h1><p>Review alerts, evidence, notes and status history.</p></div></div><div className="panel"><div className="filters"><div className="searchbox"><Search size={17}/><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search case ID, exam or status…"/></div><select value={statusFilter} onChange={e=>setStatusFilter(e.target.value)}><option>All statuses</option>{statusList.map(s=><option key={s}>{s}</option>)}</select></div><AlertTable items={filtered} onOpen={openCase}/></div></>}
   {page==='centers'&&<><div className="page-heading"><div><div className="eyebrow">MODEL OUTPUTS</div><h1>Exam Center Analysis</h1><p>Centers flagged by the analysis module for further review.</p></div></div><div className="stat-grid"><Stat icon={MapPinned} label="Centers in sample" value={centerRows.length} color="blue" sub="Illustrative records"/><Stat icon={AlertTriangle} label="High risk" value={centerRows.filter(c=>c.risk==='High').length} color="red" sub="Review first"/><Stat icon={Activity} label="Medium risk" value={centerRows.filter(c=>c.risk==='Medium').length} color="amber" sub="Review context"/><Stat icon={CheckCircle2} label="Low risk" value={centerRows.filter(c=>c.risk==='Low').length} color="green" sub="No immediate signal"/></div><div className="panel"><div className="panel-head"><div><h2>Flagged centers</h2><p>Sample anomaly scores supplied by Member 3's module (simulated here)</p></div></div><div className="center-list">{centerRows.map(c=><div className="center-card" key={c.id}><div className="center-main"><div className="center-icon"><MapPinned size={19}/></div><div><b>{c.name}</b><small>{c.id} · {c.exam}</small></div></div><div className="center-metrics"><div><small>Anomaly score</small><b>{c.score}/100</b></div><div><small>Avg marks</small><b>{c.avg}</b></div><div><small>Top scorers</small><b>{c.top}</b></div><Badge kind={c.risk}>{c.risk}</Badge></div><p className="center-note">{c.note}</p></div>)}</div><div className="notice"><CircleHelp size={17}/> Center flags are statistical signals only. They must not be treated as findings or proof.</div></div></>}
   {page==='history'&&<><div className="page-heading"><div><div className="eyebrow">PERFORMANCE TRENDS</div><h1>Historical Data</h1><p>Compare center results over time using sample records.</p></div></div><div className="panel"><div className="panel-head"><div><h2>Average marks comparison</h2><p>Sample 2025 and 2026 comparison by center</p></div></div><div className="chart-area"><div className="chart-grid"><span>100</span><span>75</span><span>50</span><span>25</span><span>0</span></div><div className="bars">{historyRows.map((r,i)=><div className="bar-group" key={i}><div className="bar-pair"><div className="chart-bar previous" style={{height:`${r.avg}%`}} title={`Average ${r.avg}`}/><div className="chart-bar current" style={{height:`${r.top*4}%`}} title={`Top scorer percentage ${r.top}%`}/></div><span className="bar-caption">{r.center}</span><small>{r.year}</small></div>)}</div></div><div className="chart-legend"><span><i className="legend previous"/> Average mark (sample)</span><span><i className="legend current"/> Top-scorer share (scaled for display)</span></div><div className="data-table-wrap"><table><thead><tr><th>Center</th><th>Exam</th><th>Year</th><th>Average marks</th><th>Top scorers</th></tr></thead><tbody>{historyRows.map((r,i)=><tr key={i}><td>{r.center}</td><td>{r.exam}</td><td>{r.year}</td><td>{r.avg}</td><td>{r.top}%</td></tr>)}</tbody></table></div></div><div className="notice"><CircleHelp size={17}/> Sample chart uses illustrative data. In the real system these fields will come from Member 3 and the shared database.</div></>}
   {page==='settings'&&<><div className="page-heading"><div><div className="eyebrow">ADMINISTRATION</div><h1>Admin Settings</h1><p>Prototype security notes and integration status.</p></div></div><div className="settings-grid"><div className="panel"><h2>Access and security</h2><SettingRow title="Admin sign-in" desc="Demo-only form. Replace with server authentication before deployment." status="Prototype"/><SettingRow title="Role-based access" desc="Planned permission checks for admins and investigators." status="Not connected"/><SettingRow title="Audit history" desc="Case status changes and notes are stored in this browser prototype." status="Enabled locally"/><SettingRow title="Data protection" desc="Do not put real student or sensitive evidence into this demo." status="Demo guidance"/></div><div className="panel"><h2>Integration status</h2><SettingRow title="Member 1 · Telegram monitor" desc="Source links and evidence metadata." status="Awaiting API"/><SettingRow title="Member 2 · OCR / leak detector" desc="Alert IDs, match score, risk and OCR evidence." status="Awaiting API"/><SettingRow title="Member 3 · ML analysis" desc="Center anomaly and historical analysis outputs." status="Awaiting API"/><SettingRow title="Shared database" desc="Common schema and API endpoints to be agreed." status="Not connected"/></div></div><div className="panel about-panel"><h2>About this prototype</h2><p>This is an interactive frontend demonstration. It uses sample records, local browser storage for case status and notes, and a mock login. It is not yet a production secure system and is not connected to the other members' modules.</p></div></>}
  </div>
  </main>
  {active&&<div className="modal-back" onClick={()=>setActive(null)}><div className="case-modal" onClick={e=>e.stopPropagation()}><div className="modal-head"><div><div className="eyebrow">CASE DETAILS</div><h2>{active.id}</h2><p>{active.exam}</p></div><button className="icon-button" onClick={()=>setActive(null)}><X/></button></div><div className="case-overview"><div><small>Risk</small><Badge kind={active.risk}>{active.risk}</Badge></div><div><small>OCR match</small><b>{active.score}%</b></div><div><small>Current status</small><Badge kind={active.status}>{active.status}</Badge></div></div><div className="case-section"><h3>Source information</h3><p><b>Source:</b> {active.source}</p><p><b>Collected:</b> {active.date}</p><p><b>Center:</b> {active.center}</p>{active.link&&<p><b>Source link:</b> <a href={active.link} target="_blank" rel="noreferrer">Open source <ExternalLink size={13}/></a></p>}</div><div className="case-section"><h3>Detection reason</h3><p className="reason-box">{active.reason}</p></div><div className="case-section"><h3>Evidence references</h3><div className="evidence-list">{active.evidence.map((f,i)=><div className="evidence-item" key={i}>{f.endsWith('.txt')?<FileText size={17}/>:<ImageIcon size={17}/>}<span>{f}</span><small>Sample reference</small></div>)}</div></div><div className="case-section"><h3>Update investigation status</h3><div className="status-options">{statusList.map(s=><button key={s} className={`status-choice ${active.status===s?'selected':''}`} onClick={()=>{changeStatus(active.id,s);setActive({...active,status:s});}}>{s}</button>)}</div></div><div className="case-section"><h3>Investigation notes</h3><textarea className="note-input" placeholder="Add observations or review notes…" value={note} onChange={e=>setNote(e.target.value)}/><button className="primary note-save" onClick={()=>addNote(active.id)}><Plus size={16}/> Save note</button>{(cases[active.id]?.notes||[]).length>0&&<div className="notes-list">{cases[active.id].notes.map((n,i)=><div className="note-card" key={i}><p>{n.text}</p><small>{n.by} · {n.at}</small></div>)}</div>}</div><div className="case-section"><h3>Case history</h3>{(cases[active.id]?.history||[]).length?cases[active.id].history.map((h,i)=><div className="history-entry" key={i}><div className="history-dot"/><div><b>{h.from} → {h.to}</b><small>{h.by} · {h.at}</small></div></div>):<p className="empty-small">No status changes recorded yet.</p>}</div><div className="modal-foot"><span>Demo records · Case data saved in this browser</span><button className="outline" onClick={()=>setActive(null)}>Done</button></div></div></div>}
  {toast&&<div className="toast"><CheckCircle2 size={17}/>{toast}</div>}
 </div>;
}
function Stat({icon:Icon,label,value,color,sub}) { return <div className="stat-card"><div className={`stat-icon ${color}`}><Icon size={18}/></div><div className="stat-label">{label}</div><div className="stat-value">{value}</div><div className="stat-sub">{sub}</div></div>; }
function AlertTable({ items, onOpen }) {
  return (
    <div className="data-table-wrap">
      <table>
        <thead>
          <tr>
            <th>Alert</th>
            <th>Exam / source</th>
            <th>Risk</th>
            <th>Match</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {items.length === 0 ? (
            <tr>
              <td colSpan="6" className="empty-row">
                No matching alerts. Try changing your search or filters.
              </td>
            </tr>
          ) : (
            items.map((a) => (
              <tr key={a.id}>
                <td>
                  <b className="alert-id">{a.id}</b>
                  <small className="date-cell">{a.date}</small>
                </td>

                <td>
                  <b>{a.exam}</b>
                  <small>{a.source}</small>
                </td>

                <td>
                  <Badge kind={a.risk}>{a.risk}</Badge>
                </td>

                <td>
                  <span className="match-score">{a.score}%</span>
                </td>

                <td>
                  <Badge kind={a.status}>{a.status}</Badge>
                </td>

                <td>
                  <button
                    className="row-action"
                    onClick={() => onOpen(a)}
                    title="Open case"
                  >
                    <Eye size={16} />
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
function ActivityList({alerts}) { return <div className="activity-list">{alerts.map((a,i)=><div className="activity-item" key={a.id}><div className={`activity-icon ${a.risk.toLowerCase()}`}><AlertTriangle size={16}/></div><div><b>{a.id} · {a.exam}</b><small>{a.status} · {a.source}</small></div><span className="activity-time">{i===0?'Recently':`${i+1} entries ago`}</span></div>)}</div>; }
function SettingRow({title,desc,status}) { return <div className="setting-row"><div><b>{title}</b><small>{desc}</small></div><span className="setting-status">{status}</span></div>; }
createRoot(document.getElementById('root')).render(<App/>);
