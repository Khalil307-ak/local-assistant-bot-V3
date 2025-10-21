# 🚀 Advanced Local Assistant Bot v3.0 - Professional Edition

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()

A comprehensive, feature-rich command-line assistant built in Python that transforms your terminal into a powerful productivity tool. This professional-grade assistant provides everything from basic system management to advanced security tools, all wrapped in a beautiful, colorful interface.

## ✨ Key Features

### 🎯 **Core Functionality**
- **Advanced Note Management**: Create, edit, search, and organize timestamped notes
- **Powerful Calculator**: Safe mathematical expressions with history tracking
- **System Monitoring**: Real-time CPU, memory, and disk usage monitoring
- **File Management**: Complete file operations (copy, move, delete, list)
- **Process Management**: View and control running processes

### 🔐 **Security & Encryption**
- **Password Generator**: Create secure passwords with customizable options
- **Text Encryption/Decryption**: Simple but effective text protection
- **Hash Generator**: MD5, SHA1, SHA256, SHA512 hash generation
- **Base64 Encoding/Decoding**: Data encoding utilities

### 📊 **Data Processing**
- **JSON Formatter**: Beautify and validate JSON data
- **Text Manipulation**: Case conversion, reversal, word counting
- **Unit Conversion**: Length, weight, temperature conversions
- **Random Generation**: Strings, numbers, and secure tokens

### 🌐 **Web Tools**
- **Weather Information**: Get current weather data for any city
- **URL Shortener**: Shorten long URLs using TinyURL
- **QR Code Generator**: Create QR codes for text or URLs
- **Programming Quotes**: Inspirational quotes for developers

### 📋 **Productivity Tools**
- **Task Management**: Add, list, complete, and delete tasks
- **Backup & Restore**: File and directory backup system
- **System Cleanup**: Automatic temporary file cleanup
- **Desktop Notifications**: Set reminders and alerts
- **Settings Management**: Customizable configuration system

### 🖥️ **System Information**
- **Hardware Details**: CPU, memory, disk, and network information
- **Battery Status**: Laptop battery monitoring
- **Network Analysis**: IP address and Wi-Fi information
- **Disk Analysis**: Detailed storage usage breakdown

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Installation

1. **Clone or Download the Project**
   ```bash
   git clone https://github.com/yourusername/advanced-local-assistant-bot.git
   cd advanced-local-assistant-bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Assistant**
   ```bash
   python main.py
   ```

### Manual Installation

If you prefer to install dependencies manually:

```bash
pip install psutil>=5.9.0
pip install rich>=13.0.0
pip install requests>=2.28.1
pip install plyer>=2.0.0
pip install qrcode>=7.4.2
pip install Pillow>=9.0.0
```

## 📖 Usage Guide

### Getting Started

1. **Launch the Assistant**
   ```bash
   python main.py
   ```

2. **View Available Commands**
   ```bash
   help
   ```

3. **Start Using Commands**
   ```bash
   time                    # Get current time
   sysinfo                # System information
   note add "Remember this" # Add a note
   calc 2+3*4             # Calculate
   ```

### Command Categories

#### 📝 **Note Management**
```bash
note add "Your note here"     # Add a new note
note show                     # Display all notes
note search "keyword"         # Search notes
note edit 1 "New text"        # Edit note by ID
note delete 1                 # Delete note by ID
note delete "keyword"         # Delete notes by keyword
```

#### 🧮 **Calculator & Math**
```bash
calc 2+3*4                    # Basic calculation
calc (500 + 3.14) * 2         # Complex expressions
calc history                  # View calculation history
convert length 10 km to mi     # Unit conversion
random string 16               # Generate random string
random number 1 100           # Generate random number
```

#### 🔐 **Security Tools**
```bash
password 16 -u -n -s          # Generate secure password
encrypt "secret text" key123  # Encrypt text
decrypt "encrypted" key123    # Decrypt text
hash "text" sha256           # Generate hash
base64 "Hello World"         # Base64 encode
decode64 "SGVsbG8gV29ybGQ="  # Base64 decode
```

#### 📁 **File Management**
```bash
file list C:\Users            # List directory contents
file copy source.txt dest.txt # Copy files
file move old.txt new.txt     # Move files
file delete temp.txt          # Delete files
backup C:\Important backup    # Backup directory
restore backup restored       # Restore from backup
```

#### 🖥️ **System Management**
```bash
sysinfo                       # System information
process list                  # List running processes
process kill 1234             # Kill process by PID
disk                          # Disk usage analysis
monitor                       # Real-time system monitoring
clean                         # Clean temporary files
battery                       # Battery status
network                       # Network information
```

#### 📋 **Task Management**
```bash
tasks add "Complete project"  # Add new task
tasks list                    # List all tasks
tasks complete 1              # Mark task complete
tasks delete 1                # Delete task
```

#### 🌐 **Web Tools**
```bash
weather London                # Get weather info
url https://example.com       # Shorten URL
qr "https://example.com"      # Generate QR code
fun quote                     # Get programming quote
fun joke                      # Get programming joke
```

#### ⚙️ **Settings & Configuration**
```bash
settings show                 # Display all settings
settings set theme dark       # Set configuration value
remind 300 "Coffee break"     # Set reminder
clear                         # Clear screen
exit                          # Exit the assistant
```

## 🎨 Interface Features

### Beautiful Terminal Interface
- **Rich Colors**: Syntax highlighting and color-coded output
- **Tables**: Organized data display with borders and styling
- **Panels**: Important information in bordered containers
- **Progress Indicators**: Visual feedback for long operations
- **Emojis**: Intuitive icons for better user experience

### User Experience
- **Case Insensitive**: Commands work regardless of case
- **Smart Parsing**: Handles quotes and spaces intelligently
- **Error Handling**: Clear, helpful error messages
- **Auto-completion**: Context-aware command suggestions
- **Multi-platform**: Works on Windows, macOS, and Linux

## 🔧 Configuration

### Settings File
The assistant uses `data/settings.json` for configuration:

```json
{
  "theme": "dark",
  "auto_save": true,
  "default_password_length": 16,
  "weather_api_key": "your_api_key_here",
  "notification_sound": true
}
```

### Environment Variables
Set these for enhanced functionality:

```bash
export WEATHER_API_KEY="your_openweathermap_api_key"
export DEFAULT_THEME="dark"
export AUTO_BACKUP="true"
```

## 📁 Project Structure

```
advanced-local-assistant-bot/
│
├── main.py              # Main application entry point
├── commands.py          # Command implementations
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── README.md           # This documentation
│
└── data/               # Data storage directory
    ├── notes.txt       # User notes
    ├── tasks.txt       # Task management
    ├── calc_history.txt # Calculation history
    ├── settings.json   # Configuration
    └── backup/         # Backup storage
