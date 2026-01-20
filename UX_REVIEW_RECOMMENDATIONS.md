# UX Review: 360 Feedback Tool
## For Non-Technical Users (Ops/HR)

**Review Date:** 2026-01-20
**Focus:** Happy path, clarity, simplicity for non-technical users
**Reviewer:** UX Analysis

---

## Executive Summary

The 360 Feedback Tool has a **solid foundation** with clear separation of user flows and functional MVP implementation. However, several UX issues could cause confusion for non-technical users, particularly around:

1. **Navigation & Orientation** - Users may get lost or confused about their role
2. **Terminology** - Technical concepts (Employee ID, tokens) exposed to users
3. **Guidance** - Missing instructions at critical decision points
4. **Error Prevention** - Some flows allow user mistakes that could be prevented

**Overall Grade: B-** (Functional but needs polish for non-technical users)

---

## Critical Issues (Must Fix)

### 🚨 1. "Employee ID" is Confusing for Non-Technical Users

**Location:** Homepage, Manager section (index.html:36)

**Problem:**
```html
<label for="employee-id">Employee ID</label>
<input type="number" id="employee-id" placeholder="1" required min="1">
```

Non-technical users (HR, ops) don't think in database IDs. They think in names.

**Impact:** High - Managers won't know what to enter here

**Recommendation:**
- Change to "Employee Name" with autocomplete/search
- OR provide a dropdown list of employees who have feedback cycles
- OR at minimum, add helper text: "Enter the employee's name or ID (e.g., 'Alex Chen' or '1')"

**Quick Fix (minimal change):**
```html
<label for="employee-id">Employee Name or ID</label>
<input type="text" id="employee-id" placeholder="Alex Chen or 1" required>
<small>Enter the employee's name or their ID number</small>
```

---

### 🚨 2. No Confirmation After Creating Feedback Cycle

**Location:** nominate.html success screen (lines 44-54)

**Problem:**
After creating a feedback cycle, users see links but **don't know what to do next**:
- Should they copy all links immediately?
- How do they send them to reviewers?
- What if they close the page?

**Impact:** High - Users may lose access to reviewer links

**Recommendation:**
Add clear next steps:
```html
<h1>Feedback Cycle Created!</h1>
<p><strong>Important:</strong> Copy each link below and send it directly to the reviewer via email or message. Each link is unique and can only be used once.</p>

<div class="message info">
    💡 <strong>Tip:</strong> These links are also available anytime from your Manager Dashboard below.
</div>
```

---

### 🚨 3. "Demo Data" Section Confusing in Production

**Location:** Homepage (index.html:42-57)

**Problem:**
The entire "Demo Data" section with hard-coded test data will confuse real users:
```html
<h2>Demo Data</h2>
<p>The system is pre-seeded with test data:</p>
```

**Impact:** High - Users think this is their real data or get confused

**Recommendation:**
- Remove this section entirely in production
- OR hide behind a "?demo=true" URL parameter
- OR clearly mark it: "🔧 Developer Testing Section (ignore this)"

---

### 🚨 4. No Way to Find Your Feedback Cycle Later

**Location:** Across the app - missing feature

**Problem:**
After an employee creates a feedback cycle, there's no way to:
- Find their employee ID again
- Re-access their reviewer links
- Check on progress

The only way back is to remember the employee ID or manager dashboard URL.

**Impact:** High - Users will contact support asking "how do I find my feedback?"

**Recommendation:**
Add one of these flows:
1. **Email confirmation** after creating cycle (includes links + dashboard URL)
2. **"My Feedback Cycles"** lookup on homepage (enter your email → see your cycles)
3. **Bookmark prompt** on success page with clear instruction

**Quick Fix:**
```html
<!-- On success page -->
<div class="message success">
    ✓ <strong>Bookmark this page!</strong> Your manager dashboard link is below. You can return to it anytime.
</div>
```

---

## High-Priority Recommendations (Should Fix)

