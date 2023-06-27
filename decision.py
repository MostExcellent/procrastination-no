#TO DO: load tasks from csv or calendar or something
import os
import numpy as np
import pandas as pd
from datetime import datetime as dt, timedelta as td

BREAK_TIME = 10 #Default break between time blocks
WORK_BLOCK = 30 #Default continuous task time unit

import os
import numpy as np
import pandas as pd
from datetime import datetime as dt, timedelta as td

BREAK_TIME = 10 #Default break between time blocks
WORK_BLOCK = 30 #Default continuous task time unit

class Tasklist:
    def __init__(self, task_df = None):
        self.task_df = task_df
    
    def load_tasks(self, csv_path):
        # If csv_path is a valid path, load the csv into a dataframe
        if os.path.isfile(csv_path):
            new_task_df = pd.read_csv(csv_path)
            #check columns
            if not set(['name', 'duration', 'deadline', 'priority', 'repeating']).issubset(new_task_df.columns):
                raise ValueError('CSV file does not contain the correct columns')
        else:
            raise ValueError('Invalid path to CSV file')
        
        if self.task_df is None:
            self.task_df = new_task_df
        else:
            # Append new tasks to the existing dataframe
            self.task_df = self.task_df.append(new_task_df, ignore_index=True)
            # Remove duplicate names
            self.task_df = self.task_df.drop_duplicates(subset='name', keep='last')
        print('Tasks loaded successfully')
    
    def add_task(self, task):
        """
        Add a new task to the task list
        """
        task_dict = {'name': task.name, 'duration': task.duration, 'deadline': task.deadline, 'priority': task.priority, 'repeating': task.repeating}
        self.task_df = self.task_df.append(task_dict, ignore_index=True)
        # Remove duplicate names
        self.task_df = self.task_df.drop_duplicates(subset='name', keep='last')
        print('Task added successfully')
    
    def remove_task(self, task_name):
        """
        Remove a task from the task list
        """
        self.task_df = self.task_df[self.task_df['name'] != task_name]
        print('Task removed successfully')
    
    def get_task(self, task_name):
        """
        Get a task from the task list
        """
        task = self.task_df[self.task_df['name'] == task_name]
        if task.empty:
            raise ValueError('Task not found')
        return Task(**task.to_dict('records')[0])
    
    def get_tasklist(self):
        """
        Get the entire task list
        """
        return self.task_df
    
    def score_tasks(self):
        """
        Calculate the score of each task based on its priority, deadline, and duration
        """
        self.task_df['score'] = self.task_df.apply(lambda row: Task(**row.to_dict()).score(), axis=1)
        self.task_df = self.task_df.sort_values(by=['score'], ascending=False)
        return self.task_df
    
class Task:
    def __init__(self, name, duration = '60M', deadline = None, priority = 1, repeating = False, safety_margin=None):
        self.name = name
        if type(duration) == int:
            self.duration = duration
        elif duration.endswith('H'):
            self.duration = int(duration[:-1]) * 60 # convert hours to minutes
        elif duration.endswith('M'):
            self.duration = int(duration[:-1])
        else:
            raise ValueError('Invalid duration format. Must be of form xH or xM.')
        if deadline is not None:
            if len(deadline) == 10: # deadline is in format Y-m-d
                deadline += ' 23:59:00'
            self.deadline = dt.strptime(deadline, '%Y-%m-%d %H:%M:%S')
        else:
            self.deadline = None
        self.priority = priority
        self.repeating = repeating
        self.safety_margin = safety_margin
    
    def __repr__(self):
        return f"Task(name='{self.name}', duration='{self.duration}M', deadline='{self.deadline}', priority={self.priority}, repeating={self.repeating}, safety_margin={self.safety_margin})"
    
    def __str__(self):
        return f"{self.name} ({self.duration} minutes)"
    
    def score(self):
        """
        Calculate the score of the task based on its priority, deadline, and duration
        """
        if self.deadline is None:
            deadline_score = 0
        else:
            time_left = (self.deadline - dt.now())
            if time_left.days == 0:
                deadline_score = time_left.seconds // 60 + 1 # add 1 minute margin of safety
            else:
                deadline_score = time_left.days * 1440 # convert days to minutes
        
        duration_score = 1 / (self.duration + 1) # prioritize tasks that take less time        

        if self.safety_margin is not None and self.safety_margin:
            if isinstance(self.safety_margin, str):
                if self.safety_margin.endswith('%'):
                    safety_margin = self.duration * int(self.safety_margin[:-1]) / 100
                else:
                    safety_margin = td()
                    safety_margin_parts = self.safety_margin.split()
                    for part in safety_margin_parts:
                        if part.endswith('D'):
                            safety_margin += td(days=int(part[:-1]))
                        elif part.endswith('H'):
                            safety_margin += td(hours=int(part[:-1]))
                        elif part.endswith('M'):
                            safety_margin += td(minutes=int(part[:-1]))
                        elif part.endswith('%'):
                            safety_margin += self.duration * int(part[:-1]) / 100
            else:
                safety_margin = td(minutes=int(self.safety_margin))
            print(safety_margin)
            duration_score *= 1 / (self.duration + safety_margin.total_seconds() // 60 + 1) # add safety margin to duration_score
        
        return (self.priority + duration_score) / (deadline_score + 1) # add duration_score to priority and divide by deadline_score + 1
