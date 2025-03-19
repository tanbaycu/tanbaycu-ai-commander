# 🤖 TANBAYCU AI COMMANDER

> **AUTHOR:** [tanbaycu](https://github.com/tanbaycu)

> **POWERED BY [g4f](https://github.com/xtekky/gpt4free)**

> **BUILT WITH PYTHON**

<p align="center">
  <img src="https://i.postimg.cc/zv32WPFn/image.png" alt="TANBAYCU AI COMMANDER Logo" width="300"/>
</p>

> Một chatbot AI tiên tiến với giao diện dòng lệnh đẹp mắt, hỗ trợ nhiều model AI, tạo hình ảnh, tìm kiếm web và nhiều tính năng mạnh mẽ khác.

## 📋 Mục lục

- [Tổng quan](#tổng-quan)
- [Lịch sử phát triển](#lịch-sử-phát-triển)
- [Tính năng chính](#tính-năng-chính)
- [Kiến trúc kỹ thuật](#kiến-trúc-kỹ-thuật)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Lệnh hỗ trợ](#lệnh-hỗ-trợ)
- [Phát triển trong tương lai](#phát-triển-trong-tương-lai)
- [Đóng góp](#đóng-góp)
- [Liên hệ](#liên-hệ)

## 🌟 Tổng quan

**TANBAYCU AI COMMANDER** là một chatbot AI tiên tiến được phát triển với Python, sử dụng thư viện Rich để tạo giao diện dòng lệnh đẹp mắt và trực quan. Chatbot này kết nối với nhiều model AI thông qua g4f.client, cho phép người dùng tương tác với các model AI mạnh mẽ nhất hiện nay như Claude, GPT-4o, Gemini và nhiều model khác.

Dự án này đã trải qua nhiều phiên bản với những cải tiến đáng kể về giao diện người dùng, hiệu suất, và tính năng, từ một chatbot đơn giản ban đầu đến một hệ thống AI toàn diện với khả năng tạo hình ảnh, tìm kiếm web, và nhiều tùy chỉnh nâng cao.

## 📈 Lịch sử phát triển

### Phiên bản 1.0: Enhanced Chatbot

Phiên bản đầu tiên tập trung vào việc cải thiện trải nghiệm người dùng cơ bản:

- **Giao diện màu sắc**: Sử dụng thư viện Rich để tạo giao diện dòng lệnh với màu sắc
- **Hiệu ứng đánh máy**: Thêm hiệu ứng đánh máy khi AI trả lời để tăng tính tương tác
- **Xử lý lỗi cơ bản**: Thêm xử lý timeout và bắt lỗi khi gọi API
- **Cấu trúc mã nguồn**: Tổ chức mã nguồn thành các phần chức năng rõ ràng

```python
# Ví dụ hiệu ứng đánh máy từ phiên bản 1.0
async def typing_effect(text: str, min_delay: float = 0.005, max_delay: float = 0.02):
    for char in text:
        console.print(char, end="", style="bright_green")
        await asyncio.sleep(random.uniform(min_delay, max_delay))
    console.print()

```

### Phiên bản 2.0: Advanced Chatbot

Phiên bản thứ hai mở rộng đáng kể về tính năng và trải nghiệm người dùng:

- **Hệ thống cấu hình toàn diện**: Tập trung hóa cấu hình với nhiều tùy chọn
- **Quản lý phiên hội thoại**: Thêm khả năng lưu và tải lại các phiên hội thoại
- **Hệ thống lệnh**: Thêm các lệnh như `/help`, `/model`, `/clear`, `/save`, `/load`
- **Phong cách trả lời**: Cho phép người dùng chọn phong cách trả lời khác nhau
- **Giao diện người dùng nâng cao**: Bảng điều khiển, bảng thông tin, và hiển thị trực quan hơn
- **Xử lý lỗi mạnh mẽ**: Cải thiện xử lý lỗi và tự động lưu khi gặp sự cố

```python 
# Ví dụ hệ thống lệnh từ phiên bản 2.0
async def handle_command(command: str) -> bool:
    global current_model, current_prompt_style, conversation_history
    
    cmd_parts = command.split()
    cmd = cmd_parts[0].lower()
    args = cmd_parts[1:] if len(cmd_parts) > 1 else []
    
    if cmd == "/help":
        await display_help()
        return True
    # ... các lệnh khác
```

### Phiên bản 2.0: Advanced Chatbot

Phiên bản thứ hai mở rộng đáng kể về tính năng và trải nghiệm người dùng:

- **Hệ thống cấu hình toàn diện**: Tập trung hóa cấu hình với nhiều tùy chọn
- **Quản lý phiên hội thoại**: Thêm khả năng lưu và tải lại các phiên hội thoại
- **Hệ thống lệnh**: Thêm các lệnh như `/help`, `/model`, `/clear`, `/save`, `/load`
- **Phong cách trả lời**: Cho phép người dùng chọn phong cách trả lời khác nhau
- **Giao diện người dùng nâng cao**: Bảng điều khiển, bảng thông tin, và hiển thị trực quan hơn
- **Xử lý lỗi mạnh mẽ**: Cải thiện xử lý lỗi và tự động lưu khi gặp sự cố


```python
# Ví dụ hệ thống lệnh từ phiên bản 2.0
async def handle_command(command: str) -> bool:
    global current_model, current_prompt_style, conversation_history
    
    cmd_parts = command.split()
    cmd = cmd_parts[0].lower()
    args = cmd_parts[1:] if len(cmd_parts) > 1 else []
    
    if cmd == "/help":
        await display_help()
        return True
    # ... các lệnh khác
```

### Phiên bản 3.0: Ultimate Chatbot (Hiện tại)

Phiên bản hiện tại là một bước nhảy vọt về tính năng và trải nghiệm:

- **Tạo hình ảnh AI**: Thêm khả năng tạo hình ảnh với nhiều model khác nhau
- **Tìm kiếm web**: Tích hợp tìm kiếm web để cung cấp thông tin cập nhật
- **Hỗ trợ nhiều model AI**: Mở rộng danh sách model AI được hỗ trợ (17+ model văn bản, 5+ model hình ảnh)
- **Prompt tùy chỉnh**: Cho phép người dùng tạo prompt hệ thống riêng
- **Giao diện người dùng cao cấp**: Thiết kế lại giao diện với tiêu đề đẹp mắt và bố cục tối ưu
- **Quản lý hình ảnh**: Lưu trữ và quản lý các hình ảnh đã tạo
- **Tự động lưu phiên**: Tự động lưu phiên hội thoại định kỳ và khi thoát


## 🚀 Tính năng chính

### Đa dạng Model AI

- **17+ model văn bản**: Claude, GPT-4o, Gemini, Llama, và nhiều model khác
- **5+ model hình ảnh**: DALL-E, Midjourney, Stable Diffusion, và các model khác
- **Dễ dàng chuyển đổi**: Chuyển đổi giữa các model chỉ với một lệnh


### Tạo hình ảnh AI

- **Tạo hình ảnh từ mô tả**: Chuyển đổi văn bản thành hình ảnh chất lượng cao
- **Quản lý thư viện hình ảnh**: Lưu trữ và xem lại các hình ảnh đã tạo
- **Tùy chọn model**: Chọn model hình ảnh phù hợp với nhu cầu


### Tìm kiếm web

- **Thông tin cập nhật**: Truy cập thông tin mới nhất từ internet
- **Dễ dàng bật/tắt**: Chuyển đổi tìm kiếm web với một lệnh đơn giản


### Phong cách trả lời tùy chỉnh

- **5 phong cách có sẵn**: Ngắn gọn, chi tiết, sáng tạo, chuyên gia, thân thiện
- **Prompt tùy chỉnh**: Tạo prompt hệ thống riêng theo nhu cầu


### Quản lý phiên hội thoại

- **Lưu và tải phiên**: Lưu trữ và khôi phục các cuộc hội thoại quan trọng
- **Tự động lưu**: Tự động lưu phiên định kỳ để tránh mất dữ liệu
- **Khôi phục khẩn cấp**: Tự động lưu khi gặp sự cố


### Giao diện người dùng trực quan

- **Hiệu ứng đánh máy**: Tạo cảm giác tương tác thực tế
- **Màu sắc và bố cục**: Giao diện màu sắc với bố cục tối ưu
- **Thông báo trạng thái**: Hiển thị rõ ràng trạng thái hệ thống


## 🔧 Kiến trúc kỹ thuật

### Thư viện chính

- **Rich**: Tạo giao diện dòng lệnh đẹp mắt với màu sắc và bố cục
- **g4f.client**: Kết nối với các API model AI
- **asyncio**: Xử lý bất đồng bộ để tăng hiệu suất
- **json**: Lưu trữ và quản lý dữ liệu phiên hội thoại


### Cấu trúc mã nguồn

- **Cấu hình tập trung**: Tất cả cấu hình trong một từ điển CONFIG
- **Mô-đun hóa**: Chia mã nguồn thành các phần chức năng rõ ràng
- **Xử lý bất đồng bộ**: Sử dụng asyncio cho các tác vụ chậm
- **Xử lý lỗi toàn diện**: Bắt và xử lý lỗi ở nhiều cấp độ


### Hiệu suất

- **Tối ưu hiệu ứng đánh máy**: Xử lý thông minh cho code blocks
- **Timeout thông minh**: Giới hạn thời gian chờ API
- **Lưu trữ hiệu quả**: Định dạng JSON nhỏ gọn cho dữ liệu phiên



## 📥 Cài đặt

### Yêu cầu

- Python 3.8 trở lên
- Pip (trình quản lý gói Python)


### Cài đặt thư viện

```shellscript
pip install rich g4f
```

### Tải mã nguồn

```shellscript
git clone https://github.com/yourusername/tanbaycu-ai-commander.git
cd tanbaycu-ai-commander
```

## 🎮 Sử dụng

### Khởi động chatbot

```shellscript
python tanbaycu_chatbot.py
```

### Tương tác cơ bản

- Nhập câu hỏi hoặc yêu cầu và nhấn Enter
- Chatbot sẽ xử lý và trả lời với hiệu ứng đánh máy
- Sử dụng các lệnh bắt đầu bằng `/` để truy cập các tính năng đặc biệt

## 🚀 Tính năng chính

### Đa dạng Model AI

- **17+ model văn bản**: Claude, GPT-4o, Gemini, Llama, và nhiều model khác
- **5+ model hình ảnh**: DALL-E, Midjourney, Stable Diffusion, và các model khác
- **Dễ dàng chuyển đổi**: Chuyển đổi giữa các model chỉ với một lệnh


### Tạo hình ảnh AI

- **Tạo hình ảnh từ mô tả**: Chuyển đổi văn bản thành hình ảnh chất lượng cao
- **Quản lý thư viện hình ảnh**: Lưu trữ và xem lại các hình ảnh đã tạo
- **Tùy chọn model**: Chọn model hình ảnh phù hợp với nhu cầu


### Tìm kiếm web

- **Thông tin cập nhật**: Truy cập thông tin mới nhất từ internet
- **Dễ dàng bật/tắt**: Chuyển đổi tìm kiếm web với một lệnh đơn giản


### Phong cách trả lời tùy chỉnh

- **5 phong cách có sẵn**: Ngắn gọn, chi tiết, sáng tạo, chuyên gia, thân thiện
- **Prompt tùy chỉnh**: Tạo prompt hệ thống riêng theo nhu cầu


### Quản lý phiên hội thoại

- **Lưu và tải phiên**: Lưu trữ và khôi phục các cuộc hội thoại quan trọng
- **Tự động lưu**: Tự động lưu phiên định kỳ để tránh mất dữ liệu
- **Khôi phục khẩn cấp**: Tự động lưu khi gặp sự cố


### Giao diện người dùng trực quan

- **Hiệu ứng đánh máy**: Tạo cảm giác tương tác thực tế
- **Màu sắc và bố cục**: Giao diện màu sắc với bố cục tối ưu
- **Thông báo trạng thái**: Hiển thị rõ ràng trạng thái hệ thống


## 🔧 Kiến trúc kỹ thuật

### Thư viện chính

- **Rich**: Tạo giao diện dòng lệnh đẹp mắt với màu sắc và bố cục
- **g4f.client**: Kết nối với các API model AI
- **asyncio**: Xử lý bất đồng bộ để tăng hiệu suất
- **json**: Lưu trữ và quản lý dữ liệu phiên hội thoại


### Cấu trúc mã nguồn

- **Cấu hình tập trung**: Tất cả cấu hình trong một từ điển CONFIG
- **Mô-đun hóa**: Chia mã nguồn thành các phần chức năng rõ ràng
- **Xử lý bất đồng bộ**: Sử dụng asyncio cho các tác vụ chậm
- **Xử lý lỗi toàn diện**: Bắt và xử lý lỗi ở nhiều cấp độ


### Hiệu suất

- **Tối ưu hiệu ứng đánh máy**: Xử lý thông minh cho code blocks
- **Timeout thông minh**: Giới hạn thời gian chờ API
- **Lưu trữ hiệu quả**: Định dạng JSON nhỏ gọn cho dữ liệu phiên


## 📥 Cài đặt

### Yêu cầu

- Python 3.8 trở lên
- Pip (trình quản lý gói Python)


### Cài đặt thư viện

```shellscript
pip install rich g4f
```

### Tải mã nguồn

```shellscript
git clone https://github.com/tanbaycu/tanbaycu-ai-commander.git
cd tanbaycu-ai-commander
```

## 🎮 Sử dụng

### Khởi động chatbot

```shellscript
python tanbaycu_chatbot.py
```

### Tương tác cơ bản

- Nhập câu hỏi hoặc yêu cầu và nhấn Enter
- Chatbot sẽ xử lý và trả lời với hiệu ứng đánh máy
- Sử dụng các lệnh bắt đầu bằng `/` để truy cập các tính năng đặc biệt


## 📝 Lệnh hỗ trợ

| Lệnh | Mô tả | Ví dụ
|-----|-----|-----
| `/help` | Hiển thị trợ giúp | `/help`
| `/model [loại]` | Đổi model AI (text/image) | `/model text`
| `/image [prompt]` | Tạo hình ảnh từ prompt | `/image mèo siamese trắng`
| `/images` | Xem danh sách hình ảnh đã tạo | `/images`
| `/style` | Quản lý phong cách trả lời | `/style`
| `/search` | Bật/tắt tìm kiếm web | `/search`
| `/clear` | Xóa màn hình và lịch sử hội thoại | `/clear`
| `/save [tên]` | Lưu phiên hội thoại | `/save dự_án_abc`
| `/load [tên]` | Tải phiên hội thoại | `/load dự_án_abc`
| `/list` | Liệt kê các phiên đã lưu | `/list`
| `/exit` | Thoát chương trình | `/exit`


## 🔮 Phát triển trong tương lai

### Tính năng đang lên kế hoạch

- **Hỗ trợ giọng nói**: Thêm khả năng nhận dạng và tổng hợp giọng nói
- **Phân tích dữ liệu**: Tích hợp công cụ phân tích dữ liệu và biểu đồ
- **Plugins**: Hệ thống plugin mở rộng cho phép thêm tính năng tùy chỉnh
- **Giao diện web**: Phiên bản web với giao diện đồ họa đầy đủ
- **Hỗ trợ đa ngôn ngữ**: Thêm nhiều ngôn ngữ giao diện


### Cải tiến kỹ thuật

- **Tối ưu hóa hiệu suất**: Cải thiện tốc độ xử lý và phản hồi
- **Bảo mật nâng cao**: Mã hóa dữ liệu phiên và thông tin nhạy cảm
- **Kiểm thử tự động**: Thêm bộ kiểm thử tự động để đảm bảo chất lượng

## 👥 Đóng góp

Chúng tôi hoan nghênh mọi đóng góp! Nếu bạn muốn tham gia phát triển:

## 🛡️ Liên hệ
[Linktree Profile](https://linktr.ee/tanbaycu)

[Linktree Projects Chatbot](https://linktr.ee/chatbottelegram)
---

<p align="center"
<strong>TANBAYCU AI COMMANDER</strong><br>
Phát triển bởi @tanbaycu<br>
Liên hệ: [tanbaycu](mailto:tranminhtan4953@gmail.com)</p>
