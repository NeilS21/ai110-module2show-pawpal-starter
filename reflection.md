# PawPal+ Project Reflection

## 1. System Design

User should be able to add pets to profile, User should be able to view tasks to be completed (i.e. going for walk or feeding pet) and mark off completed tasks, and User should be able to find/generate a recommened daily plan based on some information or requirements collected from the user.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

There are 5 main classes to consider: Owner, Pet, CareTask, Scheduler, and DailyPlan.
Owner class includes id, name, daily_time_available, prefernces, and max_tasks_per_day
Pet class includes pet_id, name, species, age, energy_level, and medical_notes
CareTask class includes task_id, pet_id, title, category, duration_minutes, priority, due_time, and is_completed
Scheduler class includes constraints, scoring_weights, and strategy
DailyPlan class includes date, scheduled_items, total_minutes_used, and unscheduled_tasks

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Added pet_id o caretask in order to link takses to a specifc pet.
In scheduleer the build_plan funtion added paraeter for current_time to keep record of timing,
the score_task added the parameters current_time to clacute due times and help prioritze urgent tasks
 and remaing_minutes to calculate time left for a task.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
