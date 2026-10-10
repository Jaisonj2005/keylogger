# Educational Keylogger Prototype ⌨️

A Python-based endpoint monitoring utility designed to demonstrate how malicious payloads intercept operating system API calls to capture keystrokes. Built to understand the triggers that alert modern Endpoint Detection and Response (EDR) platforms.

**Features:**
* Utilizes the `pynput` library to establish a system-wide background hook on OS keyboard events.
* Intelligently parses alphanumeric input while translating special control keys (e.g., Backspace, Enter, Tab) into human-readable log formats.
* Features a Tkinter GUI functioning as a localized Command and Control (C2) interface to securely initiate and terminate the logging thread.
* Writes captured telemetry to a localized, hidden session log file.

*Built as Day 25 of a 30-Day Network Engineering & Security portfolio streak. Note: For authorized testing and educational threat analysis only.*
