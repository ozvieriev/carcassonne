from jinja2 import Environment, FileSystemLoader


class htmlService:

    def __init__(self):
        pass

    def createEnvironment(self) -> Environment:
        loader = FileSystemLoader("proj/core/resources")
        env = Environment(loader=loader)
        
        return env

    def renderTemplate(self, data: dict, templateName: str) -> str:
        env = self.createEnvironment()
        template = env.get_template(f"{templateName}.html")
        
        return template.render(data)
    
    def saveToFile(self, name: str, html: str):
        with open(f"tests/output/{name}.html", "w", encoding="utf-8") as f:
            f.write(html)