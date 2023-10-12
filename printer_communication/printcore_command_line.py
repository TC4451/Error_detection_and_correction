import time
from queue import Queue
from threading import Thread
from printcore import printcore  # Assuming you've already imported the printcore class

class GCodeSender:
    def __init__(self, printer_port, baud_rate):
        self.printer = printcore(port=printer_port, baud=baud_rate)
        self.send_queue = Queue()
        self.sender_thread = None

    def start(self):
        # self.printer.start()
        self.sender_thread = Thread(target=self._sender_loop)
        self.sender_thread.start()

    def stop(self):
        self.send_queue.put(None)  # Signal sender loop to stop
        self.sender_thread.join()
        self.printer.disconnect()

    def send_command(self, command):
        self.send_queue.put(command)

    def _sender_loop(self):
        while True:
            command = self.send_queue.get()
            if command is None:
                break  # Exit the loop
            self.printer.send(command)
            time.sleep(0.1)  # Add a small delay between sending commands

if __name__ == "__main__":
    printer_port = '/dev/tty.usbmodem14201'
    baud_rate = 115200
    gcode_sender = GCodeSender(printer_port, baud_rate)
    gcode_sender.start()

    try:
        while True:
            command = input("Enter G-code command (or exit): ")
            if command.lower() == "exit":
                break
            gcode_sender.send_command(command)
    except KeyboardInterrupt:
        pass

    gcode_sender.stop()