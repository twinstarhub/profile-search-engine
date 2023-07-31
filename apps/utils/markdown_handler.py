from base64 import b64encode
from io import BytesIO

class MarkdownHandler:
    def __init__(self, filename: str):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, "w", encoding="utf-16")
        return self

    def __exit__(self, *args):
        self.file.close()

    def add_header(self, text: str, level: int = 1):
        """Add a header to the markdown file."""
        if level > 1:
            self.file.write("\n")
        self.file.write(f"{'#' * level} {text}\n")

    def write(self, text: str):
        """Write text to the markdown file."""
        self.file.write(text)

    def save_image(self, plt):
        """Save an image to the markdown file."""
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        img_data = b64encode(buffer.read()).decode()
        self.file.write(f"\n\n![image](data:image/png;base64,{img_data})\n")
        plt.clf()

    @staticmethod
    def list_to_markdown(items: list[str], flat=True):
        """Convert a list of items to a markdown list."""
        if flat:
            return "\n".join([f"- {item}" for item in items])
        num_items = len(items)
        if num_items == 0:
            return ""
        items = list(items)
        # Calculate the number of columns and rows to achieve a square-like layout
        num_columns = int(num_items**0.5)
        num_rows = (num_items + num_columns - 1) // num_columns

        # Convert NumPy array to a Python list and pad it with empty strings to make it rectangular
        items = list(items)
        items.extend([""] * (num_columns * num_rows - num_items))

        # Create the markdown table
        markdown_table = ""
        markdown_table = "| " + " | ".join([f" " for _ in range(num_columns)]) + " |\n"
        markdown_table += "| " + " | ".join([":---:" for _ in range(num_columns)]) + " |\n"
        for row in range(num_rows):
            markdown_table += "| " + " | ".join([f"{items[row + num_rows * col]}" for col in range(num_columns)]) + " |\n"

        return markdown_table

    @staticmethod
    def dict_to_table(data: dict[str, str]):
        """Convert a dictionary to a markdown table with keys as headers."""
        table = "<table>"
        table += "<tr><th>" + "</th><th>".join(data.keys()) + "</th></tr>"
        table += "<tr><td>" + "</td><td>".join(data.values()) + "</td></tr>"
        table += "</table>"
        return table
