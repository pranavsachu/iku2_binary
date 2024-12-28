from tkinter import Tk, Button, Label, StringVar, Entry, Frame, messagebox, PhotoImage
from camera import start_camera, start_training
from credits import get_credits
from database import initialize_db, register_user, validate_user, get_user_credits

# Initialize the database
initialize_db()

class IKUApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project IKU")
        self.root.geometry("800x400")
        self.root.configure(bg="black")  # Set background color to black

        # Load the GIF frames and initialize GIF-related attributes
        self.gif_frames = self.load_gif("logo.gif")
        self.gif_index = 0  # Initialize the GIF index

        # Frames
        self.login_frame = Frame(root, bg="black")
        self.main_frame = Frame(root, bg="black")

        # Initialize frames
        self.create_login_frame()
        self.create_main_frame()

        # Show login frame initially
        self.show_frame(self.login_frame)

    def load_gif(self, gif_path):
        """Load all frames of a GIF for animation."""
        frames = []
        try:
            gif = PhotoImage(file=gif_path, format="gif -index 0")
            while True:
                frames.append(gif.copy())
                gif.configure(format=f"gif -index {len(frames)}")
        except Exception:
            pass  # End of GIF frames
        return frames

    def update_gif(self, label):
        """Update the GIF animation in the specified label."""
        if self.gif_frames:
            frame = self.gif_frames[self.gif_index]
            label.config(image=frame)
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)  # Loop through frames
            self.root.after(54, self.update_gif, label)  # Adjust speed by changing the delay (100 ms)

    def create_logo(self, parent_frame):
        """Create and display the logo GIF in the parent frame."""
        logo_label = Label(parent_frame, bg="black")
        logo_label.pack(side="left", padx=10, pady=10)  # Position the logo in the left corner
        self.update_gif(logo_label)

    def create_login_frame(self):
        """Create the login frame."""
        self.create_logo(self.login_frame)

        Label(self.login_frame, text="Login", font=("Arial", 16), bg="black", fg="white").pack(pady=20)

        Label(self.login_frame, text="Username", bg="black", fg="white").pack()
        self.username_entry = Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        Label(self.login_frame, text="Password", bg="black", fg="white").pack()
        self.password_entry = Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        Button(self.login_frame, text="Login", command=self.login, width=20).pack(pady=5)
        Button(self.login_frame, text="Register", command=self.register, width=20).pack()

    def create_main_frame(self):
        """Create the main frame."""
        self.create_logo(self.main_frame)

        Label(self.main_frame, text="Project IKU", font=("Arial", 16), bg="black", fg="white").pack(pady=20)

        self.credits_label = StringVar()
        self.credits_label.set("Credits: 0 IKUs")
        Label(self.main_frame, textvariable=self.credits_label, font=("Arial", 12), bg="black", fg="white").pack(pady=10)

        Button(self.main_frame, text="Start Camera", command=self.on_start, width=20).pack(pady=10)
        Button(self.main_frame, text="Train", command=self.on_train, width=20).pack(pady=10)

        Button(self.main_frame, text="Logout", command=self.logout, width=20).pack(pady=10)

    def show_frame(self, frame):
        """Show the specified frame."""
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()
        frame.pack(fill="both", expand=True)

    def login(self):
        """Handle the login process."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = validate_user(username, password)
        if user:
            self.user_id = user[0]  # Save the logged-in user's ID
            self.show_frame(self.main_frame)
            self.update_credits_label()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        """Handle the registration process."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Registration Success", "User registered successfully!")
        else:
            messagebox.showerror("Registration Failed", "Username already exists.")

    def on_start(self):
        """Start the camera."""
        start_camera()

    def on_train(self):
        """Start the training process."""
        start_training(self.user_id)
        self.update_credits_label()

    def logout(self):
        """Log out the current user."""
        self.show_frame(self.login_frame)

    def update_credits_label(self):
        """Update the credits label with the user's credits."""
        credits = get_user_credits(self.user_id)
        self.credits_label.set(f"Credits: {credits} IKUs")

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = IKUApp(root)
    root.mainloop()