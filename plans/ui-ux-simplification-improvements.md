# UI/UX Simplification Improvements

**Type**: Enhancement
**Complexity**: Standard (7 discrete improvements)
**Scope**: Frontend only (`/static/` directory)

---

## Overview

Simplify and clarify the user experience of the 360 Feedback Summarisation Tool through 7 targeted improvements focused on consistency, intuitive components, and efficient user flows. No feature creep - only standardization and consolidation of existing patterns.

## Problem Statement

The MVP frontend has clear user flows but scattered visual and structural inconsistencies:

| Issue | Impact |
|-------|--------|
| Navigation inconsistent (`.header` vs `<nav>`, different back destinations) | Users get lost, muscle memory fails |
| `alert()` used for some notifications | Blocks interaction, jarring UX |
| Different loading text patterns ("Submitting...", "Generating...", "Saving...") | Unpredictable feedback |
| All colors hardcoded (no CSS variables) | Hard to maintain, inconsistent usage |
| No responsive breakpoints | Reviewer grid breaks on mobile |
| Empty states use different classes and messages | Visual inconsistency |

## Proposed Solution

Seven discrete improvements applied across all frontend pages:

1. **Unify navigation** - Consistent back link behavior
2. **Shared header** - Same structure on authenticated pages
3. **Toast notifications** - Replace all `alert()` calls
4. **Loading states** - Standardized button pattern
5. **CSS variables** - Centralize colors/spacing
6. **Responsive breakpoints** - Mobile support (768px)
7. **Empty states** - Single visual treatment

---

## Technical Approach

### Files Affected

| File | Changes |
|------|---------|
| `static/css/style.css` | Add CSS variables, responsive breakpoints, toast styles, loading states |
| `static/js/app.js` | Add `showToast()`, `setButtonLoading()` utilities |
| `static/index.html` | Add toast container, CSS variable usage |
| `static/dashboard.html` | Replace header with shared pattern, use toast |
| `static/nominate.html` | Unified header, loading states, toast |
| `static/review.html` | Minimal header (unauthenticated), toast |
| `static/manager.html` | Unified header, loading states, toast, responsive table |
| `static/inbox.html` | Unified header, toast |

### Design Decisions

#### Navigation Back Links

| Page | Back Destination | Rationale |
|------|-----------------|-----------|
| `nominate.html` | `/dashboard.html` | Authenticated flow |
| `manager.html` | `/dashboard.html` | Authenticated flow |
| `inbox.html` | `/` | Email lookup, not authenticated |
| `review.html` | None | Standalone token experience |

#### Shared Header Structure

**Authenticated pages** (dashboard, nominate, manager):
```html
<header class="site-header">
  <a href="/dashboard.html" class="header-brand">360 Feedback</a>
  <nav class="header-nav">
    <span class="user-name" id="user-display"></span>
    <button onclick="logout()" class="btn-link">Logout</button>
  </nav>
</header>
```

**Public pages** (review, inbox):
```html
<header class="site-header site-header--minimal">
  <span class="header-brand">360 Feedback</span>
</header>
```

#### Toast Notification Behavior

| Setting | Value |
|---------|-------|
| Position | Bottom-center |
| Success duration | 4 seconds |
| Error duration | Stay until dismissed |
| Multiple toasts | Stack (max 3), oldest auto-dismisses |
| ARIA | `role="status"`, `aria-live="polite"` |

#### Loading Button Pattern

```html
<button class="btn btn-primary" data-loading-text="Submitting...">
  <span class="btn-text">Submit Feedback</span>
  <span class="btn-spinner" hidden></span>
</button>
```

States:
- Default: Show text, hide spinner
- Loading: Disable button, show spinner + loading text, `aria-busy="true"`
- Complete: Reset to default

#### CSS Variables

```css
:root {
  /* Colors */
  --color-primary: #007bff;
  --color-primary-hover: #0056b3;
  --color-success: #28a745;
  --color-success-bg: #d4edda;
  --color-error: #dc3545;
  --color-error-bg: #f8d7da;
  --color-warning: #ffc107;
  --color-warning-bg: #fff3cd;

  --color-text: #333;
  --color-text-muted: #666;
  --color-background: #f5f5f5;
  --color-surface: #ffffff;
  --color-border: #ddd;

  /* Spacing */
  --space-xs: 5px;
  --space-sm: 10px;
  --space-md: 15px;
  --space-lg: 20px;
  --space-xl: 30px;

  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
}
```

