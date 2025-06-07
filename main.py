import json
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# Завантаження даних
def load_data(filename="phones.json"):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)

# Пошук
def search(data, query):
    return [item for item in data if query.lower() in item['title'].lower()]

# Сортування
def sort_data(data, key):
    return sorted(data, key=lambda x: x.get(key, 0), reverse=True)

# Відображення детальної інформації
def show_details(item):
    details = f"Назва: {item['title']}\nЦіна: {item.get('price', 'Немає')} грн\nРейтинг: {item.get('rating', 'Немає')}\nВідгуки: {item.get('reviews', 'Немає')}"
    messagebox.showinfo("Деталі товару", details)

# Побудова GUI
def create_gui(data):
    root = tk.Tk()
    root.title("Телефони з Rozetka")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    search_var = tk.StringVar()
    search_entry = ttk.Entry(frame, textvariable=search_var)
    search_entry.pack(fill=tk.X)

    tree = ttk.Treeview(frame, columns=("Ціна", "Рейтинг", "Відгуки"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True)

    def update_tree(items):
        tree.delete(*tree.get_children())
        for item in items:
            tree.insert("", "end", values=(item.get("price", 0), item.get("rating", 0), item.get("reviews", 0)), tags=(item['title'],))

    update_tree(data)

    def on_search():
        query = search_var.get()
        filtered = search(data, query)
        update_tree(filtered)

    def on_sort_by_price():
        sorted_data = sort_data(data, "price")
        update_tree(sorted_data)

    def on_sort_by_rating():
        sorted_data = sort_data(data, "rating")
        update_tree(sorted_data)

    def on_sort_by_reviews():
        sorted_data = sort_data(data, "reviews")
        update_tree(sorted_data)

    btn_frame = ttk.Frame(frame)
    btn_frame.pack(pady=5)

    ttk.Button(btn_frame, text="Пошук", command=on_search).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Сортувати за ціною", command=on_sort_by_price).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Сортувати за рейтингом", command=on_sort_by_rating).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Сортувати за відгуками", command=on_sort_by_reviews).pack(side=tk.LEFT, padx=5)

    def on_select(event):
        selected = tree.focus()
        title = tree.item(selected)["tags"][0]
        item = next((i for i in data if i['title'] == title), None)
        if item:
            show_details(item)

    tree.bind("<<TreeviewSelect>>", on_select)

    root.mainloop()


# === Запуск ===
if __name__ == "__main__":
    try:
        phones = load_data("phones.json")
        create_gui(phones)
    except Exception as e:
        print("Помилка:", e)
