import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime
from backend.config import get_config

# Load environment variables
config = get_config()

class CropAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("NewsLens Screenshot Crop Analyzer")
        
        # S3 client setup
        self.s3 = boto3.client('s3')
        self.bucket = config.get('S3_BUCKET_NAME')
        if not self.bucket:
            raise ValueError("S3_BUCKET_NAME environment variable not set")
        
        # Source configs
        self.sources = {
            'cnn': {'file': 'manual/2025-04-18/cnn.png', 'crop_top': 0},
            'fox': {'file': 'manual/2025-04-18/fox.png', 'crop_top': 0},
            'nytimes': {'file': 'manual/2025-04-18/nytimes.png', 'crop_top': 0},
            'usatoday': {'file': 'manual/2025-04-18/usatoday.png', 'crop_top': 0},
            'wapo': {'file': 'manual/2025-04-18/wapo.png', 'crop_top': 0}
        }
        
        self.current_source = None
        self.image = None
        self.photo = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Source selection
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Select Source:").grid(row=0, column=0, sticky=tk.W)
        self.source_var = tk.StringVar()
        source_combo = ttk.Combobox(frame, textvariable=self.source_var)
        source_combo['values'] = list(self.sources.keys())
        source_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        source_combo.bind('<<ComboboxSelected>>', self.load_source)
        
        # Crop controls
        ttk.Label(frame, text="Crop from top (px):").grid(row=1, column=0, sticky=tk.W)
        self.crop_var = tk.StringVar(value="0")
        crop_entry = ttk.Entry(frame, textvariable=self.crop_var)
        crop_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        ttk.Button(frame, text="Apply Crop", command=self.apply_crop).grid(row=1, column=2)
        ttk.Button(frame, text="Save Parameters", command=self.save_parameters).grid(row=1, column=3)
        
        # Preview
        self.canvas = tk.Canvas(frame, width=800, height=600)
        self.canvas.grid(row=2, column=0, columnspan=4, pady=10)
        
    def load_source(self, event=None):
        source = self.source_var.get()
        if not source:
            return
            
        self.current_source = source
        s3_key = self.sources[source]['file']
        
        # Download image from S3
        try:
            local_path = f"temp_{source}.png"
            self.s3.download_file(self.bucket, s3_key, local_path)
            
            # Load and display image
            self.image = Image.open(local_path)
            self.update_preview()
            
            # Clean up
            os.remove(local_path)
            
        except ClientError as e:
            print(f"Error downloading image: {e}")
            
    def apply_crop(self):
        if not self.image:
            return
            
        try:
            crop_px = int(self.crop_var.get())
            self.sources[self.current_source]['crop_top'] = crop_px
            self.update_preview()
        except ValueError:
            print("Invalid crop value")
            
    def update_preview(self):
        if not self.image:
            return
            
        # Apply crop
        crop_px = self.sources[self.current_source]['crop_top']
        cropped = self.image.crop((0, crop_px, self.image.width, self.image.height))
        
        # Resize to fit canvas
        display_size = (800, 600)
        cropped.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        # Update canvas
        self.photo = ImageTk.PhotoImage(cropped)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
    def save_parameters(self):
        # Save crop parameters to a JSON file
        params = {
            'timestamp': datetime.now().isoformat(),
            'sources': self.sources
        }
        
        with open('source_crop_params.json', 'w') as f:
            json.dump(params, f, indent=2)
        print("Saved crop parameters to source_crop_params.json")

def main():
    root = tk.Tk()
    app = CropAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 