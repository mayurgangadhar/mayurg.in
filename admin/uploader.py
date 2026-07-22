import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import yaml
import boto3
import subprocess
import config


class Uploader:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("mayurg.in Uploader")

        self.root.geometry("700x500")

        self.root.resizable(False, False)

        self.pdf_path = ""

        self.build_ui()

        self.root.mainloop()

    def build_ui(self):

        tk.Label(
            self.root,
            text="mayurg.in Uploader",
            font=("Helvetica", 22, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            self.root,
            text="Upload study resources",
            fg="gray"
        ).pack(pady=(0, 20))

        tk.Button(
            self.root,
            text="Choose PDF",
            command=self.choose_pdf,
            width=20
        ).pack()

        self.file_label = tk.Label(
            self.root,
            text="No PDF Selected",
            fg="gray"
        )

        self.file_label.pack(pady=15)

        tk.Label(
            self.root,
            text="Title"
        ).pack()

        self.title_entry = tk.Entry(
            self.root,
            width=60
        )

        self.title_entry.pack(pady=10)

        tk.Label(
            self.root,
            text="Subject"
        ).pack()

        self.subject_var = tk.StringVar()

        self.subject_var.set("ent")

        tk.OptionMenu(
            self.root,
            self.subject_var,
            "ent",
            "medicine",
            "surgery",
            "ophthalmology",
            "orthopedics",
            "obg",
            "paediatrics"
        ).pack(pady=10)

        tk.Label(
            self.root,
            text="Section"
        ).pack()

        self.section_var = tk.StringVar()

        self.section_var.set("theory")

        tk.OptionMenu(
           self.root,
           self.section_var,
           "theory",
           "practical",
           "cases"
        ).pack(pady=10)

        self.upload_button = tk.Button(
            self.root,
            text="Upload Resource",
            width=20,
            height=2,
            command=self.upload
        )

        self.upload_button.pack(pady=20)

    def choose_pdf(self):

        file = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not file:
            return

        self.pdf_path = file

        filename = Path(file).name

        self.file_label.config(text=filename)

        title = Path(file).stem

        title = title.replace("_", " ")
        title = title.replace("-", " ")

        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, title)
    
    def upload(self):

        if self.pdf_path == "":

            print("Choose a PDF first.")
            return

        title = self.title_entry.get().strip()

        subject = self.subject_var.get()

        section = self.section_var.get()

        filename = title.lower()
        filename = filename.replace(" ", "-")
        filename = filename.replace("'", "")

        filename += ".pdf"

        if section == "cases":
          remote_key = f"{subject}/practical/cases/{filename}"
        else:
          remote_key = f"{subject}/{section}/{filename}"

        try:

            url = self.upload_to_r2(
                self.pdf_path,
                remote_key
            )

            print("✅ Uploaded Successfully!")

            print(url)

        except Exception as e:

            print(e)

    def upload_to_r2(self, local_file, remote_key):

        s3 = boto3.client(
            "s3",
            endpoint_url=f"https://{config.ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=config.ACCESS_KEY_ID,
            aws_secret_access_key=config.SECRET_ACCESS_KEY,
            region_name="auto"
        )

        s3.upload_file(
            local_file,
            config.BUCKET_NAME,
            remote_key,
            ExtraArgs={
                "ContentType": "application/pdf"
            }
        )

        return f"{config.CUSTOM_DOMAIN}/{remote_key}"
    
    def update_yaml(self, title, subject, section, url):

        yaml_file = Path(__file__).resolve().parent.parent / "_data" / "resources" / f"{subject}.yml"

        if yaml_file.exists():

            with open(yaml_file, "r", encoding="utf-8") as f:

                data = yaml.safe_load(f) or []

        else:

            data = []

        data.append({

            "title": title,

            "section": section,

            "label": section.capitalize(),

            "pdf": url

        })

        with open(yaml_file, "w", encoding="utf-8") as f:

            yaml.dump(
                data,
                f,
                allow_unicode=True,
                sort_keys=False
            )

    def git_push(self):

        subprocess.run(
            ["git", "add", "."],
            cwd=Path(__file__).resolve().parent.parent
        )

        subprocess.run(
            ["git", "commit", "-m", "Add new study resource"],
            cwd=Path(__file__).resolve().parent.parent
        )

        subprocess.run(
            ["git", "push"],
            cwd=Path(__file__).resolve().parent.parent
        )
    def upload(self):

        if self.pdf_path == "":
            print("Choose a PDF first.")
            return

        title = self.title_entry.get().strip()

        subject = self.subject_var.get()

        section = self.section_var.get()

        filename = (
            title.lower()
            .replace(" ", "-")
            .replace("'", "")
        ) + ".pdf"

        remote_key = f"{subject}/{section}/{filename}"

        try:

            url = self.upload_to_r2(
                self.pdf_path,
                remote_key
            )

            self.update_yaml(
                title,
                subject,
                section,
                url
            )

            self.git_push()

            print("Uploaded Successfully!")

            print(url)

        except Exception as e:

            print(e)


Uploader()