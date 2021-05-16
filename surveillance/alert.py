from gpiozero import Buzzer, LED
import threading
import time

buzzer = Buzzer(15)
led = LED(8)


class alert_buzz(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(alert_buzz, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        buzzer.on()
        time.sleep(5)
        buzzer.off()

    def clone(self):
        return alert_buzz(*args, **kwargs)



class alert_led(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(alert_led, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        led.on()
        time.sleep(5)
        led.off()

    def clone(self):
        return alert_led(*args, **kwargs)