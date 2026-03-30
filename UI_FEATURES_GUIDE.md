# PawPal+ Streamlit UI Feature Guide

## Overview

The Streamlit UI now fully integrates the **Scheduler class algorithms** built in Phase 3. Instead of a basic list view, PawPal+ now provides a **smart, interactive dashboard** for pet care planning.

---

## 📊 Feature Breakdown

### 1. **View & Analyze Tasks** (4 Tabs)

#### Tab 1: 📅 All Tasks (Sorted Chronologically)

**What it does:** Uses `Scheduler.sort_by_time()` to display tasks ordered by due time (earliest first).

**Key Features:**
- **Professional DataFrame** showing:
  - Task name
  - Pet name
  - Duration (in minutes)
  - Priority (displayed as stars ⭐⭐⭐)
  - Due time (formatted as 12-hour clock)
  - Status (✓ Done or ○ Pending)
  - **Urgency Score** (calculated from `task.get_urgency_score()`)

- **Pet Filtering** dropdown:
  - Filter to see only one pet's tasks
  - Uses `Scheduler.filter_by_pet()`
  - Shows count of tasks for selected pet

**Code Integration:**
```python
sorted_tasks = scheduler.sort_by_time(st.session_state.tasks)
urgency = task.get_urgency_score(time(12, 0))  # Score at noon
```

---

#### Tab 2: ⚠️ Conflict Check (Conflict Detection)

**What it does:** Uses `Scheduler.detect_conflicts()` to find scheduling collisions.

**User Experience Design:**
- **Clear Warning Display** (st.warning):
  - Shows prominent red alert if conflicts exist
  - Lists each conflict with affected task pairs
  - Shows exact times where conflicts occur
  - Example: `"[CONFLICT] 'Morning Walk' (Pet: P001) and 'Dog Feeding' (Pet: P001) both scheduled at 8:00 AM"`

- **Expandable Conflict Details**:
  - Each conflict shows which pets are affected
  - Helps owner understand the impact
  - Non-intrusive but informative

- **Helpful Recommendations** (st.markdown):
  - Adjust task times to avoid overlaps
  - Batch quick tasks (feeding, water)
  - Delegate to another caregiver
  - Shows owner-friendly solutions, not just problems

- **Green Success State** (st.success):
  - If no conflicts: "✓ No scheduling conflicts detected!"
  - Reassures owner that schedule is clear

**Why this presentation helps:**
1. **Visibility**: Red warnings are impossible to miss
2. **Understanding**: Specific task names and times = clear problem
3. **Actionable**: Recommendations provide next steps
4. **Relief**: Green success message builds confidence

**Code Integration:**
```python
conflicts = scheduler.detect_conflicts(st.session_state.tasks)
if conflicts:
    st.warning("⚠️ **Scheduling Conflicts Detected!**")
    for task1, task2, warning_msg in conflicts:
        st.write(warning_msg)
```

---

#### Tab 3: 🔄 30-Day Expansion (Recurring Tasks)

**What it does:** Uses `Scheduler.expand_recurring_tasks()` to show multi-week planning.

**Key Features:**
- Lists all recurring task templates (daily, weekly, monthly)
- **Expansion Metrics** (using st.metric):
  - Daily task instances (e.g., 30 tasks over 30 days)
  - Weekly instances (e.g., 5 tasks over 30 days)
  - Monthly instances (e.g., 1-2 tasks over 30 days)

- **Sample Timeline** (DataFrame):
  - Shows first 15 expanded tasks
  - Displays: Date, Task name, Pet, Recurrence type, Time
  - Helps owner visualize recurring task frequency

- **Empty State Messaging**:
  - If no recurring tasks: Clear guidance to add them
  - Explains what patterns are supported (daily, weekly, monthly)

**Code Integration:**
```python
expanded = scheduler.expand_recurring_tasks(recurring_tasks, days=30)
daily_count = len([t for t in expanded if t.recurrence_pattern == "daily"])
st.metric("Daily Instances", daily_count)
```

