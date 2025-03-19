import asyncio
import json
import os
import random
import time
import datetime
import webbrowser
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.layout import Layout
from rich.live import Live
from rich.columns import Columns
from rich import box
from g4f.client import Client

# ============= CONFIGURATION =============
CONFIG = {
    "models": {
        # Text models
        "claude-3.7-sonnet": {"name": "Claude 3.7 Sonnet", "color": "bright_green", "type": "text"},
        "gpt-4o": {"name": "GPT-4o", "color": "bright_blue", "type": "text"},
        "gemini-1.5-pro": {"name": "Gemini 1.5 Pro", "color": "bright_magenta", "type": "text"},
        "deepseek-v3": {"name": "DeepSeek V3", "color": "bright_cyan", "type": "text"},
        "mixtral-small-28b": {"name": "Mixtral Small 28B", "color": "bright_yellow", "type": "text"},
        "llama-3.1-405b": {"name": "Llama 3.1 405B", "color": "bright_red", "type": "text"},
        "o3-mini": {"name": "O3 Mini", "color": "bright_white", "type": "text"},
        "phi-4": {"name": "Phi-4", "color": "bright_blue", "type": "text"},
        "blackboxai-pro": {"name": "BlackBox AI Pro", "color": "bright_black", "type": "text"},
        "command-r-plus": {"name": "Command R+", "color": "bright_green", "type": "text"},
        "qwq-32b": {"name": "QWQ 32B", "color": "bright_magenta", "type": "text"},
        "glm-4": {"name": "GLM-4", "color": "bright_cyan", "type": "text"},
        "minicpm-2.5": {"name": "MiniCPM 2.5", "color": "bright_yellow", "type": "text"},
        "dolphin-2.9": {"name": "Dolphin 2.9", "color": "bright_blue", "type": "text"},
        "dbrx-instruct": {"name": "DBRX Instruct", "color": "bright_red", "type": "text"},
        "o1-mini": {"name": "O1 Mini", "color": "bright_white", "type": "text"},
        "o1": {"name": "O1", "color": "bright_green", "type": "text"},
        
        # Image models
        "dall-e-3": {"name": "DALL-E 3", "color": "bright_magenta", "type": "image"},
        "dall-e-2": {"name": "DALL-E 2", "color": "bright_blue", "type": "image"},
        "midjourney": {"name": "Midjourney", "color": "bright_cyan", "type": "image"},
        "stable-diffusion-3": {"name": "Stable Diffusion 3", "color": "bright_yellow", "type": "image"},
        "playground-v2": {"name": "Playground v2", "color": "bright_green", "type": "image"}
    },
    "default_model": "claude-3.7-sonnet",
    "default_image_model": "dall-e-3",
    "typing_speed": {"min": 0.005, "max": 0.02},
    "max_history": 100,
    "timeout": 600,
    "session_dir": "chat_sessions",
    "image_dir": "generated_images",
    "theme": {
        "user_color": "bright_cyan",
        "bot_color": "bright_green",
        "system_color": "bright_yellow",
        "error_color": "bright_red",
        "highlight_color": "bright_magenta",
        "border_color": "blue",
        "image_color": "bright_green",
        "title_color": "bright_red",
        "search_color": "bright_blue"
    }
}

# Initialize Rich console
console = Console()
client = Client()
conversation_history = []
current_model = CONFIG["default_model"]
current_image_model = CONFIG["default_image_model"]
session_name = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
web_search_enabled = False  # Track whether web search is enabled

