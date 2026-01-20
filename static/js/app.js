// Shared utility functions

const API_BASE = '/api';

async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    };

    if (options.body && typeof options.body === 'object') {
        config.body = JSON.stringify(options.body);
    }

    const response = await fetch(url, config);

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
        throw new Error(error.detail || 'An error occurred');
    }

    return response.json();
}

function showMessage(container, message, type = 'info') {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${type}`;
    messageEl.textContent = message;

    // Remove existing messages
    container.querySelectorAll('.message').forEach(el => el.remove());

    container.insertBefore(messageEl, container.firstChild);

    // Auto-remove after 5 seconds
    setTimeout(() => messageEl.remove(), 5000);
}

function formatRelationship(relationship) {
    const labels = {
        'manager': 'Manager',
        'peer': 'Peer',
        'direct_report': 'Direct Report',
        'xfn': 'Cross-functional',
    };
    return labels[relationship] || relationship;
}

function formatFrequency(frequency) {
    const labels = {
        'weekly': 'Weekly',
        'monthly': 'Monthly',
        'rarely': 'Rarely',
    };
    return labels[frequency] || frequency;
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        alert('Copied to clipboard!');
    });
}

function getPathParam(index) {
    const parts = window.location.pathname.split('/').filter(Boolean);
    return parts[index] || null;
}

// Simple markdown to HTML conversion for summaries
function markdownToHtml(text) {
    if (!text) return '';

    return text
        // Headers
        .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        // Bold
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        // Italic
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        // Lists
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
        // Line breaks
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
}
