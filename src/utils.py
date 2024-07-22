# -*- coding: utf-8 -*-
# ########################################################################                          
# Program: Flux Capacitor
# Author: Jason Drawdy
# Version: 1.0.0
# Date: 07/22/24
# #########################################################################
# Description:
# This module encapsulates functions that are used globally throughout
# the library, sentinel instances, or other project modules.
# #########################################################################
import threading
import asyncio
import hashlib
import secrets
import random
import string
import base64
import time
import sys
import os

class Spinner(object):
    def __init__(self) -> None:
        self.current_thread = None
        self.output_length = 0
        self.progress_info = None # i.e. "1 file of 1000" or "(1/10)".
        self.progress = 0 # Shown as a percent.
        self.use_progress = False
        self.done = False

    def _clear_output(self):
        for _ in range(self.output_length):
            sys.stdout.write('\b')
        sys.stdout.flush()

    def _spin_cursor(self, delay: float = 0.1):
        while not self.done:
            for cursor in '|/-\\':
                output = f"{cursor} "
                if self.progress_info:
                    output += f" {self.progress_info}"
                if self.use_progress:
                    output += f" ({self.progress}%)"
                self.output_length = len(output)
                sys.stdout.write(output)
                sys.stdout.flush()
                time.sleep(delay) # Technically speed...
                self._clear_output()
    
    def _start_spinner(self):
        if not self.current_thread:
            self.current_thread = threading.Thread(target=self._spin_cursor)
            self.current_thread.start()

    def _stop_spinner(self):
        if self.current_thread:
            self.progress_info = None
            self.progress = 0
            self.done = True
            self.current_thread.join()
            while self.current_thread.is_alive(): 
                time.sleep(0.250)
            self.current_thread = None

    def start(self):
        """Creates a new thread to start animating a loading cursor in the terminal."""
        self._start_spinner()
    
    def stop(self):
        """Joins any running spinner threads to stop the cursor from animating."""
        self._stop_spinner()
        self._clear_output()

