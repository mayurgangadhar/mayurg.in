import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import yaml
import boto3
import subprocess
import re
import config


class Uploader:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("mayurg.in Bulk Uploader")

        self.root.geometry("700x420")

        self.root.resizable(False, False)

        self.pdf_paths = []

        self.build_ui()

        self.root.mainloop()


    def build_ui(self):

        tk.Label(
            self.root,
            text="mayurg.in Bulk Uploader",
            font=("Helvetica", 22, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            self.root,
            text="Upload multiple study resources",
            fg="gray"
        ).pack(pady=(0, 20))

        tk.Button(
            self.root,
            text="Choose PDFs",
            width=20,
            command=self.choose_pdfs
        ).pack()

        self.file_label = tk.Label(
            self.root,
            text="No PDFs Selected",
            fg="gray"
        )

        self.file_label.pack(pady=15)

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

        tk.Button(
            self.root,
            text="Upload",
            width=20,
            height=2,
            command=self.upload
        ).pack(pady=20)


    def choose_pdfs(self):

        files = filedialog.askopenfilenames(
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not files:
            return

        self.pdf_paths = list(files)

        self.file_label.config(
            text=f"{len(files)} PDF(s) Selected"
        )    

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


    def clean_filename(self, title):

        filename = title.lower()

        filename = filename.replace(" ", "-")

        filename = re.sub(r"[^a-z0-9-]", "", filename)

        filename = re.sub(r"-+", "-", filename)

        filename = filename.strip("-")

        return filename + ".pdf"


    def load_yaml(self, subject):

        yaml_file = (
            Path(__file__).resolve().parent.parent
            / "_data"
            / "resources"
            / f"{subject}.yml"
        )

        if yaml_file.exists():

            with open(
                yaml_file,
                "r",
                encoding="utf-8"
            ) as f:

                data = yaml.safe_load(f) or []

        else:

            data = []

        return yaml_file, data


    def save_yaml(self, yaml_file, data):

        with open(
            yaml_file,
            "w",
            encoding="utf-8"
        ) as f:

            yaml.dump(
                data,
                f,
                allow_unicode=True,
                sort_keys=False
            )   

    def git_push(self):

        repo = Path(__file__).resolve().parent.parent

        subprocess.run(["git", "add", "."], cwd=repo)

        subprocess.run(
            ["git", "commit", "-m", "Bulk upload resources"],
            cwd=repo
        )

        subprocess.run(["git", "push"], cwd=repo)


    def upload(self):

        if not self.pdf_paths:

            print("Choose PDFs first.")

            return

        subject = self.subject_var.get()

        section = self.section_var.get()

        yaml_file, data = self.load_yaml(subject)

        for pdf_path in self.pdf_paths:

            title = Path(pdf_path).stem

            filename = self.clean_filename(title)

            if section == "cases":

                remote_key = (
                    f"{subject}/practical/cases/{filename}"
                )

            else:

                remote_key = (
                    f"{subject}/{section}/{filename}"
                )

            try:

                url = self.upload_to_r2(
                    pdf_path,
                    remote_key
                )

                data.append({
                    "title": title,
                    "section": section,
                    "label": section.capitalize(),
                    "pdf": url
                })

                print(f"✓ Uploaded: {title}")

            except Exception as e:

                print(f"✗ Failed: {title}")

                print(e)

        self.save_yaml(
            yaml_file,
            data
        )

        self.git_push()

        self.file_label.config(
            text=f"Uploaded {len(self.pdf_paths)} PDF(s)"
        )

        print("Finished uploading all PDFs.")


if __name__ == "__main__":

    Uploader()