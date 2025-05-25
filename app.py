import tkinter as tk
from tkinter import ttk
from markdown import markdown
import webbrowser
from pathlib import Path

class MarkdownViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Content Viewer")
        self.root.geometry("800x600")
        
        # Create buttons frame
        button_frame = ttk.Frame(root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create buttons
        ttk.Button(button_frame, text="Summary", command=self.show_summary).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Q&A", command=self.show_qna).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quiz", command=self.show_quiz).pack(side=tk.LEFT, padx=5)
        
        # Create content frame
        self.content_frame = ttk.Frame(root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create text widget for display
        self.text_widget = tk.Text(self.content_frame, wrap=tk.WORD, font=('Arial', 12))
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
    def show_markdown(self, file_path):
        try:
            # Read the file content
            with open(file_path, 'r') as file:
                content = file.read()
                
            # Clear previous content
            self.text_widget.delete(1.0, tk.END)
            
            # Insert new content
            self.text_widget.insert(tk.END, content)
            
            # Add markdown formatting
            self.text_widget.tag_configure('bold', font=('Arial', 12, 'bold'))
            self.text_widget.tag_configure('italic', font=('Arial', 12, 'italic'))
            self.text_widget.tag_configure('heading', font=('Arial', 14, 'bold'))
            
            # Process markdown content
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    self.text_widget.insert(tk.END, line[2:] + '\n', 'heading')
                elif line.startswith('## '):
                    self.text_widget.insert(tk.END, line[3:] + '\n', 'heading')
                elif line.startswith('* '):
                    self.text_widget.insert(tk.END, '• ' + line[2:] + '\n')
                else:
                    self.text_widget.insert(tk.END, line + '\n')
            
        except FileNotFoundError:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, f"File not found: {file_path}")
        except Exception as e:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, f"Error reading file: {str(e)}")
    
    def show_summary(self):
        self.show_markdown('output/relational_algebra_summary.txt')
    
    def show_qna(self):
        self.show_markdown('output/mit_oop_qna.txt')
    
    def show_quiz(self):
        self.show_markdown('output/mit_oop_quiz.txt')

def main():
    root = tk.Tk()
    app = MarkdownViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