---

#### Tab 4: 📊 Analytics Dashboard

**What it does:** Provides high-level overview of the task portfolio.

**Metrics Displayed** (st.metric):
- **Total Tasks**: Count of all tasks
- **Completed**: Count of finished tasks (filter_by_completion with completed=True)
- **Pending**: Count of unfinished tasks (filter_by_completion with completed=False)
- **Recurring**: Count of non-one-time tasks (get_recurring_tasks)

**Time Utilization Tracking**:
- **Total Time Needed**: Sum of pending task durations
- **Owner Available**: From owner.daily_time_available
- **Visual Progress Bar**: Shows % of available time used
- **Smart Status Messages**:
  - ⚠️ Red: Tasks exceed available time (overbooked)
  - ⚡ Blue: 80%+ utilization (very full schedule)
  - ✓ Green: Comfortable headroom left

**Code Integration:**
```python
total_duration = sum(t.duration_minutes for t in tasks if not t.is_completed)
utilization = (total_duration / owner_available) * 100
st.progress(min(utilization / 100, 1.0))
```

---

### 2. **Build Daily Schedule** (Optimized Timeline)

**What it does:** Combines sorting and conflict detection into a final schedule view.

**Workflow:**
1. Uses `sort_by_time()` to order tasks
2. Checks `detect_conflicts()` to find problems
3. Displays professional **schedule timeline** using st.dataframe

**Schedule Display** (Professional Table):
- **Time Column**: 12-hour format with start/end times
- **Task Name**: Clear task identification
- **Pet**: Which pet the task is for
- **Duration**: Task length in minutes
- **Priority**: Visual star rating (⭐⭐)
- **Status**: Done/Pending indicator

