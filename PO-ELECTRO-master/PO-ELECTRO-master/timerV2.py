import threading
import time


class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        threading.Thread(target=self._run).start()

    def stop(self):
        self.is_running = False

    def _run(self):
        old_time = time.perf_counter_ns()
        while True:
            new_time = time.perf_counter_ns()
            if not self.is_running:
                break

            if new_time - old_time > self.interval*1000000000:
                self.function(*self.args, **self.kwargs)
                old_time = new_time

            time.sleep(0.001)


