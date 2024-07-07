from rich.text import Text, Hyperlink

class NamedLink:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        link = Hyperlink(self.name, href=self.url)
        return f"{link}"

link1 = NamedLink("Visit Google", "https://www.google.com/")
link2 = NamedLink("Explore Stack Overflow", "https://stackoverflow.com/")

print(link1)
print(link2)
