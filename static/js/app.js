// Shared utility functions

const API_BASE = '/api';

// === Toast Notification System ===
const Toast = {
    container: null,

    init() {
        this.container = document.getElementById('toast-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container';
            this.container.setAttribute('role', 'status');
            this.container.setAttribute('aria-live', 'polite');
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'info', duration = 4000) {
        if (!this.container) this.init();

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span>${message}</span>
            ${type === 'error' ? '<button class="dismiss" onclick="this.parentElement.remove()" aria-label="Dismiss">×</button>' : ''}
        `;

        this.container.appendChild(toast);

        // Limit to 3 toasts
        while (this.container.children.length > 3) {
            this.container.firstChild.remove();
        }

        // Trigger animation
        requestAnimationFrame(() => toast.classList.add('visible'));

        // Auto-dismiss (except errors)
        if (type !== 'error') {
            setTimeout(() => {
                toast.classList.remove('visible');
                setTimeout(() => toast.remove(), 300);
            }, duration);
        }
    },

    success(msg) { this.show(msg, 'success'); },
    error(msg) { this.show(msg, 'error'); },
    info(msg) { this.show(msg, 'info'); }
};

// Initialize toast on page load
document.addEventListener('DOMContentLoaded', () => Toast.init());

// === Loading Button State ===
function setButtonLoading(button, isLoading, loadingText) {
    const textEl = button.querySelector('.btn-text') || button;
    const spinnerEl = button.querySelector('.spinner');
    const originalText = button.dataset.originalText || textEl.textContent;

    if (isLoading) {
        button.dataset.originalText = originalText;
        button.setAttribute('aria-busy', 'true');
        button.disabled = true;
        textEl.textContent = loadingText || 'Loading...';
        if (spinnerEl) spinnerEl.hidden = false;
    } else {
        button.removeAttribute('aria-busy');
        button.disabled = false;
        textEl.textContent = originalText;
        if (spinnerEl) spinnerEl.hidden = true;
    }
}

// User session management
function getCurrentUser() {
    const userJson = localStorage.getItem('user');
    return userJson ? JSON.parse(userJson) : null;
}

function requireLogin() {
    const user = getCurrentUser();
    if (!user) {
        window.location.href = '/';
        return null;
    }
    return user;
}

function logout() {
    localStorage.removeItem('user');
    window.location.href = '/';
}

async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
    };

    if (options.body && typeof options.body === 'object') {
        config.body = JSON.stringify(options.body);
    }

    const response = await fetch(url, config);

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
        // Handle FastAPI validation errors (422) which return detail as an array
        let message = 'An error occurred';
        if (typeof error.detail === 'string') {
            message = error.detail;
        } else if (Array.isArray(error.detail)) {
            // FastAPI validation error format
            message = error.detail.map(e => `${e.loc?.join('.')}: ${e.msg}`).join(', ');
        }
        throw new Error(message);
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
        Toast.success('Copied to clipboard!');
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            Toast.success('Copied to clipboard!');
        } catch (e) {
            Toast.error('Failed to copy');
        }
        document.body.removeChild(textarea);
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
