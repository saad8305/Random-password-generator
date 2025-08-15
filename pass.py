import secrets
import string
import tkinter as tk
from tkinter import messagebox

def gen_pass(length=12,use_lower=True,use_upper=True,use_digits=True,use_symbols=True,exclude_similar=True):
    if length<4:
        return "Password must be at least 4 characters!"
    lower=string.ascii_lowercase
    upper=string.ascii_uppercase
    digits=string.digits
    symbols="@#$^&*-?/"
    similar_chars="0Oo1lI"
    if exclude_similar:
        lower="".join(c for c in lower if c not in similar_chars)
        upper="".join(c for c in upper if c not in similar_chars)
        digits="".join(c for c in digits if c not in similar_chars)
    categories=[]
    if use_lower:categories.append(lower)
    if use_upper:categories.append(upper)
    if use_digits:categories.append(digits)
    if use_symbols:categories.append(symbols)
    if not categories:
        return "No character sets selected!"
    password=[secrets.choice(cat) for cat in categories]
    all_chars="".join(categories)
    password+=[secrets.choice(all_chars) for _ in range(length-len(password))]
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def save_passwords(passwords,filename="passwords.txt"):
    with open(filename,"w") as f:
        for pw in passwords:
            f.write(pw+"\n")
    messagebox.showinfo("Success",f"Passwords saved to {filename}")

def check_strength(password):
    if len(password)<8:
        return "Weak","red"
    has_lower=any(c.islower() for c in password)
    has_upper=any(c.isupper() for c in password)
    has_digit=any(c.isdigit() for c in password)
    has_symbol=any(c in "@#$^&*-?/" for c in password)
    if has_lower and has_upper and has_digit and has_symbol:
        return "Strong","green"
    elif (has_lower and has_upper) or (has_lower and has_digit) or (has_upper and has_digit):
        return "Medium","yellow"
    else:
        return "Weak","red"

def generate_passwords():
    try:
        length=int(length_entry.get())
        num_passwords=int(num_passwords_entry.get())
        use_lower=lower_var.get()
        use_upper=upper_var.get()
        use_digits=digits_var.get()
        use_symbols=symbols_var.get()
        exclude_similar=exclude_similar_var.get()
        if length<4:
            raise ValueError("Password length must be at least 4 characters.")
        passwords=[]
        for _ in range(num_passwords):
            pw=gen_pass(length,use_lower,use_upper,use_digits,use_symbols,exclude_similar)
            passwords.append(pw)
        output_text.delete(1.0,tk.END)
        for pw in passwords:
            output_text.insert(tk.END,pw+"\n")
            
        strength, color=check_strength(passwords[0])
        strength_label.config(text=f"Password Strength: {strength}",fg=color)
        if save_var.get():
            save_passwords(passwords)
    except ValueError as e:
        messagebox.showerror("Error",str(e))

root=tk.Tk()
root.title("Password Generator")
tk.Label(root,text="Password Length:").grid(row=0,column=0)
length_entry=tk.Entry(root)
length_entry.grid(row=0,column=1)
length_entry.insert(0,"12")
tk.Label(root,text="Number of Passwords:").grid(row=1,column=0)
num_passwords_entry=tk.Entry(root)
num_passwords_entry.grid(row=1,column=1)
num_passwords_entry.insert(0,"1")
lower_var=tk.BooleanVar(value=True)
tk.Checkbutton(root,text="Include Lowercase Letters",variable=lower_var).grid(row=2,columnspan=2,sticky="w")
upper_var=tk.BooleanVar(value=True)
tk.Checkbutton(root,text="Include Uppercase Letters",variable=upper_var).grid(row=3,columnspan=2,sticky="w")
digits_var=tk.BooleanVar(value=True)
tk.Checkbutton(root,text="Include Digits",variable=digits_var).grid(row=4,columnspan=2,sticky="w")
symbols_var=tk.BooleanVar(value=True)
tk.Checkbutton(root,text="Include Symbols",variable=symbols_var).grid(row=5,columnspan=2,sticky="w")
exclude_similar_var=tk.BooleanVar(value=True)
tk.Checkbutton(root,text="Exclude Similar Characters (e.g.,O0,l1)",variable=exclude_similar_var).grid(row=6,columnspan=2,sticky="w")
save_var=tk.BooleanVar(value=False)
tk.Checkbutton(root,text="Save passwords to file",variable=save_var).grid(row=7,columnspan=2,sticky="w")
generate_button=tk.Button(root,text="Generate Passwords",command=generate_passwords)
generate_button.grid(row=8,columnspan=2)
output_text=tk.Text(root,height=10,width=30)
output_text.grid(row=9,columnspan=2)
strength_label=tk.Label(root,text="Password Strength: ",font=("Arial",12))
strength_label.grid(row=10,columnspan=2)

root.mainloop()