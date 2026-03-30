"""
Simple tests for PawPal+ system using pytest.
"""
import pytest
from datetime import date, time
from pawal_system import CareTask, DailyPlan


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
