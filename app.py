import streamlit as st
from pawal_system import Owner, Pet, CareTask, Scheduler, DailyPlan
from datetime import time, date, timedelta
import pandas as pd

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+ Smart Pet Care Scheduler")

# Initialize session state if not already done
if 'owner' not in st.session_state:
    st.session_state.owner = None

if 'pets' not in st.session_state:
    st.session_state.pets = []

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Create Owner & Pets")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_time = st.number_input("Daily time available (minutes)", min_value=30, max_value=480, value=180)

if st.button("Create/Update Owner"):
    owner = Owner(
        owner_id="O001",
        name=owner_name,
        daily_time_available=available_time,
        preferences="flexible",
        max_tasks_per_day=10
    )
    # Set the owner's preferences and time using the class methods
    owner.set_available_time(available_time)
    owner.update_preferences("flexible")
    
    st.session_state.owner = owner
    st.success(f"Owner '{owner_name}' saved to session!")

if st.session_state.owner:
    st.info(f"✓ Owner: {st.session_state.owner.name} | Available: {st.session_state.owner.daily_time_available} min/day")

st.markdown("### Add Pets")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird"])
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    if st.session_state.owner:
        # Create the pet
        pet = Pet(
            pet_id=f"P{len(st.session_state.pets) + 1:03d}",
            name=pet_name,
            species=species,
            age=age,
            energy_level="high",
            medical_notes=""
        )
        
        # Call Pet.update_profile() to initialize/validate the pet data
        pet.update_profile()
        
        # Append to session state (this triggers a Streamlit rerun)
        st.session_state.pets.append(pet)
        st.success(f"Pet '{pet_name}' added!")
    else:
        st.error("Please create an Owner first.")

if st.session_state.pets:
    st.write(f"**Pets ({len(st.session_state.pets)}):**")
    for pet in st.session_state.pets:
        # Call get_care_needs() to show what care this pet needs
        care_needs = pet.get_care_needs()
        st.text(f"  • {pet.name} ({pet.species}, age {pet.age})")
        if care_needs:
            st.caption(f"    Care needs: {', '.join(care_needs)}")

st.divider()

st.subheader("Add Tasks")

if st.session_state.pets:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=30)
    with col3:
        priority = st.slider("Priority (1-5)", 1, 5, 3)
    with col4:
        selected_pet = st.selectbox("Pet", [p.name for p in st.session_state.pets])

    if st.button("Add Task"):
        pet_obj = next(p for p in st.session_state.pets if p.name == selected_pet)
        task = CareTask(
            task_id=f"T{len(st.session_state.tasks) + 1:03d}",
            pet_id=pet_obj.pet_id,
            title=task_title,
            category="general",
            duration_minutes=int(duration),
            priority=priority,
            due_time=None
        )
        
        # Append the task to session state (triggers Streamlit rerun, UI updates automatically)
        st.session_state.tasks.append(task)
        st.success(f"Task '{task_title}' added to {pet_obj.name}!")

    if st.session_state.tasks:
        st.write(f"**Tasks ({len(st.session_state.tasks)}):**")
        for task in st.session_state.tasks:
            # Get the pet name for display
            pet = next((p for p in st.session_state.pets if p.pet_id == task.pet_id), None)
            status = "✓ Done" if task.is_completed else "○ Pending"
            st.text(f"  • [{status}] {task.title} ({task.duration_minutes}min, priority {task.priority}) - {pet.name if pet else 'Unknown'}")
            
            # Add checkbox to mark task complete (calls CareTask.mark_complete())
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.checkbox("Done", value=task.is_completed, key=f"task_{task.task_id}"):
                    task.mark_complete()
else:
    st.info("Add a pet first to add tasks.")

st.divider()

st.subheader("View & Analyze Tasks")

