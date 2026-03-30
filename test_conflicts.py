"""
Step 4: Conflict Detection Demo
Simple test of task conflict detection functionality.
"""
from datetime import date, time
from pawal_system import Owner, Pet, CareTask, Scheduler


def main():
    print("="*70)
    print("STEP 4: TASK CONFLICT DETECTION")
    print("="*70)
    
    # Create Owner and Pets
    owner = Owner(
        owner_id="O001",
        name="Alice",
        daily_time_available=180,
        preferences="flexible",
        max_tasks_per_day=5
    )
    
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
    
    print("\nOwner: {} | Available time: {} min/day".format(owner.name, owner.daily_time_available))
    print("Pets: {} (Dog), {} (Cat)\n".format(dog.name, cat.name))
    
    # Create Scheduler
    scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
    
    # SCENARIO 1: No conflicts
    print("-" * 70)
    print("SCENARIO 1: Tasks with NO conflicts")
    print("-" * 70)
    
    task1 = CareTask(
        task_id="T001",
        pet_id="P001",
        title="Morning Walk",
        category="exercise",
        duration_minutes=30,
        priority=3,
        due_time=time(7, 0),  # 7:00 AM
        is_completed=False,
        recurrence_pattern="once"
    )
    
    task2 = CareTask(
        task_id="T002",
        pet_id="P002",
        title="Cat Feeding",
        category="feeding",
        duration_minutes=10,
        priority=1,
        due_time=time(8, 0),  # 8:00 AM (different time)
        is_completed=False,
        recurrence_pattern="once"
    )
    
    tasks_no_conflict = [task1, task2]
    
    print("\nScheduled tasks:")
    for task in tasks_no_conflict:
        print("  - {} at {} (Pet: {})".format(
            task.title, 
            task.due_time.strftime('%I:%M %p'), 
            task.pet_id
        ))
    
    conflicts = scheduler.detect_conflicts(tasks_no_conflict)
    if conflicts:
        print("\n[!] Conflicts found:")
        for task_a, task_b, warning in conflicts:
            print("  " + warning)
    else:
        print("\n[OK] No conflicts detected\n")
    
    # SCENARIO 2: Conflict - two tasks at same time
    print("-" * 70)
    print("SCENARIO 2: Tasks WITH conflicts (same time)")
    print("-" * 70)
    
    task3 = CareTask(
        task_id="T003",
        pet_id="P001",
        title="Evening Play",
        category="enrichment",
        duration_minutes=20,
        priority=2,
        due_time=time(18, 0),  # 6:00 PM
        is_completed=False,
        recurrence_pattern="once"
    )
    
    task4 = CareTask(
        task_id="T004",
        pet_id="P002",
        title="Cat Feeding",
        category="feeding",
        duration_minutes=10,
        priority=1,
        due_time=time(18, 0),  # 6:00 PM - SAME TIME!
        is_completed=False,
        recurrence_pattern="once"
    )
    
    tasks_with_conflict = [task3, task4]
    
    print("\nScheduled tasks:")
    for task in tasks_with_conflict:
        print("  - {} at {} (Pet: {})".format(
            task.title,
            task.due_time.strftime('%I:%M %p'),
            task.pet_id
        ))
    
    conflicts = scheduler.detect_conflicts(tasks_with_conflict)
    if conflicts:
        print("\n[WARNING] {} conflict(s) detected:\n".format(len(conflicts)))
        for task_a, task_b, warning in conflicts:
            print("  " + warning)
    else:
        print("\n[OK] No conflicts detected\n")
    
    # SCENARIO 3: Multiple conflicts
    print("-" * 70)
    print("SCENARIO 3: Multiple task conflicts")
    print("-" * 70)
    
    task5 = CareTask(
        task_id="T005",
        pet_id="P001",
        title="Grooming",
        category="hygiene",
        duration_minutes=30,
        priority=2,
        due_time=time(14, 0),  # 2:00 PM
        is_completed=False,
        recurrence_pattern="once"
    )
    
    task6 = CareTask(
        task_id="T006",
        pet_id="P002",
        title="Grooming",
        category="hygiene",
        duration_minutes=20,
        priority=2,
        due_time=time(14, 0),  # 2:00 PM - SAME!
        is_completed=False,
        recurrence_pattern="once"
    )
    
    task7 = CareTask(
        task_id="T007",
        pet_id="P001",
        title="Vet Visit",
        category="medical",
        duration_minutes=60,
        priority=5,
        due_time=time(10, 0),  # 10:00 AM
        is_completed=False,
        recurrence_pattern="once"
    )
    
    task8 = CareTask(
        task_id="T008",
        pet_id="P002",
        title="Vet Checkup",
        category="medical",
        duration_minutes=30,
        priority=4,
        due_time=time(10, 0),  # 10:00 AM - SAME!
        is_completed=False,
        recurrence_pattern="once"
    )
    
    tasks_multiple_conflicts = [task5, task6, task7, task8]
    
    print("\nScheduled tasks:")
    for task in tasks_multiple_conflicts:
        print("  - {} at {} (Pet: {})".format(
            task.title,
            task.due_time.strftime('%I:%M %p'),
            task.pet_id
        ))
    
    conflicts = scheduler.detect_conflicts(tasks_multiple_conflicts)
    if conflicts:
        print("\n[WARNING] {} conflict(s) detected:\n".format(len(conflicts)))
        for task_a, task_b, warning in conflicts:
            print("  " + warning)
    else:
        print("\n[OK] No conflicts detected\n")
    
    # Summary
    print("="*70)
    print("CONFLICT DETECTION SUMMARY")
    print("="*70)
    print("\nThe detect_conflicts() method:")
    print("  - Compares all tasks with due_time")
    print("  - Identifies tasks scheduled at the same time")
    print("  - Returns warning messages (doesn't crash)")
    print("  - Works across pets (detects any time overlap)")
    print("\nUsage:")
    print("  conflicts = scheduler.detect_conflicts(task_list)")
    print("  if conflicts:")
    print("      for task1, task2, warning in conflicts:")
    print("          print(warning)")
    print()


if __name__ == "__main__":
    main()
