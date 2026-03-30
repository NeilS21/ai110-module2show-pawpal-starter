"""
Simple tests for PawPal+ system using pytest.
"""
import pytest
from datetime import date, time, timedelta
from pawal_system import CareTask, DailyPlan, Scheduler, Owner, Pet


class TestTaskCompletion:
    """Test task completion functionality."""
    
    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() changes is_completed from False to True."""
        # Create a task that starts as incomplete
        task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Morning Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            is_completed=False
        )
        
        # Task should initially be incomplete
        assert task.is_completed is False
        
        # Mark task as complete
        task.mark_complete()
        
        # Task should now be complete
        assert task.is_completed is True


class TestTaskAddition:
    """Test adding tasks to the daily plan."""
    
    def test_adding_task_increases_scheduled_count(self):
        """Verify that adding a task to a DailyPlan increases the scheduled task count."""
        # Create a daily plan
        plan = DailyPlan(date=date.today())
        
        # Plan should start empty
        assert len(plan.scheduled_items) == 0
        
        # Create and add a task
        task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Feeding",
            category="feeding",
            duration_minutes=10,
            priority=1,
            due_time=time(8, 0)
        )
        plan.add_item(task, time(8, 0))
        
        # Plan should now contain 1 scheduled task
        assert len(plan.scheduled_items) == 1
        
        # Add another task
        task2 = CareTask(
            task_id="T002",
            pet_id="P002",
            title="Litter Box",
            category="hygiene",
            duration_minutes=15,
            priority=2
        )
        plan.add_item(task2, time(9, 0))
        
        # Plan should now contain 2 scheduled tasks
        assert len(plan.scheduled_items) == 2


class TestSortingCorrectness:
    """Test task sorting by chronological order."""
    
    def test_sort_by_time_chronological_order(self):
        """Verify tasks are returned in chronological order (earliest to latest)."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        # Create tasks with different times (not in order)
        task1 = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Evening Walk",
            category="exercise",
            duration_minutes=30,
            priority=2,
            due_time=time(18, 0)  # 6:00 PM
        )
        
        task2 = CareTask(
            task_id="T002",
            pet_id="P001",
            title="Morning Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            due_time=time(7, 0)  # 7:00 AM
        )
        
        task3 = CareTask(
            task_id="T003",
            pet_id="P001",
            title="Lunch feeding",
            category="feeding",
            duration_minutes=10,
            priority=1,
            due_time=time(12, 0)  # 12:00 PM
        )
        
        # Create unsorted list
        unsorted_tasks = [task1, task2, task3]
        
        # Sort by time
        sorted_tasks = scheduler.sort_by_time(unsorted_tasks)
        
        # Verify order: 7:00 AM < 12:00 PM < 6:00 PM
        assert sorted_tasks[0].due_time == time(7, 0)
        assert sorted_tasks[1].due_time == time(12, 0)
        assert sorted_tasks[2].due_time == time(18, 0)
    
    def test_sort_by_time_tasks_without_due_time(self):
        """Verify tasks without due_time are placed at the end."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        # Create tasks with and without due times
        task_with_time = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Morning Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            due_time=time(7, 0)
        )
        
        task_without_time1 = CareTask(
            task_id="T002",
            pet_id="P001",
            title="Grooming",
            category="hygiene",
            duration_minutes=45,
            priority=2
            # No due_time
        )
        
        task_without_time2 = CareTask(
            task_id="T003",
            pet_id="P001",
            title="Playtime",
            category="exercise",
            duration_minutes=20,
            priority=1
            # No due_time
        )
        
        unsorted_tasks = [task_without_time1, task_with_time, task_without_time2]
        sorted_tasks = scheduler.sort_by_time(unsorted_tasks)
        
        # Task with time should be first
        assert sorted_tasks[0].due_time == time(7, 0)
        # Tasks without times should be at the end
        assert sorted_tasks[1].due_time is None
        assert sorted_tasks[2].due_time is None
    
    def test_sort_by_time_empty_list(self):
        """Verify sorting an empty task list returns empty list."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        sorted_tasks = scheduler.sort_by_time([])
        
        assert sorted_tasks == []
    
    def test_sort_by_time_boundary_times(self):
        """Verify boundary times (midnight, end of day) sort correctly."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        task_midnight = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Midnight task",
            category="feeding",
            duration_minutes=10,
            priority=1,
            due_time=time(0, 0)  # 12:00 AM
        )
        
        task_end_of_day = CareTask(
            task_id="T002",
            pet_id="P001",
            title="End of day task",
            category="feeding",
            duration_minutes=10,
            priority=1,
            due_time=time(23, 59)  # 11:59 PM
        )
        
        task_noon = CareTask(
            task_id="T003",
            pet_id="P001",
            title="Noon task",
            category="feeding",
            duration_minutes=10,
            priority=1,
            due_time=time(12, 0)  # 12:00 PM
        )
        
        unsorted_tasks = [task_end_of_day, task_midnight, task_noon]
        sorted_tasks = scheduler.sort_by_time(unsorted_tasks)
        
        # Verify order: midnight < noon < end of day
        assert sorted_tasks[0].due_time == time(0, 0)
        assert sorted_tasks[1].due_time == time(12, 0)
        assert sorted_tasks[2].due_time == time(23, 59)


class TestRecurrenceLogic:
    """Test recurring task generation and completion."""
    
    def test_daily_task_completion_generates_next_day(self):
        """Verify marking a daily task complete generates a task for the next day."""
        # Create a daily task
        daily_task = CareTask(
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
        
        # Mark as complete today
        next_task = daily_task.mark_complete(date.today())
        
        # Verify original task is marked complete
        assert daily_task.is_completed is True
        
        # Verify new task was generated
        assert next_task is not None
        assert next_task.is_completed is False
        
        # Verify new task is for tomorrow
        expected_next_date = date.today() + timedelta(days=1)
        assert next_task.original_due_date == expected_next_date
        
        # Verify other properties are preserved
        assert next_task.title == daily_task.title
        assert next_task.pet_id == daily_task.pet_id
        assert next_task.due_time == daily_task.due_time
        assert next_task.recurrence_pattern == "daily"
    
    def test_weekly_task_completion_generates_next_week(self):
        """Verify marking a weekly task complete generates a task for next week (7 days)."""
        weekly_task = CareTask(
            task_id="T002",
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
        
        # Mark as complete today
        next_task = weekly_task.mark_complete(date.today())
        
        # Verify original task is marked complete
        assert weekly_task.is_completed is True
        
        # Verify new task was generated
        assert next_task is not None
        
        # Verify new task is for 7 days from now
        expected_next_date = date.today() + timedelta(days=7)
        assert next_task.original_due_date == expected_next_date
        
        # Verify recurrence pattern is preserved
        assert next_task.recurrence_pattern == "weekly"
    
    def test_monthly_task_completion_generates_next_month(self):
        """Verify marking a monthly task complete generates a task ~30 days later."""
        monthly_task = CareTask(
            task_id="T003",
            pet_id="P001",
            title="Vet Checkup",
            category="medical",
            duration_minutes=60,
            priority=5,
            is_completed=False,
            recurrence_pattern="monthly",
            original_due_date=date.today()
        )
        
        # Mark as complete today
        next_task = monthly_task.mark_complete(date.today())
        
        # Verify new task was generated
        assert next_task is not None
        
        # Verify new task is for ~30 days from now
        expected_next_date = date.today() + timedelta(days=30)
        assert next_task.original_due_date == expected_next_date
        
        # Verify recurrence pattern is preserved
        assert next_task.recurrence_pattern == "monthly"
    
    def test_one_time_task_no_next_occurrence(self):
        """Verify marking a one-time task complete does NOT generate a new task."""
        one_time_task = CareTask(
            task_id="T004",
            pet_id="P001",
            title="Vet Visit",
            category="medical",
            duration_minutes=60,
            priority=5,
            is_completed=False,
            recurrence_pattern="once",
            original_due_date=date.today()
        )
        
        # Mark as complete
        next_task = one_time_task.mark_complete(date.today())
        
        # Verify original task is marked complete
        assert one_time_task.is_completed is True
        
        # Verify NO new task was generated
        assert next_task is None
    
    def test_task_id_increments_for_recurring_tasks(self):
        """Verify task IDs increment correctly for generated recurring tasks."""
        daily_task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Morning Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            is_completed=False,
            recurrence_pattern="daily",
            original_due_date=date.today()
        )
        
        # Mark as complete and get next task
        next_task = daily_task.mark_complete(date.today())
        
        # Verify task ID incremented: T001 -> T001_1
        assert next_task.task_id == "T001_1"
        
        # Mark the next task as complete
        next_next_task = next_task.mark_complete(next_task.original_due_date)
        
        # Verify second increment: T001_1 -> T001_2
        assert next_next_task.task_id == "T001_2"
    
    def test_recurring_task_preserves_properties(self):
        """Verify generated recurring tasks preserve all relevant properties."""
        original_task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Dog Feeding",
            category="feeding",
            duration_minutes=15,
            priority=1,
            due_time=time(8, 0),
            is_completed=False,
            recurrence_pattern="daily",
            original_due_date=date.today()
        )
        
        # Mark as complete
        next_task = original_task.mark_complete(date.today())
        
        # Verify all properties are preserved
        assert next_task.title == original_task.title
        assert next_task.pet_id == original_task.pet_id
        assert next_task.category == original_task.category
        assert next_task.duration_minutes == original_task.duration_minutes
        assert next_task.priority == original_task.priority
        assert next_task.due_time == original_task.due_time
        assert next_task.is_completed is False  # New task is incomplete
        assert next_task.last_completed_date is None  # Not yet completed


class TestConflictDetection:
    """Test conflict detection for simultaneous tasks."""
    
    def test_detect_conflict_same_time_same_pet(self):
        """Verify conflict detection identifies two tasks at the same time."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        task1 = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Morning Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            due_time=time(8, 0)
        )
        
        task2 = CareTask(
            task_id="T002",
            pet_id="P001",
            title="Dog Feeding",
            category="feeding",
            duration_minutes=10,
            priority=1,
            due_time=time(8, 0)  # Same time!
        )
        
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Verify conflict was detected
        assert len(conflicts) == 1
        
        # Verify conflict pair
        task_a, task_b, warning = conflicts[0]
        assert task_a.task_id in ["T001", "T002"]
        assert task_b.task_id in ["T001", "T002"]
        assert task_a.task_id != task_b.task_id
        assert "CONFLICT" in warning
        assert "8:00 AM" in warning or "08:00" in warning
    
    def test_detect_multiple_conflicts(self):
        """Verify detection of multiple conflicts (3+ tasks at same time)."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        # Create 3 tasks all at 9:00 AM
        tasks = []
        for i in range(3):
            task = CareTask(
                task_id=f"T{i:03d}",
                pet_id="P001",
                title=f"Task {i}",
                category="activity",
                duration_minutes=10,
                priority=1,
                due_time=time(9, 0)  # All same time
            )
            tasks.append(task)
        
        conflicts = scheduler.detect_conflicts(tasks)
        
        # With 3 tasks at same time, we expect 3 pairs: (T000,T001), (T000,T002), (T001,T002)
        assert len(conflicts) == 3
    
    def test_no_conflict_different_times(self):
        """Verify no conflicts when tasks have different times."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        task1 = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Morning Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            due_time=time(7, 0)
        )
        
        task2 = CareTask(
            task_id="T002",
            pet_id="P001",
            title="Evening Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            due_time=time(18, 0)  # Different time
        )
        
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # No conflicts should be detected
        assert len(conflicts) == 0
    
    def test_no_conflict_when_no_due_time(self):
        """Verify no conflicts when tasks have no due_time."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        task1 = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Grooming",
            category="hygiene",
            duration_minutes=45,
            priority=2
            # No due_time
        )
        
        task2 = CareTask(
            task_id="T002",
            pet_id="P001",
            title="Playtime",
            category="exercise",
            duration_minutes=30,
            priority=1
            # No due_time
        )
        
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # No conflicts should be detected (tasks without times are excluded)
        assert len(conflicts) == 0
    
    def test_conflict_different_pets_same_time(self):
        """Verify conflicts are detected even when tasks are for different pets."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        task_dog = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Dog Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            due_time=time(10, 0)
        )
        
        task_cat = CareTask(
            task_id="T002",
            pet_id="P002",
            title="Cat Feeding",
            category="feeding",
            duration_minutes=10,
            priority=1,
            due_time=time(10, 0)  # Same time, different pet
        )
        
        conflicts = scheduler.detect_conflicts([task_dog, task_cat])
        
        # Conflict should still be detected (owner can't do both simultaneously)
        assert len(conflicts) == 1
        assert "P001" in conflicts[0][2]
        assert "P002" in conflicts[0][2]
    
    def test_detect_conflict_empty_list(self):
        """Verify empty task list returns no conflicts."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        conflicts = scheduler.detect_conflicts([])
        
        assert len(conflicts) == 0


class TestFilteringFunctionality:
    """Test filtering tasks by various criteria."""
    
    def test_filter_by_completion_incomplete_tasks(self):
        """Verify filtering returns only incomplete tasks."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        incomplete_task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            is_completed=False
        )
        
        complete_task = CareTask(
            task_id="T002",
            pet_id="P001",
            title="Feeding",
            category="feeding",
            duration_minutes=10,
            priority=1,
            is_completed=True
        )
        
        tasks = [incomplete_task, complete_task]
        filtered = scheduler.filter_by_completion(tasks, completed=False)
        
        # Should only return incomplete task
        assert len(filtered) == 1
        assert filtered[0].task_id == "T001"
    
    def test_filter_by_pet_id(self):
        """Verify filtering returns only tasks for specified pet."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        dog_task1 = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Walk",
            category="exercise",
            duration_minutes=30,
            priority=3
        )
        
        dog_task2 = CareTask(
            task_id="T002",
            pet_id="P001",
            title="Feeding",
            category="feeding",
            duration_minutes=10,
            priority=1
        )
        
        cat_task = CareTask(
            task_id="T003",
            pet_id="P002",
            title="Litter Box",
            category="hygiene",
            duration_minutes=15,
            priority=2
        )
        
        tasks = [dog_task1, dog_task2, cat_task]
        filtered = scheduler.filter_by_pet(tasks, "P001")
        
        # Should only return dog tasks
        assert len(filtered) == 2
        assert all(task.pet_id == "P001" for task in filtered)
    
    def test_filter_by_pet_no_matching_tasks(self):
        """Verify filtering returns empty list when pet has no tasks."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Walk",
            category="exercise",
            duration_minutes=30,
            priority=3
        )
        
        filtered = scheduler.filter_by_pet([task], "P999")  # Non-existent pet
        
        assert len(filtered) == 0


