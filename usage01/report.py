"""Standalone HTML report. No server or CDN is required to read it."""
import json


def render(summary, model, cases, path):
    payload = json.dumps({'summary': summary, 'model': model, 'cases': cases}, ensure_ascii=False)
    payload = payload.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    page = '''<!doctype html>
<html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CONT-USAGE-01 · Diagnostic de continuation</title>
<style>
:root{font:16px/1.6 system-ui,sans-serif;color:#142c32;background:#f2f6f6}*{box-sizing:border-box}
body{margin:0}main{max-width:1120px;margin:auto;padding:40px 24px 70px}h1{font-size:clamp(28px,4vw,44px);line-height:1.15;max-width:850px}h2{font-size:24px;margin-top:36px}h3{font-size:17px}.eyebrow{letter-spacing:.12em;font-size:12px;font-weight:700;color:#42636a}
.intro{max-width:840px}.metrics,.branches{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.metrics{grid-template-columns:repeat(4,minmax(0,1fr));margin:28px 0}.card{padding:20px;background:white;border:1px solid #cfdddf;border-radius:10px}.value{font-size:32px;line-height:1.2;color:#005b62;font-weight:750}.label{font-size:13px;color:#46646b}.tag{display:inline-block;background:#d8edeb;color:#145955;padding:2px 8px;border-radius:6px;font-size:13px}
select,button{font:inherit;background:white;border:1px solid #91abad;border-radius:7px;padding:10px;max-width:100%}button{cursor:pointer;color:#005b62;margin-top:16px}code,pre{font:13px/1.5 ui-monospace,monospace;background:#edf3f3}code{padding:3px 5px;border-radius:4px}pre{white-space:pre-wrap;padding:16px;border-radius:7px}table{width:100%;border-collapse:collapse;font-size:14px;background:white}th,td{text-align:left;border-bottom:1px solid #d5e2e3;padding:11px 12px;vertical-align:top}th{background:#e4efef}ul{padding-left:22px}.muted{color:#536e75;font-size:14px}.callout{border-left:4px solid #207c78;padding:10px 18px;background:#e2eeed}.scroll{overflow:auto}.actions{font:14px ui-monospace,monospace}.pill{display:inline-block;padding:3px 7px;background:#e8f0f1;border-radius:4px;margin:2px}.note{background:#f2ece0;color:#5e4a28;padding:18px;border-radius:8px}
@media(max-width:650px){.metrics,.branches{grid-template-columns:1fr}main{padding:24px 16px}table{min-width:560px}}
</style>
<main><div class="eyebrow">CONT-USAGE-01 · DÉMONSTRATEUR EXÉCUTÉ</div>
<h1>Le même statut peut cacher deux futurs différents</h1>
<p class="intro" id="intro"></p>
<p><span class="tag" id="target-tag"></span></p>
<div class="metrics" id="metrics"></div>
<h2>Un témoin que l'on peut vérifier</h2>
<p>Sélectionnez une paire d'histoires. Le test prépare chaque branche séparément et applique ensuite exactement la même continuation.</p>
<select id="picker" aria-label="Témoin de continuation"></select>
<div id="witness"></div><button id="download">Télécharger ce test en JSON</button>
<h2>Ce que le diagnostic ajoute au statut courant</h2>
<p>Une mémoire fondée uniquement sur le statut confond des états qui exigent des prédictions différentes. Le modèle appris garde ces distinctions et se met à jour après chaque action et chaque observation.</p>
<div class="scroll"><table><thead><tr><th>État appris</th><th>Préparation d'accès</th><th>Statut affiché</th><th id="prediction-head">Prédiction</th></tr></thead><tbody id="states"></tbody></table></div>
<p class="muted">Les numéros d'état ne nomment pas des variables cachées physiques. Ce sont des classes de comportement apprises sur les sorties déclarées.</p>
<h2>Audit de l'ordre des actions</h2><div class="scroll"><table><thead><tr><th>Statut de l'ordre</th><th>Paires examinées</th><th>Interprétation</th></tr></thead><tbody id="orders"></tbody></table></div>
<h2>Exécution et portée</h2><div id="execution" class="card"></div>
<p class="note" id="scope-note"></p>
<ul id="assumptions"></ul>
<h2>Reproduire et raccorder une autre cible</h2>
<pre>python3 run_demo.py
python3 verify_results.py
python3 -m unittest discover -s tests -v

# Sur une cible de test déjà accessible :
python3 diagnose.py --config interface.json --out results/custom

# Rejouer les tests exportés :
python3 replay.py --config interface.json --cases results/reference/regression_cases.json</pre>
<p>Le fichier <code>README.md</code> précise le contrat de préparation, le sens des observations et les conditions de la borne d'états. Les journaux JSON conservent toutes les observations réellement exécutées.</p>
</main><script type="application/json" id="data">__PAYLOAD__</script>
<script>
const {summary:s,model:m,cases}=JSON.parse(document.getElementById('data').textContent);
const $=id=>document.getElementById(id);const esc=x=>String(x).replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));
const word=x=>x.length?x.map(esc).join(' → '):'Départ préparé';
$('intro').textContent='Le diagnostic interroge la cible par HTTP, reconstruit sa mémoire de continuation, puis transforme les différences de passé en tests de régression rejouables. Statuts observés : '+s.current_view_values.join(', ')+'.';
$('target-tag').textContent=s.controlled_fixture?'Cible de test indépendante · processus HTTP local':s.target;
$('scope-note').textContent=(s.controlled_fixture?'Ce résultat porte sur un service de test contrôlé. ':'Ce résultat porte sur la cible et la projection d’observation déclarées. ')+'Il ne constitue ni un déploiement en production, ni une preuve d’originalité d’usage face à LearnLib, AALpy ou ALEX. La certification est conditionnelle aux hypothèses ci-dessous.';
const metrics=[[s.observed_states,'états de continuation'],[s.current_view_values.length,'statuts affichés'],[s.order_pairs,'paires d’ordre examinées'],[s.replay_cases_passed,'témoins rejoués avec succès']];
$('metrics').innerHTML=metrics.map(([n,l])=>`<div class="card"><div class="value">${n}</div><div class="label">${l}</div></div>`).join('');
const primary=cases.findIndex(c=>c.id==='order-0-APPROVE-EDIT');
cases.forEach((c,i)=>{let o=document.createElement('option');o.value=i;o.textContent=c.id+' · '+(c.same_current_view?'même statut':'statuts différents');$('picker').append(o)});
$('picker').value=primary>=0?primary:0;
function show(){const c=cases[Number($('picker').value)];if(!c){$('witness').textContent='Aucun témoin de divergence dans le modèle appris sous les hypothèses déclarées.';$('picker').hidden=true;$('download').hidden=true;return}$('witness').innerHTML=`<p class="callout">${c.same_current_view?'Le statut courant fusionne les deux branches.':'Le statut courant distingue déjà ces branches.'} La continuation <strong>${word(c.continuation)}</strong> révèle leur différence de futur.</p><div class="branches">${['left','right'].map((side,i)=>{let b=c[side];return `<div class="card"><h3>Branche ${i+1}</h3><p class="actions">${word(b.history)}</p><p>Statut : <code>${esc(b.view)}</code></p><p>Après ${word(c.continuation)} :</p>${b.expected_tail.map(o=>`<p><span class="pill">${esc(o.decision)}</span><span class="pill">${esc(o.view)}</span></p>`).join('')}</div>`}).join('')}</div>`}
$('picker').onchange=show;show();
$('download').onclick=()=>{const c=cases[Number($('picker').value)];const u=URL.createObjectURL(new Blob([JSON.stringify([c],null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=u;a.download=c.id+'.json';a.click();URL.revokeObjectURL(u)};
const ci=Math.max(0,m.alphabet.indexOf('COMMIT'));$('prediction-head').textContent='Prédiction '+m.alphabet[ci];$('states').innerHTML=m.table.map((row,i)=>`<tr><td>${i}</td><td>${word(m.access_words[i])}</td><td>${esc(s.state_views[i])}</td><td>${esc(JSON.parse(row[ci][1]).decision)}</td></tr>`).join('');
const regimes=[['invisible_redundant','Ordre invisible, sans conséquence','Même statut et même état de continuation.'],['invisible_relevant','Ordre invisible, pertinent','Même statut, futurs distinguables.'],['visible_redundant','Ordre visible, redondant','Statuts différents, futur équivalent.'],['visible_relevant','Ordre visible, pertinent','Statuts différents et futurs distinguables.']];
$('orders').innerHTML=regimes.map(([k,l,d])=>`<tr><td>${l}</td><td>${s.order_regimes[k]||0}</td><td>${d}</td></tr>`).join('');
$('execution').innerHTML=`<p><strong>${s.counts.preparations}</strong> préparations et <strong>${s.counts.event_calls}</strong> actions effectivement exécutées par HTTP, dont ${s.final_fresh_conformance_words} mots de conformité réexécutés sans cache.</p><p>${s.replay_cases_passed}/${s.witness_cases} témoins ont été rejoués sur la cible.${s.controlled_fixture?' Le contrôle mutant « approbation conservée après EDIT » est vérifié séparément dans <code>mutation_results.json</code>.':''}</p><p class="muted">Borne déclarée : ${s.declared_max_states}. ${esc(s.bound_source)} Durée locale de cette exécution : ${s.seconds}s ; ce temps n'est pas une comparaison de performance.</p>`;
$('assumptions').innerHTML=s.assumptions.map(a=>`<li>${esc(a)}</li>`).join('');
</script></html>'''
    path.write_text(page.replace('__PAYLOAD__', payload), encoding='utf-8')
