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

The detect_conflicts() function uses exact time matching rather than duration overlap detection. 
THis only flags conflicts when you have multiple tasks with the exact same due time, rather than
the detection of overlapping durations (i.e. time conflict for the range from start to end of task).
This exact matching decreases time complexity than calculating duration overlaps, and in terms of scaling
can handle more tasks efficiently.
The main limitation being tasks with different start times but overlapping durations will not be flagged as conflicts

---

## 3. AI Collaboration
**a. How you used AI**

I used VS Code Copilot in several key ways:
Building the test suite (Copilot helped generate the structure for 32 tests across 7 categories (sorting, recurrence, conflict detection, etc.). I specified what to test, and Copilot created the test cases. I then verified each one by running pytest)
UI integration: using copilot to modify the streamlit functionalty to display algorithm results and bridge the gap between backend logic and frontend

**b. Judgment and verification**

One clear example: When working on the algorithms, Copilot initially created a very detailed, formal description with complexity notation (O(n), O(n²)) and extensive explanations. I explicitly asked for a "minimal and simple" approach instead. I rejected the complex approach and prompted Copilot to refactor it into concise feature categories with 2-3 line descriptions each. The result was much cleaner and more readable.

Verification approach: I didn't just accept suggestions, I tested them. For every algorithm Copilot helped optimize, I ran pytest. For every UI component, I loaded the app and checked it worked. The 32 passing tests gave me reassurance the system was not failing any edge cases or input testing, not just blindly copying the AI output.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I built 32 tests organized into 7 categories:
- **Sorting correctness** (4 tests): Tasks ordered by time, boundary times like midnight and 11:59 PM, empty task lists
- **Recurrence logic** (6 tests): Daily, weekly, and monthly patterns generate next tasks correctly; task IDs chain properly (T001 → T001_1)
- **Conflict detection** (6 tests): Multiple tasks at the same time flagged, different pets don't conflict, no false positives
- **Filtering** (3 tests): Filter by pet ID and completion status return accurate results
- **Task expansion** (5 tests): 30-day plans show correct counts (30 daily, 5 weekly, 1-2 monthly)
- **Urgency scoring** (3 tests): Tasks without due times handled, overdue bonuses applied correctly
- **Edge cases** (5 tests): Empty pet lists, boundary dates, task properties preserved during generation

These tests were important because they proved the core logic works before we built the UI on top of it.

**b. Confidence**
- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Confidence: 5 out of 5 stars confidence; as all 32 tests passed (0.13 seconds execution). I tested not just the happy path but edge cases like tasks with no due time, monthly patterns at month boundaries, and empty lists. The test suite covers the main algorithms and their interactions, so I'm confident the scheduler behaves correctly in real use.

---

## 5. Reflection

**a. What went well**
- What part of this project are you most satisfied with?

I'm most satisfied with how the scheduler algorithms and UI came together. The backend has clean, focused methods, and the Streamlit UI directly shows what each algorithm does. Users can see the sorted tasks, spot conflicts, expand recurring tasks, and check time utilization—all driven by the actual scheduling logic. The testing gives me confidence that everything actually works too.

**b. What you would improve**
- If you had another iteration, what would you improve or redesign?

The conflict detection currently uses exact time matching (two tasks at the same time). A better approach would be duration overlap detection—flagging when tasks have overlapping time ranges instead of just matching start times. This would catch more real scheduling problems. I chose exact matching for simplicity (time complexity), but in a real app managing many tasks, overlap detection would be more useful.

**c. Key takeaway**
- What is one important thing you learned about designing systems or working with AI on this project?

The most important lesson, is that AI can hallucinate,; you are the lead architect, not the AI. Copilot is powerful at generating code and ideas, but you need to guide it. When I asked for a Features section and Copilot made it too complex or verbose, Igave it the feedback to adjust and modify through prompting. When it suggested UI components, I picked the ones that actually made sense for showing algorithm results. Using separate chat sessions for different phases (testing phase, UI phase, documentation phase) helped me stay organized and keep each conversation focused.