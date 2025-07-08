import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class AdvancedContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Contact Book")
        self.root.geometry("800x600")
        
        # Create data file if not exists
        self.data_file = "contacts.json"
        self.contacts = self.load_contacts()
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Create main frames
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=5)
        
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=5)
        
        self.contacts_frame = ttk.Frame(self.main_frame)
        self.contacts_frame.pack(fill=tk.BOTH, expand=True)
        
        self.details_frame = ttk.Frame(self.main_frame)
        self.details_frame.pack(fill=tk.X, pady=10)
        
        # Header
        ttk.Label(self.header_frame, text="Advanced Contact Book", style='Header.TLabel').pack()
        
        # Search
        ttk.Label(self.search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(self.search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_contacts)
        
        # Contacts list (Treeview)
        self.contacts_tree = ttk.Treeview(self.contacts_frame, columns=('Name', 'Phone'), selectmode='browse')
        self.contacts_tree.heading('#0', text='ID')
        self.contacts_tree.heading('Name', text='Name')
        self.contacts_tree.heading('Phone', text='Phone')
        self.contacts_tree.column('#0', width=50, stretch=tk.NO)
        self.contacts_tree.column('Name', width=200)
        self.contacts_tree.column('Phone', width=150)
        
        self.scrollbar = ttk.Scrollbar(self.contacts_frame, orient=tk.VERTICAL, command=self.contacts_tree.yview)
        self.contacts_tree.configure(yscrollcommand=self.scrollbar.set)
        self.contacts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contacts_tree.bind('<<TreeviewSelect>>', self.show_contact_details)
        
        # Contact details
        self.detail_labels = {}
        fields = ['Name', 'Phone', 'Email', 'Address', 'Notes']
        
        for i, field in enumerate(fields):
            ttk.Label(self.details_frame, text=f"{field}:").grid(row=i, column=0, sticky=tk.E, padx=5, pady=2)
            self.detail_labels[field] = ttk.Label(self.details_frame, text="", width=40)
            self.detail_labels[field].grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(self.button_frame, text="Add Contact", command=self.add_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Edit Contact", command=self.edit_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Export Contacts", command=self.export_contacts).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Import Contacts", command=self.import_contacts).pack(side=tk.LEFT, padx=5)
        
        # Load contacts
        self.update_contacts_list()
    
    def load_contacts(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                return json.load(file)
        return []
    
    def save_contacts(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.contacts, file, indent=4)
    
    def update_contacts_list(self, contacts=None):
        self.contacts_tree.delete(*self.contacts_tree.get_children())
        display_contacts = contacts if contacts else self.contacts
        
        for idx, contact in enumerate(display_contacts, 1):
            self.contacts_tree.insert('', 'end', iid=idx, text=str(idx),
                                    values=(contact['name'], contact['phone']))
    
    def search_contacts(self, event):
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_contacts_list()
            return
        
        filtered = [contact for contact in self.contacts 
                   if (search_term in contact['name'].lower()) or 
                   (search_term in contact['phone'])]
        self.update_contacts_list(filtered)
    
    def show_contact_details(self, event):
        selected = self.contacts_tree.selection()
        if not selected:
            return
        
        contact_id = int(selected[0]) - 1
        contact = self.contacts[contact_id]
        
        for field in ['name', 'phone', 'email', 'address', 'notes']:
            self.detail_labels[field.capitalize()].config(text=contact.get(field, ''))
    
    def add_contact(self):
        self.contact_dialog("Add New Contact")
    
    def edit_contact(self):
        selected = self.contacts_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to edit")
            return
        
        contact_id = int(selected[0]) - 1
        self.contact_dialog("Edit Contact", contact_id)
    
    def contact_dialog(self, title, contact_id=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.grab_set()
        
        fields = ['Name', 'Phone', 'Email', 'Address', 'Notes']
        entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(dialog, text=f"{field}:").grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)
            entries[field] = ttk.Entry(dialog, width=40)
            entries[field].grid(row=i, column=1, padx=5, pady=5)
        
        if contact_id is not None:
            contact = self.contacts[contact_id]
            for field in fields:
                entries[field].insert(0, contact.get(field.lower(), ''))
        
        def save_contact():
            contact_data = {field.lower(): entries[field].get() for field in fields}
            
            if not contact_data['name']:
                messagebox.showerror("Error", "Name is required")
                return
            
            if contact_id is not None:
                self.contacts[contact_id] = contact_data
            else:
                self.contacts.append(contact_data)
            
            self.save_contacts()
            self.update_contacts_list()
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save_contact).grid(row=len(fields), column=1, pady=10, sticky=tk.E)
    
    def delete_contact(self):
        selected = self.contacts_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?"):
            return
        
        contact_id = int(selected[0]) - 1
        del self.contacts[contact_id]
        self.save_contacts()
        self.update_contacts_list()
        
        # Clear details
        for label in self.detail_labels.values():
            label.config(text="")
    
    def export_contacts(self):
        file_path = tk.filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export contacts to"
        )
        
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.contacts, file, indent=4)
            messagebox.showinfo("Success", "Contacts exported successfully")
    
    def import_contacts(self):
        file_path = tk.filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Select contacts file to import"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    imported = json.load(file)
                
                if not isinstance(imported, list):
                    messagebox.showerror("Error", "Invalid contacts format")
                    return
                
                self.contacts.extend(imported)
                self.save_contacts()
                self.update_contacts_list()
                messagebox.showinfo("Success", f"Successfully imported {len(imported)} contacts")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import contacts: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedContactBook(root)
    root.mainloop()