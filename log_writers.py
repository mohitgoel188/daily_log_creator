from colorama import Fore, Style
import os

class LogWriter:
    def write(self, log_content, timestamp):
        raise NotImplementedError

class LocalLogWriter(LogWriter):
    def __init__(self, filepath):
        self.filepath = filepath

    def write(self, log_content, timestamp):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(log_content)
        print(Fore.GREEN + f"Your entry has been added to {self.filepath}!" + Style.RESET_ALL)

class JoplinLogWriter(LogWriter):
    def __init__(self, note_id=None):
        api_key = os.environ.get("JOPLIN_API_KEY")
        if not api_key:
            raise RuntimeError("JOPLIN_API_KEY environment variable not set.")
        from joppy.client_api import ClientApi
        self.joplin_client = ClientApi(token=api_key)
        # Prefer note_id from env if not given
        self.note_id = note_id or os.environ.get("JOPLIN_NOTE_ID")

    def write(self, log_content, timestamp):
        if self.note_id:
            note = self.joplin_client.get_notes(self.note_id)
            if not note:
                print(Fore.RED + f"Note with ID {self.note_id} not found in Joplin." + Style.RESET_ALL)
                return
            updated_body = note['body'] + "\n" + log_content
            self.joplin_client.modify_note(self.note_id, body=updated_body)
            print(Fore.GREEN + f"Your entry has been appended to Joplin note {self.note_id}!" + Style.RESET_ALL)
        else:
            note_title = f"Daily Log - {timestamp}"
            self.joplin_client.add_note(title=note_title, body=log_content)
            print(Fore.GREEN + "Your entry has been added as a new note in Joplin!" + Style.RESET_ALL)
