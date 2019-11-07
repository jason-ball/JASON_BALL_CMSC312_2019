from tkinter import Tk, Label, W, E, Button
import tables

class ProcessGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('fakeOS: Processes')
        self.window.resizable(False, False)
        self.labels = {}
        row = 0
        for pcb in tables.PCBs:
            cells = {}
            cells['id'] = Label(self.window, text=f'Process {pcb.process.pid}:', font=('Arial', 32))
            cells['id'].grid(row=row, column=0, sticky=W)
            cells['state'] = Label(self.window, text=pcb.state, font=('Arial Bold', 32))
            cells['state'].grid(row=row, column=1, sticky=E)
            self.labels[pcb.process.pid] = cells
            row += 1
        self.start_button = Button(self.window, text="Add new randomized process")
        self.start_button.grid(row=row, column=0, columnspan=2, sticky=W+E)


    def start(self):
        self.window.after(100, self.update)
        self.window.mainloop()

    def update(self):
        for pcb in tables.PCBs:
            self.labels[pcb.process.pid]['state'].configure(text=pcb.state)
            if pcb.process.has_cs:
                self.labels[pcb.process.pid]['state'].configure(fg="blue")
            elif pcb.process.is_waiting_for_cs:
                self.labels[pcb.process.pid]['state'].configure(fg="red")
            elif pcb.state == 'DONE':
                self.labels[pcb.process.pid]['state'].configure(fg="green")
            else:
                self.labels[pcb.process.pid]['state'].configure(fg="black")
        self.window.after(100, self.update)
