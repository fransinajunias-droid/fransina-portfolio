import flet as ft
import os
import shutil
from pathlib import Path
import warnings

# Suppress harmless Flet framework deprecation warnings from cluttering the terminal
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ---------- MODERN DESIGN TOKENS ----------
BG = "#0B0813"           # Deep slate midnight blue/purple background
CARD_BG = "#161224"      # Dark elevated card container background
PRIMARY = "#9D4EDD"     # Neon violet accent for chips, highlights, primary buttons
TEXT = "#F4F1DE"        # Crisp off-white for strong headers and main text
SUBTEXT = "#A0A0B0"     # Soft muted gray-purple for secondary body copy


# ---------- CERTIFICATE MANAGER ----------
class CertificateManager:
    def __init__(self, cert_dir="assets/certs"):
        self.cert_dir = Path(cert_dir)
        self.ensure_cert_dir()
    
    def ensure_cert_dir(self):
        """Create certificates directory if it doesn't exist"""
        if not self.cert_dir.exists():
            self.cert_dir.mkdir(parents=True, exist_ok=True)
    
    def download_certificate(self, filename, download_path=None):
        """Download certificate to user's Downloads folder"""
        cert_path = self.cert_dir / filename
        
        if not cert_path.exists():
            return False, f"File '{filename}' not found."
        
        if download_path is None:
            download_path = Path.home() / "Downloads"
        else:
            download_path = Path(download_path)
        
        try:
            dest_path = download_path / filename
            shutil.copy2(str(cert_path), str(dest_path))
            return True, f"Downloaded to {dest_path}"
        except Exception as e:
            return False, str(e)


# ---------- HELPERS ----------
def section_title(title):
    return ft.Text(
        title,
        size=24,
        weight=ft.FontWeight.BOLD,
        color=TEXT,
    )


def skill_chip(skill):
    return ft.Container(
        content=ft.Text(skill, color="white", weight=ft.FontWeight.W_500, size=13),
        bgcolor=PRIMARY,
        border_radius=8,
        padding=ft.Padding(left=14, right=14, top=6, bottom=6),
    )


