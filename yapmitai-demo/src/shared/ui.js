export function page(title, en, desc, body) {
  return `
    <section>
      <div class="page-title"><span class="eyebrow">${en}</span><h1>${title}</h1><p>${desc}</p></div>
      ${body}
    </section>`;
}

export function panel(title, en, body) {
  return `<section class="panel"><div class="panel-head"><div><h2>${title}</h2><span>${en}</span></div></div>${body}</section>`;
}

export function kpi(item) {
  return `<article class="kpi-card" style="--accent:${item.color}"><span>${item.title}</span><strong>${item.value}<small>${item.unit}</small></strong><em>${item.trend}</em></article>`;
}

export function metric(item) {
  return `<article class="metric"><strong>${item.value}<small>${item.unit}</small></strong><span>${item.label}</span></article>`;
}

export function miniStat(label, value) {
  return `<div class="mini-stat"><span>${label}</span><strong>${value}</strong></div>`;
}

export function lineChart(data, aKey, bKey, aLabel, bLabel, compact = false) {
  const max = Math.max(...data.flatMap((item) => [item[aKey], item[bKey]]));
  const points = (key) => data
    .map((item, index) => `${index * (100 / (data.length - 1))},${100 - item[key] / max * 86}`)
    .join(" ");
  return `<div class="chart-box ${compact ? "compact" : ""}"><svg viewBox="0 0 100 100" preserveAspectRatio="none"><line x1="0" x2="100" y1="20" y2="20"></line><line x1="0" x2="100" y1="40" y2="40"></line><line x1="0" x2="100" y1="60" y2="60"></line><line x1="0" x2="100" y1="80" y2="80"></line><polyline points="${points(aKey)}" class="line-a"></polyline><polyline points="${points(bKey)}" class="line-b"></polyline></svg><div class="chart-legend"><span class="dot a"></span>${aLabel}<span class="dot b"></span>${bLabel}</div></div>`;
}

export function donutChart(data) {
  let start = 0;
  const total = data.reduce((sum, item) => sum + item.value, 0);
  const gradient = data.map((item) => {
    const end = start + item.value / total * 100;
    const segment = `${item.color} ${start}% ${end}%`;
    start = end;
    return segment;
  }).join(", ");
  return `<div class="donut-wrap"><div class="donut" style="background:conic-gradient(${gradient})"><span>${total}</span></div><div class="donut-list">${data.map((item) => `<span><i style="background:${item.color}"></i>${item.label} ${item.value}%</span>`).join("")}</div></div>`;
}

export function progress(label, value, slim = false) {
  return `<div class="progress ${slim ? "slim" : ""}">${label ? `<div><span>${label}</span><b>${value}%</b></div>` : ""}<i><span style="width:${value}%"></span></i></div>`;
}

export function statusBadge(status) {
  const text = { working: "工作中", standby: "待命中", offline: "离线" }[status] || status;
  return `<span class="status-badge ${status}">${text}</span>`;
}

export function toggle(checked, id) {
  return `<button class="toggle ${checked ? "on" : ""}" data-toggle="${id}"><span></span></button>`;
}
