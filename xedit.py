import sys

from textual import events
from textual.app import App, ComposeResult
from textual.widgets import TextLog, Header, Footer


def getText():
    with open(sys.argv[1], 'r+') as f:
        text = f.read()
    return text


def saveText(text):
    with open(sys.argv[1], 'w') as f:
        f.write(text[:len(text) - 1].replace(" \n", "\n"))


class Input(TextLog):

    def __init__(self, inpt):
        self.i = len(inpt) + 1
        self.text = inpt + " "
        super().__init__()
        self.markup = True

    def on_mount(self):
        self.write(self.text[:self.i - 1] + "[u]" +
                   self.text[self.i - 1] + "[/u]")
        self.focus()

    def _on_key(self, event: events.Key) -> None:

        if event.is_printable:
            self.text = self.text[:self.i - 1] + \
                event.character + self.text[self.i - 1:]
            self.i += 1

        if event.key == "backspace":
            if self.i > 1:
                if self.text[self.i-2] == '\n':
                    self.text = self.text[:self.i - 2] + self.text[self.i:]
                    self.i -= 1
                else:
                    self.text = self.text[:self.i - 2] + self.text[self.i - 1:]
                self.i -= 1

            #     self.text = self.text[:self.i - 2] + self.text[self.i - 1:]

        if event.key == "delete":
            if self.i < len(self.text):
                self.text = self.text[:self.i-1] + self.text[self.i:]

        if event.key == "enter":
            self.text = self.text[:self.i - 1] + " \n" + self.text[self.i - 1:]
            self.i += 2

        if event.key == "tab":
            self.text = self.text[:self.i - 1] + "  " + self.text[self.i - 1:]
            self.i += 1

        if event.key == "left":
            if self.i > 1:
                self.i -= 1
                if self.text[self.i-1] == '\n':
                    self.i -= 1

        if event.key == "right":
            if self.i < len(self.text):
                self.i += 1
                if self.text[self.i-1] == '\n':
                    self.i += 1

        if event.key == "up":
            n1 = self.text.rfind('\n', 0, self.i-1)
            x = self.i-n1
            n2 = self.text.rfind('\n', 0, n1-1)
            if n2 + x > self.i:
                self.i = 1
            else:
                self.i = n2 + x

            if n1 < self.i:
                self.i = n1

            if self.i < 1:
                self.i = 1

        if event.key == "down":
            n1 = self.text.rfind('\n', 0, self.i-1)
            x = self.i-n1
            n2 = self.text.find('\n', self.i, len(self.text))
            if n2 + x < self.i:
                self.i = len(self.text)
            else:
                self.i = n2 + x

            if self.i > len(self.text):
                self.i = len(self.text)

        self.clear()
        self.write(self.text[:self.i - 1] + "[u]" + self.text[self.i -
                   1] + "[/u]" + self.text[self.i:] + "\n" + str(self.i))


class MainApp(App):
    BINDINGS = [("ctrl+s", "save", "Save"),
                ("escape", "exit", "Exit")]
    textBox = None

    textBox = Input(getText())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield self.textBox

    def action_save(self):
        saveText(self.textBox.text)

    def action_exit(self):
        sys.exit(0)


if __name__ == "__main__":
    app = MainApp()
    app.run()
