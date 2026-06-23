import tkinter as tk
import os
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, messagebox
from database import problems
from search_engine import search_problem
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
all_problem_names = []
import os

save_folder = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "LeanAdvisor Reports"
)

os.makedirs(
    save_folder,
    exist_ok=True
)

for category in problems.values():
    all_problem_names.extend(category.keys())

# ================= WINDOW =================
root = tk.Tk()
root.title(
    "LeanAdvisor - Lean Construction Knowledge and Decision Support System"
)
root.state("zoomed")
root.configure(
    bg="#F0F4F8"
)

# ================= TOP FRAME =================
top_frame = tk.Frame(root)
top_frame.pack(pady=10)
# ================= MAIN TOP SECTION =================

main_frame = tk.Frame(root)
main_frame.pack(pady=10)

left_frame = tk.Frame(main_frame)
left_frame.pack(
    side="left",
    padx=50,
    anchor="n"
)

right_frame = tk.Frame(main_frame)
right_frame.pack(
    side="left",
    padx=50,
    anchor="n"
)
title_label = tk.Label(
    top_frame,
    text="LeanAdvisor",
    font=("Segoe UI", 20, "bold"),
    fg="#004A99"
)

title_label.pack()

subtitle_label = tk.Label(
    top_frame,
    text="Lean Construction Knowledge and Decision Support System",
    font=("Segoe UI", 11)
)

subtitle_label.pack(pady=(0,15))
ai_label = tk.Label(
    left_frame,
    text="Search Problem",
    font=("Segoe UI", 12)
)
ai_label.pack()

search_frame = tk.Frame(left_frame)
search_frame.pack(pady=5)

suggestion_frame = tk.Frame(left_frame)
suggestion_frame.pack(
    anchor="w",
    padx=5
)

ai_entry = tk.Entry(
    search_frame,
    width=80,
    font=("Segoe UI", 11)
)

ai_entry.pack(
    side="left",
    padx=5
)
def search():

    query = ai_entry.get()

    if query == "":
        return

    match = search_problem(query)[0]

    category = match["category"]

    problem = match["problem"]

    category_dropdown.set(category)

    problem_dropdown["values"] = list(
        problems[category].keys()
    )

    problem_dropdown.set(problem)

    show_result()

    ai_entry.delete(0, tk.END)

    ai_entry.focus_set()

root.after(
    50,
    ai_entry.focus_set
)

search_button = tk.Button(
    search_frame,
    text="SEARCH",
    font=("Segoe UI", 10, "bold"),
    command=search,
    takefocus=False,
)

search_button.pack(
    side="left"
)

# Category Label
category_label = tk.Label(
    right_frame,
    text="Select Problem Category",
    font=("Segoe UI", 12)
)
category_label.pack()

# Category Dropdown
category_dropdown = ttk.Combobox(
    right_frame,
    values=list(problems.keys()),
    state="readonly",
    width=50
)
category_dropdown.pack(pady=5)

# Problem Label
problem_label = tk.Label(
    right_frame,
    text="Select Problem",
    font=("Segoe UI", 12)
)
problem_label.pack()

# Problem Dropdown
problem_dropdown = ttk.Combobox(
    right_frame,
    state="readonly",
    width=50
)
problem_dropdown.pack(pady=5)


# ================= UPDATE PROBLEMS =================
def update_problems(event):

    selected_category = category_dropdown.get()

    problem_dropdown["values"] = list(
        problems[selected_category].keys()
    )

    problem_dropdown.set("")


category_dropdown.bind(
    "<<ComboboxSelected>>",
    update_problems
)
# ================= LIVE SEARCH SUGGESTIONS =================

def update_search_suggestions(event):

    typed = ai_entry.get().lower()

    suggestion_list.delete(
        0,
        tk.END
    )

    if typed == "":

     suggestion_list.pack_forget()

     return


    suggestion_list.pack()

    ai_entry.focus_set()

    for problem in all_problem_names:

        if typed in problem.lower():

            suggestion_list.insert(
                tk.END,
                problem
            )
   

