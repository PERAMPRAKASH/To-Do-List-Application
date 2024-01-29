import pymongo
from bson.objectid import ObjectId
from tkinter import *
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["todo_items"]

def add_task():
    task = task_entry.get()
    if task:
        task = {"task": task, "done": False}
        collection.insert_one(task)
        task_entry.delete(0, "end")  # Clear the entry field
        list_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

def list_tasks():
    tasks = collection.find({})
    task_list.delete(0, "end")
    for task in tasks:
        task_status = "✓" if task["done"] else " "
        task_list.insert("end", f"[{task_status}] {task['task']} ({str(task['_id'])})")

def mark_task_done():
    selected_task = task_list.get(
        ACTIVE)
    if selected_task:
        task_id = selected_task.split()[-1][1:-1]
        collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"done": True}})
        list_tasks()

def delete_task():
    selected_task = task_list.get(
        ACTIVE)
    if selected_task:
        task_id = selected_task.split()[-1][1:-1]
        collection.delete_one({"_id": ObjectId(task_id)})
        list_tasks()

window = Tk()
window.title("To-Do List")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

task_entry = Entry(window, width=50)
task_entry.pack()

add_button = Button(window, text="Add Task", command=add_task)
add_button.pack()

task_list = Listbox(window, selectmode=SINGLE, width=50)
task_list.pack()

done_button = Button(window, text="Mark as Done", command=mark_task_done)
done_button.pack()

delete_button = Button(window, text="Delete Task", command=delete_task)
delete_button.pack()

quit_button = Button(window, text="Quit", command=window.quit)
quit_button.pack()

list_tasks()
window.mainloop()