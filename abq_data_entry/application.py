import tkinter as tk
from tkinter import ttk
from . import views as v
from . import models as m


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = m.CSVModel()

        self.title("ABQ Data Entry Application")
        self.columnconfigure(0, weight=1)
        ttk.Label(
            self, text="ABQ Data Entry Application", font=("TkDefaultFont", 16)
        ).grid(row=0)

        self.recordform = v.DataRecordForm(self, self.model)
        self.recordform.grid(row=1, padx=10, sticky=(tk.W + tk.E))
        self.recordform.bind("<<SaveRecord>>", self._on_save)

        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.status).grid(
            sticky=(tk.W + tk.E), row=2, padx=10
        )
        records_saved = 0

    def _on_save(self, *_):
        """Handles file-save requests"""
        errors = self.recordform.get_errors()
        if errors:
            self.status.set(
                "Cannot save, error in fields: {}".format(", ".join(errors.keys()))
            )
            return
        data = self.recordform.get()
        self.model.save_record(data)
        self._records_saved += 1
        self.status.set(f"{self._records_saved} records saved this session")
        self.recordform.reset()

    def get_errors(self):
        """Get a list of field errors in the form"""
        errors = {}
        for key, var in self._vars.items():
            inp = var.label_widget.input
            error = var.label_widget.error
            if hasattr(inp, "trigger_focusout_validation"):
                inp.trigger_focusout_validation()
            if error.get():
                errors[key] = error.get()
        return errors