class SystemUtils:
    """Encapsulation of common operating system utilities."""
    windows = "nt"
    linux = "posix"
    macos = "posix"
    cygwin = "posix"

    @staticmethod
    def get_system() -> str:
        """
        Returns the name of the currently running operating system.
        
        Returns
        ----------
        :class:`str`
            The name of the current system type.
        """
        return os.name

    @staticmethod
    def get_system_delimiter() -> str:
        """
        Returns a delimiter character which is appropriate for the current operating system.
        
        Returns
        ----------
        :class:`str`
            The delimiter used during parsing and concatenation of strings.
        """
        delimiters = {
            "nt": "\\",
            "posix": "/"
        }
        return delimiters.get(SystemUtils.get_system(), "")
    
    @staticmethod
    def get_line(filepath: str) -> str:
        """
        Returns the first line of a provided file in a read-only fashion.
        
        Parameters
        ----------
        filepath : :class:`str`
            The path of the file to read a line.

        Raises
        ----------
        IOError
            The file could not be opened or modified.
        Exception
            The file could not be written in general.

        Returns
        ----------
        :class:`str`
            The line that was read from the file.
        """
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    return f.readline().replace('\n', '') # Make sure to trim newlines because they can break db connections.
            except IOError: raise IOError(f"The file '{filepath}' could not be opened or read.") # pragma: no cover
            except: raise Exception(f"The file '{filepath}' could not be read.") # pragma: no cover
        else: return None

    @staticmethod
    def read_from_file(filepath: str) -> str:
        """
        Returns all data of a provided file in a read-only fashion.
        
        Parameters
        ----------
        filepath : :class:`str`
            The path of the file to read.

        Raises
        ----------
        IOError
            The file could not be opened or modified.
        Exception
            The file could not be written in general.

        Returns
        ----------
        :class:`str`
            Data that was read from the file.
        """
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    details = f.read()
                    return details
            except IOError: raise IOError(f"The file '{filepath}' could not be opened or read.") # pragma: no cover
            except: raise Exception(f"The file '{filepath}' could not be read.") # pragma: no cover
        else: return None            

    @staticmethod
    def write_to_file(filepath: str, data: str) -> int:
        """
        Writes all data to the provided file in a truncated fashion.
        
        Parameters
        ----------
        filepath : :class:`str`
            The path of the file to write.
        data : :class:`str`
            The data to be written to the file.

        Raises
        ----------
        IOError
            The file could not be opened or modified.
        Exception
            The file could not be written in general.

        Returns
        ----------
        :class:`int`
            The return value of the :func:`open.write()` function.
        """
        try:
            if not os.path.exists(os.path.dirname(os.path.abspath(filepath))):
                os.makedirs(os.path.dirname(os.path.abspath(filepath)))
            with open(filepath, "w") as f:
                details = f.write(data)
                return details
        except IOError: raise IOError(f"The file '{filepath}' could not be opened or read.") # pragma: no cover
        except: raise Exception(f"The file '{filepath}' could not be written.") # pragma: no cover

    @staticmethod
    def get_file_checksum(filename: str, block: int = 2**20) -> str:
        """
        Generates a calculated ``SHA512`` hash for a given file.

        Parameters
        ----------
        filename : :class:`str`
            The name of the file to generate the checksum for.
        block : Optional[:class:`int`]
            Chunk size to read and hash the file in bytes. Default is ``2^20``.

        Returns
        ----------
        :class:`str`
            The calculated ``SHA512`` hash of the file, or ``None`` if there was an error generating the checksum.

        Notes
        ----------
        - This function generates a ``SHA512`` hash for a given file by reading the file in blocks and hashing each block.\
        The generated hash is a digest checksum (a unique fixed-sized representation of the file content).\
        The file is treated as a binary file (read in ``rb`` mode) for proper handling of all types of files.
        
        - The reason ``SHA512`` was chosen is purely for the lack of collisions at runtime when performing dynamic checks.
        """
        try:
            sha512 = hashlib.sha512()
            with open(filename, 'rb') as file:
                while True:
                    data = file.read(block)
                    if not data:
                        break
                    sha512.update(data)
                return sha512.hexdigest()
        except IOError: # pragma: no cover
            print("File \'" + filename + "\' not found!")
            return None
        
    @staticmethod
    def is_submodule(parent: str, child: str) -> bool:
        """
        Returns a flag if the compared child module is from the parent
        and contains a ``{parent}.{child}`` path structure.
        
        Parameters
        ----------
        parent : :class:`str`
            The path of the original parent sys module.
        child : :class:`str`
            The path of the child sys module.

        Returns
        ----------
        :class:`bool`
            A flag determining if the child is a submodule of the parent module.
        """
        return parent == child or child.startswith(f"{parent}.")

    @staticmethod
    async def continue_async(delay: float = sys.float_info.min) -> None:
        """``|coro|``
        
        Sleeps the thread for the least possible amount of time for the system
        in order to allow a function to be truly async and awaitable; or a 
        specified time delay in seconds.
        
        Parameters
        ----------
        delay : Optional[:class:`float`]
            The amount of time to sleep the thread.
        """
        await asyncio.sleep(delay)

class TextUtils:
    """Contains a collection of text generation utilities such as random id and cid strings."""
    @staticmethod
    def generate_id(length: int = 10,  use_sample: bool = False) -> str:
        """
        Returns an alphanumeric identifier based on a given length and random sampling, if desired.

        Parameters
        ----------
        length : Optional[:class:`int`]
            The length of the identifier to be generated.
        use_sample : Optional[:class:`bool`]
            Use :func:`random.sample()` instead of :func:`secrets.choice()` on available characters.

        Returns
        ----------
        :class:`str`
            The generated id of a specified length.
        """
        characters = string.ascii_letters + string.digits
        if use_sample:
            return random.sample(characters, length)
        else:
            return ''.join((secrets.choice(characters) for i in range(length)))

    @staticmethod
    def generate_cid(length: int = 64) -> str:
        """
        Returns a Base64 encoded cryptographically strong random identifier.
        
        Parameters
        ----------
        length : Optional[:class:`int`]
            The length of the identifier to be generated.

        Returns
        ----------
        :class:`str`
            The generated cryptographic id of a specified length.
        """
        return base64.b64encode(str.encode(TextUtils.generate_id(length))).decode('utf-8')