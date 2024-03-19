from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import numpy as np

def Load_diagram(exp, inc, month):
    expens_list = []
    income_list = []
    months = []
    months_names = []

    for x,y in exp.items():
        for z in exp[x]:
            months.append(str(z))
            months_names.append(f"{month[z]} ({x})")
            expens_list.append(np.sum(exp[x][z]))
    for x,y in inc.items():
        for z in inc[x]:
            income_list.append(np.sum(inc[x][z]))
            if exp == {}:
                months.append(str(z))
                months_names.append(f"{month[z]} ({x})")

    if income_list == []:
        income_list.append(0)
    if expens_list == []:
        expens_list.append(0)
        
    def draw_chart(month=None):
        fig = Figure(figsize=(5, 4), dpi=150)
        plot = fig.add_subplot(1, 1, 1)

        if month:
            month_index = months_names.index(month)
            plot.bar(['Приходи', 'Разходи'], [income_list[month_index], expens_list[month_index]], color=['green', 'red'])
        else:
            barWidth = 0.3
            r1 = np.arange(len(income_list))
            r2 = [x + barWidth for x in r1]

            plot.bar(r1, income_list, color='b', width=barWidth, edgecolor='grey', label='Приходи')
            plot.bar(r2, expens_list, color='r', width=barWidth, edgecolor='grey', label='Разходи')
            plot.set_xticks([r + barWidth for r in range(len(income_list))])
            plot.set_xticklabels(months)
        return fig

    def update_chart(event=None):
        month = month_combobox.get()
        for widget in chart_frame.winfo_children():
            widget.destroy()
        fig = draw_chart(month if month != 'Всички' else None)
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    window = tk.Tk()
    window.title("Приходи и разходи в лева") 
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 5 * 150
    window_height = 4 * 150
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    window.geometry(f'{int(window_width)}x{int(window_height)}+{center_x}+{center_y}')
    window.attributes('-topmost', True)
    month_combobox = ttk.Combobox(window, values=['Всички'] + months_names)
    month_combobox.pack()
    month_combobox.bind("<<ComboboxSelected>>", update_chart)
    month_combobox.set('Всички')
    chart_frame = tk.Frame(window)
    chart_frame.pack(fill=tk.BOTH, expand=True)
    update_chart()
    window.mainloop()