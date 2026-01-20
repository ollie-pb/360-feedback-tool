# UX Review Reconciliation Against MVP PRD

**Date:** 2026-01-20
**Purpose:** Reconcile UX recommendations against original MVP scope and constraints

---

## Original MVP Constraints

From `MVP PRD.md`:
- **Timebox:** 6 hours
- **Priority:** Working happy-path > polish/edge cases
- **Target Users:** Not specified (UX review added: non-technical ops/HR)
- **Out of Scope:**
  - Authentication/login
  - Email sending
  - Multiple review cycles
  - Edge case handling
  - **Responsive design / styling polish**
  - PDF export
  - Reminder nudges

---

## Reconciliation Analysis

### ✅ ALIGNED WITH MVP SCOPE
*These recommendations improve the happy path without adding scope*

#### 1. Employee ID Confusion (Critical Issue #1)
**UX Recommendation:** Change "Employee ID" to "Employee Name or ID" with helper text
**MVP Alignment:** ✅ **ALIGNED** - Happy path improvement
**Rationale:**
- PRD doesn't specify how users find employees
- Current implementation **blocks the happy path** for non-technical users
- Simple text change, no API changes needed
- **KEEP THIS RECOMMENDATION**

#### 2. Missing "Next Steps" Guidance (Critical Issue #2)
**UX Recommendation:** Add instructions on success screens about what to do with links
**MVP Alignment:** ✅ **ALIGNED** - Happy path clarity
**Rationale:**
- PRD says: "Display links to copy/share (no email send)"
- Current implementation shows links but **users don't know what to do**
- Adding guidance text is not "polish" - it's **completing the happy path**
- **KEEP THIS RECOMMENDATION**

#### 3. Demo Data Section Confusion (Critical Issue #3)
**UX Recommendation:** Hide or clearly mark demo data section
**MVP Alignment:** ✅ **ALIGNED** - Demo infrastructure, not user-facing
**Rationale:**
- PRD says: "Pre-seed test data for demo"
- This was meant for **developer testing**, not user UI
- Showing it to users confuses the happy path
- **KEEP THIS RECOMMENDATION**

#### 4. No Privacy/Anonymity Notice (High Priority #7)
**UX Recommendation:** Add confidentiality notice to review form
**MVP Alignment:** ✅ **ALIGNED** - Happy path enabler
**Rationale:**
- PRD doesn't specify, but **reviewers won't give honest feedback** without knowing it's confidential
- Blocks the happy path (quality feedback collection)
- Single text addition, no scope increase
- **KEEP THIS RECOMMENDATION**

#### 5. Unclear "Finalise" Action (High Priority #10)
**UX Recommendation:** Better confirmation dialog explaining consequences
**MVP Alignment:** ✅ **ALIGNED** - Happy path clarity
**Rationale:**
- PRD says: "Finalise locks the summary from further editing"
- Current implementation has basic confirm() - **users don't understand consequences**
- Better dialog text prevents mistakes on happy path
- **KEEP THIS RECOMMENDATION**

#### 6. Manager Dashboard Button Priority (High Priority #9)
**UX Recommendation:** Reorder buttons to show primary action first
**MVP Alignment:** ✅ **ALIGNED** - Happy path guidance
**Rationale:**
- PRD doesn't specify button order
- Three equal buttons confuse the workflow
- Reordering guides users through happy path
- **KEEP THIS RECOMMENDATION**

---

### ⚠️ SCOPE EXPANSION (But Justified for Happy Path)
*These add minimal scope but significantly improve usability*

#### 7. No Way to Retrieve Feedback Cycles (Critical Issue #4)
**UX Recommendation:** Add email confirmation or "My Cycles" lookup
**MVP Alignment:** ⚠️ **SCOPE EXPANSION**
**Rationale:**
- PRD is silent on this
- Out of scope: "Email sending" (explicitly excluded)
- **However:** Current implementation **breaks the happy path entirely** if user closes browser
- **COMPROMISE SOLUTION:** Add "Bookmark this page" reminder (zero scope) instead of email
- **MODIFY RECOMMENDATION TO MINIMAL VERSION**

