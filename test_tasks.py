from datetime import datetime, timedelta
from decision import Task

# Test task with no deadline or safety margin
task1 = Task('Task 1', 60)

# Test task with deadline and safety margin as minutes
deadline = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
task2 = Task('Task 2', 120, deadline=deadline, safety_margin=30)

# Test task with deadline and safety margin as string
task3 = Task('Task 3', 180, deadline=deadline, safety_margin='2H')

# Test task with safety margin as percentage of duration
task4 = Task('Task 4', 240, safety_margin='25%')

# Test task with zero duration and safety margin
task5 = Task('Task 5', 0, safety_margin='30M')

# Test task with zero duration and no safety margin
task6 = Task('Task 6', 0)

# Print scores for each task
print(task1.score())
print(task2.score())
print(task3.score())
print(task4.score())
print(task5.score())
print(task6.score())