# System prompts
SYSTEM_PROMPTS = {
    "concise": """Hãy trả lời ngắn gọn nhất có thể, cần đảm bảo không nói dài dòng, lan man, trả lời tập trung vào các ý chính.""",
    "detailed": """Hãy trả lời chi tiết, đầy đủ và có cấu trúc rõ ràng. Nếu cần thiết, hãy liệt kê các bước hoặc chia thành các phần.""",
    "creative": """Hãy trả lời một cách sáng tạo, độc đáo và thú vị. Có thể sử dụng ví dụ, phép so sánh hoặc cách tiếp cận mới lạ.""",
    "expert": """Hãy trả lời với tư cách là một chuyên gia trong lĩnh vực này. Cung cấp thông tin chuyên sâu, chính xác và cập nhật nhất.""",
    "friendly": """Hãy trả lời với giọng điệu thân thiện, gần gũi và dễ hiểu. Sử dụng ngôn ngữ đơn giản và ví dụ thực tế.""",
    "custom": """Prompt tùy chỉnh của người dùng."""
}
current_prompt_style = "concise"
custom_prompt = "Hãy trả lời một cách hữu ích và chính xác."

# ============= UTILITY FUNCTIONS =============
def ensure_directories():
    """Ensure all required directories exist"""
    for directory in [CONFIG["session_dir"], CONFIG["image_dir"]]:
        if not os.path.exists(directory):
            os.makedirs(directory)

async def typing_effect(text: str, min_delay: float = None, max_delay: float = None):
    """Create a typing effect with random delays between characters"""
    min_delay = min_delay or CONFIG["typing_speed"]["min"] /    2
    max_delay = max_delay or CONFIG["typing_speed"]["max"] /    2
    
    # Process markdown formatting for code blocks
    in_code_block = False
    buffer = ""
    i = 0
    
    while i < len(text):
        if i + 2 < len(text) and text[i:i+3] == "```":
            # Toggle code block state and print the buffer
            in_code_block = not in_code_block
            buffer += "```"
            i += 3
            if len(buffer) > 3:  # Don't print empty buffer
                console.print(buffer, end="", style=CONFIG["theme"]["bot_color"])
                await asyncio.sleep(random.uniform(min_delay, max_delay))
            buffer = ""
            continue
            
        if in_code_block:
            # Collect code block content
            buffer += text[i]
            i += 1
            if i < len(text) and (text[i:i+3] == "```" or i == len(text) - 1):
                console.print(buffer, end="", style="bright_white")
                buffer = ""
                await asyncio.sleep(0.001)  # Minimal delay for code blocks
        else:
            # Normal text typing effect
            console.print(text[i], end="", style=CONFIG["theme"]["bot_color"])
            await asyncio.sleep(random.uniform(min_delay, max_delay))
            i += 1
            
    console.print()