#### 8. Reviewer Selection Guidance (High Priority #5)
**UX Recommendation:** Add contextual help about choosing reviewers
**MVP Alignment:** ⚠️ **MINOR SCOPE EXPANSION**
**Rationale:**
- PRD says: "Add 3-6 reviewers" but doesn't explain **why** or **which**
- Adding explanatory text is not in original scope
- **However:** Without it, users don't know what makes a "good" reviewer mix
- This is **clarifying implicit requirements**, not adding features
- **KEEP BUT SIMPLIFY** - 2-3 sentences max, not full help section

#### 9. Feedback Quality Guidance (High Priority #8)
**UX Recommendation:** Add example-driven placeholders and tips
**MVP Alignment:** ⚠️ **MINOR SCOPE EXPANSION**
**Rationale:**
- PRD shows basic placeholders: "Describe behaviours, skills..."
- Better examples improve **feedback quality** (core product value)
- **COMPROMISE:** Improve placeholder text only, skip "Tips" section
- **MODIFY TO MINIMAL VERSION**

---

### ❌ OUT OF MVP SCOPE
*These are polish/features explicitly excluded*

#### 10. Progress Indicators (Medium Priority #11)
**UX Recommendation:** Add step indicators for multi-step forms
**MVP Alignment:** ❌ **OUT OF SCOPE** - This is "styling polish"
**Rationale:**
- PRD explicitly excludes "styling polish"
- Forms are simple enough without this
- **REMOVE THIS RECOMMENDATION**

#### 11. Character Count for Textareas (Medium Priority #13)
**UX Recommendation:** Show "X / 2000 characters" counter
**MVP Alignment:** ❌ **OUT OF SCOPE** - Polish feature
**Rationale:**
- PRD has `maxlength="2000"` - browser handles this
- Character counter is nice-to-have, not essential to happy path
- **REMOVE THIS RECOMMENDATION**

#### 12. Copy Button Feedback Improvement (Medium Priority #14)
**UX Recommendation:** Change button text to "✓ Copied!" temporarily
**MVP Alignment:** ❌ **OUT OF SCOPE** - Polish
**Rationale:**
- Current implementation has `alert("Copied!")` which works
- Fancier feedback is polish
- **REMOVE THIS RECOMMENDATION**

#### 13. "Send via Email" Helper (Medium Priority #15)
**UX Recommendation:** Add mailto links
**MVP Alignment:** ❌ **OUT OF SCOPE** - PRD explicitly excludes "Email sending"
**Rationale:**
- PRD: "Display links to copy/share (no email send)"
- mailto links = email sending
- **REMOVE THIS RECOMMENDATION**

#### 14. Timestamp on Reviews (Medium Priority #16)
**UX Recommendation:** Show "Submitted on Jan 15" in table
**MVP Alignment:** ❌ **OUT OF SCOPE** - Additional feature
**Rationale:**
- PRD specifies: "Name | Relationship | Frequency | Status"
- Timestamps not in original design
- **REMOVE THIS RECOMMENDATION**

#### 15. Download Summary as PDF (Medium Priority #17)
**UX Recommendation:** Add PDF export
**MVP Alignment:** ❌ **OUT OF SCOPE** - PRD explicitly excludes "PDF export"
**Rationale:**
- Listed in "Out of Scope (Explicitly)"
- **REMOVE THIS RECOMMENDATION**

#### 16. Better Empty States (Medium Priority #12)
**UX Recommendation:** More helpful empty state messages
**MVP Alignment:** ⚠️ **EDGE CASE** - PRD says "happy path > edge cases"
**Rationale:**
- Empty inbox is an edge case (demo has seeded data)
- **COMPROMISE:** Basic improvement OK if < 5 min, skip elaborate empty states
- **MODIFY TO MINIMAL VERSION**

---

### 🤔 AMBIGUOUS / REQUIRES CLARIFICATION

