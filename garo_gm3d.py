import RPi.GPIO as GPIO

class Garo:
    gpio_pin = 0
    watt_hours = 0

    def __init__(self, gpio_pin, current_watt_hours):
        self.gpio_pin = gpio_pin
        self.watt_hours = current_watt_hours

    def listen(self):
        print 'Start listening on gpio "{0}"'.format(self.gpio_pin)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.IN)
        GPIO.add_event_detect(self.gpio_pin, GPIO.RISING, callback=self.gpio_callback, bouncetime=300)

    def gpio_callback(self, channel):
        self.watt_hours += 10 # Each GPIO event (from low to high) represent 10 watt hours.
        print "GPIO triggered! The energy meter has currently drawn  ",self.watt_hours," Wh."

    def get_watt_hours(self):
        return self.watt_hours