#### Responsive Breakpoint

Single breakpoint at 768px:
- Below 768px: Mobile layout (single column, stacked forms)
- 768px and above: Desktop layout (current behavior)

Mobile adaptations:
- `.reviewer-row`: Stack vertically (1 column)
- Tables: Horizontal scroll with visual hint
- Buttons: Full-width on mobile

#### Empty State Component

```html
<div class="empty-state">
  <p class="empty-state-title">No feedback cycles yet</p>
  <p class="empty-state-description">Create your first cycle to start collecting feedback.</p>
  <a href="/nominate.html" class="btn btn-primary">Create Feedback Cycle</a>
</div>
```

CTAs included where user can take action, omitted for waiting states.

---

## Implementation Phases

### Phase 1: CSS Foundation

**Tasks:**
- [ ] Add CSS variables to `:root` in `style.css`
- [ ] Replace hardcoded colors with variables throughout `style.css`
- [ ] Add responsive breakpoint (768px) with mobile styles
- [ ] Add `.reviewer-row` mobile layout (single column)
- [ ] Add table horizontal scroll wrapper

**Files:**
- `static/css/style.css`

**Acceptance:**
- All colors use CSS variables
- Reviewer form works on 375px viewport
- Tables scroll horizontally on mobile

### Phase 2: Toast System

**Tasks:**
- [ ] Add toast CSS to `style.css`
- [ ] Add toast container to each HTML page
- [ ] Add `showToast()` function to `app.js`
- [ ] Replace `copyToClipboard()` alert with toast
- [ ] Add `aria-live` region for accessibility

**Files:**
- `static/css/style.css`
- `static/js/app.js`
- All HTML pages (toast container)

**Acceptance:**
- Toast appears bottom-center
- Success auto-dismisses in 4s
- Error stays until dismissed
- Screen reader announces toast

### Phase 3: Loading States

**Tasks:**
- [ ] Add loading button CSS (spinner, disabled state)
- [ ] Add `setButtonLoading()` function to `app.js`
- [ ] Update all form submit handlers to use loading state
- [ ] Update summary generation button
- [ ] Update save/finalise buttons in manager

**Files:**
- `static/css/style.css`
- `static/js/app.js`
- `nominate.html`, `review.html`, `manager.html`

**Acceptance:**
- All async buttons show spinner when loading
- Buttons disabled during operation
- Buttons reset on success or error

### Phase 4: Navigation Unification

**Tasks:**
- [ ] Add shared header CSS (`.site-header`)
- [ ] Update `dashboard.html` header to new pattern
- [ ] Update `nominate.html` header to new pattern
- [ ] Update `manager.html` header to new pattern
- [ ] Update `inbox.html` to minimal header
- [ ] Remove back link from `review.html`

**Files:**
- `static/css/style.css`
- `dashboard.html`, `nominate.html`, `manager.html`, `inbox.html`, `review.html`

**Acceptance:**
- All authenticated pages have consistent header
- Back links go to correct destinations
- Review page has minimal header only

### Phase 5: Empty States

**Tasks:**
- [ ] Add unified `.empty-state` CSS
- [ ] Update dashboard empty states (my cycles, managed cycles, pending reviews)
- [ ] Update inbox empty state
- [ ] Update manager "waiting for reviews" state
- [ ] Add CTAs where appropriate

**Files:**
- `static/css/style.css`
- `dashboard.html`, `inbox.html`, `manager.html`

**Acceptance:**
- All empty states use same visual treatment
- CTAs present on dashboard and inbox
- No CTA on waiting states

---

## Acceptance Criteria

### Functional Requirements

- [ ] All navigation back links work correctly
- [ ] Shared header appears on all authenticated pages
- [ ] Toast notifications replace all `alert()` calls
- [ ] Loading states appear on all async buttons
- [ ] CSS variables used for all colors
- [ ] Mobile layout works at 375px viewport
- [ ] Empty states consistent across pages

### Non-Functional Requirements

- [ ] No JavaScript build step required
- [ ] No new dependencies added
- [ ] All pages load in <1s on 3G (already achieved)
- [ ] WCAG 2.1 AA compliance for toasts (aria-live)

### Quality Gates