#### 17. Responsive Design Issues (Mobile Responsiveness)
**UX Recommendation:** Fix grid breaking on mobile
**MVP Alignment:** 🤔 **AMBIGUOUS** - PRD excludes "responsive design / styling polish"
**Rationale:**
- PRD explicitly lists "Responsive design / styling polish" as out of scope
- **However:** Current grid completely breaks on mobile (unusable, not just unpolished)
- **Question:** Is "broken" different from "not optimized"?
- **DECISION:** If grid is **unusable** (can't fill form), it's a happy path blocker → FIX
- If it's just **ugly**, it's polish → SKIP
- **KEEP MINIMAL FIX IF BLOCKING, SKIP IF JUST UGLY**

#### 18. Accessibility Issues (ARIA labels, keyboard nav)
**UX Recommendation:** Add screen reader support
**MVP Alignment:** 🤔 **AMBIGUOUS** - Not mentioned in PRD
**Rationale:**
- PRD doesn't mention accessibility
- Could argue it's part of "happy path" for screen reader users
- Could argue it's "polish" for MVP
- **DECISION:** Skip for MVP, note for post-MVP
- **REMOVE THIS RECOMMENDATION** (for MVP)

---

## Revised Recommendations: MVP-Scoped Only

### 🔴 CRITICAL (Must Fix - Happy Path Blockers)

1. **Employee ID → Employee Name/ID** ✅
   - Change label text and placeholder
   - Add helper text
   - **Effort:** 2 minutes

2. **Add "What's Next" on Success Screens** ✅
   - Nomination success: Explain to share links + bookmark dashboard
   - Review success: Already clear
   - **Effort:** 5 minutes

3. **Hide/Mark Demo Data Section** ✅
   - Add conditional rendering or clear "Testing Only" header
   - **Effort:** 2 minutes

4. **Add Bookmark Reminder** ✅ (instead of email)
   - Show: "⚠️ Save this page! You can return to your dashboard at: [URL]"
   - No email needed, zero scope
   - **Effort:** 3 minutes

**Total Critical Fixes: 12 minutes**

---

### 🟡 HIGH PRIORITY (Should Fix - Happy Path Clarity)

5. **Add Confidentiality Notice** ✅
   - Single message box on review form
   - **Effort:** 3 minutes

6. **Better Finalise Confirmation** ✅
   - Improve confirm() dialog text
   - **Effort:** 2 minutes

7. **Reorder Manager Buttons** ✅
   - CSS or HTML reordering
   - **Effort:** 5 minutes

8. **Add Reviewer Selection Guidance** ✅ (simplified)
   - 2-3 sentences above form: "For best results, include your manager, 2-3 peers, and cross-functional colleagues"
   - **Effort:** 5 minutes

9. **Improve Feedback Placeholders** ✅ (minimal)
   - Better example text in existing placeholders
   - **Effort:** 5 minutes

10. **Add Workflow Steps to Manager Dashboard** ✅
    - Simple numbered list: "1. Review summary 2. Edit if needed 3. Finalise"
    - **Effort:** 3 minutes

**Total High Priority: 23 minutes**

---

### 🟢 NICE-TO-HAVE (If Time Permits)

11. **Basic Empty State Improvement** ⚠️
    - Replace "No feedback requests found" with slightly more helpful text
    - **Effort:** 2 minutes

12. **Mobile Grid Fix** ⚠️ (only if broken, not if ugly)
    - Test on mobile - if form is unusable, add basic responsive CSS
    - **Effort:** 10 minutes (only if blocking)

**Total Nice-to-Have: 2-12 minutes**

---

## Total Implementation Time

- **Critical Fixes:** 12 minutes
- **High Priority:** 23 minutes
- **Nice-to-Have:** 2-12 minutes

**Total: 37-47 minutes** (well under 1 hour)

---

## Removed Recommendations (Out of Scope)

The following from the original UX review are **NOT recommended for MVP**:

- ❌ Progress indicators (polish)
- ❌ Character counters (polish)
- ❌ Copy button fancy feedback (polish)
- ❌ Email helpers / mailto links (email sending excluded)
- ❌ Review timestamps (feature expansion)
- ❌ PDF export (explicitly excluded)
- ❌ Elaborate empty states (edge case handling)
- ❌ Full accessibility (post-MVP)
- ❌ Advanced mobile optimization (responsive polish excluded)

---

## Key Insights from Reconciliation

### 1. "Happy Path" vs "Polish" Definition

The MVP PRD distinguishes between:
- **Happy path:** Core user journey must work clearly
- **Polish:** Nice-to-have improvements, visual refinements

**Insight:** Several UX issues were mislabeled as "polish" when they actually **block the happy path**:
- Users can't find employees (ID confusion)
- Users don't know what to do with links (missing guidance)
- Users lose access to dashboards (no retrieval method)
- Reviewers may hold back feedback (no privacy notice)

These are **happy path blockers**, not polish.

---

### 2. MVP Scope Was Developer-Focused, Not User-Focused

**Original PRD priority:** "Working happy-path > polish/edge cases"

**Interpretation:** PRD focused on **technical implementation** of happy path (API works, data flows correctly) but didn't specify **user clarity** requirements.

**Example:**
- PRD: ✅ "Display links to copy/share"
- Implementation: ✅ Links are displayed
- **Missing:** Instructions on what to do with them

**Insight:** UX recommendations **complete the happy path**, they don't add scope.

---

### 3. "Non-Technical User" Context Was Missing

**Original PRD:** Silent on target user technical proficiency

**UX Review Addition:** "Target user: ops/HR (non-technical)"

**Impact:** Changes interpretation of what's "clear enough":
- Developer thinks: "Employee ID is obvious (it's in the URL)"
- HR person thinks: "What's an ID? I know names."

**Insight:** Several recommendations simply **adapt language for non-technical users** without changing functionality.

---

### 4. Demo vs Production Separation

**PRD Intent:** "Pre-seed test data for demo"

**Implementation:** Demo data **displayed in production UI**

**UX Impact:** Confuses real users

**Insight:** Need to separate **developer testing data** from **user-facing interface**.

---

## Final Recommendation

### Implement in This Session (37-47 min)

**Rationale:**
1. All recommendations are **happy path improvements**, not scope creep
2. Total time (< 1 hour) is **small compared to original 6-hour MVP**
3. These fix **usability blockers** that would prevent real deployment
4. No API changes needed - all frontend text/guidance
5. Aligns with MVP goal: **"working happy path"**

**What This Fixes:**
- ✅ Non-technical users can navigate the tool
- ✅ Users understand what to do at each step
- ✅ Users don't lose access to their data
- ✅ Reviewers feel safe giving honest feedback
- ✅ Managers understand the workflow

---

### Post-MVP Enhancements (Not Now)

Save these for post-MVP iterations:
- Email notifications (requires email sending implementation)
- PDF export (requires new dependency)
- Full responsive design (mobile optimization)
- Accessibility (ARIA, keyboard nav)
- Advanced features (timestamps, analytics, etc.)

---

## Terminology Alignment

### Aligned Terms to Change

| Current | Better | PRD Status |
|---------|--------|------------|
| "Employee ID" | "Employee Name or ID" | ✅ Not specified in PRD, improvement allowed |
| "Finalise Summary" | "Finalise & Share Summary" | ✅ PRD says "locks summary", clarifying is good |
| Demo Data heading | "🔧 Testing Data (Ignore)" | ✅ PRD says "for demo", meant for devs |

### Terms to Keep (PRD-Specified)

| Term | Reason |
|------|--------|
| "Start doing / Stop doing / Continue doing" | ✅ Specified in PRD (pages section) |
| "Relationship" and "Frequency" | ✅ Core data model terms |
| "Manager Dashboard" | ✅ PRD terminology |
| "Reviewer", "Employee" | ✅ Core domain terms |

---

## Conclusion

### Original UX Review Assessment: **B-**

After reconciliation:
- ✅ **Correctly identified** that happy path has clarity gaps
- ⚠️ **Over-recommended** some polish features out of MVP scope
- ✅ **Valid insight** that non-technical users need different language

### Reconciled Recommendations: **10 Critical/High Priority Items**

All are **MVP-scoped, happy-path improvements** requiring < 1 hour total.

### Next Action

**Proceed with implementation?**
- Yes → Implement 10 items (37-47 minutes)
- No → Discuss which subset to implement
- Defer → Document for post-MVP

---

## Comparison: Before vs After Reconciliation

### UX Review (Original)
- **Critical Issues:** 4
- **High Priority:** 6
- **Medium Priority:** 7
- **Total Recommendations:** 17
- **Estimated Time:** 4-6 hours

### Reconciled (MVP-Scoped)
- **Critical Issues:** 4
- **High Priority:** 6
- **Nice-to-Have:** 2
- **Total Recommendations:** 12
- **Estimated Time:** 37-47 minutes
- **Removed:** 5 items (polish, explicitly out of scope)

**Result:** Focused, actionable, MVP-aligned improvements that respect the original timebox constraints while fixing real usability issues.
