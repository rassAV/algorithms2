from enum import Enum
import json


class Alignment(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Widget():
    def __init__(self, parent):
        self.parent = parent
        self.childrens = []

        if self.parent is not None:
            self.parent.addChildren(self)

    def getParent(self):
        return self.parent

    def getChildrens(self):
        return self.childrens

    def getAlignment(self):
        return self.alignment
    
    def addChildren(self, children: "Widget"):
        self.childrens.append(children)

    def to_json(self):
        match self.__class__.__name__:
            case "MainWindow":
                s_json = {"mainwindow": [[child.to_json() for child in self.childrens], self.title]}
            case "Layout":
                return {"layout": [[child.to_json() for child in self.childrens], 1 if self.alignment == Alignment.HORIZONTAL else 2]}
            case "LineEdit":
                return {"lineedit": [[child.to_json() for child in self.childrens], self.max_length]}
            case "ComboBox":
                return {"combobox": [[child.to_json() for child in self.childrens], self.items]}
        return json.dumps(s_json)


    @classmethod
    def from_json(cls, s_json):
        data = json.loads(s_json)
        match list(data.keys())[0]:
            case 'mainwindow':
                instance = MainWindow(data['mainwindow'][1])
                [instance.addChildren(cls.from_json(json.dumps(child))) for child in data['mainwindow'][0]]
            case 'layout':
                instance = Layout(None, Alignment.HORIZONTAL if data['layout'][1]==1 else Alignment.VERTICAL)
                [instance.addChildren(cls.from_json(json.dumps(child))) for child in data['layout'][0]]
            case 'lineedit':
                instance = LineEdit(None, data['lineedit'][1])
                [instance.addChildren(cls.from_json(json.dumps(child))) for child in data['lineedit'][0]]
            case 'combobox':
                instance = ComboBox(None, data['combobox'][1])
                [instance.addChildren(cls.from_json(json.dumps(child))) for child in data['combobox'][0]]
        return instance

    def __str__(self):
        return f"{self.__class__.__name__}{self.childrens}"

    def __repr__(self):
        return str(self)


class MainWindow(Widget):
    def __init__(self, title: str):
        super().__init__(None)
        self.title = title

class Layout(Widget):
    def __init__(self, parent, alignment: Alignment):
        super().__init__(parent)
        self.alignment = alignment

class LineEdit(Widget):
    def __init__(self, parent, max_length: int=10):
        super().__init__(parent)
        self.max_length = max_length

class ComboBox(Widget):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items



app = MainWindow("Application")
layout1 = Layout(app, Alignment.HORIZONTAL)
layout2 = Layout(app, Alignment.VERTICAL)

edit1 = LineEdit(layout1, 20)
edit2 = LineEdit(layout1, 30)

box1 = ComboBox(layout2, [1, 2, 3, 4])
box2 = ComboBox(layout2, ["a", "b", "c"])



print(app)
s_json = app.to_json()

print(s_json)
print(len(s_json))

new_app = MainWindow.from_json(s_json)
print(new_app)
print(new_app.childrens[1].childrens[1].items)
