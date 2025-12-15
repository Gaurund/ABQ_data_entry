import tkinter as tk
from tkinter import ttk
from datetime import datetime
from . import widgets as w


class DataRecordForm(ttk.Frame):
    """The input form for our widgets"""

    def _add_frame(self, label, cols=3):
        """Add a LabelFrame to the form"""
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.model= model
        fields = self.model.fields
        self._vars = {
            "Date": tk.StringVar(),
            "Time": tk.StringVar(),
            "Technician": tk.StringVar(),
            "Lab": tk.StringVar(),
            "Plot": tk.IntVar(),
            "Seed Sample": tk.StringVar(),
            "Humidity": tk.DoubleVar(),
            "Light": tk.DoubleVar(),
            "Temperature": tk.DoubleVar(),
            "Equipment Fault": tk.BooleanVar(),
            "Plants": tk.IntVar(),
            "Blossoms": tk.IntVar(),
            "Fruit": tk.IntVar(),
            "Min Height": tk.DoubleVar(),
            "Max Height": tk.DoubleVar(),
            "Med Height": tk.DoubleVar(),
            "Notes": tk.StringVar(),
        }
        r_info = self._add_frame("Record Information")
        w.LabelInput(r_info, "Date", var=self._vars["Date"], input_class=w.DateEntry).grid(
            row=0, column=0
        )
        w.LabelInput(
            r_info,
            "Time",
            input_class=w.ValidatedCombobox,
            var=self._vars["Time"],
            input_args={"values": ["8:00", "12:00", "16:00", "20:00"]},
        ).grid(row=0, column=1)
        w.LabelInput(
            r_info,
            "Technician",
            var=self._vars["Technician"],
            input_class=w.RequiredEntry,
        ).grid(row=0, column=2)

        w.LabelInput(
            r_info,
            "Lab",
            input_class=w.ValidatedRadioGroup,
            var=self._vars["Lab"],
            input_args={"values": ["A", "B", "C"]},
        ).grid(row=1, column=0)
        w.LabelInput(
            r_info,
            "Plot",
            input_class=ttk.Combobox,
            var=self._vars["Plot"],
            input_args={"values": list(range(1, 21))},
        ).grid(row=1, column=1)
        w.LabelInput(r_info, "Seed Sample", var=self._vars["Seed Sample"]).grid(
            row=1, column=2
        )

        e_info = self._add_frame("Environment Data")
        w.LabelInput(
            e_info,
            "Humidity (g/m³)",
            input_class=w.ValidatedSpinbox,
            var=self._vars["Humidity"],
            input_args={"from_": 0.5, "to": 52.0, "increment": 0.01},
            disable_var=self._vars["Equipment Fault"],
        ).grid(row=0, column=0)
        w.LabelInput(
            e_info,
            "Light (klx)",
            input_class=w.ValidatedSpinbox,
            var=self._vars["Light"],
            input_args={"from_": 0, "to": 100, "increment": 0.01},
            disable_var=self._vars["Equipment Fault"],
        ).grid(row=0, column=1)
        w.LabelInput(
            e_info,
            "Temperature (°C)",
            input_class=w.ValidatedSpinbox,
            var=self._vars["Temperature"],
            input_args={"from_": 4, "to": 40, "increment": 0.01},
            disable_var=self._vars["Equipment Fault"],
        ).grid(row=0, column=2)
        w.LabelInput(
            e_info,
            "Equipment Fault",
            input_class=ttk.Checkbutton,
            var=self._vars["Equipment Fault"],
        ).grid(row=1, column=0, columnspan=3)

        p_info = self._add_frame("Plant Data")
        w.LabelInput(
            p_info,
            "Plants",
            input_class=w.ValidatedSpinbox,
            var=self._vars["Plants"],
            input_args={"from_": 0, "to": 20},
        ).grid(row=0, column=0)
        w.LabelInput(
            p_info,
            "Blossoms",
            input_class=w.ValidatedSpinbox,
            var=self._vars["Blossoms"],
            input_args={"from_": 0, "to": 1000},
        ).grid(row=0, column=1)
        w.LabelInput(
            p_info,
            "Fruit",
            input_class=w.ValidatedSpinbox,
            var=self._vars["Fruit"],
            input_args={"from_": 0, "to": 1000},
        ).grid(row=0, column=2)

        min_height_var = tk.DoubleVar(value="-infinity")
        max_height_var = tk.DoubleVar(value="infinity")

        w.LabelInput(
            p_info,
            "Min Height (cm)",
            input_class=w.ValidatedSpinbox,
            var=self._vars["Min Height"],
            input_args={
                "from_": 0,
                "to": 1000,
                "increment": 0.01,
                "max_var": max_height_var,
                "focus_update_var": min_height_var,
            },
        ).grid(row=1, column=0)
        w.LabelInput(
            p_info,
            "Max Height (cm)",
            input_class=w.ValidatedSpinbox,
            var=self._vars["Max Height"],
            input_args={
                "from_": 0,
                "to": 1000,
                "increment": 0.01,
                "max_var": max_height_var,
                "focus_update_var": min_height_var,
            },
        ).grid(row=1, column=1)
        w.LabelInput(
            p_info,
            "Median Height (cm)",
            input_class=w.ValidatedSpinbox,
            var=self._vars["Med Height"],
            input_args={
                "from_": 0,
                "to": 1000,
                "increment": 0.01,
                "max_var": max_height_var,
                "focus_update_var": min_height_var,
            },
        ).grid(row=1, column=2)

        w.LabelInput(
            self,
            "Notes",
            input_class=w.BoundText,
            var=self._vars["Notes"],
            input_args={"width": 75, "height": 10},
        ).grid(sticky=tk.W, row=3, column=0)

        buttons = tk.Frame(self)
        buttons.grid(sticky=tk.W + tk.E, row=4)
        self.savebutton = ttk.Button(buttons, text="Save", command=self.master._on_save)
        self.savebutton.pack(side=tk.RIGHT)
        self.resetbutton = ttk.Button(buttons, text="Reset", command=self.reset)
        self.resetbutton.pack(side=tk.RIGHT)

    def reset(self):
        """Resets the form entries"""
        lab = self._vars["Lab"].get()
        time = self._vars["Time"].get()
        technician = self._vars["Technician"].get()
        try:
            plot = self._vars["Plot"].get()
        except tk.TclError:
            plot = ""
        plot_values = self._vars["Plot"].label_widget.input.cget("values")
        for var in self._vars.values():
            if isinstance(var, tk.BooleanVar):
                var.set(False)
            else:
                var.set("")
        current_date = datetime.today().strftime("%Y-%m-%d")
        self._vars["Date"].set(current_date)
        self._vars["Time"].label_widget.input.focus()
        if plot not in ("", 0, plot_values[-1]):
            self._vars["Lab"].set(lab)
            self._vars["Time"].set(time)
            self._vars["Technician"].set(technician)
            next_plot_index = plot_values.index(str(plot)) + 1
            self._vars["Plot"].set(plot_values[next_plot_index])
            self._vars["Seed Sample"].label_widget.input.focus()

    def get(self):
        data = dict()
        fault = self._vars["Equipment Fault"].get()
        for key, variable in self._vars.items():
            if fault and key in ("Light", "Humidity", "Temperature"):
                data[key] = ""
            else:
                try:
                    data[key] = variable.get()
                except tk.TclError:
                    message = f"Error in field: {key}.  Data was not saved!"
                    raise ValueError(message)
        return data