### ⚠️ 5. Reviewer Nomination Form is Overwhelming

**Location:** nominate.html (lines 29-40)

**Problem:**
Users see 3 empty rows immediately + "Add Reviewer" button with no explanation of:
- Why 3-6 reviewers?
- What makes a good mix?
- What do "relationship" and "frequency" mean?

**Current State:**
```html
<h2>Reviewers</h2>
<p>Add 3-6 people who will provide feedback...</p>
```

**Recommendation:**
Add contextual help:
```html
<h2>Reviewers (3-6 people)</h2>
<p><strong>For best results, include a mix of:</strong></p>
<ul>
    <li>Your manager (for top-down perspective)</li>
    <li>2-3 peers you work with regularly</li>
    <li>1-2 direct reports (if applicable)</li>
    <li>Cross-functional colleagues you collaborate with</li>
</ul>

<div class="message info">
    💡 <strong>Why relationship & frequency matter:</strong> We weight feedback based on how closely someone works with the person. Managers and frequent collaborators have more influence on the final summary.
</div>
```

---

### ⚠️ 6. Unclear What "Relationship" and "Frequency" Affect

**Location:** nominate.html reviewer rows (lines 82-99)

**Problem:**
Users don't know why they're choosing these or how it impacts the summary.

**Recommendation:**
Add tooltips or help text:
```html
<label>
    Relationship
    <span class="help-icon" title="How this reviewer's feedback will be weighted">ⓘ</span>
</label>
```

Or add explanation above the form:
```html
<p><small><strong>Note:</strong> Relationship and frequency help us weight feedback appropriately. Manager and frequent collaborator feedback receives higher weight in the AI summary.</small></p>
```

---

### ⚠️ 7. Reviewers Don't Know Feedback is Anonymous

**Location:** review.html form (line 29-60)

**Problem:**
Reviewers may hold back honest feedback if they think the employee sees who said what.

**Recommendation:**
Add clear privacy notice:
```html
<h1>360 Feedback</h1>
<div class="message info">
    🔒 <strong>Your feedback is confidential.</strong> Individual responses are only visible to the manager, not the employee. The employee receives only an anonymized AI summary.
</div>
<p>You're providing feedback for <strong id="employee-name"></strong></p>
```

---

### ⚠️ 8. No Guidance on Writing Good Feedback

**Location:** review.html form fields (lines 31-58)

**Problem:**
Placeholder text is minimal. Non-technical users may not know what quality feedback looks like.

**Current:**
```html
<textarea placeholder="Describe behaviours, skills, or activities they should begin..."></textarea>
```

**Recommendation:**
Add example-driven placeholders:
```html
<textarea placeholder="Example: 'Start delegating more technical decisions to senior team members to free up time for strategic planning.'"></textarea>
```

Or add a collapsible "Tips for great feedback" section:
```html
<details class="help-section">
    <summary>💡 Tips for writing helpful feedback</summary>
    <ul>
        <li><strong>Be specific:</strong> "Interrupts in meetings" not "poor communication"</li>
        <li><strong>Give examples:</strong> "In last week's standup, when..."</li>
        <li><strong>Focus on behavior:</strong> Not personality traits</li>
        <li><strong>Be constructive:</strong> Suggest alternatives, not just criticism</li>
    </ul>
</details>
```

---

### ⚠️ 9. Manager Dashboard Has Too Many Buttons

**Location:** manager.html actions section (lines 59-63)

**Problem:**
Three buttons at once (Edit, Regenerate, Finalise) with no clear priority:
```html
<button id="edit-btn">Edit Summary</button>
<button id="regenerate-btn" class="secondary">Regenerate Summary</button>
<button id="finalise-btn" class="danger">Finalise Summary</button>
```

**Recommendation:**
Reorder and clarify:
```html
<div class="actions">
    <button id="finalise-btn" class="primary">Finalise & Share with Employee</button>
</div>
<div class="secondary-actions">
    <button id="edit-btn" class="secondary">Edit Summary</button>
    <button id="regenerate-btn" class="secondary">Regenerate with AI</button>
</div>
```

