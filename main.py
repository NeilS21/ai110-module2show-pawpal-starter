"""
Main script: Demo of PawPal+ system with sample Owner, Pets, and Tasks.
"""
from datetime import date, time
from pawal_system import Owner, Pet, CareTask, DailyPlan


def main():
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

    # Create Tasks
    task1 = CareTask(
        task_id="T001",
        pet_id="P001",
        title="Morning Walk",
        category="exercise",
        duration_minutes=30,
        priority=3,
        due_time=time(7, 0),
        is_completed=False
    )
    
    task2 = CareTask(
        task_id="T002",
        pet_id="P001",
        title="Feeding",
        category="feeding",
        duration_minutes=10,
        priority=1,
        due_time=time(8, 0),
        is_completed=False
    )
    
    task3 = CareTask(
        task_id="T003",
        pet_id="P002",
        title="Litter Box Cleaning",
        category="hygiene",
        duration_minutes=15,
        priority=2,
        due_time=time(9, 0),
        is_completed=False
    )
    
    task4 = CareTask(
        task_id="T004",
        pet_id="P002",
        title="Feeding",
        category="feeding",
        duration_minutes=10,
        priority=1,
        due_time=time(18, 0),
        is_completed=False
    )
    
    task5 = CareTask(
        task_id="T005",
        pet_id="P001",
        title="Evening Walk",
        category="exercise",
        duration_minutes=30,
        priority=3,
        due_time=time(18, 30),
        is_completed=False
    )

    tasks = [task1, task2, task3, task4, task5]
    print(f"Tasks Created ({len(tasks)} total):")
    for task in tasks:
        print(f"  - [{task.task_id}] {task.title} ({task.category})")
        print(f"    Pet: {task.pet_id}, Duration: {task.duration_minutes}min, Priority: {task.priority}, Due: {task.due_time}\n")

    # Build a sample daily plan
    plan = DailyPlan(
        date=date.today(),
        total_minutes_used=0,
        scheduled_items={},
        unscheduled_tasks=[]
    )

    # Manually schedule tasks
    plan.add_item(task1, time(7, 0))    # Morning walk at 7:00 AM
    plan.add_item(task2, time(8, 0))    # Dog feeding at 8:00 AM
    plan.add_item(task3, time(9, 0))    # Litter box at 9:00 AM
    plan.add_item(task4, time(18, 0))   # Cat feeding at 6:00 PM
    plan.add_item(task5, time(18, 30))  # Evening walk at 6:30 PM

    plan.total_minutes_used = sum(t.duration_minutes for t in tasks)

    # Display the daily schedule
    print("\n" + "="*60)
    print(f"TODAY'S SCHEDULE - {plan.date}")
    print("="*60)
    print(f"\nScheduled Tasks ({len(plan.scheduled_items)} items):\n")
    
    for task_id, start_time in sorted(plan.scheduled_items.items(), key=lambda x: x[1]):
        # Find the task object
        task = next(t for t in tasks if t.task_id == task_id)
        end_minutes = start_time.hour * 60 + start_time.minute + task.duration_minutes
        end_hour = end_minutes // 60
        end_min = end_minutes % 60
        end_time = time(end_hour, end_min)
        
        print(f"  {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')} | {task.title}")
        print(f"    Pet: {task.pet_id} | Duration: {task.duration_minutes}min | Priority: {task.priority}")
        print()
    
    print(f"Total time allocated: {plan.total_minutes_used} minutes")
    print(f"Daily time available: {owner.daily_time_available} minutes")
    print(f"Remaining time: {owner.daily_time_available - plan.total_minutes_used} minutes")
    print("="*60)


if __name__ == "__main__":
    main()
