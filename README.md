# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling Features

This implementation includes advanced algorithmic features to improve pet care scheduling:

### Chronological Sorting
- **`sort_by_time()`** – Sorts tasks by due time in chronological order (O(n log n))
- Tasks without due times are placed at the end for filtering flexibility
- Uses lambda function to convert time to minutes for comparison

### Intelligent Filtering
- **`filter_by_pet()`** – Return all tasks for a specific pet
- **`filter_by_completion()`** – Separate pending and completed tasks
- Enables focused views of the schedule

### Recurring Task Automation
- **`mark_complete()` & `_generate_next_occurrence()`** – Automatically generate next occurrences for recurring tasks
- Supports daily, weekly, and monthly patterns using `timedelta` calculations
- Each completion generates the next task instance with proper date math
- Useful for regular care activities (daily feeding, weekly grooming, etc.)

### 30-Day Schedule Expansion
- **`expand_recurring_tasks()`** – Expands recurring tasks across 30+ days
- Generates task instances for multi-week scheduling
- Calculates pattern-based dates (daily=every 1 day, weekly=every 7 days, monthly=every 30 days)

### Conflict Detection
- **`detect_conflicts()`** – Identifies when multiple tasks are scheduled at the same time
- Lightweight O(n²) algorithm comparing exact time matches
- Returns detailed warning messages showing which tasks and pets are in conflict
- Prevents scheduling oversights and helps optimize the daily plan

### Design Principle
All algorithms prioritize **readability and maintainability** over micro-optimizations, making them ideal for learning and future expansion.