async def get_bot_response(messages: List[Dict[str, str]]) -> str:
    """Get response from the bot with improved error handling and timeout"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn(f"[{CONFIG['theme']['highlight_color']}]AI đang suy nghĩ..."),
            transient=True
        ) as progress:
            task = progress.add_task("", total=None)
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    client.chat.completions.create,
                    model=current_model,
                    messages=messages,
                    web_search=web_search_enabled  # Use the web_search_enabled flag
                ),
                timeout=CONFIG["timeout"]
            )
        return response.choices[0].message.content
    except asyncio.TimeoutError:
        return f"⚠️ Rất tiếc, phản hồi mất quá nhiều thời gian (>{CONFIG['timeout']}s). Vui lòng thử lại với câu hỏi ngắn hơn hoặc đổi model khác."
    except Exception as e:
        return f"⚠️ Lỗi khi gọi API: {str(e)}. Vui lòng thử lại sau."

async def generate_image(prompt: str, model: str = None) -> Dict:
    """Generate an image using the specified model"""
    if model is None:
        model = current_image_model
        
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn(f"[{CONFIG['theme']['highlight_color']}]Đang tạo hình ảnh..."),
            transient=True
        ) as progress:
            task = progress.add_task("", total=None)
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    client.images.generate,
                    model=model,
                    prompt=prompt,
                    response_format="url"
                ),
                timeout=600  # Images can take longer
            )
        
        # Save image metadata
        ensure_directories()
        image_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "model": model,
            "prompt": prompt,
            "url": response.data[0].url
        }
        
        # Generate a unique filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}.json"
        file_path = os.path.join(CONFIG["image_dir"], filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(image_data, f, ensure_ascii=False, indent=2)
            
        return {
            "success": True,
            "url": response.data[0].url,
            "file_path": file_path
        }
    except asyncio.TimeoutError:
        return {
            "success": False,
            "error": f"Tạo hình ảnh mất quá nhiều thời gian (>60s). Vui lòng thử lại với prompt ngắn hơn hoặc đổi model khác."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Lỗi khi tạo hình ảnh: {str(e)}. Vui lòng thử lại sau."
        }

def save_session(name: Optional[str] = None):
    """Save the current conversation to a file"""
    ensure_directories()
    
    if name is None:
        name = session_name
    
    session_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "model": current_model,
        "prompt_style": current_prompt_style,
        "custom_prompt": custom_prompt if current_prompt_style == "custom" else "",
        "web_search_enabled": web_search_enabled,  # Save web search setting
        "history": conversation_history
    }
    
    file_path = os.path.join(CONFIG["session_dir"], f"{name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    
    return file_path

def load_session(name: str):
    """Load a conversation from a file"""
    global conversation_history, current_model, current_prompt_style, custom_prompt, session_name, web_search_enabled
    
    file_path = os.path.join(CONFIG["session_dir"], f"{name}.json")
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, "r", encoding="utf-8") as f:
        session_data = json.load(f)
    
    conversation_history = session_data.get("history", [])
    current_model = session_data.get("model", CONFIG["default_model"])
    current_prompt_style = session_data.get("prompt_style", "concise")
    if current_prompt_style == "custom":
        custom_prompt = session_data.get("custom_prompt", "")
    web_search_enabled = session_data.get("web_search_enabled", False)  # Load web search setting
    session_name = name
    
    return True

def list_sessions():
    """List all saved sessions"""
    ensure_directories()
    
    sessions = []
    for file in os.listdir(CONFIG["session_dir"]):
        if file.endswith(".json"):
            file_path = os.path.join(CONFIG["session_dir"], file)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    sessions.append({
                        "name": file[:-5],
                        "timestamp": data.get("timestamp", "Unknown"),
                        "model": data.get("model", "Unknown"),
                        "messages": len(data.get("history", [])) // 2
                    })
                except:
                    pass
    
    return sorted(sessions, key=lambda x: x["timestamp"], reverse=True)

def list_images():
    """List all saved image metadata"""
    ensure_directories()
    
    images = []
    for file in os.listdir(CONFIG["image_dir"]):
        if file.endswith(".json"):
            file_path = os.path.join(CONFIG["image_dir"], file)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    images.append({
                        "name": file[:-5],
                        "timestamp": data.get("timestamp", "Unknown"),
                        "model": data.get("model", "Unknown"),
                        "prompt": data.get("prompt", "Unknown"),
                        "url": data.get("url", "Unknown")
                    })
                except:
                    pass
    
    return sorted(images, key=lambda x: x["timestamp"], reverse=True)

# ============= UI COMPONENTS =============
async def display_welcome():
    """Display a welcome message with enhanced styling"""
    console.clear()
    
    # Create cool title
    title_text = Text()
    title_text.append("╔═══════════════════════════════════════════╗\n", style=CONFIG["theme"]["title_color"])
    title_text.append("║                                           ║\n", style=CONFIG["theme"]["title_color"])
    title_text.append("║   ", style=CONFIG["theme"]["title_color"])
    title_text.append("⚡ TANBAYCU AI COMMANDER ⚡", style="bold bright_white")
    title_text.append("   ║\n", style=CONFIG["theme"]["title_color"])
    title_text.append("║                                           ║\n", style=CONFIG["theme"]["title_color"])
    title_text.append("╚═══════════════════════════════════════════╝", style=CONFIG["theme"]["title_color"])
    
    # Create model info
    model_info = Text.assemble(
        ("Model văn bản: ", CONFIG["theme"]["system_color"]),
        (CONFIG["models"][current_model]["name"], CONFIG["models"][current_model]["color"]),
        ("\nModel hình ảnh: ", CONFIG["theme"]["system_color"]),
        (CONFIG["models"][current_image_model]["name"], CONFIG["models"][current_image_model]["color"]),
        ("\nPhong cách: ", CONFIG["theme"]["system_color"]),
        (current_prompt_style.capitalize(), "bright_white"),
        ("\nTìm kiếm web: ", CONFIG["theme"]["system_color"]),
        ("Bật" if web_search_enabled else "Tắt", "bright_green" if web_search_enabled else "bright_red")
    )
    
    # Create command help
    commands = Table(show_header=False, box=None)
    commands.add_column(style=CONFIG["theme"]["highlight_color"])
    commands.add_column(style=CONFIG["theme"]["system_color"])
    commands.add_row("/help", "Hiển thị trợ giúp")
    commands.add_row("/model", "Đổi model AI")
    commands.add_row("/image", "Tạo hình ảnh")
    commands.add_row("/style", "Quản lý phong cách")
    commands.add_row("/search", "Bật/tắt tìm kiếm web")
    commands.add_row("/clear", "Xóa màn hình & lịch sử")
    commands.add_row("/save", "Lưu phiên hội thoại")
    commands.add_row("/load", "Tải phiên hội thoại")
    commands.add_row("/exit", "Thoát chương trình")
    
    command_panel = Panel(
        commands,
        title="Lệnh hỗ trợ",
        border_style=CONFIG["theme"]["border_color"],
        padding=(1, 2)
    )
    
    # Layout
    layout = Layout()
    layout.split(
        Layout(title_text, name="header", size=6),
        Layout(name="body")
    )
    layout["body"].split_row(
        Layout(model_info, name="info"),
        Layout(command_panel, name="commands")
    )
    
    console.print(layout)
    console.print("─" * 80, style="dim")

async def display_help():
    """Display help information"""
    help_table = Table(title="Hướng dẫn sử dụng", box=box.ROUNDED)
    help_table.add_column("Lệnh", style=CONFIG["theme"]["highlight_color"])
    help_table.add_column("Mô tả", style=CONFIG["theme"]["system_color"])
    help_table.add_column("Ví dụ", style="dim")
    
    help_table.add_row("/help", "Hiển thị trợ giúp này", "/help")
    help_table.add_row("/model [loại]", "Đổi model AI (text/image)", "/model text")
    help_table.add_row("/image [prompt]", "Tạo hình ảnh từ prompt", "/image mèo siamese trắng")
    help_table.add_row("/images", "Xem danh sách hình ảnh đã tạo", "/images")
    help_table.add_row("/style", "Quản lý phong cách trả lời", "/style")
    help_table.add_row("/search", "Bật/tắt tìm kiếm web", "/search")
    help_table.add_row("/clear", "Xóa màn hình và lịch sử hội thoại", "/clear")
    help_table.add_row("/save [tên]", "Lưu phiên hội thoại", "/save dự_án_abc")
    help_table.add_row("/load [tên]", "Tải phiên hội thoại", "/load dự_án_abc")
    help_table.add_row("/list", "Liệt kê các phiên đã lưu", "/list")
    help_table.add_row("/exit", "Thoát chương trình", "/exit")
    
    console.print(Panel(help_table, border_style=CONFIG["theme"]["border_color"]))

async def display_model_selection(model_type="text"):
    """Display model selection menu for text or image models"""
    # Filter models by type
    filtered_models = {k: v for k, v in CONFIG["models"].items() if v["type"] == model_type}
    
    if not filtered_models:
        console.print(f"Không có model loại {model_type} nào được cấu hình.", style=CONFIG["theme"]["error_color"])
        return None
    
    model_table = Table(title=f"Chọn Model {model_type.upper()}", box=box.ROUNDED)
    model_table.add_column("STT", style="dim")
    model_table.add_column("Model", style=CONFIG["theme"]["highlight_color"])
    model_table.add_column("Mô tả", style=CONFIG["theme"]["system_color"])
    
    current = current_model if model_type == "text" else current_image_model
    
    for i, (model_id, model_info) in enumerate(filtered_models.items(), 1):
        model_table.add_row(
            str(i),
            model_info["name"],
            f"Model ID: {model_id}" + (" (đang dùng)" if model_id == current else "")
        )
    
    console.print(Panel(model_table, border_style=CONFIG["theme"]["border_color"]))
    
    choice = Prompt.ask(
        f"Chọn model {model_type} (nhập số thứ tự hoặc 'c' để hủy)",
        choices=[str(i) for i in range(1, len(filtered_models)+1)] + ["c"]
    )
    
    if choice == "c":
        return None
        
    model_id = list(filtered_models.keys())[int(choice)-1]
    return model_id

async def display_style_manager():
    """Display style management menu with custom prompt option"""
    global current_prompt_style, custom_prompt
    
    # First, show the current styles
    style_table = Table(title="Phong cách trả lời", box=box.ROUNDED)
    style_table.add_column("STT", style="dim")
    style_table.add_column("Phong cách", style=CONFIG["theme"]["highlight_color"])
    style_table.add_column("Mô tả", style=CONFIG["theme"]["system_color"])
    
    styles = {
        "concise": "Ngắn gọn, súc tích, đi thẳng vào vấn đề",
        "detailed": "Chi tiết, đầy đủ, có cấu trúc rõ ràng",
        "creative": "Sáng tạo, độc đáo và thú vị",
        "expert": "Chuyên sâu, chuyên môn cao, dành cho chuyên gia",
        "friendly": "Thân thiện, gần gũi, dễ hiểu",
        "custom": "Prompt tùy chỉnh của người dùng"
    }
    
    for i, (style_id, description) in enumerate(styles.items(), 1):
        style_table.add_row(
            str(i),
            style_id.capitalize() + (" (đang dùng)" if style_id == current_prompt_style else ""),
            description
        )
    
    console.print(Panel(style_table, border_style=CONFIG["theme"]["border_color"]))
    
    # If current style is custom, show the custom prompt
    if current_prompt_style == "custom":
        console.print(Panel(
            Text(f"Prompt tùy chỉnh hiện tại:\n\n{custom_prompt}"),
            title="Prompt tùy chỉnh",
            border_style=CONFIG["theme"]["border_color"]
        ))
    
    # Show options
    options_table = Table(show_header=False, box=None)
    options_table.add_column(style=CONFIG["theme"]["highlight_color"])
    options_table.add_column(style=CONFIG["theme"]["system_color"])
    options_table.add_row("1", "Chọn phong cách có sẵn")
    options_table.add_row("2", "Tạo prompt tùy chỉnh")
    options_table.add_row("3", "Xem chi tiết các prompt")
    options_table.add_row("c", "Hủy")
    
    console.print(Panel(options_table, title="Tùy chọn", border_style=CONFIG["theme"]["border_color"]))
    
    choice = Prompt.ask("Chọn tùy chọn", choices=["1", "2", "3", "c"])
    
    if choice == "c":
        return
    
    if choice == "1":
        # Choose from existing styles
        style_choice = Prompt.ask(
            "Chọn phong cách (nhập số thứ tự)",
            choices=[str(i) for i in range(1, len(styles)+1)]
        )
        style_id = list(styles.keys())[int(style_choice)-1]
        current_prompt_style = style_id
        console.print(f"Đã chuyển sang phong cách: {current_prompt_style.capitalize()}", 
                     style=CONFIG["theme"]["system_color"])
    
    elif choice == "2":
        # Create custom prompt
        console.print("Nhập prompt tùy chỉnh của bạn (hướng dẫn AI cách trả lời):", 
                     style=CONFIG["theme"]["highlight_color"])
        new_prompt = console.input("[bold]> ")
        
        if new_prompt.strip():
            custom_prompt = new_prompt
            current_prompt_style = "custom"
            console.print("Đã thiết lập prompt tùy chỉnh thành công!", 
                         style=CONFIG["theme"]["system_color"])
        else:
            console.print("Prompt không được để trống.", style=CONFIG["theme"]["error_color"])
    
    elif choice == "3":
        # Show detailed prompts
        for style, prompt in SYSTEM_PROMPTS.items():
            if style == "custom":
                prompt = custom_prompt
                
            console.print(Panel(
                Text(prompt),
                title=f"Phong cách: {style.capitalize()}" + (" (đang dùng)" if style == current_prompt_style else ""),
                border_style=CONFIG["theme"]["border_color"] if style == current_prompt_style else "dim"
            ))

async def display_sessions():
    """Display saved sessions"""
    sessions = list_sessions()
    
    if not sessions:
        console.print("Không có phiên hội thoại nào được lưu.", style=CONFIG["theme"]["system_color"])
        return None
    
    session_table = Table(title="Phiên hội thoại đã lưu", box=box.ROUNDED)
    session_table.add_column("STT", style="dim")
    session_table.add_column("Tên", style=CONFIG["theme"]["highlight_color"])
    session_table.add_column("Thời gian", style=CONFIG["theme"]["system_color"])
    session_table.add_column("Model", style=CONFIG["theme"]["system_color"])
    session_table.add_column("Số tin nhắn", style="dim")
    
    for i, session in enumerate(sessions, 1):
        try:
            timestamp = datetime.datetime.fromisoformat(session["timestamp"]).strftime("%d/%m/%Y %H:%M")
        except:
            timestamp = "Unknown"
            
        session_table.add_row(
            str(i),
            session["name"],
            timestamp,
            session["model"],
            str(session["messages"])
        )
    
    console.print(Panel(session_table, border_style=CONFIG["theme"]["border_color"]))
    
    choice = Prompt.ask(
        "Chọn phiên để tải (nhập số thứ tự hoặc 'c' để hủy)",
        choices=[str(i) for i in range(1, len(sessions)+1)] + ["c"]
    )
    
    if choice == "c":
        return None
        
    return sessions[int(choice)-1]["name"]

async def display_images():
    """Display saved images"""
    images = list_images()
    
    if not images:
        console.print("Không có hình ảnh nào được lưu.", style=CONFIG["theme"]["system_color"])
        return None
    
    image_table = Table(title="Hình ảnh đã tạo", box=box.ROUNDED)
    image_table.add_column("STT", style="dim")
    image_table.add_column("Thời gian", style=CONFIG["theme"]["system_color"])
    image_table.add_column("Model", style=CONFIG["theme"]["system_color"])
    image_table.add_column("Prompt", style=CONFIG["theme"]["highlight_color"], width=40)
    
    for i, image in enumerate(images, 1):
        try:
            timestamp = datetime.datetime.fromisoformat(image["timestamp"]).strftime("%d/%m/%Y %H:%M")
        except:
            timestamp = "Unknown"
            
        # Truncate prompt if too long
        prompt = image["prompt"]
        if len(prompt) > 37:
            prompt = prompt[:37] + "..."
            
        image_table.add_row(
            str(i),
            timestamp,
            image["model"],
            prompt
        )
    
    console.print(Panel(image_table, border_style=CONFIG["theme"]["border_color"]))
    
    choice = Prompt.ask(
        "Chọn hình ảnh để xem (nhập số thứ tự hoặc 'c' để hủy)",
        choices=[str(i) for i in range(1, len(images)+1)] + ["c"]
    )
    
    if choice == "c":
        return None
        
    selected_image = images[int(choice)-1]
    
    # Display image details
    image_panel = Panel(
        Text.assemble(
            ("Prompt: ", CONFIG["theme"]["system_color"]),
            (selected_image["prompt"], CONFIG["theme"]["highlight_color"]),
            ("\nModel: ", CONFIG["theme"]["system_color"]),
            (selected_image["model"], CONFIG["models"][selected_image["model"]]["color"]),
            ("\nURL: ", CONFIG["theme"]["system_color"]),
            (selected_image["url"], "bright_blue underline")
        ),
        title="Chi tiết hình ảnh",
        border_style=CONFIG["theme"]["border_color"]
    )
    console.print(image_panel)
    
    # Ask if user wants to open the image in browser
    if Confirm.ask("Bạn có muốn mở hình ảnh trong trình duyệt?"):
        webbrowser.open(selected_image["url"])
    
    return selected_image["url"]

# ============= COMMAND HANDLERS =============
async def handle_command(command: str) -> bool:
    """Handle special commands, return True if command was handled"""
    global current_model, current_image_model, current_prompt_style, custom_prompt, conversation_history, web_search_enabled
    
    cmd_parts = command.split(maxsplit=1)
    cmd = cmd_parts[0].lower()
    args = cmd_parts[1] if len(cmd_parts) > 1 else ""
    
    if cmd == "/help":
        await display_help()
        return True
        
    elif cmd == "/model":
        if args.lower() in ["text", "văn bản"]:
            model_id = await display_model_selection("text")
            if model_id:
                current_model = model_id
                console.print(f"Đã chuyển sang model văn bản: {CONFIG['models'][current_model]['name']}", 
                             style=CONFIG["theme"]["system_color"])
        elif args.lower() in ["image", "hình ảnh", "ảnh"]:
            model_id = await display_model_selection("image")
            if model_id:
                current_image_model = model_id
                console.print(f"Đã chuyển sang model hình ảnh: {CONFIG['models'][current_image_model]['name']}", 
                             style=CONFIG["theme"]["system_color"])
        elif args in CONFIG["models"]:
            model_type = CONFIG["models"][args]["type"]
            if model_type == "text":
                current_model = args
                console.print(f"Đã chuyển sang model văn bản: {CONFIG['models'][current_model]['name']}", 
                             style=CONFIG["theme"]["system_color"])
            else:
                current_image_model = args
                console.print(f"Đã chuyển sang model hình ảnh: {CONFIG['models'][current_image_model]['name']}", 
                             style=CONFIG["theme"]["system_color"])
        else:
            console.print("Vui lòng chọn loại model (text/image):", style=CONFIG["theme"]["system_color"])
            choice = Prompt.ask("Loại model", choices=["text", "image"])
            model_id = await display_model_selection(choice)
            if model_id:
                if choice == "text":
                    current_model = model_id
                    console.print(f"Đã chuyển sang model văn bản: {CONFIG['models'][current_model]['name']}", 
                                 style=CONFIG["theme"]["system_color"])
                else:
                    current_image_model = model_id
                    console.print(f"Đã chuyển sang model hình ảnh: {CONFIG['models'][current_image_model]['name']}", 
                                 style=CONFIG["theme"]["system_color"])
        return True
        
    elif cmd == "/search":
        # Toggle web search
        web_search_enabled = not web_search_enabled
        status = "bật" if web_search_enabled else "tắt"
        console.print(f"Đã {status} tìm kiếm web.", 
                     style=CONFIG["theme"]["search_color"])
        return True
        
    elif cmd == "/clear":
        if Confirm.ask("Bạn có chắc muốn xóa màn hình và lịch sử hội thoại?"):
            conversation_history = []
            console.clear()
            await display_welcome()
            console.print("Đã xóa màn hình và lịch sử hội thoại.", style=CONFIG["theme"]["system_color"])
        return True
        
    elif cmd == "/save":
        name = args if args else None
        if name:
            session_name = name
        file_path = save_session(session_name)
        console.print(f"Đã lưu phiên hội thoại: {session_name}", style=CONFIG["theme"]["system_color"])
        return True
        
    elif cmd == "/load":
        if args:
            name = args
            if load_session(name):
                console.print(f"Đã tải phiên hội thoại: {name}", style=CONFIG["theme"]["system_color"])
            else:
                console.print(f"Không tìm thấy phiên hội thoại: {name}", style=CONFIG["theme"]["error_color"])
        else:
            name = await display_sessions()
            if name and load_session(name):
                console.print(f"Đã tải phiên hội thoại: {name}", style=CONFIG["theme"]["system_color"])
        return True
        
    elif cmd == "/list":
        await display_sessions()
        return True
        
    elif cmd == "/images":
        await display_images()
        return True
        
    elif cmd == "/image":
        if not args:
            prompt = Prompt.ask("[bold]Nhập mô tả hình ảnh bạn muốn tạo")
        else:
            prompt = args
            
        console.print(f"Đang tạo hình ảnh với prompt: '{prompt}'", style=CONFIG["theme"]["system_color"])
        result = await generate_image(prompt)
        
        if result["success"]:
            image_panel = Panel(
                Text.assemble(
                    ("✅ Đã tạo hình ảnh thành công!\n\n", CONFIG["theme"]["image_color"]),
                    ("URL: ", CONFIG["theme"]["system_color"]),
                    (result["url"], "bright_blue underline")
                ),
                title=f"Hình ảnh từ {CONFIG['models'][current_image_model]['name']}",
                border_style=CONFIG["theme"]["border_color"]
            )
            console.print(image_panel)
            
            # Ask if user wants to open the image in browser
            if Confirm.ask("Bạn có muốn mở hình ảnh trong trình duyệt?"):
                webbrowser.open(result["url"])
                
            # Add to conversation history
            conversation_history.append({
                "role": "user", 
                "content": f"/image {prompt}"
            })
            conversation_history.append({
                "role": "assistant", 
                "content": f"Đã tạo hình ảnh với prompt: '{prompt}'\nURL: {result['url']}"
            })
        else:
            console.print(f"❌ {result['error']}", style=CONFIG["theme"]["error_color"])
            
        return True
        
    elif cmd == "/style":
        await display_style_manager()
        return True
        
    elif cmd == "/exit":
        return False
        
    return False

# ============= MAIN CHAT FUNCTION =============
async def chat():
    """Main chat function with enhanced features"""
    global conversation_history
    
    # Ensure directories exist
    ensure_directories()
    
    # Display welcome screen
    await display_welcome()
    
    while True:
        # Get user input with rich styling
        user_input = Prompt.ask(f"[bold {CONFIG['theme']['user_color']}]Bạn")
        
        # Check if it's a command
        if user_input.startswith("/"):
            result = await handle_command(user_input)
            if user_input.lower() == "/exit":
                goodbye_text = Text("Tạm biệt! Hẹn gặp lại.", style=CONFIG["theme"]["bot_color"])
                goodbye_panel = Panel(goodbye_text, border_style=CONFIG["theme"]["border_color"])
                console.print(goodbye_panel)
                
                # Auto-save on exit
                if conversation_history and Confirm.ask("Bạn có muốn lưu phiên hội thoại này?"):
                    save_session()
                    
                break
            if result:
                continue
        
        # Build message context
        system_prompt = SYSTEM_PROMPTS[current_prompt_style]
        if current_prompt_style == "custom":
            system_prompt = custom_prompt
            
        messages = [{"role": "system", "content": system_prompt}] + conversation_history[-CONFIG["max_history"]*2:]
        messages.append({"role": "user", "content": user_input})
        
        # Get bot response
        start_time = time.time()
        bot_reply = await get_bot_response(messages)
        response_time = time.time() - start_time
        
        # Display bot response with typing effect
        model_info = CONFIG["models"][current_model]
        bot_header = Text.assemble(
            (f"{model_info['name']} ", model_info["color"]),
            (f"({response_time:.2f}s)", "dim"),
            (" 🔍" if web_search_enabled else "", CONFIG["theme"]["search_color"])
        )
        console.print(bot_header)
        
        # Display response with typing effect
        await typing_effect(bot_reply)
        console.print("─" * 80, style="dim")
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": bot_reply})
        
        # Auto-save after every few messages
        if len(conversation_history) % 10 == 0:
            save_session()

# ============= MAIN ENTRY POINT =============
if __name__ == "__main__":
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        console.print("\nChương trình đã bị dừng bởi người dùng.", style=CONFIG["theme"]["system_color"])
        # Auto-save on interrupt
        if conversation_history:
            save_session()
    except Exception as e:
        console.print(f"\nLỗi không mong muốn: {e}", style=CONFIG["theme"]["error_color"])
        # Try to save on crash
        if conversation_history:
            try:
                crash_session = f"crash_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                save_session(crash_session)
                console.print(f"Đã lưu phiên hội thoại khẩn cấp: {crash_session}", style=CONFIG["theme"]["system_color"])
            except:
                pass
