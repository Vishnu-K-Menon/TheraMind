---
quick_id: 260412-skp
description: "Enforce design.MD UI Guidelines on HTML files"
mode: quick-full
must_haves:
  truths:
    - "tailwind-config script is IDENTICAL in both index.html and doctor.html"
    - "tailwind-config contains primary: '#2169fe'"
    - "tailwind-config contains secondary: '#646dd5'"
    - "tailwind-config contains tertiary: '#ae56a8'"
    - "tailwind-config contains neutral: '#71749e'"
    - "tailwind-config contains surface, surface-container-low, surface-container-lowest tokens"
    - "No border-r classes on aside elements"
    - "No border-t classes on layout containers (header-to-content, sidebar separators)"
    - "No border-slate-200, border-slate-800 classes on layout containers"
    - "glass-card CSS class replaced with ambient shadow styling"
    - "JavaScript <script> blocks at bottom of both files are COMPLETELY UNALTERED"
  artifacts:
    - "static/index.html"
    - "static/doctor.html"
  key_links:
    - "static/index.html lines 163-325: JS block MUST NOT be modified"
    - "static/doctor.html lines 390-561: JS block MUST NOT be modified"
---

# Quick Plan: Enforce design.MD UI Guidelines on HTML files

## Task 1: Update index.html with unified design tokens and no-line/no-glass rules

**files:** `static/index.html`
**action:**
1. Replace the `tailwind-config` script (line 14) with the unified config containing design.MD colors
2. Replace `.glass-card` CSS with ambient shadow styling
3. Remove `.bg-clinical-gradient` and use surface tokens on body
4. Remove `border-r`, `border-t`, `border-slate-*` from layout containers (header, aside, sticky input)
5. Replace `bg-slate-*`, `text-slate-*` with semantic tokens
6. Replace `backdrop-blur` heavy effects with clean surface-based depth
7. DO NOT MODIFY lines 163-325 (JavaScript block)

**verify:**
- tailwind-config contains `#2169fe`
- No `border-r` on aside
- No `border-t` on sticky input area  
- No `.glass-card` with backdrop-filter
- JS block (lines 163-325) completely unchanged

**done:** index.html uses unified design tokens with no-line/no-glass rules

## Task 2: Update doctor.html with the SAME unified config and rules

**files:** `static/doctor.html`
**action:**
1. Replace the `tailwind-config` script (lines 20-21) with the EXACT SAME config from Task 1
2. Replace `.glass-card` and `.glass-card-dark` CSS with ambient shadow styling
3. Remove layout borders from aside, header, and content separators
4. Replace `bg-slate-*`, `text-slate-*` with semantic tokens
5. Use surface background tokens for body and containers
6. DO NOT MODIFY lines 390-561 (JavaScript block)

**verify:**
- tailwind-config is IDENTICAL to index.html's config
- No `border-r`, `border-t` on layout containers
- No `.glass-card` with backdrop-filter heavy effects
- JS block (lines 390-561) completely unchanged

**done:** doctor.html uses same unified design tokens as index.html
