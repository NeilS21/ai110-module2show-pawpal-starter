import streamlit as st
from pawal_system import Owner, Pet, CareTask, Scheduler, DailyPlan
from datetime import time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

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

st.subheader("Build Schedule")
st.caption("This creates a DailyPlan and adds tasks to it using DailyPlan.add_item().")

if st.button("Generate schedule"):
    if st.session_state.owner and st.session_state.tasks:
        from datetime import date
        
        # Create a DailyPlan for today using DailyPlan.__init__()
        plan = DailyPlan(date=date.today())
        
        # Add tasks to the plan using DailyPlan.add_item()
        start_hour = 7  # Start scheduling at 7 AM
        for i, task in enumerate(st.session_state.tasks):
            task_start_time = time(start_hour + i, 0)  # Each task starts 1 hour apart
            plan.add_item(task, task_start_time)  # Call the class method to add item
            start_hour += (task.duration_minutes // 60) + 1
        
        # Display the generated plan
        st.success("✓ Schedule generated!")
        st.write(f"**Daily Plan for {plan.date}**")
        st.info(f"Owner: {st.session_state.owner.name} | Total time available: {st.session_state.owner.daily_time_available} min")
        
        for task_id, start_time in sorted(plan.scheduled_items.items(), key=lambda x: x[1]):
            task = next((t for t in st.session_state.tasks if t.task_id == task_id), None)
            if task:
                end_minutes = start_time.hour * 60 + start_time.minute + task.duration_minutes
                end_hour = end_minutes // 60
                end_min = end_minutes % 60
                end_time = time(end_hour, end_min)
                st.text(f"  {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')} | {task.title}")
        
        # Show plan explanation if implemented
        explanation = plan.explain_plan()
        if explanation:
            st.markdown("**Plan Explanation:**")
            st.write(explanation)
    else:
        st.error("Please create an Owner and at least one Task first.")
