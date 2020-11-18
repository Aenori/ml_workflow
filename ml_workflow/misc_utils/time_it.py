import time

class TimeIt:
    def __enter__(self):
        self.begin = time.time()
        return self
        
    def __exit__(self, *args, **kwargs):
        self.end = time.time()
        
    def duration(self):
        return self.end - self.begin