# data_entry_app.py
"""The ABQ Data Entry application"""
from decimal import Decimal, InvalidOperation
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pathlib import Path
import csv



class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ABQ Data Entry Application")
        self.columnconfigure(0, weight=1)
        ttk.Label(
            self, text="ABQ Data Entry Application", font=("TkDefaultFont", 16)
        ).grid(row=0)
        self.recordform = DataRecordForm(self)
        self.recordform.grid(row=1, padx=10, sticky=(tk.W + tk.E))
        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.status).grid(
            sticky=(tk.W + tk.E), row=2, padx=10
        )
        records_saved = 0

    def _on_save(self):
        """Handles save button clicks"""
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "abq_data_record_{}.csv".format(datestring)
        newfile = not Path(filename).exists()
        try:
            data = self.recordform.get()
        except ValueError as e:
            self.status.set(str(e))
            return
        with open(filename, "a", newline="") as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)
        self._records_saved += 1
        self.status.set("{} records saved this session".format(self._records_saved))
        self.recordform.reset()
        errors = self.recordform.get_errors()
        if errors:
            self.status.set(
                "Cannot save, error in fields: {}".format(", ".join(errors.keys()))
            )
            return

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


if __name__ == "__main__":
    app = Application()
    app.mainloop()
