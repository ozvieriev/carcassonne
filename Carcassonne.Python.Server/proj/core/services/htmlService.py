from jinja2 import Environment, FileSystemLoader


class htmlService:

    def __init__(self):
        pass

    def renderTemplate(self, data: dict) -> str:
        loader = loader = FileSystemLoader("proj/core/resources")
        env = Environment(loader=loader)

        template = env.get_template("template.html")
        return template.render(data)
    
    def saveToFile(self, name: str, html: str):
        with open(f"tests/output/{name}.html", "w", encoding="utf-8") as f:
            f.write(html)