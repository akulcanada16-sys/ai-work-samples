// Spreadsheet programs can ignore leading whitespace/control characters before
// interpreting one of these values as a formula.
export const FORMULA_PREFIX = /^[\s\u0000-\u001F\u007F]*[=+\-@]/;
const CONTROL = /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/;

export function detectDelimiter(text) {
  const candidates = [',', ';', '\t', '|'];
  return candidates
    .map(delimiter => ({ delimiter, ...scoreDelimiter(text, delimiter) }))
    .sort((a, b) => b.consistency - a.consistency || b.occurrences - a.occurrences || candidates.indexOf(a.delimiter) - candidates.indexOf(b.delimiter))[0].delimiter;
}
function scoreDelimiter(text, delimiter) {
  const widths = [], limit = Math.min(text.length, 12000); let quoted = false, fields = 1, occurrences = 0;
  for (let i = 0; i < limit; i++) {
    const char = text[i];
    if (char === '"') { if (quoted && text[i + 1] === '"') i++; else quoted = !quoted; continue; }
    if (!quoted && char === delimiter) { fields++; occurrences++; continue; }
    if (!quoted && (char === '\n' || char === '\r')) { if (char === '\r' && text[i + 1] === '\n') i++; widths.push(fields); fields = 1; if (widths.length === 24) break; }
  }
  if (fields > 1 || (!widths.length && text.length)) widths.push(fields);
  const multiFieldRows = widths.filter(width => width > 1).length;
  const common = widths.length ? Math.max(...widths.map(width => widths.filter(other => other === width).length)) : 0;
  // A real delimiter makes a stable table. Incidental punctuation inside a
  // comma field can be frequent, but produces uneven row widths.
  return { occurrences, consistency: multiFieldRows === widths.length && widths.length > 0 ? common / widths.length : 0 };
}

export function parseCsv(input, delimiter = detectDelimiter(input)) {
  const records=[], positions=[], errors=[]; let row=[], field='', state='unquoted', atStart=true, rowStart=1, line=1;
  const pushRow = () => { row.push(field); records.push(row); positions.push(rowStart); row=[]; field=''; atStart=true; rowStart=line + 1; };
  for(let i=0;i<input.length;i++) { const c=input[i];
    if(state==='quoted') { if(c==='"') { if(input[i+1]==='"'){ field+='"'; i++; } else state='afterQuote'; } else { field+=c; if(c==='\n') line++; } continue; }
    if(state==='afterQuote') {
      if(c===delimiter) { row.push(field); field=''; atStart=true; state='unquoted'; continue; }
      if(c==='\r') { if(input[i+1]==='\n') i++; pushRow(); line++; state='unquoted'; continue; }
      if(c==='\n') { pushRow(); line++; state='unquoted'; continue; }
      errors.push({ line, code:'TRAILING_TEXT_AFTER_QUOTE', message:'Only a delimiter or record end may follow a closing quote.' });
      field+=c; atStart=false; state='unquoted'; continue;
    }
    if(c==='"' && atStart) { state='quoted'; atStart=false; continue; }
    if(c===delimiter) { row.push(field); field=''; atStart=true; continue; }
    if(c==='\r') { if(input[i+1]==='\n') i++; pushRow(); line++; continue; }
    if(c==='\n') { pushRow(); line++; continue; }
    if(c==='"') errors.push({ line, code:'UNEXPECTED_QUOTE', message:'Quote begins after unquoted text.' });
    field+=c; atStart=false;
  }
  if(state==='quoted') errors.push({ line: rowStart, code:'UNCLOSED_QUOTE', message:'Quoted field is not closed.' });
  // Preserve every final record, including a quoted-empty record and a delimiter-created empty field.
  if(input.length && !(input.endsWith('\n') || input.endsWith('\r'))) pushRow();
  return { records, positions, errors, delimiter };
}
export function inferType(value) { const v=value.trim(); if(v==='')return 'empty'; if(/^(true|false)$/i.test(v))return 'boolean'; if(/^[-+]?\d+(\.\d+)?([eE][-+]?\d+)?$/.test(v))return 'number'; if(/^\d{4}-\d{2}-\d{2}(?:[T ].*)?$/.test(v) && !Number.isNaN(Date.parse(v)))return 'date'; return 'text'; }
export function quoteCell(value, delimiter) { const s=String(value); return /["\r\n]/.test(s) || s.includes(delimiter) ? `"${s.replaceAll('"','""')}"` : s; }
export function stringifyCsv(records, delimiter) { return records.map(r => r.map(c => quoteCell(c, delimiter)).join(delimiter)).join('\r\n') + '\r\n'; }
export function auditCsv(text, keyIndex = -1) {
  const delimiter=detectDelimiter(text), parsed=parseCsv(text, delimiter), findings=[...parsed.errors.map(e=>({severity:'critical', code:e.code, line:e.line, message:e.message}))];
  const [headers=[], ...rows]=parsed.records, lines=parsed.positions; const used=new Set(), normalized=[];
  headers.forEach((h,i)=>{ const base=h.trim() || `column_${i+1}`; let name=base, suffix=2; while(used.has(name.toLocaleLowerCase())) name=`${base}_${suffix++}`; if(!h.trim())findings.push(f('warning','BLANK_HEADER',lines[0]||1,i, 'Blank header will be named '+name+'.')); if(name!==base)findings.push(f('warning','DUPLICATE_HEADER',lines[0]||1,i, `Header “${base}” conflicts with an earlier header; normalized as “${name}”.`)); used.add(name.toLocaleLowerCase()); normalized.push(name); });
  const width=headers.length, seenKeys=new Map(), typeSets=headers.map(()=>new Set());
  rows.forEach((row, ri)=>{ const line=lines[ri+1]||ri+2; if(row.length!==width)findings.push({severity:'critical',code:'ROW_WIDTH',line,message:`Expected ${width} fields; found ${row.length}.`}); row.forEach((cell,ci)=>{ if(CONTROL.test(cell))findings.push(f('warning','CONTROL_CHARACTER',line,ci,'Contains a non-printing control character.')); if(FORMULA_PREFIX.test(cell))findings.push(f('warning','FORMULA_PREFIX',line,ci,'May execute as a spreadsheet formula when opened.')); if(ci<typeSets.length && cell.trim()!=='')typeSets[ci].add(inferType(cell)); }); if(keyIndex>=0 && keyIndex<width){const k=(row[keyIndex]??'').trim();if(!k)findings.push(f('warning','BLANK_KEY',line,keyIndex,'Key value is blank.'));else if(seenKeys.has(k))findings.push(f('warning','DUPLICATE_KEY',line,keyIndex,`Duplicates key first seen on row ${seenKeys.get(k)}.`));else seenKeys.set(k,line);} });
  typeSets.forEach((types,i)=>{ if(types.size>1)findings.push(f('warning','TYPE_DRIFT',null,i,`Values mix ${[...types].join(', ')} types.`)); });
  const safe=parsed.errors.length===0 && rows.every(r=>r.length===width) && width>0;
  const cleaned=[normalized, ...rows.map(r=>normalized.map((_,i)=>{ const v=r[i]??''; return FORMULA_PREFIX.test(v) ? `'${v}` : v; }))];
  return { delimiter, headers, normalizedHeaders:normalized, rows, findings, safe, cleaned, stats:{records:rows.length, columns:width, critical:findings.filter(x=>x.severity==='critical').length, warnings:findings.filter(x=>x.severity==='warning').length} };
}
function f(severity,code,line,column,message){return {severity,code,line,column,message};}