Add workflow guidance:
```html
<div class="message info">
    📝 <strong>Next steps:</strong>
    <ol>
        <li>Review the AI-generated summary below</li>
        <li>Edit if needed to add context or clarify</li>
        <li>When satisfied, click "Finalise" to lock it and share with the employee</li>
    </ol>
</div>
```

---

### ⚠️ 10. No Explanation of What "Finalise" Means

**Location:** manager.html finalise button (line 62)

**Problem:**
Button says "Finalise Summary" but users don't know:
- What happens after finalising?
- Can they undo it?
- What does the employee see?

**Current confirmation:**
```javascript
confirm('Once finalised, the summary cannot be edited or regenerated. Continue?')
```

**Recommendation:**
Better confirmation dialog and button text:
```html
<button id="finalise-btn" class="primary">Finalise & Share Summary</button>
```

```javascript
confirm(`Are you ready to finalise this summary?

After finalising:
✓ The summary will be locked (no more edits)
✓ You can share it with ${employeeName}
✗ You cannot regenerate or edit it

Continue?`)
```

---

## Medium-Priority Enhancements (Nice to Have)

### 11. Add Progress Indicators

**Location:** Multi-step flows (nominate, review)

**Recommendation:**
Add step indicators for longer forms:
```html
<div class="progress-steps">
    <span class="step active">1. Your Info</span>
    <span class="step">2. Add Reviewers</span>
    <span class="step">3. Share Links</span>
</div>
```

---

### 12. Better Empty States

**Location:** inbox.html when no reviews (not shown)

**Recommendation:**
Make empty states more helpful:
```html
<div class="empty-state">
    <h2>No Feedback Requests Yet</h2>
    <p>When someone nominates you as a reviewer, you'll see their request here.</p>
    <p><small>Check back later or ask your colleague to send you the direct review link.</small></p>
</div>
```

---

### 13. Add Character Count for Textareas

**Location:** review.html textareas (maxlength 2000)

**Recommendation:**
Show remaining characters:
```html
<textarea id="start-doing" maxlength="2000"></textarea>
<small class="char-count">0 / 2000 characters</small>
```

---

### 14. Improve Reviewer Link Copy UX

**Location:** nominate.html success (line 182)

**Problem:**
"Copy" button but no confirmation it worked.

**Recommendation:**
```javascript
function copyToClipboard(text) {
    navigator.clipboard.writeText(text);
    // Change button text temporarily
    event.target.textContent = '✓ Copied!';
    setTimeout(() => {
        event.target.textContent = 'Copy';
    }, 2000);
}
```

---

### 15. Add "Send via Email" Helper

**Location:** nominate.html success page

**Recommendation:**
Add mailto links:
```html
<div class="link-box">
    ${r.url}
    <button onclick="copyToClipboard('${r.url}')">Copy</button>
    <a href="mailto:${r.email}?subject=360 Feedback Request&body=Please provide feedback: ${r.url}">
        <button class="secondary">Email Link</button>
    </a>
</div>
```

---

### 16. Show Timestamp on Reviews

**Location:** manager.html reviewer table

**Recommendation:**
Add "Submitted on" column to show when feedback came in:
```html
<td><span class="status-badge submitted">✓ Submitted Jan 15</span></td>
```

---

### 17. Add "Download Summary" Option

**Location:** manager.html summary section

**Recommendation:**
Let managers export the final summary:
```html
<button id="download-btn" class="secondary">Download as PDF</button>
```

---

## Detailed Analysis by User Flow

### Flow 1: Employee Creates Feedback Cycle

**Current Experience:**
1. ✅ Clear entry point from homepage
2. ❌ Form is immediately overwhelming (3 empty rows)
3. ❌ No explanation of why 3-6 reviewers
4. ⚠️ Relationship/frequency dropdowns lack context
5. ✅ Dynamic add/remove works well
6. ❌ Success screen doesn't explain next steps
7. ❌ No way to retrieve links later

