"""Module that implements simple multithreaded stopwatch utility"""
import threading
import threading as th
from time import sleep


class Stopwatch:
    """Stopwatch class"""


    def __init__(self, stopwatch_type='countdown', out_function: callable = lambda x: None,
                 *, hours: int = 0, minutes: int = 0, seconds: int = 0):
        """
        Initialize a new stopwatch instance
        :param stopwatch_type: type of stopwatch - countdown or timer
        :param out_function: function to print stopwatch time
        :param hours: number of hours to countdown
        :param minutes: number of minutes to countdown
        :param seconds: number of seconds to countdown
        """
        if stopwatch_type not in ('countdown', 'timer'):
            raise ValueError(f"Type should be countdown or timer, "
                             f"{stopwatch_type} is not implemented.")
        self.type = stopwatch_type
        if self.type == 'countdown':
            self.seconds = hours*3600 + minutes * 60 + seconds
        else:
            self.seconds = 0
        self.killed = False
        self.thread = th.Thread(target=self.loop, args=[threading.current_thread(), out_function])
        out_function(str(self))
        self.paused = True
        self.thread.start()

    def close(self):
        """Kills running thread if exists"""
        print("closing")
        self.killed = True

    def __str__(self):
        """
        Convert actual time to H:MM:SS format
        :return: string with converted time
        :note: this method makes a copy of self.seconds variable to be independent on it
        """
        seconds = int(self.seconds)
        str_rep = ""
        if seconds >= 3600:
            # Hours
            str_rep += str(seconds // 3600) + ":"
        if (seconds % 3600) < 600:
            # less than 10 minutes
            str_rep += "0"
        str_rep += str((seconds % 3600) // 60) + ":"
        if (seconds % 60) < 10:
            # less than 10 seconds
            str_rep += "0"
        str_rep += str(seconds % 60)
        return str_rep

    def __int__(self):
        """
        :return: actual number of seconds
        """
        return int(self.seconds)

    def __iadd__(self, other):
        """
        Adds more time to counter-entity
        :param other: integer (number of seconds) or another countdown
        :return: self-reference
        :note: if the result is negative, timer is set to 0
        """
        if isinstance(other, Stopwatch):
            self.seconds += other.seconds
        elif isinstance(other, int):
            self.seconds += other
        else:
            raise TypeError("Added attribute should be integer or other stopwatch.")
        self.seconds = max(self.seconds, 0)
        return self

    def __isub__(self, other):
        """
        Subtracts some time from counter-entity
        :param other: integer (number of seconds) or another countdown
        :return: self-reference
        :note: if the result is negative, timer is set to 0
        """
        if isinstance(other, Stopwatch):
            self.seconds -= other.seconds
        elif isinstance(other, int):
            self.seconds -= other
        else:
            raise TypeError("Added attribute should be integer or other stopwatch.")
        self.seconds = max(self.seconds, 0)
        return self

    def start(self):
        """
        Starts the clock if there is some remaining time
        :return: current time remaining
        """
        if self.type == 'countdown' and not self:
            return 0
        self.paused = False
        return int(self)

    def stop(self) -> int:
        """
        Pauses the clock
        :return: current time remaining
        """
        self.paused = True
        return int(self)

    def __bool__(self) -> bool:
        """
        Check if countdown is expired (there is some time remaining)
        :return: True if so, False othervise
        """
        return self.seconds > 0

    def __enter__(self):
        """Start wrapper for usage by with clause"""
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop wrapper for usage by with clause"""
        self.stop()
        if exc_type is not None:
            print(exc_tb)
            raise exc_type(exc_val)

    def output(self, output_function):
        """Function that is called in thread and outputs time"""
        try:
            output_function(str(self))
        except RuntimeError:
            print("fail")
            self.close()

    def loop(self, parent_thread, out_function: callable):
        """Method tisSethat is called in thread that counts time"""
        out_function(str(self))
        while (self.type == 'countdown' and self) or self.type == 'timer':
            if not parent_thread.is_alive() or self.killed:
                break
            if self.paused:
                continue
            sleep(1)
            if self.type == 'countdown' and not self.paused:
                self.seconds -= 1
                print_th = th.Thread(target=self.output, args=[out_function])
                print_th.start()
            elif not self.paused:
                self.seconds += 1
                print_th = th.Thread(target=self.output, args=[out_function])
                print_th.start()


if __name__ == "__main__":
    st = Stopwatch(out_function=lambda x: print(x, end="\r"), minutes=1)
    st.start()
