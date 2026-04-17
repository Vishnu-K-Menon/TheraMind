const fs = require('fs');

const tailwindConfig = `<script id="tailwind-config">tailwind.config = {darkMode: "class", theme: {extend: {colors: {primary: "#3A7BD5", navy: "#1D2D50", teal: "#124D41", cyan: "#63C9D6", sky: "#D6ECFF", "doc-bg": "#0B132B", "doc-card": "#1C2541", "doc-text": "#F7F9FB", "pat-offwhite": "#F6FBFF"}, fontFamily: {headline: ["Manrope"], body: ["Inter"], label: ["Inter"], display: "Manrope"}, borderRadius: {DEFAULT: "0.5rem", lg: "1rem", xl: "1.5rem", full: "9999px"}}}};</script>`;

// Update index.html
let indexHtml = fs.readFileSync('index.html', 'utf8');
indexHtml = indexHtml.replace(/<script id="tailwind-config">.*?<\/script>/s, tailwindConfig);
indexHtml = indexHtml.replace(/background-color: #9fa3d7;/g, 'background: linear-gradient(135deg, #F6FBFF 0%, #D6ECFF 100%);');
indexHtml = indexHtml.replace(/text-on-surface-variant/g, 'text-slate-500');
indexHtml = indexHtml.replace(/text-on-surface/g, 'text-navy');
indexHtml = indexHtml.replace(/text-on-primary/g, 'text-white');
indexHtml = indexHtml.replace(/bg-surface-container-low/g, 'bg-white/50');
indexHtml = indexHtml.replace(/bg-surface-container-lowest/g, 'bg-white');
indexHtml = indexHtml.replace(/bg-secondary-container/g, 'bg-sky/50');
indexHtml = indexHtml.replace(/bg-[^ ]*blue-50[^ ]*/g, 'bg-white/80');
indexHtml = indexHtml.replace(/text-slate-950/g, 'text-navy');
indexHtml = indexHtml.replace(/text-blue-600 dark:text-blue-400 drop-shadow-sm/g, 'text-navy');
indexHtml = indexHtml.replace(/bg-primary\/90 backdrop-blur-md/g, 'bg-primary/95 backdrop-blur-md');
// Make sure agent bubbles pop beautifully with deep navy text and clean white background
fs.writeFileSync('index.html', indexHtml);

// Update doctor.html
let doctorHtml = fs.readFileSync('doctor.html', 'utf8');
doctorHtml = doctorHtml.replace(/<script id="tailwind-config">.*?<\/script>/s, tailwindConfig);

const glassCardDarkCss = `.glass-card {
      background: rgba(28, 37, 65, 0.7);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .glass-card-dark {
      background: rgba(11, 19, 43, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.1);
    }`;

doctorHtml = doctorHtml.replace(/\.glass-card\s*\{.*?\.glass-card-dark\s*\{.*?\}/s, glassCardDarkCss);

doctorHtml = doctorHtml.replace(/text-on-surface-variant/g, 'text-slate-400');
doctorHtml = doctorHtml.replace(/text-on-surface/g, 'text-doc-text');
doctorHtml = doctorHtml.replace(/text-on-primary/g, 'text-white');
doctorHtml = doctorHtml.replace(/bg-surface-container-low/g, 'bg-doc-card/50');
doctorHtml = doctorHtml.replace(/bg-surface-container-lowest/g, 'bg-doc-card');
doctorHtml = doctorHtml.replace(/bg-secondary-container/g, 'bg-doc-card/80');
doctorHtml = doctorHtml.replace(/bg-gradient-to-br from-slate-800 via-slate-900 to-slate-950/g, 'bg-gradient-to-br from-[#121c36] via-[#0B132B] to-black');
// Erase previously forced slate-950 and replace with doc-text soft white
doctorHtml = doctorHtml.replace(/text-slate-950/g, 'text-doc-text');
// Erase slate-800 and slate-900 explicitly if they existed
doctorHtml = doctorHtml.replace(/text-slate-[89]00/g, 'text-doc-text');
doctorHtml = doctorHtml.replace(/font-medium dark:text-slate-50/g, 'font-medium');
doctorHtml = doctorHtml.replace(/bg-surface/g, 'bg-[#050B14]');
doctorHtml = doctorHtml.replace(/text-slate-900/g, 'text-doc-text');
doctorHtml = doctorHtml.replace(/text-slate-800/g, 'text-doc-text');

fs.writeFileSync('doctor.html', doctorHtml);
console.log('Update Complete');