**Conflict Warnings** (If Present):
- Expandable section showing all conflicts
- Each conflict individually displayed with `st.warning()`
- Non-blocking (warning doesn't prevent schedule display)
- Helps owner see conflicts AND schedule together

**Success Message**:
- "✓ Schedule is ready for the day!" indicates completion
- Green success state provides positive feedback

**Code Integration:**
```python
sorted_tasks = scheduler.sort_by_time(st.session_state.tasks)
conflicts = scheduler.detect_conflicts(sorted_tasks)
if conflicts:
    st.markdown("#### ⚠️ Scheduling Conflicts")
    for task1, task2, warning_msg in conflicts:
        st.warning(warning_msg)
```

---

## 🎨 Streamlit Components Used

| Component | Purpose | Example |
|-----------|---------|---------|
| **st.dataframe()** | Professional table display | Task lists, schedules, timelines |
| **st.warning()** | Conflict alerts | "⚠️ [CONFLICT] Task A and Task B at 8:00 AM" |
| **st.success()** | Validation & positive feedback | "✓ No conflicts detected!" |
| **st.info()** | Informational messages | Owner name, available time |
| **st.error()** | Error states | Missing owner/tasks |
| **st.metric()** | Key statistics | Total tasks: 5, Completed: 2 |
| **st.progress()** | Visual utilization | 75% of time used ▓▓▓░ |
| **st.tabs()** | Organized views | All Tasks, Conflicts, Expansion, Analytics |
| **st.expander()** | Hidden details | Conflict details, expansions |
| **st.caption()** | Helper text | Explanations, context |

---

## 🔄 How Conflicts Are Presented to Owners

### Scenario: Two tasks at same time

**The Problem:**
- 8:00 AM: Morning Walk (30 min) for Max (dog)
- 8:00 AM: Dog Feeding (10 min) for Max (dog)

**How PawPal+ Presents It:**

**Step 1: Conflict Tab Alert**
```
⚠️ Scheduling Conflicts Detected!

1 conflict(s) found:

⚠️ #1
[CONFLICT] 'Morning Walk' (Pet: P001) and 'Dog Feeding' (Pet: P001) 
both scheduled at 8:00 AM

✅ Recommendations:
- Adjust task times to avoid overlaps
- Consider batching quick tasks (feeding, water)
- Delegate one task to another caregiver if available
```

**Step 2: Analytics Impact**
- Tab 4 shows:
  - ⚠️ **Time exceeds available** (if tasks > available time)
  - Tasks can't realistically be done

**Step 3: Schedule View**
- Both tasks appear in timeline
- Expandable conflict warning shows why
- Owner can see the exact overlap visually

**Why This Design Works:**
1. **Visible**: Color + emoji draw attention
2. **Specific**: Shows exact task names, times, and pets
3. **Actionable**: Provides specific recommendations
4. **Non-blocking**: Owner sees everything still (not frozen)
5. **Professional**: Uses structured messages, not error boxes

---

## 🚀 User Workflow Example

### Scenario: Pet owner wants to schedule the week

**Step 1: Create Owner & Pets**
- Owner: "Alice" with 3 hours available/day
- Pets: Max (dog), Whiskers (cat)

**Step 2: Add Tasks**
- 7:00 AM: Morning Walk (30 min, priority 3) - Max
- 8:00 AM: Dog Feeding (10 min, priority 1) - Max
- 12:00 PM: Cat Feeding (10 min, priority 1) - Whiskers
- 6:00 PM: Evening Walk (30 min, priority 3) - Max

**Step 3: View & Analyze** (4 Tabs)

| Tab | What Alice Sees |
|-----|-----------------|
| **All Tasks** | Tasks sorted: Morning Walk → Dog Feeding → Cat Feeding → Evening Walk. Urgency scores show which are most pressing. |
| **Conflicts** | ✓ "No conflicts detected!" - all tasks are at different times. |
| **30-Day** | Morning/Evening Walk repeating daily = 60 instances. Feeding repeating daily = 60 instances. Total: 120 task instances. |
| **Analytics** | 4 total tasks, 0 completed, 4 pending, 2 recurring. Total time needed: 80 min. Available: 180 min. 44% utilization - lots of headroom. ✓ |

**Step 4: Build Daily Schedule**
- Click "Generate Optimized Schedule"
- See professional 4-task timeline: 7:00 AM - 7:00 PM
- ✓ "Schedule is ready for the day!"

---

## 📋 Summary of Scheduler Integration

| Scheduler Method | Where Used | Streamlit Component |
|------------------|-----------|-------------------|
| `sort_by_time()` | All Tasks tab, Daily Schedule | st.dataframe() |
| `detect_conflicts()` | Conflicts tab, Daily Schedule | st.warning() |
| `filter_by_pet()` | All Tasks pet filter | st.selectbox() |
| `filter_by_completion()` | Analytics tab metrics | st.metric() |
| `get_recurring_tasks()` | 30-Day tab, Analytics | st.markdown() |
| `expand_recurring_tasks()` | 30-Day tab expansion | st.dataframe() |
| `get_urgency_score()` | All Tasks urgency column | st.dataframe() |

---

## 🎯 Key Design Principles Applied

1. **Progressive Disclosure**: Basics visible, details in tabs/expanders
2. **Status Indicators**: Colors (red/green) + emoji (✓/⚠️) for quick scanning
3. **Professional Display**: DataFrames instead of text lists
4. **Context-Aware**: Time utilization shows if schedule is feasible
5. **Non-Blocking Warnings**: Conflicts don't prevent viewing schedule
6. **Actionable Insights**: Recommendations, not just problems
7. **Metrics-First**: Numbers + visuals (progress bar) 
8. **Clear Messaging**: Plain English explanations of what algorithms did

---

## 🔄 Try It Out

To see the full UI in action:

```bash
streamlit run app.py
```

Then:
1. Create an owner
2. Add 2-3 pets
3. Add 4-6 tasks with some at the same times
4. Click through all 4 tabs to see analytics
5. Build a schedule to see conflicts (if any)

The UI will automatically show the results of sorting, filtering, detecting conflicts, and expanding recurring tasks!
