# -*- coding: utf-8 -*-
# ########################################################################                          
# Program: Flux Capacitor
# Author: Jason Drawdy
# Version: 1.0.0
# Date: 07/22/24
# #########################################################################
# Description:
# This module is responsible for the encapsulation of console color codes
# and their corresponding functionality.
# #########################################################################
import random
import os

class Colors:
    """Encapsulates colors that can be used to modify and or customize the current bot terminal."""
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    blink = "\033[5m"
    faint = "\033[2m"
    italic = "\033[3m"
    negative = "\033[7m"

    class Foreground:
        """A collection of available escape code colors for system terminals that change the forground color of the text."""
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class Background:
        """A collection of available escape code colors for system terminals that change the background color of the text."""
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'
        #darkgrey = "\033[1;30m"
        
    @staticmethod
    def random_color() -> int:
        """
        Returns a random color as an integer.
        
        Returns
        ----------
        :class:`int`
            An integer in hexadecimal, e.g: ``0xffffff``, representing a random color.
        """
        return random.randint(0, 0xfffff)
    
    @staticmethod
    def clear_console() -> None:
        clear_on_windows = lambda: os.system('cls')
        clear_on_linux = lambda: os.system('clear')
        try:
            clear_on_windows()
            clear_on_linux()
        except: pass