- [ ] Manual test on Chrome, Firefox, Safari
- [ ] Manual test on mobile viewport (375px)
- [ ] Screen reader test for toast announcements

---

## MVP Implementation

### static/css/style.css additions

```css
/* === CSS Variables === */
:root {
  --color-primary: #007bff;
  --color-primary-hover: #0056b3;
  --color-success: #28a745;
  --color-success-bg: #d4edda;
  --color-success-text: #155724;
  --color-error: #dc3545;
  --color-error-bg: #f8d7da;
  --color-error-text: #721c24;
  --color-warning: #ffc107;
  --color-warning-bg: #fff3cd;
  --color-text: #333;
  --color-text-muted: #666;
  --color-background: #f5f5f5;
  --color-surface: #ffffff;
  --color-border: #ddd;
  --space-xs: 5px;
  --space-sm: 10px;
  --space-md: 15px;
  --space-lg: 20px;
  --space-xl: 30px;
  --radius-sm: 4px;
  --radius-md: 8px;
}

/* === Toast Notifications === */
#toast-container {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.toast {
  padding: 12px 24px;
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s, transform 0.3s;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.toast.visible {
  opacity: 1;
  transform: translateY(0);
}

.toast.success {
  background: var(--color-success-bg);
  border-color: var(--color-success);
  color: var(--color-success-text);
}

.toast.error {
  background: var(--color-error-bg);
  border-color: var(--color-error);
  color: var(--color-error-text);
}

.toast .dismiss {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0 0 0 var(--space-sm);
  opacity: 0.5;
}

/* === Loading Button === */
.btn .spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.btn[aria-busy="true"] {
  opacity: 0.7;
  cursor: wait;
}

/* === Shared Header === */
.site-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md) var(--space-lg);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--space-lg);
}

.header-brand {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.site-header--minimal {
  justify-content: center;
}

/* === Empty States === */
.empty-state {
  text-align: center;
  padding: var(--space-xl);
  color: var(--color-text-muted);
}

.empty-state-title {
  font-size: 1.1rem;
  margin-bottom: var(--space-sm);
  color: var(--color-text);
}

.empty-state-description {
  margin-bottom: var(--space-lg);
}

/* === Responsive === */
@media (max-width: 768px) {
  .reviewer-row {
    grid-template-columns: 1fr;
    gap: var(--space-sm);
  }

  .reviewer-row > div {
    margin-bottom: var(--space-xs);
  }

  .table-responsive {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .btn {
    width: 100%;
  }

  .actions {
    flex-direction: column;
  }
}
```

### static/js/app.js additions

```javascript
// Toast notification system
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
      ${type === 'error' ? '<button class="dismiss" onclick="this.parentElement.remove()">×</button>' : ''}
    `;

    this.container.appendChild(toast);

    // Limit to 3 toasts
    while (this.container.children.length > 3) {
      this.container.firstChild.remove();
    }

    requestAnimationFrame(() => toast.classList.add('visible'));

    if (type !== 'error') {
      setTimeout(() => {
        toast.classList.remove('visible');
        setTimeout(() => toast.remove(), 300);
      }, duration);
    }
  },

  success(msg) { this.show(msg, 'success'); },
  error(msg) { this.show(msg, 'error'); }
};

// Loading button state
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

// Updated clipboard function
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    Toast.success('Copied to clipboard!');
  }).catch(() => {
    // Fallback
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
```

---

## References

### Internal Files

| File | Purpose |
|------|---------|
| `static/css/style.css:1-339` | Current CSS (all hardcoded colors) |
| `static/js/app.js:57-69` | Current `showMessage()` function |
| `static/js/app.js:90-103` | Current `copyToClipboard()` with alert |
| `static/dashboard.html:11-17` | Current `.header` pattern |
| `static/nominate.html:10-13` | Current `<nav>` pattern |

### Best Practices

- Toast accessibility: [Sara Soueidan - ARIA Live Regions](https://www.sarasoueidan.com/blog/accessible-notifications-with-aria-live-regions-part-1/)
- CSS Variables: [MDN - Using CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- Loading States: [UX Movement - Button Loading States](https://uxmovement.com/buttons/when-you-need-to-show-a-buttons-loading-state/)
- Empty States: [UXPin - Designing Empty States](https://www.uxpin.com/studio/blog/ux-best-practices-designing-the-overlooked-empty-states/)