class TestRecurringTaskExpansion:
    """Test expanding recurring tasks over multiple days."""
    
    def test_expand_daily_tasks_30_days(self):
        """Verify daily task expands to 30 instances over 30 days."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        daily_task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Morning Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            due_time=time(7, 0),
            recurrence_pattern="daily",
            original_due_date=date.today()
        )
        
        expanded = scheduler.expand_recurring_tasks([daily_task], days=30)
        
        # Daily task should have 30 instances
        assert len(expanded) == 30
        
        # Verify all instances are for this task
        assert all(task.title == "Morning Walk" for task in expanded)
        assert all(task.task_id.startswith("T001") for task in expanded)
    
    def test_expand_weekly_tasks_30_days(self):
        """Verify weekly task expands to ~4-5 instances over 30 days."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        weekly_task = CareTask(
            task_id="T002",
            pet_id="P001",
            title="Bath Time",
            category="hygiene",
            duration_minutes=45,
            priority=2,
            recurrence_pattern="weekly",
            original_due_date=date.today()
        )
        
        expanded = scheduler.expand_recurring_tasks([weekly_task], days=30)
        
        # Weekly task should appear at days 0, 7, 14, 21, 28 = 5 times
        assert len(expanded) == 5
    
    def test_expand_monthly_tasks_30_days(self):
        """Verify monthly task expands correctly over 30 days."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        monthly_task = CareTask(
            task_id="T003",
            pet_id="P001",
            title="Vet Checkup",
            category="medical",
            duration_minutes=60,
            priority=5,
            recurrence_pattern="monthly",
            original_due_date=date.today()
        )
        
        # Over 30 days, only day offset 0 matches (range goes 0-29)
        expanded = scheduler.expand_recurring_tasks([monthly_task], days=30)
        assert len(expanded) == 1
        
        # Over 31 days, day offsets 0 and 30 both match
        expanded_31 = scheduler.expand_recurring_tasks([monthly_task], days=31)
        assert len(expanded_31) == 2
    
    def test_expand_multiple_recurring_tasks(self):
        """Verify expansion works with multiple recurring task templates."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        daily_walk = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Morning Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            recurrence_pattern="daily",
            original_due_date=date.today()
        )
        
        weekly_bath = CareTask(
            task_id="T002",
            pet_id="P001",
            title="Bath Time",
            category="hygiene",
            duration_minutes=45,
            priority=2,
            recurrence_pattern="weekly",
            original_due_date=date.today()
        )
        
        expanded = scheduler.expand_recurring_tasks([daily_walk, weekly_bath], days=30)
        
        # Should have 30 daily + 5 weekly = 35 total instances
        assert len(expanded) == 35
    
    def test_expand_empty_recurring_list(self):
        """Verify expanding empty recurring list returns empty list."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        expanded = scheduler.expand_recurring_tasks([], days=30)
        
        assert expanded == []


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_task_with_no_due_time_in_urgency_scoring(self):
        """Verify task without due_time receives base priority score only."""
        task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Grooming",
            category="hygiene",
            duration_minutes=45,
            priority=3
            # No due_time
        )
        
        urgency = task.get_urgency_score(time(12, 0))
        
        # Should be base priority only (3.0)
        assert urgency == 3.0
    
    def test_overdue_task_urgency_score(self):
        """Verify overdue task receives highest urgency bonus."""
        task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Feeding",
            category="feeding",
            duration_minutes=10,
            priority=2,
            due_time=time(8, 0)  # Due 8:00 AM
        )
        
        # Check at 10:00 AM (2 hours late)
        urgency = task.get_urgency_score(time(10, 0))
        
        # Should be priority (2.0) + overdue bonus (10) = 12.0
        assert urgency == 12.0
    
    def test_task_due_within_30_minutes(self):
        """Verify task due within 30 minutes gets +5 bonus."""
        task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Feeding",
            category="feeding",
            duration_minutes=10,
            priority=1,
            due_time=time(9, 0)  # Due at 9:00 AM
        )
        
        # Check at 8:45 AM (15 minutes before)
        urgency = task.get_urgency_score(time(8, 45))
        
        # Should be priority (1.0) + 30min bonus (5) = 6.0
        assert urgency == 6.0
    
    def test_pet_with_no_tasks(self):
        """Verify filtering for pet with no tasks returns empty list."""
        scheduler = Scheduler(constraints={}, scoring_weights={}, strategy="priority")
        
        # Empty task list
        filtered = scheduler.filter_by_pet([], "P001")
        
        assert filtered == []
    
    def test_complete_task_preserves_last_completed_date(self):
        """Verify mark_complete sets last_completed_date correctly."""
        task = CareTask(
            task_id="T001",
            pet_id="P001",
            title="Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            recurrence_pattern="daily",
            original_due_date=date.today()
        )
        
        completion_date = date(2024, 3, 15)
        task.mark_complete(completion_date)
        
        # Verify last_completed_date is set
        assert task.last_completed_date == completion_date
    
    def test_recurring_task_with_complex_task_id(self):
        """Verify task ID generation handles complex ID formats."""
        task = CareTask(
            task_id="T001_ABC",  # Contains non-numeric suffix
            pet_id="P001",
            title="Walk",
            category="exercise",
            duration_minutes=30,
            priority=3,
            recurrence_pattern="daily",
            original_due_date=date.today()
        )
        
        next_task = task.mark_complete(date.today())
        
        # Should append _1 since last part isn't numeric
        assert next_task.task_id == "T001_ABC_1"
