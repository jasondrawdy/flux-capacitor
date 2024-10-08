# -*- coding: utf-8 -*-
# ########################################################################                          
# Program: Flux Capacitor
# Author: Jason Drawdy
# Version: 1.0.0
# Date: 07/22/24
# #########################################################################
# Description:
# This module auto-commits updates to a history file in order to maintain a
# consistent git streak on the Github platform.
# #########################################################################
# Import native Python libraries and functions.
import os # Only calling os.chdir() in the __init__ function.
import sys # Exits the program if there are errors commiting.
import time # Allows the sentinel to cleanup garbage files.
import json
from json import JSONDecodeError
from datetime import datetime, timezone
# Import 3rd party pip package resources.
from git import Repo, PushInfo
from git.exc import InvalidGitRepositoryError
# Import custom packages and modules.
from logger import Logger
from sentinel import Sentinel

logger = Logger(__name__)

def keep_system_clean():
    sentinel = Sentinel()
    sentinel.authorized = True
    sentinel.start()

class CommitDetails():
    def __init__(self, history: dict) -> None:
        self.update_last_date = history['LAST_UPDATE']
        self.update_count = history['UPDATE_COUNT']
        self.message = f"Updated history {self.update_count} time(s). Last updated on {self.update_last_date}"

class FluxCapacitor():
    def __init__(self: "FluxCapacitor") -> None:
        self._default_path: str = "."
        self._daily_file: str = f"{self._default_path}/data/history.json"
        self._repository: Repo = Repo(self._default_path)

    def _read_file(self: "FluxCapacitor", filepath: str):
        with open(filepath, 'r') as file:
            return file.read()

    def _write_file(self: "FluxCapacitor", filepath: str, data: str):
        with open(filepath, 'w') as file:
            file.write(data)

    def _update_history(self: "FluxCapacitor"):
        contents = self._read_file(self._daily_file)
        data = json.loads(contents)
        data['LAST_UPDATE'] = str(datetime.now(tz=timezone.utc))
        data['UPDATE_COUNT'] = int(data['UPDATE_COUNT']) + 1
        self._details = CommitDetails(data)
        self._write_file(self._daily_file, json.dumps(data))

    def commit_repository(self: "FluxCapacitor"):
        self._update_history()
        self._repository.git.add(update=True)
        self._repository.index.commit(self._details.message)
        origin = self._repository.remote(name='origin')
        result: list[PushInfo] = origin.push()[0]
        if "failed" in result.summary:
            logger.error(f"An error was encountered while pushing updates: {result.summary}")
            sys.exit(2)
            
if __name__ == '__main__':
    try:
        os.chdir("..") # Make sure to use the whole project instead of just "src".
        keep_system_clean()
        flux_capacitor = FluxCapacitor()
        flux_capacitor.commit_repository()
        logger.success("The repository was successfully updated!")
    except OSError:
        logger.error("The history file does not exist or could not be modified!")
    except JSONDecodeError:
        logger.error("The history file is not a valid JSON formatted file!")
    except InvalidGitRepositoryError:
        logger.error("The current project is not a real Git repo.")
    time.sleep(1) # Allow our sentinel to cleanup any garbage -- if not already.