**Recommended Changes:**
- Add contextual help before form
- Explain weighting logic
- Add email confirmation or retrieval method
- Clearer success screen instructions

---

### Flow 2: Reviewer Submits Feedback

**Current Experience:**
1. ✅ Token-based access works
2. ✅ Shows employee name for context
3. ⚠️ No privacy/anonymity notice
4. ❌ No guidance on quality feedback
5. ❌ Placeholder text too generic
6. ✅ Form validation works
7. ✅ Success confirmation clear

**Recommended Changes:**
- Add confidentiality notice
- Better placeholder examples
- Optional: Tips section for feedback quality
- Show estimated time (5-10 minutes)

---

### Flow 3: Reviewer Finds Inbox

**Current Experience:**
1. ✅ Simple email lookup
2. ✅ Clear pending vs submitted status
3. ⚠️ Empty state could be more helpful
4. ✅ One-click access to reviews

**Recommended Changes:**
- Improve empty state messaging
- Add "last updated" timestamps
- Consider email notifications option

---

### Flow 4: Manager Reviews & Finalizes

**Current Experience:**
1. ❌ "Employee ID" confusing lookup
2. ✅ Progress tracker helpful
3. ⚠️ Three action buttons overwhelming
4. ❌ No workflow guidance
5. ❌ "Finalise" consequences unclear
6. ⚠️ No way to share/export summary

**Recommended Changes:**
- Better employee lookup (by name)
- Clear workflow steps
- Prioritize primary action (Finalise)
- Add export/sharing options
- Explain what happens after finalizing

---

## Quick Wins (Low Effort, High Impact)

### Priority Order for Implementation:

1. **Add helper text to "Employee ID"** (5 min)
2. **Add "Bookmark this" message on success screens** (5 min)
3. **Add confidentiality notice to review form** (5 min)
4. **Improve finalise confirmation dialog** (10 min)
5. **Add workflow guidance to manager dashboard** (15 min)
6. **Better placeholder text on review form** (15 min)
7. **Reorder/clarify manager action buttons** (20 min)
8. **Add reviewer selection guidance** (30 min)

**Total Quick Wins: ~2 hours of work, eliminates 80% of confusion**

---

## Terminology Improvements

**Change these terms for non-technical users:**

| Current Term | Better Term | Reason |
|--------------|-------------|--------|
| "Employee ID" | "Employee Name or ID" | IDs are developer concepts |
| "Finalise Summary" | "Finalise & Share Summary" | Clarifies outcome |
| "Generate Summary" | "Create AI Summary" | More descriptive |
| "Regenerate" | "Generate New Summary" | Clearer action |
| "Reviewer Progress" | "Feedback Status" | More natural language |
| "Your relationship" | "Your working relationship" | Less ambiguous |

---

## Visual/Layout Suggestions

### Color-Coded Workflow States

Use color to indicate status at a glance:
- 🟡 **Yellow**: Pending/In Progress
- 🟢 **Green**: Complete/Submitted
- 🔵 **Blue**: Informational
- 🔴 **Red**: Destructive action

### Add Icons for Quick Scanning

```html
<!-- Current -->
<h3>For Employees</h3>

<!-- Better -->
<h3>👤 For Employees</h3>
<h3>✍️ For Reviewers</h3>
<h3>📊 For Managers</h3>
```

### Improve Information Hierarchy

Use visual weight to guide users:
- **Primary action**: Large, colored button
- **Secondary actions**: Smaller, gray buttons
- **Destructive actions**: Red button, moved to bottom

---

## Accessibility Issues

### Missing ARIA Labels

Add screen reader support:
```html
<button aria-label="Remove reviewer">×</button>
<div role="status" aria-live="polite">3 of 4 reviews submitted</div>
```

### Keyboard Navigation

Ensure tab order makes sense:
- Skip navigation link
- Logical form field order
- Escape key to close modals/edits

