#TO DO: load tasks from csv or calendar or something

import numpy as np

BREAK_TIME = 10 #Default break between time blocks
WORK_BLOCK = 30 #Default continuous task time unit

class Task:
    def __init__(self, time_est, time_left, benefit_value, effort_value,
                 break_unit=BREAK_TIME, work_block=WORK_BLOCK):
        self.eta = time_est
        self.to_deadline = time_left
        self._effort = effort_value
        self._benefit = benefit_value
        self._break = break_unit
        self._block = work_block
        self.blocks = np.divmod(self.eta,self._block)
        self.total_time = self.blocks[0]*(self._block+self._break)+self.blocks[1]
        self._rand = np.random.rand()/10+0.9
    
    def score(self):
        effort = self._effort+(self.blocks[0]/5) #the "mañana" score
        value = self._benefit*(np.exp(-(self.to_deadline-self.total_time)
                                      /self.to_deadline)+1) #include confidence value?
        return (value/effort)*self._rand
    
    def am_i_screwed(self):
        if self.eta < self._block or self._block == 0:
            return self.eta > self.to_deadline
        else:
            #whole_blocks = np.ceil(self.eta/self._block)
            return self.total_time > self.to_deadline

foo = Task(120, 120, 11, 7)
bar = Task(600, 720, 8, 5)
woo = Task(20, 240, 5, 3)

print(foo.score())
print(bar.score())
print(woo.score())
#print(foo.am_i_screwed())
