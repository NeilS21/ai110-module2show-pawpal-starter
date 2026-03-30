"""
PawPal+ System: Core classes for pet care scheduling and planning.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import date, time, timedelta
from enum import Enum


@dataclass
class Owner:
    """Represents a pet owner and their preferences."""
    owner_id: str
    name: str
    daily_time_available: int
    preferences: str
    max_tasks_per_day: int

    def update_preferences(self, preferences: str) -> None:
        """Update owner preferences."""
        self.preferences = preferences

    def set_available_time(self, daily_minutes: int) -> None:
        """Set the daily time available for pet care."""
        self.daily_time_available = daily_minutes

    def mark_task_complete(self, task_id: str) -> None:
        """Mark a task as complete."""
        pass


@dataclass
class Pet:
    """Represents a pet and its care needs."""
    pet_id: str
    name: str
    species: str
    age: int
    energy_level: str
    medical_notes: str

    def update_profile(self) -> None:
        """Update pet profile information."""
        # Pet can update its profile (currently a placeholder for validation)
        pass

    def get_care_needs(self) -> List[str]:
        """Return the care needs for this pet."""
        # Return common care needs based on species
        needs = ["feeding", "water"]
        if self.species.lower() == "dog":
            needs.extend(["walk", "exercise"])
        elif self.species.lower() == "cat":
            needs.extend(["litter box", "play"])
        return needs


@dataclass
class CareTask:
    """Represents a single care task for a pet."""
    task_id: str
    pet_id: str
    title: str
    category: str
    duration_minutes: int
    priority: int
    due_time: Optional[time] = None
    is_completed: bool = False
    recurrence_pattern: str = "once"  # "once", "daily", "weekly", "monthly"
    original_due_date: Optional[date] = None  # Track original date for recurring tasks
    last_completed_date: Optional[date] = None  # When was this task last completed?

    def mark_complete(self, completion_date: Optional[date] = None) -> Optional["CareTask"]:
        """Mark this task as complete and generate next occurrence if recurring.
        
        Args:
            completion_date: Date when the task was completed (defaults to today)
            
        Returns:
            A new CareTask instance for the next occurrence if recurring, None otherwise
        """
        if completion_date is None:
            completion_date = date.today()
        
        self.is_completed = True
        self.last_completed_date = completion_date
        
        # If task is recurring, generate next occurrence
        if self.recurrence_pattern != "once":
            return self._generate_next_occurrence(completion_date)
        
        return None
    
    def _generate_next_occurrence(self, completed_date: date) -> "CareTask":
        """Generate the next occurrence of a recurring task using timedelta.
        
        Args:
            completed_date: Date the task was completed
            
        Returns:
            A new CareTask instance with updated due date
        """
        # Calculate next due date based on recurrence pattern
        if self.recurrence_pattern == "daily":
            # Next occurrence is tomorrow
            next_due_date = completed_date + timedelta(days=1)
        
        elif self.recurrence_pattern == "weekly":
            # Next occurrence is 7 days from now
            next_due_date = completed_date + timedelta(days=7)
        
        elif self.recurrence_pattern == "monthly":
            # Next occurrence is 30 days from now (approximation)
            next_due_date = completed_date + timedelta(days=30)
        
        else:
            # Default to daily if pattern not recognized
            next_due_date = completed_date + timedelta(days=1)
        
        # Create new task instance with updated due date
        # Generate a new task_id by incrementing the numeric suffix
        task_id_parts = self.task_id.rsplit('_', 1)
        if len(task_id_parts) == 2 and task_id_parts[1].isdigit():
            # Increment occurrence number (e.g., T001_1 -> T001_2)
            new_task_id = f"{task_id_parts[0]}_{int(task_id_parts[1]) + 1}"
        else:
            # Append _1 if no occurrence number (e.g., T001 -> T001_1)
            new_task_id = f"{self.task_id}_1"
        
        # Create new task with same properties but reset completion
        next_task = CareTask(
            task_id=new_task_id,
            pet_id=self.pet_id,
            title=self.title,
            category=self.category,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            due_time=self.due_time,  # Keep same time of day
            is_completed=False,
            recurrence_pattern=self.recurrence_pattern,
            original_due_date=next_due_date,
            last_completed_date=None
        )
        
        return next_task
    
    def update_task(self) -> None:
        """Update task details."""
        pass

    def get_urgency_score(self, current_time: time) -> float:
        """Calculate urgency score based on due time and priority.
        
        Scores combine task priority (1-5) and time proximity to due time.
        Overdue tasks receive highest score.
        """
        # Base score is the priority (1-5)
        score = float(self.priority)
        
        # If task has a due time, add urgency based on proximity
        if self.due_time:
            current_minutes = current_time.hour * 60 + current_time.minute
            due_minutes = self.due_time.hour * 60 + self.due_time.minute
            minutes_until_due = due_minutes - current_minutes
            
            if minutes_until_due < 0:
                score += 10  # Overdue
            elif minutes_until_due < 30:
                score += 5   # Due within 30 min
            elif minutes_until_due < 120:
                score += 2   # Due within 2 hours
        
        return score


class Scheduler:
    """Scheduling engine that creates daily plans."""
    
    def __init__(self, constraints: dict, scoring_weights: dict, strategy: str):
        self.constraints = constraints
        self.scoring_weights = scoring_weights
        self.strategy = strategy

    def sort_by_time(self, tasks: List[CareTask]) -> List[CareTask]:
        """Sort tasks by due_time in chronological order.
        
        Uses a lambda function to convert time to minutes for comparison.
        Tasks without due_time are placed at the end.
        """
        # Separate tasks with and without due_time
        tasks_with_time = [t for t in tasks if t.due_time is not None]
        tasks_without_time = [t for t in tasks if t.due_time is None]
        
        # Sort by converting time to minutes: hour * 60 + minute
        sorted_with_time = sorted(
            tasks_with_time,
            key=lambda task: task.due_time.hour * 60 + task.due_time.minute
        )
        
        # Return sorted times first, then tasks without times
        return sorted_with_time + tasks_without_time
    
    def filter_by_completion(self, tasks: List[CareTask], completed: bool = False) -> List[CareTask]:
        """Filter tasks by completion status.
        
        Args:
            tasks: List of tasks to filter
            completed: If True, return completed tasks; if False, return incomplete tasks
            
        Returns:
            Filtered list of tasks
        """
        return [task for task in tasks if task.is_completed == completed]
    
    def filter_by_pet(self, tasks: List[CareTask], pet_id: str) -> List[CareTask]:
        """Filter tasks by pet ID.
        
        Args:
            tasks: List of tasks to filter
            pet_id: The pet ID to filter by
            
        Returns:
            List of tasks for the specified pet
        """
        return [task for task in tasks if task.pet_id == pet_id]
    
    def complete_task(self, task: CareTask, completion_date: Optional[date] = None) -> List[CareTask]:
        """Mark a task complete and handle recurring task generation.
        
        For recurring tasks (daily, weekly, monthly), this will automatically
        generate a new task instance for the next occurrence.
        
        Args:
            task: The task to mark complete
            completion_date: When the task was completed (defaults to today)
            
        Returns:
            List containing the next task instance if recurring, empty list if one-time
        """
        if completion_date is None:
            completion_date = date.today()
        
        # Mark task as complete
        next_task = task.mark_complete(completion_date)
        
        # Return new task if recurring, otherwise return empty list
        return [next_task] if next_task else []
    
    def get_recurring_tasks(self, tasks: List[CareTask]) -> List[CareTask]:
        """Filter tasks that are recurring (not one-time).
        
        Args:
            tasks: List of tasks to filter
            
        Returns:
            List of recurring tasks
        """
        return [t for t in tasks if t.recurrence_pattern != "once"]
    
    def expand_recurring_tasks(self, recurring_tasks: List[CareTask], days: int = 30) -> List[CareTask]:
        """Expand recurring tasks across a date range.
        
        This generates instances of recurring tasks for the specified number of days.
        Useful for building multi-week schedules.
        
        Args:
            recurring_tasks: List of recurring task templates
            days: Number of days to expand (default 30 days)
            
        Returns:
            List of task instances for the date range
        """
        expanded_tasks = []
        today = date.today()
        
        for recurring_task in recurring_tasks:
            current_task = recurring_task
            
            for day_offset in range(days):
                target_date = today + timedelta(days=day_offset)
                
                # Determine if this task should occur on this date
                should_occur = False
                
                if recurring_task.recurrence_pattern == "daily":
                    should_occur = True
                
                elif recurring_task.recurrence_pattern == "weekly":
                    # Occurs every 7 days
                    if day_offset % 7 == 0:
                        should_occur = True
                
                elif recurring_task.recurrence_pattern == "monthly":
                    # Simplified: occurs every 30 days
                    if day_offset % 30 == 0:
                        should_occur = True
                
                if should_occur:
                    # Create a task instance for this date
                    task_instance = CareTask(
                        task_id=f"{recurring_task.task_id}_d{day_offset}",
                        pet_id=recurring_task.pet_id,
                        title=recurring_task.title,
                        category=recurring_task.category,
                        duration_minutes=recurring_task.duration_minutes,
                        priority=recurring_task.priority,
                        due_time=recurring_task.due_time,
                        is_completed=False,
                        recurrence_pattern=recurring_task.recurrence_pattern,
                        original_due_date=target_date,
                        last_completed_date=None
                    )
                    expanded_tasks.append(task_instance)
        
        return expanded_tasks
    
    def detect_conflicts(self, tasks: List[CareTask]) -> List[Tuple[CareTask, CareTask, str]]:
        """Detect and report task conflicts (same time scheduling).
        
        Lightweight conflict detection: compares tasks by due_time and returns
        a list of conflicts with warning messages instead of crashing.
        
        Args:
            tasks: List of tasks to check for conflicts
            
        Returns:
            List of tuples: (task1, task2, warning_message)
            Empty list if no conflicts found
        """
        conflicts = []
        tasks_with_time = [t for t in tasks if t.due_time is not None]
        
        # Compare each task with every other task
        for i in range(len(tasks_with_time)):
            for j in range(i + 1, len(tasks_with_time)):
                task1 = tasks_with_time[i]
                task2 = tasks_with_time[j]
                
                # Check if they have the same due time
                if task1.due_time == task2.due_time:
                    warning = (
                        f"[CONFLICT] '{task1.title}' (Pet: {task1.pet_id}) and "
                        f"'{task2.title}' (Pet: {task2.pet_id}) both scheduled at {task1.due_time.strftime('%I:%M %p')}"
                    )
                    conflicts.append((task1, task2, warning))
        
        return conflicts

    def build_plan(self, owner: Owner, pet: Pet, tasks: List[CareTask], current_time: time) -> "DailyPlan":
        """Build an optimized daily plan based on constraints and scoring weights."""
        pass

    def score_task(self, task: CareTask, current_time: time, remaining_minutes: int) -> float:
        """Calculate priority score based on urgency, priority, and available time."""
        pass

    def resolve_conflicts(self) -> None:
        """Resolve scheduling conflicts by rescheduling tasks to different times."""
        pass


@dataclass
class DailyPlan:
    """Represents a daily schedule of tasks."""
    date: date
    total_minutes_used: int = 0
    scheduled_items: dict[str, time] = field(default_factory=dict)  # task_id -> start_time
    unscheduled_tasks: List[CareTask] = field(default_factory=list)

    def add_item(self, task: CareTask, start_time: time) -> None:
        """Add a task to the schedule at a specific start time."""
        self.scheduled_items[task.task_id] = start_time

    def remove_item(self, task_id: str) -> None:
        """Remove a task from the schedule by ID (no error if not found)."""
        if task_id in self.scheduled_items:
            del self.scheduled_items[task_id]

    def explain_plan(self) -> str:
        """Generate a human-readable explanation of the daily plan."""
        pass