if st.session_state.tasks:
    # Create a Scheduler instance for smart analysis
    scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📅 All Tasks", "⚠️ Conflict Check", "🔄 30-Day Expansion", "📊 Analytics"])
    
    with tab1:
        st.markdown("### Tasks Sorted by Time (Earliest First)")
        
        # Sort tasks chronologically using Scheduler.sort_by_time()
        sorted_tasks = scheduler.sort_by_time(st.session_state.tasks)
        
        if sorted_tasks:
            # Create a table for professional display
            task_data = []
            for task in sorted_tasks:
                pet = next((p for p in st.session_state.pets if p.pet_id == task.pet_id), None)
                due_time_str = task.due_time.strftime('%I:%M %p') if task.due_time else "No time set"
                
                # Calculate urgency score if task has a due time
                urgency = None
                if task.due_time:
                    urgency = task.get_urgency_score(time(12, 0))  # Score relative to noon
                
                task_data.append({
                    "Task": task.title,
                    "Pet": pet.name if pet else "Unknown",
                    "Duration (min)": task.duration_minutes,
                    "Priority": f"{'⭐' * task.priority}",
                    "Due Time": due_time_str,
                    "Status": "✓ Done" if task.is_completed else "○ Pending",
                    "Urgency Score": f"{urgency:.1f}" if urgency else "—"
                })
            
            df = pd.DataFrame(task_data)
            st.dataframe(df, use_container_width=True)
            st.success(f"✓ {len(sorted_tasks)} task(s) sorted by time")
        
        # Filter by pet
        st.markdown("#### Filter by Pet")
        pet_options = {p.name: p.pet_id for p in st.session_state.pets}
        selected_pet_name = st.selectbox("Show tasks for:", ["All Pets"] + list(pet_options.keys()))
        
        if selected_pet_name != "All Pets":
            pet_id = pet_options[selected_pet_name]
            filtered_tasks = scheduler.filter_by_pet(st.session_state.tasks, pet_id)
            st.write(f"**{len(filtered_tasks)} task(s) for {selected_pet_name}:**")
            for task in filtered_tasks:
                status = "✓ Done" if task.is_completed else "○ Pending"
                st.write(f"  • [{status}] {task.title} ({task.duration_minutes}min, priority {task.priority})")
    
    with tab2:
        st.markdown("### 🔍 Conflict Detection")
        st.caption("Detects when multiple tasks are scheduled for the same time (blocking the owner from doing both).")
        
        # Detect conflicts using Scheduler.detect_conflicts()
        conflicts = scheduler.detect_conflicts(st.session_state.tasks)
        
        if conflicts:
            st.warning("⚠️ **Scheduling Conflicts Detected!**")
            st.markdown(f"**{len(conflicts)} conflict(s) found:**\n")
            
            for i, (task1, task2, warning_msg) in enumerate(conflicts, 1):
                with st.container():
                    col1, col2, col3 = st.columns([1, 4, 2])
                    with col1:
                        st.error(f"⚠️ #{i}")
                    with col2:
                        st.write(warning_msg)
                    with col3:
                        if st.button("📋 View conflicting tasks", key=f"conflict_{i}"):
                            st.info(f"**{task1.title}** for {task1.pet_id}\n—\n**{task2.title}** for {task2.pet_id}")
            
            st.markdown("**✅ Recommendations:**")
            st.markdown("- Adjust task times to avoid overlaps")
            st.markdown("- Consider batching quick tasks (feeding, water)")
            st.markdown("- Delegate one task to another caregiver if available")
        else:
            st.success("✓ No scheduling conflicts detected! Tasks are spread out appropriately.")
    
    with tab3:
        st.markdown("### 📅 30-Day Schedule Expansion")
        st.caption("Shows how recurring tasks expand across a month.")
        
        # Get recurring tasks
        recurring_tasks = scheduler.get_recurring_tasks(st.session_state.tasks)
        
        if recurring_tasks:
            st.write(f"**Recurring Tasks ({len(recurring_tasks)}):**")
            
            # Show current recurring tasks
            for task in recurring_tasks:
                pet = next((p for p in st.session_state.pets if p.pet_id == task.pet_id), None)
                st.write(f"  • {task.title} ({task.recurrence_pattern.upper()}) - {pet.name if pet else 'Unknown'}")
            
            # Expand and show statistics
            expanded = scheduler.expand_recurring_tasks(recurring_tasks, days=30)
            
            if expanded:
                st.success(f"✓ Expanded to {len(expanded)} task instances over 30 days")
                
                # Group by recurrence type for summary
                daily_count = len([t for t in expanded if t.recurrence_pattern == "daily"])
                weekly_count = len([t for t in expanded if t.recurrence_pattern == "weekly"])
                monthly_count = len([t for t in expanded if t.recurrence_pattern == "monthly"])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Daily Instances", daily_count)
                with col2:
                    st.metric("Weekly Instances", weekly_count)
                with col3:
                    st.metric("Monthly Instances", monthly_count)
                
                # Show expanded schedule timeline
                st.markdown("#### Sample Expansion (First 15 days)")
                expansion_data = []
                for task in expanded[:15]:
                    pet = next((p for p in st.session_state.pets if p.pet_id == task.pet_id), None)
                    expansion_data.append({
                        "Date": task.original_due_date.strftime('%a, %b %d'),
                        "Task": task.title,
                        "Pet": pet.name if pet else "Unknown",
                        "Recurrence": task.recurrence_pattern.upper(),
                        "Time": task.due_time.strftime('%I:%M %p') if task.due_time else "—"
                    })
                
                df_expanded = pd.DataFrame(expansion_data)
                st.dataframe(df_expanded, use_container_width=True)
        else:
            st.info("No recurring tasks yet. Add tasks with recurrence patterns (daily, weekly, monthly) to see expansion.")
    
    with tab4:
        st.markdown("### 📊 Task Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_tasks = len(st.session_state.tasks)
            st.metric("Total Tasks", total_tasks)
        
        with col2:
            completed = len(scheduler.filter_by_completion(st.session_state.tasks, completed=True))
            st.metric("Completed", completed)
        
        with col3:
            pending = len(scheduler.filter_by_completion(st.session_state.tasks, completed=False))
            st.metric("Pending", pending)
        
        with col4:
            recurring = len(scheduler.get_recurring_tasks(st.session_state.tasks))
            st.metric("Recurring", recurring)
        
        # Time summary
        st.markdown("#### Time Summary")
        total_duration = sum(t.duration_minutes for t in st.session_state.tasks if not t.is_completed)
        owner_available = st.session_state.owner.daily_time_available if st.session_state.owner else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Time Needed (pending)", f"{total_duration} min")
        with col2:
            st.metric("Owner Available", f"{owner_available} min")
        
        if owner_available > 0 and total_duration > 0:
            utilization = (total_duration / owner_available) * 100
            st.progress(min(utilization / 100, 1.0))
            st.caption(f"{utilization:.1f}% of available time used")
            
            if utilization > 100:
                st.warning(f"⚠️ Pending tasks ({total_duration} min) exceed available time ({owner_available} min)!")
            elif utilization > 80:
                st.info(f"⚡ Schedule is quite full ({utilization:.0f}% utilized)")
            else:
                st.success(f"✓ Comfortable schedule with {owner_available - total_duration} min buffer")

else:
    st.info("📝 Add tasks in the section above to view and analyze them here.")

st.divider()

st.subheader("Build Daily Schedule")
st.caption("Creates an optimized daily plan using sorted and conflict-checked tasks.")

if st.button("Generate Optimized Schedule"):
    if st.session_state.owner and st.session_state.tasks:
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        # Create a DailyPlan for today
        plan = DailyPlan(date=date.today())
        
        # Sort tasks by time first
        sorted_tasks = scheduler.sort_by_time(st.session_state.tasks)
        
        # Get conflicts
        conflicts = scheduler.detect_conflicts(sorted_tasks)
        
        # Check for time issues
        st.success("✓ Schedule generated!")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**Daily Plan for {plan.date.strftime('%A, %B %d, %Y')}**")
            st.info(f"👤 {st.session_state.owner.name} | ⏱️ Available: {st.session_state.owner.daily_time_available} min/day")
        
        with col2:
            if conflicts:
                st.warning(f"⚠️ {len(conflicts)} Conflict(s)")
            else:
                st.success("✓ No Conflicts")
        
        # Display sorted schedule as timeline
        st.markdown("#### 📅 Timeline View")
        
        schedule_data = []
        start_hour = 7
        for task in sorted_tasks:
            pet = next((p for p in st.session_state.pets if p.pet_id == task.pet_id), None)
            task_start_time = time(start_hour, 0)
            task_end_minutes = start_hour * 60 + task.duration_minutes
            task_end_hour = task_end_minutes // 60
            task_end_min = task_end_minutes % 60
            task_end_time = time(task_end_hour % 24, task_end_min)  # Handle overflow
            
            plan.add_item(task, task_start_time)
            
            schedule_data.append({
                "Time": f"{task_start_time.strftime('%I:%M %p')} - {task_end_time.strftime('%I:%M %p')}",
                "Task": task.title,
                "Pet": pet.name if pet else "Unknown",
                "Duration": f"{task.duration_minutes} min",
                "Priority": f"{'⭐' * task.priority}",
                "Status": "✓ Done" if task.is_completed else "○ Pending"
            })
            
            start_hour = task_end_hour + 1
        
        df_schedule = pd.DataFrame(schedule_data)
        st.dataframe(df_schedule, use_container_width=True)
        
        # Show conflict warnings if any
        if conflicts:
            st.markdown("#### ⚠️ Scheduling Conflicts")
            with st.expander("View conflict details", expanded=True):
                for task1, task2, warning_msg in conflicts:
                    st.warning(warning_msg)
        
        st.success("✓ Schedule is ready for the day!")
    else:
        st.error("Please create an Owner and at least one Task first.")
