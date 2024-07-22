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
import sys
import time
import json
from json import JSONDecodeError
from datetime import datetime, timezone
# Import 3rd party pip package resources.
from git import Repo, Remote, PushInfo
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
        self._daily_file: str = "../data/history.json"
        self._repository: Repo = Repo("..") # Make sure to use the whole project instead of just "src".
        self._origin: Remote = self.repository.remote('origin')
        self._details: CommitDetails = None

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
        self.details = CommitDetails(data)
        self._write_file(self._daily_file, json.dumps(data))

    def commit_repository(self: "FluxCapacitor"):
        self._origin.pull()
        self._update_history()
        self._repository.index.add([self._daily_file])
        self._repository.index.commit(self._details.message)
        result: list[PushInfo] = self._origin.push()
        for entry in result:
            if entry.flags == entry.ERROR:
                logger.error("An error was encountered while pushing updates.")
                sys.exit(2)
            
if __name__ == '__main__':
    try:
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