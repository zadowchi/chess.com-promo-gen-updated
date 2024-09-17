from colorama import Fore, Style
import time
from pystyle import Colors
from datetime import datetime

# ignore cuz I MADE IN 2 MINUTES

class Logger:

    @staticmethod
    def Log(work_done, message, color, **kwargs):
        timestamp = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
        output_message = f"{Colors.dark_gray}{timestamp} » {color}{work_done} {Colors.dark_gray}•{Colors.white} {message}{Colors.dark_gray} \u2794 "

        for key, value in kwargs.items():
            output_message += f" {Colors.white}{key} [{color}{value}{Colors.white}]{Colors.dark_gray} \u2794 "

        output_message = output_message[:-3]
        output_message += f" {Colors.white}{Style.RESET_ALL}"
        
        print(output_message)

        
    @staticmethod
    def w_Input(message):
        timestamp = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
        return input(f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}{timestamp}{Fore.LIGHTBLACK_EX}] {Fore.LIGHTMAGENTA_EX}[INPUT] {Fore.RESET}{message}")

