
import ipywidgets as widgets
from IPython.display import display
from PIL import Image
import json
import io

class LabelingTool:
    def __init__(self, catalog_path):
        self.catalog_path = catalog_path
        with open(catalog_path) as f:
            self.catalog = json.load(f)

        self.current = next(
            (i for i, e in enumerate(self.catalog) if e["label"] is None), 0
        )
        self.total = len(self.catalog)

        self.img_widget   = widgets.Image(format="jpeg", width=640, height=480)
        self.status_label = widgets.Label()
        self.progress_bar = widgets.IntProgress(min=0, max=self.total, description="Progress:")

        self.good_btn = widgets.Button(description="Good (G)", button_style="success",
                                       layout=widgets.Layout(width="200px", height="50px"))
        self.bad_btn  = widgets.Button(description="Bad (B)", button_style="danger",
                                       layout=widgets.Layout(width="200px", height="50px"))
        self.skip_btn = widgets.Button(description="Skip", button_style="warning",
                                       layout=widgets.Layout(width="200px", height="50px"))
        self.back_btn = widgets.Button(description="Back", button_style="info",
                                       layout=widgets.Layout(width="200px", height="50px"))

        self.good_btn.on_click(lambda b: self.label("good"))
        self.bad_btn.on_click(lambda b: self.label("bad"))
        self.skip_btn.on_click(lambda b: self.label(None))
        self.back_btn.on_click(lambda b: self.go_back())

        self.ui = widgets.VBox([
            self.status_label,
            self.progress_bar,
            self.img_widget,
            widgets.HBox([self.good_btn, self.bad_btn, self.skip_btn, self.back_btn])
        ])

        self.show_frame()
        display(self.ui)

    def show_frame(self):
        if self.current >= self.total:
            self.status_label.value = "All frames labeled!"
            return
        entry = self.catalog[self.current]
        img   = Image.open(entry["path"]).resize((640, 360))
        buf   = io.BytesIO()
        img.save(buf, format="JPEG")
        self.img_widget.value = buf.getvalue()
        self.status_label.value = "Frame {}/{} | Label: {} | Good: {} | Bad: {}".format(
            self.current + 1, self.total,
            entry["label"] if entry["label"] else "unlabeled",
            sum(1 for e in self.catalog if e["label"] == "good"),
            sum(1 for e in self.catalog if e["label"] == "bad")
        )
        self.progress_bar.value = self.current

    def label(self, value):
        self.catalog[self.current]["label"] = value
        self.save()
        self.current += 1
        self.show_frame()

    def go_back(self):
        if self.current > 0:
            self.current -= 1
            self.show_frame()

    def save(self):
        with open(self.catalog_path, "w") as f:
            json.dump(self.catalog, f, indent=2)
