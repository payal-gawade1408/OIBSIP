import secrets
import string
import tkinter as tk
from tkinter import messagebox

AMBIGUOUS = set("0O1lI")


def generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    groups = []
    if use_upper:
        groups.append(string.ascii_uppercase)
    if use_lower:
        groups.append(string.ascii_lowercase)
    if use_digits:
        groups.append(string.digits)
    if use_symbols:
        groups.append("!@#$%^&*()-_=+[]{};:,.?/")

    if len(groups) < 2:
        raise ValueError("Select at least two character types.")
    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    if exclude_ambiguous:
        groups = ["".join(ch for ch in group if ch not in AMBIGUOUS) for group in groups]

    if any(not group for group in groups):
        raise ValueError("One selected character type has no usable characters.")

    # Guarantee at least one character from every selected group.
    chars = [secrets.choice(group) for group in groups]
    all_chars = "".join(groups)
    chars.extend(secrets.choice(all_chars) for _ in range(length - len(chars)))

    # Securely shuffle the characters.
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("620x620")
        self.root.configure(bg="#f3f7fb")
        self.history = []

        tk.Label(root, text="Secure Password Generator", font=("Arial", 20, "bold"),
                 bg="#f3f7fb", fg="#17324d").pack(pady=(18, 4))
        tk.Label(root, text="Create a strong password with your preferred rules",
                 font=("Arial", 10), bg="#f3f7fb", fg="#536779").pack(pady=(0, 14))

        panel = tk.Frame(root, bg="white", padx=18, pady=16, highlightbackground="#d8e2ec",
                         highlightthickness=1)
        panel.pack(fill="x", padx=24)

        tk.Label(panel, text="Password length (minimum 8):", bg="white",
                 font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=16)
        tk.Spinbox(panel, from_=8, to=128, textvariable=self.length_var, width=8,
                   font=("Arial", 11)).grid(row=0, column=1, sticky="w", padx=10, pady=8)

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_var = tk.BooleanVar(value=False)

        options = [
            ("Uppercase letters (A-Z)", self.upper_var),
            ("Lowercase letters (a-z)", self.lower_var),
            ("Numbers (0-9)", self.digits_var),
            ("Symbols (!@#$...)", self.symbols_var),
            ("Exclude ambiguous characters (0, O, 1, l, I)", self.exclude_var),
        ]
        for row, (label, variable) in enumerate(options, start=1):
            tk.Checkbutton(panel, text=label, variable=variable, bg="white",
                           font=("Arial", 10), activebackground="white").grid(
                               row=row, column=0, columnspan=2, sticky="w", pady=3)

        tk.Button(root, text="Generate Password", command=self.generate,
                  bg="#087f8c", fg="white", activebackground="#066b75",
                  font=("Arial", 11, "bold"), relief="flat", padx=18, pady=9).pack(pady=14)

        self.password_var = tk.StringVar(value="Your password will appear here")
        self.password_entry = tk.Entry(root, textvariable=self.password_var, justify="center",
                                       font=("Consolas", 13), width=42, state="readonly",
                                       readonlybackground="white", fg="#17324d")
        self.password_entry.pack(padx=20, pady=4, ipady=8)

        self.strength_label = tk.Label(root, text="Strength: —", bg="#f3f7fb",
                                       font=("Arial", 10, "bold"), fg="#536779")
        self.strength_label.pack(pady=4)

        buttons = tk.Frame(root, bg="#f3f7fb")
        buttons.pack()
        tk.Button(buttons, text="Copy", command=self.copy_password, width=12,
                  bg="#dbeafe", relief="flat", pady=6).grid(row=0, column=0, padx=5)
        tk.Button(buttons, text="Generate Again", command=self.generate, width=14,
                  bg="#dbeafe", relief="flat", pady=6).grid(row=0, column=1, padx=5)

        tk.Label(root, text="Recent passwords (session only)", bg="#f3f7fb",
                 font=("Arial", 11, "bold"), fg="#17324d").pack(pady=(14, 5))
        self.history_box = tk.Listbox(root, height=5, width=55, font=("Consolas", 9))
        self.history_box.pack(padx=20, pady=(0, 14))

        tk.Label(root, text="Security note: passwords are not saved to a file.",
                 bg="#f3f7fb", fg="#536779", font=("Arial", 9)).pack(pady=(0, 10))

    def generate(self):
        try:
            password = generate_password(
                int(self.length_var.get()), self.upper_var.get(), self.lower_var.get(),
                self.digits_var.get(), self.symbols_var.get(), self.exclude_var.get()
            )
        except (ValueError, tk.TclError) as exc:
            messagebox.showerror("Invalid settings", str(exc) or "Enter a valid length.")
            return

        self.password_var.set(password)
        self.strength_label.config(text=f"Strength: {self.get_strength(password)}")
        self.history.insert(0, password)
        self.history = self.history[:5]
        self.history_box.delete(0, tk.END)
        for item in self.history:
            self.history_box.insert(tk.END, item)

    @staticmethod
    def get_strength(password):
        variety = sum([
            any(c.islower() for c in password),
            any(c.isupper() for c in password),
            any(c.isdigit() for c in password),
            any(not c.isalnum() for c in password),
        ])
        if len(password) >= 16 and variety >= 3:
            return "Strong"
        if len(password) >= 10 and variety >= 2:
            return "Medium"
        return "Weak"

    def copy_password(self):
        password = self.password_var.get()
        if not password or password.startswith("Your password"):
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