```

## 🚀 Advanced Features

### Real-time Monitoring
```bash
monitor                    # Start real-time system monitoring
# Press Ctrl+C to stop
```

### Batch Operations
```bash
# Process multiple files
file list C:\Documents
file copy *.txt backup/

# Bulk note operations
note delete "old"
note search "important"
```

### Custom Workflows
```bash
# Daily routine example
tasks add "Check emails"
tasks add "Review code"
tasks add "Update documentation"
tasks list
```

## 🔒 Security Considerations

- **Password Generation**: Uses cryptographically secure random generation
- **Text Encryption**: Simple Base64 encoding (for basic obfuscation)
- **Hash Generation**: Industry-standard algorithms (MD5, SHA family)
- **File Operations**: Safe file handling with error checking
- **Process Management**: Respects system permissions

## 🌍 Cross-Platform Support

### Windows
- Full Windows 10/11 support
- PowerShell and Command Prompt compatible
- Windows-specific optimizations

### macOS
- Native macOS integration
- Terminal.app and iTerm2 support
- macOS-specific features

### Linux
- Ubuntu, Debian, CentOS, Fedora support
- GNOME Terminal, Konsole, xterm compatible
- Linux-specific optimizations

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Setup
```bash
git clone https://github.com/yourusername/advanced-local-assistant-bot.git
cd advanced-local-assistant-bot
pip install -r requirements.txt
python main.py
```

## 📋 Roadmap

### Version 3.1 (Planned)
- [ ] Database integration (SQLite)
- [ ] Plugin system
- [ ] GUI mode
- [ ] Cloud sync
- [ ] Advanced encryption

### Version 3.2 (Future)
- [ ] Machine learning integration
- [ ] Voice commands
- [ ] Mobile app companion
- [ ] API server mode
- [ ] Multi-user support

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Permission Errors**
```bash
# On Linux/macOS
sudo pip install -r requirements.txt

# On Windows (run as Administrator)
pip install -r requirements.txt
```

**QR Code Issues**
```bash
pip install Pillow
```

**Notification Issues**
```bash
# On Linux
sudo apt-get install libnotify-bin
```

### Getting Help

1. **Check the Help Menu**: `help`
2. **View System Info**: `sysinfo`
3. **Check Settings**: `settings show`
4. **Report Issues**: Create a GitHub issue

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Rich Library**: For beautiful terminal output
- **psutil**: For system information
- **requests**: For HTTP operations
- **plyer**: For desktop notifications
- **qrcode**: For QR code generation

## 📞 Support

- **Documentation**: This README
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**:khalil.akram307@gmail.com

---

<div align="center">

**Made with ❤️ by the Advanced Local Assistant Bot Team**

[⭐ Star this repo](https://github.com/yourusername/advanced-local-assistant-bot) | [🐛 Report Bug](https://github.com/yourusername/advanced-local-assistant-bot/issues) | [💡 Request Feature](https://github.com/yourusername/advanced-local-assistant-bot/issues)

</div>
