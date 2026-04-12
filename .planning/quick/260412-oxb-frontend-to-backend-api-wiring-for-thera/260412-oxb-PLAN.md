---
quick_id: 260412-oxb
description: "Frontend-to-Backend API Wiring for TheraMind"
mode: quick-full
must_haves:
  truths:
    - "chatHistory array maintained in memory in both index.html and doctor.html"
    - "index.html send button triggers fetch('/chat') with absolute path"
    - "doctor.html Generate SOAP button triggers fetch('/generate_soap') with absolute path"
    - "All fetch requests use absolute paths with leading forward slash"
    - "Error handling via try/catch in both files"
    - "Loading indicator shown during API calls"
  artifacts:
    - "static/index.html"
    - "static/doctor.html"
  key_links:
    - "app.py - FastAPI backend with /chat and /generate_soap endpoints"
---

# Quick Plan: Frontend-to-Backend API Wiring for TheraMind

## Task 1: Wire index.html (Patient Mode) to `/chat` endpoint

**files:** `static/index.html`
**action:**
1. Add `id="chat-messages"` to the conversation container div (line 124, `<div class="space-y-6">`)
2. Add `id="chat-input"` to the textarea (line 193)
3. Add `id="send-btn"` to the send button (line 201)
4. Remove the hardcoded sample conversation messages (lines 125-183) — these will be populated dynamically
5. Add a `<script>` block at the end of `<body>` that:
   - Initializes `const chatHistory = []`
   - Creates helper functions: `appendUserMessage(text)`, `appendAIMessage(text)`, `showLoading()`, `hideLoading()`
   - Adds click event listener on `#send-btn` that:
     a. Gets text from `#chat-input`
     b. Clears the input
     c. Appends user message to UI via `appendUserMessage()`
     d. Pushes `{role: "user", content: text}` to `chatHistory`
     e. Shows loading indicator
     f. Calls `fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: text, history: chatHistory}) })` — NOTE: absolute path with leading `/`
     g. Parses JSON response
     h. Hides loading indicator
     i. Appends AI response to UI via `appendAIMessage()`
     j. Pushes `{role: "assistant", content: response}` to `chatHistory`
   - Wraps the fetch call in try/catch for error handling
   - Adds Enter key listener on textarea for sending
   - Auto-resizes textarea as user types

**verify:** 
- `chatHistory` array is declared and managed correctly
- `fetch('/chat'` uses absolute path (leading `/`)
- try/catch wraps the fetch call
- Loading indicator is created and removed
- User and AI messages are appended to the DOM

**done:** index.html has working chat functionality wired to `/chat` endpoint

## Task 2: Wire doctor.html to `/generate_soap` endpoint

**files:** `static/doctor.html`
**action:**
1. Add `id="generate-soap-btn"` to the "Generate SOAP Note" button (line 154-159)
2. Add `id="soap-content"` to the SOAP document content container (line 180, `<div class="p-8 space-y-12">`)
3. Add `id="soap-status-badge"` to the status badge (line 172)
4. Add a `<script>` block at the end of `<body>` that:
   - Initializes `let chatHistory = []` — this will be populated from patient mode or shared via localStorage
   - Adds `window.addEventListener('storage', ...)` to pick up chatHistory from patient mode via localStorage
   - Adds click event listener on `#generate-soap-btn` that:
     a. Reads chatHistory (from localStorage fallback if local is empty)
     b. Shows loading state on the button
     c. Calls `fetch('/generate_soap', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({history: chatHistory}) })` — NOTE: absolute path with leading `/`
     d. Parses JSON response
     e. Updates the SOAP content section with the response data
     f. Updates the status badge to "Live AI Draft"
     g. Restores button state
   - Wraps the fetch call in try/catch for error handling
   - Displays error state in the UI if the request fails

**verify:**
- `chatHistory` array is declared
- `fetch('/generate_soap'` uses absolute path (leading `/`)
- try/catch wraps the fetch call
- SOAP content area is updated with response
- Error state is handled gracefully

**done:** doctor.html has working SOAP generation wired to `/generate_soap` endpoint

## Task 3: Add chatHistory cross-page persistence via localStorage

**files:** `static/index.html`, `static/doctor.html`
**action:**
1. In index.html: After each chatHistory update, also call `localStorage.setItem('theraMindChatHistory', JSON.stringify(chatHistory))`
2. In doctor.html: On page load, attempt `chatHistory = JSON.parse(localStorage.getItem('theraMindChatHistory') || '[]')`
3. This ensures doctor mode can access the patient conversation even after page navigation

**verify:**
- localStorage.setItem called in index.html after chatHistory updates
- localStorage.getItem called in doctor.html on page load
- JSON parse/stringify used correctly

**done:** chatHistory persists across pages via localStorage
