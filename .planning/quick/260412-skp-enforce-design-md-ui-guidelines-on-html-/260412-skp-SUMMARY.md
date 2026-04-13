# Summary: Enforce design.MD UI Guidelines on HTML files

**Quick Task:** 260412-skp
**Date:** 2026-04-13
**Commit:** 9938906

## What was done

### Unified Tailwind Config (both files)
Replaced divergent configs with one identical design system:
- **Primary:** `#2169fe` · **Secondary:** `#646dd5` · **Tertiary:** `#ae56a8` · **Neutral:** `#71749e`
- **Surface tokens:** `surface`, `surface-dim`, `surface-container-lowest` (#ffffff), `surface-container-low` (#f4f2fe), `surface-container` (#eeecf8), `surface-container-high` (#e8e6f2), `surface-container-highest` (#e2e1ed)
- **On-surface tokens:** `on-surface` (#1b1b22), `on-surface-variant` (#46464f)
- **Custom shadows:** `ambient` (0 12px 40px rgba(25,28,30,0.06)), `ambient-lg` (0 16px 48px rgba(25,28,30,0.08))

### "No-Line" Rule Enforcement
- **Removed:** `border-r border-slate-200/50` from `<aside>` in index.html
- **Removed:** `border-t border-white/20` from sticky input area in index.html
- **Removed:** `border-t border-slate-200 dark:border-slate-800` from sidebar footer in doctor.html
- **Removed:** `border-b border-surface-container/50` from SOAP card header in doctor.html
- **Removed:** `border-t border-surface-container/50` from SOAP card footer in doctor.html
- **Removed:** `border-b border-white/20` from patient info rows in doctor.html
- **Replaced all** with background color shifts (`bg-surface-container-low`, `bg-surface-container`)

### Glass-Card → Ambient Depth
- **Removed:** `.glass-card` (backdrop-filter: blur(12px/16px), border: 1px solid rgba(255,255,255,0.4/0.5))
- **Removed:** `.glass-card-dark` (same heavy blur)
- **Replaced with:** `bg-surface-container-lowest` + `shadow-ambient` / `shadow-ambient-lg`
- Cards now get "natural lift" from white surface sitting on #f4f2fe background

### Hardcoded Slates → Semantic Tokens
| Before | After |
|--------|-------|
| `text-slate-900` | `text-on-surface` |
| `text-slate-500/600` | `text-on-surface-variant` |
| `bg-slate-100/50/200` | `bg-surface-container-*` |
| `bg-slate-400` (pill) | `bg-surface-container-high` |
| `text-blue-700` | `text-primary` |
| `border-blue-700` | `border-primary` |
| `bg-white` (cards) | `bg-surface-container-lowest` |

### JS Blocks Preserved ✅
- index.html: SHA256 hash identical before/after editing
- doctor.html: IIFE, fetch, localStorage all verified intact

## Files changed
- `static/index.html` — Config, CSS, and ~20 class replacements in HTML
- `static/doctor.html` — Config, CSS, and ~40 class replacements in HTML
