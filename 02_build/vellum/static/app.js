/* Vellum — contact surface JS
   Minimal: reply submission + emoji routing.
   Devon-b5dc | 2026-05-14
*/

async function sendReply(sheetId, content) {
    try {
        const res = await fetch(`/api/v1/sheets/${sheetId}/reply`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content: content.trim(), author: "Ewan" }),
        });
        const data = await res.json();
        showToast(data.intent, data.confidence);
        refreshEntries(sheetId);
    } catch (err) {
        console.error("Reply failed:", err);
    }
}

function submitReply(event, sheetId) {
    event.preventDefault();
    const input = document.getElementById("reply-input");
    const content = input.value.trim();
    if (!content) return false;
    sendReply(sheetId, content);
    input.value = "";
    return false;
}

function refreshEntries(sheetId) {
    const el = document.getElementById("entries");
    if (!el) return;

    const url = el.getAttribute("hx-get") || el.getAttribute("data-hx-get");
    if (!url) return;

    const swap = el.getAttribute("hx-swap") || el.getAttribute("data-hx-swap") || "innerHTML";
    htmx.ajax("GET", url, { target: el, swap: swap });
}

function showToast(intent, confidence) {
    const toast = document.createElement("div");
    toast.style.cssText = `
        position: fixed; bottom: 80px; right: 16px;
        background: #161b22; border: 1px solid #30363d;
        border-radius: 8px; padding: 8px 16px;
        color: #e6edf3; font-size: 0.85rem;
        z-index: 100; opacity: 0; transition: opacity 0.3s;
    `;
    toast.textContent = `${intent} (${Math.round(confidence * 100)}%)`;
    document.body.appendChild(toast);
    requestAnimationFrame(() => { toast.style.opacity = "1"; });
    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}
