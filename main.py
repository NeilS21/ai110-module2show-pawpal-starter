"""
Main script: Demo of PawPal+ system with recurring task automation.
Demonstrates sorting, filtering, and automatic recurring task generation using timedelta.
"""
from datetime import date, time, timedelta
from pawal_system import Owner, Pet, CareTask, DailyPlan, Scheduler


def main():
    """Demonstrate PawPal+ system features across 8 demos.
    
    Showcases: task creation, recurring automation, sorting, filtering,
    30-day expansion planning, and conflict detection algorithm.
    """
    # Create an Owner
    owner = Owner(
        owner_id="O001",
        name="Alice",
        daily_time_available=180,  # 3 hours per day
        preferences="morning and evening",
        max_tasks_per_day=5
    )
    print(f"Owner: {owner.name} (ID: {owner.owner_id})")
    print(f"  Available time: {owner.daily_time_available} minutes/day")
    print(f"  Preferences: {owner.preferences}\n")

    # Create Pets
    dog = Pet(
        pet_id="P001",
        name="Max",
        species="Dog",
        age=3,
        energy_level="high",
        medical_notes="None"
    )
    
    cat = Pet(
        pet_id="P002",
        name="Whiskers",
        species="Cat",
        age=5,
        energy_level="medium",
        medical_notes="Sensitive stomach"
    )
    
    print(f"Pets:")
    print(f"  1. {dog.name} ({dog.species}, age {dog.age}) - Energy: {dog.energy_level}")
    print(f"  2. {cat.name} ({cat.species}, age {cat.age}) - Energy: {cat.energy_level}\n")

    # Create Recurring Tasks
    print("Creating recurring and one-time tasks:\n")
    
    # DAILY TASKS
    morning_walk = CareTask(
        task_id="T001",
        pet_id="P001",
        title="Morning Walk",
        category="exercise",
        duration_minutes=30,
        priority=3,
        due_time=time(7, 0),
        is_completed=False,
        recurrence_pattern="daily",
        original_due_date=date.today()
    )
    
    feeding_dog = CareTask(
        task_id="T002",
        pet_id="P001",
        title="Dog Feeding",
        category="feeding",
        duration_minutes=10,
        priority=1,
        due_time=time(8, 0),
        is_completed=False,
        recurrence_pattern="daily",
        original_due_date=date.today()
    )
    
    feeding_cat = CareTask(
        task_id="T003",
        pet_id="P002",
        title="Cat Feeding",
        category="feeding",
        duration_minutes=10,
        priority=1,
        due_time=time(18, 0),
        is_completed=False,
        recurrence_pattern="daily",
        original_due_date=date.today()
    )
    
    # WEEKLY TASKS
    bath = CareTask(
        task_id="T004",
        pet_id="P001",
        title="Bath Time",
        category="hygiene",
        duration_minutes=45,
        priority=2,
        due_time=time(14, 0),
        is_completed=False,
        recurrence_pattern="weekly",
        original_due_date=date.today()
    )
    
    nail_trim = CareTask(
        task_id="T005",
        pet_id="P002",
        title="Nail Trimming",
        category="hygiene",
        duration_minutes=20,
        priority=2,
        due_time=time(15, 0),
        is_completed=False,
        recurrence_pattern="weekly",
        original_due_date=date.today()
    )
    
    # ONE-TIME TASKS
    vet_visit = CareTask(
        task_id="T006",
        pet_id="P001",
        title="Vet Visit",
        category="medical",
        duration_minutes=60,
        priority=5,
        due_time=time(10, 0),
        is_completed=False,
        recurrence_pattern="once",
        original_due_date=date.today()
    )

    tasks = [morning_walk, feeding_dog, feeding_cat, bath, nail_trim, vet_visit]
    
    print(f"[OK] Created {len(tasks)} tasks\n")
    for task in tasks:
        recurrence = f"[{task.recurrence_pattern.upper()}]" if task.recurrence_pattern != "once" else "[ONE-TIME]"
        print(f"  {recurrence:12} {task.title:<25} | {task.pet_id} | {task.due_time}")

    # Create Scheduler
    scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")

    print("\n" + "="*80)
    print("DEMONSTRATION: RECURRING TASK AUTOMATION")
    print("="*80)

    # DEMO 1: Complete a daily task and show next occurrence
    print("\n📋 DEMO 1: Complete a Daily Task → Auto-generate Next Occurrence")
    print("-" * 80)
    
    print(f"\nOriginal task: {morning_walk.title}")
    print(f"  Task ID: {morning_walk.task_id}")
    print(f"  Recurrence: {morning_walk.recurrence_pattern}")
    print(f"  Due time: {morning_walk.due_time}")
    print(f"  Status: {'✓ COMPLETED' if morning_walk.is_completed else '⏳ PENDING'}\n")
    
    # Mark task as complete TODAY
    print(f"Marking '{morning_walk.title}' as complete on {date.today()}...\n")
    next_task = morning_walk.mark_complete(date.today())
    
    print(f"Updated task: {morning_walk.title}")
    print(f"  Status: {'✓ COMPLETED' if morning_walk.is_completed else '⏳ PENDING'}")
    print(f"  Last completed: {morning_walk.last_completed_date}\n")
    
    if next_task:
        next_due = date.today() + timedelta(days=1)
        print(f"✨ NEW TASK GENERATED for next occurrence:")
        print(f"  Task ID: {next_task.task_id}")
        print(f"  Title: {next_task.title}")
        print(f"  Due date: {next_due}")
        print(f"  Due time: {next_task.due_time}")
        print(f"  Status: {'✓ COMPLETED' if next_task.is_completed else '⏳ PENDING'}")

    # DEMO 2: Complete a weekly task
    print("\n\n📋 DEMO 2: Complete a Weekly Task → Auto-generate Next Week's Task")
    print("-" * 80)
    
    print(f"\nOriginal task: {bath.title}")
    print(f"  Recurrence: {bath.recurrence_pattern}")
    print(f"  Due: {bath.due_time} on {date.today()}\n")
    
    print(f"Marking '{bath.title}' as complete on {date.today()}...\n")
    next_bath = bath.mark_complete(date.today())
    
    if next_bath:
        next_due = date.today() + timedelta(days=7)
        print(f"✨ NEW TASK GENERATED for next week:")
        print(f"  Due date: {next_due} (1 week later, using timedelta(days=7))")
        print(f"  Due time: {next_bath.due_time}")

    # DEMO 3: One-time task doesn't generate next occurrence
    print("\n\n📋 DEMO 3: One-Time Task → No auto-generation")
    print("-" * 80)
    
    print(f"\nOriginal task: {vet_visit.title}")
    print(f"  Recurrence: {vet_visit.recurrence_pattern}")
    
    print(f"Marking '{vet_visit.title}' as complete...\n")
    next_vet = vet_visit.mark_complete(date.today())
    
    print(f"✓ Task marked complete: {vet_visit.title}")
    print(f"  Status: {'✓ COMPLETED' if vet_visit.is_completed else '⏳ PENDING'}")
    if next_vet:
        print(f"  Next task: Generated")
    else:
        print(f"  ✨ No next task generated (one-time task)")

    # DEMO 4: Identify and filter recurring tasks
    print("\n\n📋 DEMO 4: Identify Recurring vs One-Time Tasks")
    print("-" * 80)
    
    recurring = scheduler.get_recurring_tasks(tasks)
    print(f"\nRecurring Tasks ({len(recurring)}):")
    for task in recurring:
        print(f"  {task.title:<25} | {task.recurrence_pattern.upper():<7} | {task.pet_id}")
    
    one_time = [t for t in tasks if t.recurrence_pattern == "once"]
    print(f"\nOne-Time Tasks ({len(one_time)}):")
    for task in one_time:
        print(f"  {task.title:<25} | ONE-TIME | {task.pet_id}")

    # DEMO 5: Expand recurring tasks over a month
    print("\n\n📋 DEMO 5: Expand Recurring Tasks Over 30 Days (using timedelta)")
    print("-" * 80)
    
    recurring_tasks = scheduler.get_recurring_tasks(tasks)
    expanded = scheduler.expand_recurring_tasks(recurring_tasks, days=30)
    
    print(f"\nExpanded {len(recurring_tasks)} recurring task templates into {len(expanded)} task instances over 30 days\n")
    
    # Count by type
    daily_count = len([t for t in expanded if t.recurrence_pattern == "daily"])
    weekly_count = len([t for t in expanded if t.recurrence_pattern == "weekly"])
    
    print(f"Daily task instances:  {daily_count} (30 days × {len([t for t in recurring if t.recurrence_pattern == 'daily'])} daily templates = ~90 tasks)")
    print(f"Weekly task instances: {weekly_count} (30 days ÷ 7 = ~{len([t for t in recurring if t.recurrence_pattern == 'weekly']) * 5} occurrences total)")
    
    # Show sample expanded schedule
    print(f"\nSample expanded tasks (first 10):")
    for task in expanded[:10]:
        print(f"  {task.original_due_date} | {task.title:<25} | {task.pet_id}")

    # DEMO 6: Build a 3-day sample schedule with recurring tasks
    print("\n\n" + "="*80)
    print("3-DAY RECURRING TASK SCHEDULE (Generated with timedelta)")
    print("="*80)
    
    for day_offset in range(3):
        current_date = date.today() + timedelta(days=day_offset)
        
        print(f"\n📅 {current_date.strftime('%A, %B %d, %Y')}")
        print("-" * 80)
        
        # Get daily and weekly tasks for this date
        day_tasks = []
        for task in recurring_tasks:
            if task.recurrence_pattern == "daily":
                day_tasks.append(task)
            elif task.recurrence_pattern == "weekly" and day_offset % 7 == 0:
                day_tasks.append(task)
        
        # Sort by time
        day_tasks = scheduler.sort_by_time(day_tasks)
        
        if day_tasks:
            total_time = sum(t.duration_minutes for t in day_tasks)
            print(f"  Total duration: {total_time} minutes\n")
            for task in day_tasks:
                print(f"  {task.due_time.strftime('%I:%M %p')} | {task.title:<25} | {task.duration_minutes:3}min | 🐾 {task.pet_id}")
        else:
            print("  No recurring tasks scheduled for this day")

    # DEMO 7: Show how timedelta works
    print("\n\n" + "="*80)
    print("HOW TIMEDELTA WORKS")
    print("="*80)
    
    today = date.today()
    print(f"\nToday: {today}")
    print(f"\nUsing timedelta() from datetime module:\n")
    print(f"  today + timedelta(days=1)   = {today + timedelta(days=1)}   (next day)")
    print(f"  today + timedelta(days=7)   = {today + timedelta(days=7)}   (next week)")
    print(f"  today + timedelta(days=30)  = {today + timedelta(days=30)}  (next month approx)")
    print(f"  today + timedelta(weeks=1)  = {today + timedelta(weeks=1)}  (same as days=7)")
    print(f"  today + timedelta(hours=24) = {today + timedelta(hours=24)}  (same as days=1)")
    
    print("\nThis is how recurring tasks calculate their next due date:")
    print("  • Daily tasks:   completed_date + timedelta(days=1)")
    print("  • Weekly tasks:  completed_date + timedelta(days=7)")
    print("  • Monthly tasks: completed_date + timedelta(days=30)")

    # DEMO 8: Conflict Detection
    print("\n\n" + "="*80)
    print("CONFLICT DETECTION - Lightweight Warning System")
    print("="*80)
    
    # Create two tasks at the same time (conflict)
    evening_play = CareTask(
        task_id="T007",
        pet_id="P001",
        title="Evening Play Session",
        category="enrichment",
        duration_minutes=20,
        priority=2,
        due_time=time(18, 0),  # SAME TIME as cat feeding!
        is_completed=False,
        recurrence_pattern="once"
    )
    
    print("\nCreated 2 tasks scheduled at the same time:\n")
    print(f"  Task 1: {feeding_cat.title} at {feeding_cat.due_time.strftime('%I:%M %p')} (Pet: {feeding_cat.pet_id})")
    print(f"  Task 2: {evening_play.title} at {evening_play.due_time.strftime('%I:%M %p')} (Pet: {evening_play.pet_id})\n")
    
    # Check for conflicts
    conflicting_tasks = tasks + [evening_play]  # Add the new conflict task
    conflicts = scheduler.detect_conflicts(conflicting_tasks)
    
    if conflicts:
        print(f"[!] Found {len(conflicts)} conflict(s):\n")
        for task1, task2, warning in conflicts:
            print(f"  {warning}")
    else:
        print("[OK] No conflicts detected")


if __name__ == "__main__":
    main()