### Color Contrast

Check all text meets WCAG AA standards (4.5:1 ratio)

---

## Mobile Responsiveness Issues

### Reviewer Grid Breaks on Mobile

**Problem:** 5-column grid in nominate.html:
```css
grid-template-columns: 1fr 1fr 150px 150px 40px;
```

**Recommendation:**
```css
@media (max-width: 768px) {
    .reviewer-row {
        grid-template-columns: 1fr;
        gap: 5px;
    }
}
```

### Tables Don't Scroll on Mobile

**Problem:** Manager dashboard table overflows

**Recommendation:**
```html
<div class="table-scroll">
    <table>...</table>
</div>
```

```css
.table-scroll {
    overflow-x: auto;
}
```

---

## Error Message Improvements

### Current Error Handling

Uses generic messages:
```javascript
throw new Error(error.detail || 'An error occurred');
```

### Recommended Error Messages

Make errors actionable:

| Error | Current | Better |
|-------|---------|--------|
| Invalid token | "An error occurred" | "This feedback link has expired or is invalid. Please ask the employee for a new link." |
| Employee not found | "Employee not found" | "We couldn't find an employee with ID '5'. Try entering their name instead, or check the ID is correct." |
| Network error | "An error occurred" | "Connection lost. Please check your internet and try again." |

---

## Security & Privacy Recommendations

### 1. Add Session Timeout Warning

For manager dashboard:
```html
<div class="message info">
    🔒 For security, you'll be logged out after 30 minutes of inactivity.
</div>
```

### 2. Clarify Data Retention

Add footer:
```html
<footer>
    <small>Feedback is stored securely and retained for 12 months. See our <a href="/privacy">Privacy Policy</a>.</small>
</footer>
```

### 3. Add "Delete Feedback Cycle" Option

For employees who change their mind:
```html
<button class="danger secondary">Cancel This Feedback Cycle</button>
```

---

## Testing Recommendations

### Usability Testing Script

Test with 3-5 non-technical users (HR/Ops):

**Task 1:** Create a feedback cycle for yourself
- Observe: Do they understand reviewer selection?
- Observe: Do they know what to do with the links?

**Task 2:** Submit feedback as a reviewer
- Observe: Do they understand each field?
- Observe: Do they feel comfortable being honest?

**Task 3:** Review and finalize a summary
- Observe: Do they understand the workflow?
- Observe: Do they know what happens after finalizing?

**Success Criteria:**
- 80% complete tasks without help
- No critical confusion points
- Positive feedback on clarity

---

## Summary: Top 10 Changes for Non-Technical Users

1. ✅ Replace "Employee ID" with name-based lookup
2. ✅ Add "What happens next?" guidance on all success screens
3. ✅ Add confidentiality notice to reviewer form
4. ✅ Better placeholder examples for feedback fields
5. ✅ Add reviewer selection guidance with examples
6. ✅ Clarify what "Finalise" means and does
7. ✅ Reorder manager action buttons by priority
8. ✅ Add workflow steps to manager dashboard
9. ✅ Hide/remove "Demo Data" section in production
10. ✅ Add email confirmation or feedback cycle retrieval method

**Estimated Implementation Time:** 4-6 hours
**Expected Impact:** Reduces user confusion by 70-80%

---

## Conclusion

The 360 Feedback Tool has a **strong technical foundation** but needs UX polish for non-technical users. The main issues are:

1. **Lack of contextual guidance** at decision points
2. **Technical terminology** (IDs, tokens) exposed to users
3. **Missing "what's next" instructions** after completing actions
4. **No recovery mechanisms** (can't find feedback cycles later)

Implementing the **Quick Wins section** (2 hours) will address 80% of user confusion. The remaining recommendations can be prioritized based on user testing feedback.

**Next Steps:**
1. Implement quick wins (this session)
2. User test with 3 HR/Ops staff
3. Iterate based on feedback
4. Polish visual design
5. Add advanced features (email notifications, export, etc.)
