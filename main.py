import random
from datetime import datetime
from time import monotonic

from art import text2art
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

WELCOME_MESSAGE = 'Welcome!'
LOGO_TEXT = 'ASDF'

class TimeDisplay(Static):
    time = reactive(0.0)
    speaker_name = WELCOME_MESSAGE

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update time to current."""
        self.time =  (self.end_time - monotonic())

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{self.speaker_name} {hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self, speaker_name, time_to_speak) -> None:
        self.speaker_name = speaker_name
        self.end_time = monotonic() + time_to_speak
        self.update_timer.resume()


class StandUpApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "stopwatch.css"

    BINDINGS = [
        ("a", "previous", "Previous Speaker"),
        ("d", "next", "Next Speaker")
    ]

    current_speaker_idx = -1
    primary_speakers = ['A', 'B', 'C', 'F', 'G']
    secondary_speakers = ['X', 'Z']
    random.shuffle(primary_speakers)
    random.shuffle(secondary_speakers)
    speakers=[WELCOME_MESSAGE] + primary_speakers + secondary_speakers +[ 'Misc, QA']

    def init(self):
        list_view = self.query_one(ListView)
        for speaker in self.speakers[1:]:
                list_view.append(ListItem(Label(speaker)))

    def compose(self) -> ComposeResult:
        yield Header()
        yield TimeDisplay()
        yield ListView()
        yield Static(text2art(LOGO_TEXT))
        yield Footer()

    def action_next(self) -> None:
        list_view = self.query_one(ListView)
        if self.current_speaker_idx == -1:
            for speaker in self.speakers[1:]:
                list_view.append(ListItem(Label(speaker)))
            self.current_speaker_idx = 1
        else:
            self.current_speaker_idx += 1

        end_time = datetime.strptime('09:25', '%H:%M')
        now = datetime.strptime(datetime.now().strftime('%H:%M:%S'), '%H:%M:%S')
        left_for_all = end_time - now
        left_for_next = left_for_all / (len(self.speakers) - self.current_speaker_idx)

        time_display = self.query_one(TimeDisplay)
        time_display.start(speaker_name=self.speakers[self.current_speaker_idx], time_to_speak=left_for_next.seconds)

        list_view.index = self.current_speaker_idx-1

    def action_previous(self) -> None:
        self.current_speaker_idx -= 1
        list_view = self.query_one(ListView)
        list_view.index = self.current_speaker_idx


if __name__ == "__main__":
    app = StandUpApp()
    app.run()
