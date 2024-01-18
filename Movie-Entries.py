import csv
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import unittest

class MovieDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Entry App")
        self.root.configure(bg="#F0F0F0")

        self.entries = []

        title_label = tk.Label(self.root, text="Title", font=("Helvetica", 12), bg="#F0F0F0", fg="#333333", padx=10, pady=5)
        title_label.grid(row=0, column=0, sticky=tk.W)

        self.title_entry = tk.Entry(self.root, bg="#FFFFFF", fg="#333333")
        self.title_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        director_label = tk.Label(self.root, text="Director", font=("Helvetica", 12), bg="#F0F0F0", fg="#333333", padx=10, pady=5)
        director_label.grid(row=1, column=0, sticky=tk.W)

        self.director_entry = tk.Entry(self.root, bg="#FFFFFF", fg="#333333")
        self.director_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        genre_label = tk.Label(self.root, text="Genres", font=("Helvetica", 12), bg="#F0F0F0", fg="#333333", padx=10, pady=5)
        genre_label.grid(row=2, column=0, sticky=tk.W)

        genres = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Musicals", "Mystery", "Romance", "Science Fiction", "Sports", "Thriller", "Western"]
        self.genre_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, height=len(genres), bg="#FFFFFF", fg="#333333")
        for idx, genre in enumerate(genres):
            self.genre_listbox.insert(idx, genre)
        self.genre_listbox.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        rating_label = tk.Label(self.root, text="Rating", font=("Helvetica", 12), bg="#F0F0F0", fg="#333333", padx=10, pady=5)
        rating_label.grid(row=3, column=0, sticky=tk.W)

        self.rating_var = tk.DoubleVar()
        rating_frame = tk.Frame(self.root, bg="#F0F0F0")
        rating_frame.grid(row=3, column=1, padx=10, pady=5, columnspan=5, sticky=tk.W)
        rating_scale = tk.Scale(self.root, variable=self.rating_var, from_=0, to=5, orient="horizontal", resolution=0.1, command=lambda value: self.update_star_rating(value), bg="#FFFFFF", fg="#333333")
        rating_scale.grid(row=3, column=1, padx=10, pady=5, columnspan=5, sticky=tk.W)

        release_year_label = tk.Label(self.root, text="Release Year", font=("Helvetica", 12), bg="#F0F0F0", fg="#333333", padx=10, pady=5)
        release_year_label.grid(row=4, column=0, sticky=tk.W)

        release_years = list(range(1940, 2025))
        self.release_year_var = tk.StringVar()
        release_year_dropdown = ttk.Combobox(self.root, textvariable=self.release_year_var, values=release_years, state="readonly", background="#FFFFFF", foreground="#333333")
        release_year_dropdown.set(2024)  
        release_year_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

        add_button = tk.Button(self.root, text="Add Entry", command=self.add_entry, bg="#4CAF50", fg="#FFFFFF", pady=5, width=15)
        add_button.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        export_csv_button = tk.Button(self.root, text="Export to CSV", command=self.export_to_csv, bg="#4CAF50", fg="#FFFFFF", pady=5, width=15)
        export_csv_button.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

        update_button = tk.Button(self.root, text="Update Entry", command=self.update_entry, bg="#4CAF50", fg="#FFFFFF", pady=5, width=15)
        update_button.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

        import_csv_button = tk.Button(self.root, text="Import from CSV", command=self.import_from_csv, bg="#4CAF50", fg="#FFFFFF", pady=5, width=15)
        import_csv_button.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)

        delete_button = tk.Button(self.root, text="Delete Entry", command=self.delete_entry, bg="#4CAF50", fg="#FFFFFF", pady=5, width=15)
        delete_button.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

        export_json_button = tk.Button(self.root, text="Export to JSON", command=self.export_to_json, bg="#4CAF50", fg="#FFFFFF", pady=5, width=15)
        export_json_button.grid(row=7, column=1, padx=10, pady=5, sticky=tk.W)

        self.table = ttk.Treeview(self.root, columns=("#0","title", "director", "genres", "rating", "release_year"), style="Custom.Treeview")
        self.table.heading("#1", text="Index")
        self.table.heading("title", text="Title")
        self.table.heading("director", text="Director")
        self.table.heading("genres", text="Genres")
        self.table.heading("rating", text="Rating")
        self.table.heading("release_year", text="Release Year")
        self.table.grid(row=0, column=2,  rowspan=6, padx=10, pady=10, sticky=(tk.N, tk.S, tk.W, tk.E))

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.table.yview)
        self.scrollbar.grid(row=0, column=3, rowspan=6, sticky="ns")
        self.table.configure(yscrollcommand=self.scrollbar.set)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(6, weight=1)
        self.root.columnconfigure(3, weight=0)

    def add_entry(self):
        title = self.title_entry.get()
        director = self.director_entry.get()
        genres = self.genre_listbox.curselection()
        selected_genres = [self.genre_listbox.get(idx) for idx in genres]
        rating = self.rating_var.get()
        release_year = self.release_year_var.get()

        if not title or not director or not selected_genres:
            messagebox.showwarning("Input Error", "Title, Director, and at least one Genre are required.")
            return

        try:
            entry = {
                "title": title,
                "director": director,
                "genres": selected_genres,
                "rating": rating,
                "release_year": release_year
            }
            self.entries.append(entry)
            self.update_table()
            self.clear_entry_fields()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def update_entry(self):
        try:
            selected_row = self.table.focus()
            index = int(self.table.item(selected_row, "values")[0])
            title = self.title_entry.get()
            director = self.director_entry.get()
            genres = self.genre_listbox.curselection()
            selected_genres = [self.genre_listbox.get(idx) for idx in genres]
            rating = self.rating_var.get()
            release_year = self.release_year_var.get()

            if not title or not director or not selected_genres:
                messagebox.showwarning("Input Error", "Title, Director, and at least one Genre are required.")
                return

            self.entries[index] = {
                "title": title,
                "director": director,
                "genres": selected_genres,
                "rating": rating,
                "release_year": release_year
            }

            self.update_table()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating an entry: {str(e)}")

    def delete_entry(self):
        try:
            selected_row = self.table.focus()
            if not selected_row:
                messagebox.showwarning("No Selection", "Please select an entry to delete.")
                return

            index = int(self.table.item(selected_row, "values")[0])
            confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this entry?")
            if confirmation:
                self.entries.pop(index)
                self.update_table()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting an entry: {str(e)}")

    def clear_entry_fields(self):
        self.root.children['.!entry'].delete(0, tk.END)
        self.root.children['.!entry2'].delete(0, tk.END)
        self.genre_listbox.selection_clear(0, tk.END)
        self.rating_var.set(0)
        self.release_year_var.set(2024)

    def export_to_csv(self):
        try:
            file_name = filedialog.asksaveasfilename(defaultextension=".csv")
            if file_name:
                with open(file_name, "w", newline="") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=["title", "director", "genres", "rating", "release_year"])
                    writer.writeheader()
                    for entry in self.entries:
                        # Exclude the "index" field before writing to CSV
                        entry_without_index = {key: entry[key] for key in entry if key != "index"}
                        writer.writerow(entry_without_index)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while exporting to CSV: {str(e)}")

    def import_from_csv(self):
        try:
            file_name = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if file_name:
                with open(file_name, "r", newline="") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        self.entries.append(row)
                self.update_table()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while importing from CSV: {str(e)}")

    def export_to_json(self):
        try:
            file_name = filedialog.asksaveasfilename(defaultextension=".json")
            if file_name:
                with open(file_name, "w") as jsonfile:
                    json.dump(self.entries, jsonfile, indent=4)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while exporting to JSON: {str(e)}")

    def update_table(self):
        try:
            self.table.delete(*self.table.get_children())
            for i, entry in enumerate(self.entries):
                stars = "★" * int(entry["rating"]) + "☆" * (5 - int(entry["rating"]))
                self.table.insert("", tk.END, values=(i, entry["title"], entry["director"], ", ".join(entry["genres"]), stars, entry["release_year"]))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating the table: {str(e)}")

    def update_star_rating(self, value):
        for widget in self.rating_frame.winfo_children():
            widget.destroy()

        filled_star = "★"
        empty_star = "☆"

        for i in range(5):
            if i < int(value):
                label = tk.Label(self.rating_frame, text=filled_star, font=("Helvetica", 12), fg="#FFA500", padx=2)
            else:
                label = tk.Label(self.rating_frame, text=empty_star, font=("Helvetica", 12), fg="#FFA500", padx=2)
            label.pack(side=tk.LEFT)

    def run(self):
        self.root.mainloop()

class TestMovieDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        self.initial_entries = [
            {"title": "Test Movie", "director": "Test Director", "genres": ["Test"], "rating": 4.5, "release_year": 2023}
        ]
        self.entries = []

    def test_add_entry(self):
        initial_count = len(self.entries)
        app.add_entry()
        self.entries = app.entries.copy()
        updated_count = len(self.entries)
        self.assertEqual(updated_count, initial_count + 1, "Adding entry failed")

    def test_update_entry(self):
        initial_entry = self.entries[0].copy()
        app.update_entry()
        updated_entry = self.entries[0]
        self.assertNotEqual(initial_entry, updated_entry, "Updating entry failed")

    def test_delete_entry(self):
        initial_count = len(self.entries)
        app.delete_entry()
        self.entries = app.entries.copy()
        updated_count = len(self.entries)
        self.assertEqual(updated_count, initial_count - 1, "Deleting entry failed")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieDatabaseApp(root)
    app.run()


