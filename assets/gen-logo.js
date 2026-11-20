// Generates assets/icon.svg and assets/logo.svg for the OpenObserve app.
// Usage: node gen-logo.js <output-dir>
const fs = require("fs");
const path = require("path");

const out = process.argv[2];

// Home Assistant blues for the ring (light / dark alternating)
const RING = ["#41BDF5", "#0A86C8", "#18BCF2", "#0B5E8E"]; // top, right, bottom, left
// OpenObserve colours for the house
const OO = { purple: "#6B76E3", red: "#F45B49", green: "#5ACA7A", blue: "#45A4F3" };

const C = 64, R = 53, W = 12;

function pt(deg) {
  const a = (deg * Math.PI) / 180;
  return [C + R * Math.cos(a), C + R * Math.sin(a)].map((v) => v.toFixed(2));
}
function arc(from, to) {
  const [x1, y1] = pt(from), [x2, y2] = pt(to);
  return `M${x1} ${y1}A${R} ${R} 0 0 1 ${x2} ${y2}`;
}

// Segments centred on top (270), right (0), bottom (90), left (180).
// Slight rotation gives the swirling look of the OpenObserve ring.
const SPAN = 74, ROT = -18;
const centers = [270, 360, 450, 540];
const ring = centers
  .map((c, i) => {
    const a = c + ROT - SPAN / 2, b = c + ROT + SPAN / 2;
    return `<path d="${arc(a, b)}" stroke="${RING[i]}"/>`;
  })
  .join("\n    ");

const house = `
  <!-- House inspired by the Home Assistant logo, in OpenObserve colours -->
  <!-- Apex and bottom corners are about 42 px from the centre, so the gap to the ring is even -->
  <path d="M64 25L91 52V93H37V52Z" fill="${OO.purple}" stroke="${OO.purple}" stroke-width="6" stroke-linejoin="round"/>
  <!-- Pulse line as in observability charts (no antenna of the Home Assistant logo) -->
  <path d="M47 70H54L58 60L64 82L70 50L75 70H81" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <g stroke="#FFFFFF" stroke-width="2.5">
    <circle cx="46" cy="70" r="4" fill="${OO.red}"/>
    <circle cx="82" cy="70" r="4" fill="${OO.green}"/>
  </g>`;

const mark = `
  <g fill="none" stroke-width="${W}" stroke-linecap="round">
    ${ring}
  </g>${house}`;

const icon = `<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">${mark}
</svg>
`;

const logo = `<svg xmlns="http://www.w3.org/2000/svg" width="250" height="100" viewBox="0 0 250 100">
  <g transform="translate(4 4) scale(0.72)">${mark.replace(/\n/g, "\n  ")}
  </g>
  <text x="102" y="52" font-family="Segoe UI, Roboto, Helvetica, Arial, sans-serif" font-size="23" font-weight="600" fill="${OO.purple}">Open<tspan fill="#18BCF2">Observe</tspan></text>
  <text x="103" y="72" font-family="Segoe UI, Roboto, Helvetica, Arial, sans-serif" font-size="14" fill="#8A8F98">for Home Assistant</text>
</svg>
`;

fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, "icon.svg"), icon);
fs.writeFileSync(path.join(out, "logo.svg"), logo);
console.log("written to", out);