# ================= BUTTON FRAME =================
#button_frame = tk.Frame(root)
#button_frame.pack(pady=10)


# ================= RESULT FRAME =================
result_frame = tk.Frame(root)
result_frame.pack(pady=10)

# Top row inside result frame
pdf_frame = tk.Frame(result_frame)
pdf_frame.pack(
    anchor="e",
    fill="x"
)
# ================= PDF FUNCTION =================
def change_save_location():

    global save_folder

    folder = filedialog.askdirectory()

    if folder:

        save_folder = folder

        messagebox.showinfo(
            "Save Location Updated",
            f"PDF reports will now be saved to:\n\n{save_folder}"
        )

def generate_pdf():

    print("PDF button pressed")

    category = category_dropdown.get()
    problem = problem_dropdown.get()

    if category == "" or problem == "":
        return

    data = problems[category][problem]

    from datetime import datetime

    filename = datetime.now().strftime(
        "LeanAdvisor_Report_%Y%m%d_%H%M%S.pdf"
    )

    filepath = os.path.join(
        save_folder,
        filename
    )

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "LeanAdvisor Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Problem:</b> {problem}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Waste Type:</b> {data['waste']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Lean Principle:</b> {data['principle']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Principle Definition:</b> {data['principle_definition']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Principle Explanation:</b> {data['principle_explanation']}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Recommended Tools</b>",
            styles["Heading2"]
        )
    )

    for tool in data["tools"]:

        story.append(
            Paragraph(
                "• " + tool,
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph(
            "<b>Tool Explanation</b>",
            styles["Heading2"]
        )
    )

    for tool, explanation in data["tool_explanation"].items():

        story.append(
            Paragraph(
                f"<b>{tool}</b>",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                explanation,
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph(
            "<b>Root Causes</b>",
            styles["Heading2"]
        )
    )

    for cause in data["root_causes"]:

        story.append(
            Paragraph(
                "• " + cause,
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph(
            "<b>Expected Benefits</b>",
            styles["Heading2"]
        )
    )

    for benefit in data["benefits"]:

        story.append(
            Paragraph(
                "• " + benefit,
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph(
            "<b>Implementation Steps</b>",
            styles["Heading2"]
        )
    )

    for step in data["implementation_steps"]:

        story.append(
            Paragraph(
                "• " + step,
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph(
            "<b>Preventive Measures</b>",
            styles["Heading2"]
        )
    )

    for item in data["preventive_measures"]:

        story.append(
            Paragraph(
                "• " + item,
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph(
            "<b>Corrective Measures</b>",
            styles["Heading2"]
        )
    )

    for item in data["corrective_measures"]:

        story.append(
            Paragraph(
                "• " + item,
                styles["BodyText"]
            )
        )

    story.append(
        Paragraph(
            "<b>Priority Level</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            data["priority"],
            styles["BodyText"]
        )
    )

    doc.build(story)

    messagebox.showinfo(
        "PDF Generated",
        f"PDF report generated successfully!\n\nSaved to:\n{save_folder}"
    )

change_location_button = tk.Button(
    pdf_frame,
    text="📂 CHANGE LOCATION",
    font=("Segoe UI", 10, "bold"),
    width=18,
    command=change_save_location
)

pdf_button = tk.Button(
    pdf_frame,
    text="📄 GENERATE PDF",
    font=("Segoe UI", 10, "bold"),
    width=18,
    command=generate_pdf,
    takefocus=False
)
change_location_button.pack(
    side="right",
    padx=10,
    pady=(0,20)
)

pdf_button.pack(
    side="right",
    padx=10,
    pady=(0,20)
)
result_box = ScrolledText(
    result_frame,
    wrap="word",
    width=200,
    height=25,
    font=("Segoe UI", 11),
    padx=20,
    pady=20
)

result_box.pack()

# ================= SUGGESTION LIST =================

suggestion_list = tk.Listbox(
    suggestion_frame,
    width=91,
    height=5,
    font=("Segoe UI", 10),
    bg="white",
    fg="black",
    selectbackground="#0078D7",
    selectforeground="white",
    relief="flat",
    bd=1,
    highlightthickness=1,
    highlightbackground="#D0D0D0"
)

suggestion_list.pack(
    pady=2
)
   
# Enable live suggestions while typing
ai_entry.bind(
    "<KeyRelease>",
    update_search_suggestions
)
def select_suggestion(event):

    if not suggestion_list.curselection():
        return

    selected = suggestion_list.get(
        suggestion_list.curselection()
    )

    ai_entry.delete(
        0,
        tk.END
    )

    ai_entry.insert(
        0,
        selected
    )

    suggestion_list.delete(
        0,
        tk.END
    )

    suggestion_list.pack_forget()



suggestion_list.bind(
    "<<ListboxSelect>>",
    select_suggestion
)
# ================= SHOW RESULT FUNCTION =================

def show_result():

    category = category_dropdown.get()
    problem = problem_dropdown.get()

    if category == "" or problem == "":
        return

    data = problems[category][problem]

    output = ""

    output += "============================================================\n\n"
    output += "PROBLEM\n\n"
    output += f"{problem}\n\n"

    output += "============================================================\n\n"
    output += "WASTE TYPE\n\n"
    output += f"{data['waste']}\n\n"

    output += "============================================================\n\n"
    output += "LEAN PRINCIPLE\n\n"
    output += f"{data['principle']}\n\n"

    output += "============================================================\n\n"
    output += "PRINCIPLE DEFINITION\n\n"
    output += f"{data['principle_definition']}\n\n"

    output += "============================================================\n\n"
    output += "PRINCIPLE EXPLANATION\n\n"
    output += f"{data['principle_explanation']}\n\n"

    output += "============================================================\n\n"
    output += "RECOMMENDED TOOLS\n\n"

    for tool in data["tools"]:
        output += f"• {tool}\n"

    output += "\n"
    output += "============================================================\n\n"
    output += "TOOL EXPLANATION\n\n"

    for tool, explanation in data["tool_explanation"].items():

        output += f"{tool.upper()}\n\n"
        output += f"{explanation}\n\n"

    output += "============================================================\n\n"
    output += "IMPLEMENTATION STEPS\n\n"

    for step in data["implementation_steps"]:
        output += f"• {step}\n"

    output += "\n"
    output += "============================================================\n\n"
    output += "EXPECTED BENEFITS\n\n"

    for benefit in data["benefits"]:
        output += f"• {benefit}\n"

    output += "\n"
    output += "============================================================\n\n"
    output += "ROOT CAUSES\n\n"

    for cause in data["root_causes"]:
        output += f"• {cause}\n"

    output += "\n"
    output += "============================================================\n\n"
    output += "PREVENTIVE MEASURES\n\n"

    for item in data["preventive_measures"]:
        output += f"• {item}\n"

    output += "\n"
    output += "============================================================\n\n"
    output += "CORRECTIVE MEASURES\n\n"

    for item in data["corrective_measures"]:
        output += f"• {item}\n"

    output += "\n"
    output += "============================================================\n\n"
    output += "PRIORITY LEVEL\n\n"
    output += f"{data['priority']}\n"

    output += "\n============================================================"

    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, output)
    result_box.config(state="disabled")
    ai_entry.focus_set()

    # Clear selections
    #category_dropdown.set("")
    #problem_dropdown.set("")
    #problem_dropdown["values"] = []


# ================= BUTTON =================
button = tk.Button(
    right_frame,
    text="SHOW RESULT",
    font=("Segoe UI", 10, "bold"),
    width=12,
    command=show_result,
    takefocus=False
)

button.pack(
    pady=10
)

status_label = tk.Label(
    root,
    text="Categories: 20     Problems: 400     Search Engine: Active",
    bd=1,
    relief="sunken",
    anchor="w"
)

status_label.pack(
    side="bottom",
    fill="x"
)

# ================= START =================
root.mainloop()
