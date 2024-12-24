from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from datetime import datetime
from typing import List, Dict

class ConsoleUI:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.changes: List[Dict] = []
        
    def setup_layout(self):
        """Thiết lập layout cho giao diện"""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
    def create_header(self) -> Panel:
        """Tạo header của ứng dụng"""
        return Panel(
            "[bold green]Auto Commit[/bold green] - [yellow]File Watching System[/yellow]",
            style="blue",
            border_style="bright_blue",
        )
        
    def create_file_table(self) -> Table:
        """Tạo bảng hiển thị các thay đổi"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="bright_blue",
            title="Recent Changes"
        )
        
        table.add_column("Time", style="cyan", width=10)
        table.add_column("Type", style="green", width=10)
        table.add_column("File", style="blue")
        table.add_column("Status", style="yellow", width=10)
        
        # Hiển thị 10 thay đổi gần nhất
        for change in self.changes[-10:]:
            table.add_row(
                change["time"],
                change["type"],
                change["file"],
                change["status"]
            )
            
        return table
        
    def create_footer(self) -> Panel:
        """Tạo footer với thông tin trạng thái"""
        return Panel(
            f"[green]Active[/green] - Press Ctrl+C to exit - Watching changes: {len(self.changes)}",
            style="blue",
            border_style="bright_blue"
        )
        
    def add_change(self, file_path: str, change_type: str, status: str = "committed"):
        """Thêm một thay đổi mới vào danh sách"""
        self.changes.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": change_type,
            "file": str(file_path),
            "status": status
        })
        
    def update_display(self):
        """Cập nhật giao diện"""
        self.layout["header"].update(self.create_header())
        self.layout["main"].update(self.create_file_table())
        self.layout["footer"].update(self.create_footer())
        
    def start(self):
        """Khởi động giao diện"""
        self.setup_layout()
        with Live(self.layout, refresh_per_second=1, screen=True):
            while True:
                self.update_display() 