def certificate_card(title, filename, cert_manager, page):
    """Certificate card with integrated open and download functionality"""
    
    async def handle_download(e):
        success, message = cert_manager.download_certificate(filename)
        snack = ft.SnackBar(
            ft.Text(message, color="white"),
            bgcolor="#2D6A4F" if success else "#A4161A"
        )
        page.overlay.append(snack)
        snack.open = True
        await page.update_async() if hasattr(page, 'update_async') else page.update()
        
    async def handle_open(e):
        local_file = (Path("assets") / "certs" / filename).resolve()
        
        if local_file.exists():
            try:
                os.startfile(str(local_file))
            except Exception:
                await page.launch_url(local_file.as_uri())
        else:
            snack = ft.SnackBar(
                ft.Text(f"Error: '{filename}' not found in assets/certs/", color="white"),
                bgcolor="#A4161A"
            )
            page.overlay.append(snack)
            snack.open = True
            await page.update_async() if hasattr(page, 'update_async') else page.update()
    
    return ft.Container(
        bgcolor=BG,
        border_radius=12,
        padding=20,
        width=240,
        border=ft.Border.all(1, "#251F3D"),
        content=ft.Column(
            [
                ft.Icon(
                    ft.Icons.PICTURE_AS_PDF,
                    size=40,
                    color="#E63946",
                ),
                ft.Text(
                    title,
                    color=TEXT,
                    weight=ft.FontWeight.W_600,
                    text_align=ft.TextAlign.CENTER,
                    size=14,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Column(
                    [
                        ft.ElevatedButton(
                            "Open",
                            icon=ft.Icons.OPEN_IN_NEW,
                            on_click=handle_open,
                            style=ft.ButtonStyle(
                                color="white",
                                bgcolor="#251F3D",
                                overlay_color=PRIMARY,
                                shape=ft.RoundedRectangleBorder(radius=6)
                            ),
                            width=180,
                        ),
                        ft.ElevatedButton(
                            "Download",
                            icon=ft.Icons.DOWNLOAD,
                            on_click=handle_download,
                            style=ft.ButtonStyle(
                                color="white",
                                bgcolor="#251F3D",
                                overlay_color=PRIMARY,
                                shape=ft.RoundedRectangleBorder(radius=6)
                            ),
                            width=180,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
        ),
    )


def project_card(page):
    """
    Project card embedding an interactive video presentation player.
    Uses dynamic absolute path resolution to guarantee Windows launches the file.
    """
    status_text = ft.Text("Ready to play walkthrough", color=SUBTEXT, size=13)
    
    async def play_embedded_video(e):
        status_text.value = "Opening presentation walkthrough..."
        status_text.color = PRIMARY
        await page.update_async() if hasattr(page, 'update_async') else page.update()
        
        try:
            # 1. Locate the exact directory where app.py is running on your machine
            base_path = Path(__file__).parent.resolve()
            
            # 2. Build the absolute Windows path directly to the video asset file
            absolute_video_path = base_path / "assets" / "projects" / "VID-20260614-WA0037.mp4"
            
            if absolute_video_path.exists():
                # 3. Force Windows to launch it via system shell
                os.startfile(str(absolute_video_path))
                status_text.value = "Playing presentation walkthrough"
                status_text.color = "#2D6A4F"  # Success green
            else:
                status_text.value = f"Error: Video file missing from absolute path:\n{absolute_video_path}"
                status_text.color = "#A4161A"
                
        except Exception as ex:
            status_text.value = f"System Error: {str(ex)}"
            status_text.color = "#A4161A"
            
        await page.update_async() if hasattr(page, 'update_async') else page.update()

    return ft.Container(
        bgcolor=BG,
        border_radius=12,
        padding=25,
        border=ft.Border.all(1, "#251F3D"),
        content=ft.Column(
            [
                ft.Text(
                    "Design & Implementation Walkthrough",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT,
                ),
                ft.Text(
                    "This section showcases my semester project development, system configurations, "
                    "and practical engineering results. Click the interactive media frame below to watch.",
                    color=SUBTEXT,
                    size=14,
                    style=ft.TextStyle(height=1.4)
                ),
                ft.Container(height=10), 
                
                # ---------- VIDEO TRIGGER CANVAS ----------
                ft.Container(
                    bgcolor="#05030A",
                    border_radius=10,
                    height=240,
                    alignment=ft.alignment.Alignment(0, 0), 
                    on_click=play_embedded_video,
                    border=ft.Border.all(1, "#332954"),
                    content=ft.Stack(
                        [
                            ft.Container(
                                alignment=ft.alignment.Alignment(0, 0),
                                content=ft.Column(
                                    [
                                        ft.Icon(
                                            ft.Icons.ONDEMAND_VIDEO_ROUNDED,
                                            size=64,
                                            color=PRIMARY
                                        ),
                                        ft.Text(
                                            "Click to Play Presentation",
                                            color=TEXT,
                                            size=14,
                                            weight=ft.FontWeight.W_600
                                        ),
                                        status_text
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=10
                                )
                            ),
                        ]
                    )
                ),
            ],
            spacing=10
        ),
    )


# ---------- MAIN APP ----------
async def main(page: ft.Page):
    page.title = "Fransina Junias Portfolio"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.scroll = ft.ScrollMode.AUTO
    page.padding = ft.Padding(left=40, right=40, top=30, bottom=30)

    cert_manager = CertificateManager()

    certificate_data = [
        ("Desktop and Troubleshooting", "certificate DESKTOP AND TROUBLESHOOTING.pdf"),
        ("Explore Data", "certificate explore data.pdf"),
        ("Calculations with Vectors and Matrices", "certificate for calculations with vectors and matrices.pdf"),
        ("Make and Manipulate Arrays", "certificate make and manipulate.pdf"),
        ("Simulink", "simulink onramp.pdf"),
        ("Machine Learning", "machine learning certificate.pdf"),
        ("MATLAB Onramp", "MATLAB onramp certificate.pdf"),
        ("Simulink Lab Manual", "Simulink_Lab_Manual.pdf"),
    ]

    # ---------- HERO ----------
    hero = ft.Container(
        bgcolor=CARD_BG,
        border_radius=16,
        padding=40,
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "WELCOME TO MY PORTFOLIO",
                            size=12,
                            color=PRIMARY,
                            weight=ft.FontWeight.W_700,
                            style=ft.TextStyle(letter_spacing=1.5)
                        ),
                        ft.Text(
                            "FRANSINA JUNIAS",
                            size=38,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT,
                        ),
                        ft.Text(
                            "Electrical Engineering Student",
                            size=18,
                            color=SUBTEXT,
                        ),
                    ],
                    expand=True,
                    spacing=6
                ),
                ft.CircleAvatar(
                    foreground_image_src="profile/profile.jpg",
                    radius=65,
                    bgcolor=PRIMARY
                ),
            ]
        ),
    )

    # ---------- ABOUT ----------
    about = ft.Container(
        bgcolor=CARD_BG,
        border_radius=16,
        padding=30,
        content=ft.Column(
            [
                section_title("About Me"),
                ft.Text(
                    "I am Fransina Junias, an Electrical Engineering student at the University of Namibia. "
                    "My interests include MATLAB, Python programming, engineering calculations, "
                    "power systems analysis and software development.",
                    color=SUBTEXT,
                    size=15,
                    style=ft.TextStyle(height=1.5)
                ),
            ],
            spacing=12
        ),
    )

    # ---------- SKILLS ----------
    skills = ft.Container(
        bgcolor=CARD_BG,
        border_radius=16,
        padding=30,
        content=ft.Column(
            [
                section_title("Skills"),
                ft.Row(
                    [
                        skill_chip("Python"),
                        skill_chip("MATLAB"),
                        skill_chip("Simulink"),
                        skill_chip("Engineering Maths"),
                        skill_chip("Problem Solving"),
                    ],
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                ),
            ],
            spacing=16
        ),
    )

    # ---------- CERTIFICATES ----------
    cards = [certificate_card(title, fname, cert_manager, page) for title, fname in certificate_data]
    
    certificates = ft.Container(
        bgcolor=CARD_BG,
        border_radius=16,
        padding=30,
        content=ft.Column(
            [
                section_title("Certificates"),
                ft.Row(
                    controls=cards,
                    wrap=True,
                    spacing=15,
                    run_spacing=15,
                )
            ],
            spacing=16
        )
    )

    # ---------- PROJECT ----------
    project = ft.Container(
        bgcolor=CARD_BG,
        border_radius=16,
        padding=30,
        content=ft.Column(
            [
                section_title("Semester Project"),
                project_card(page),
            ],
            spacing=16
        ),
    )

    # ---------- TIMELINE ----------
    timeline = ft.Container(
        bgcolor=CARD_BG,
        border_radius=16,
        padding=30,
        content=ft.Column(
            [
                section_title("Project Timeline"),
                ft.Column([
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=PRIMARY, size=18), ft.Text("Week 1 - Started MATLAB coursework", color=SUBTEXT, size=14)]),
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=PRIMARY, size=18), ft.Text("Week 2 - Completed MATLAB Onramp", color=SUBTEXT, size=14)]),
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=PRIMARY, size=18), ft.Text("Week 4 - Started semester project", color=SUBTEXT, size=14)]),
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=PRIMARY, size=18), ft.Text("Week 8 - Implemented project features", color=SUBTEXT, size=14)]),
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=PRIMARY, size=18), ft.Text("Week 10 - Developed portfolio website", color=SUBTEXT, size=14)]),
                ], spacing=10)
            ],
            spacing=16
        ),
    )

    # ---------- CONTACT ----------
    contact = ft.Container(
        bgcolor=CARD_BG,
        border_radius=16,
        padding=30,
        content=ft.Column(
            [
                section_title("Contact"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.EMAIL, color=PRIMARY),
                    title=ft.Text("fransinajunias@gmail.com", color=TEXT, size=14),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PHONE, color=PRIMARY),
                    title=ft.Text("+264 81 5634670", color=TEXT, size=14),
                ),
            ],
            spacing=10
        ),
    )

    # ---------- APP STRUCTURE LAYOUT ----------
    page.add(
        ft.Column(
            [
                hero,
                about,
                skills,
                certificates,
                project,
                timeline,
                contact,
            ],
            spacing=20,
        )
    )


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")