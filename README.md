# ComfyUI-Installer-GUI
Windows ComfyUI Installer GUI
# ComfyUI Installer GUI – Standard & Pro

🇮🇹 La versione italiana è disponibile qui: [ComfyUI-Installer-GUI-ITA](https://github.com/Karmabu/ComfyUI-Installer-GUI-Italian)

This GUI allows you to install **ComfyUI** in two different modes:

## Available Modes

### ✅ Comfy Standard

- Requirements:
  - Python 3.12.9
  - CUDA Toolkit 12.4

- Actions performed:
  - Clone the ComfyUI repository
  - Create a virtual environment **outside** the ComfyUI folder
  - Install:
    - PyTorch 2.6.0 with CUDA 12.4 support
    - Dependencies from `requirements.txt`
    - onnxruntime-gpu, wheel, setuptools, packaging, ninja
    - accelerate, diffusers, transformers
  - Clear Triton and TorchInductor caches
  - Generate:
    - `Run_Comfyui.bat`
    - `Activate_Venv.bat`
    - `Update_Comfy.bat`
  - Automatically clone custom nodes:
    - ComfyUI-Manager
    - ComfyUI-Crystools

### 🔑 Comfy Pro  
(Triton 3.2.0 for Python 3.12 & SageAttention – including compilation)

- Requirements:
  - Python 3.12.9
  - CUDA Toolkit 12.4

- Additional actions:
  - Everything included in the **Standard** version
  - Install:
    - Triton 3.2.0 for Python 3.12
    - SageAttention (with automatic compilation)
  - Advanced system checks:
    - Presence of Visual Studio Build Tools 2022
    - `cl.exe` compiler available and configured in PATH
    - Valid native build environment for compiled modules

## GUI Features

- ☑ Toggle between **Comfy Standard** and **Comfy Pro** modes (mutually exclusive)
- 📂 Load custom JSON configuration files
- 📃 Show info panel (loaded from `info_comfyui_versions.json`)
- 🔍 “Check Prerequisites” button:
  - Verifies Python and CUDA versions
  - Checks for VS Build Tools and `cl.exe`
  - Detailed output in a dark-themed console with green text
- ▶ “Run Installation” button:
  - Executes each command from the JSON step-by-step
  - Real-time log display in the interface

## Supported Files

### `prerequisites_check.json` (TEST)
- Automatically loaded on GUI startup
- Contains test logic for:
  - Standard Mode: Python 3.12.9 + CUDA 12.4
  - Pro Mode: adds Visual Studio Build Tools and compiler checks

### `install_standard.json` (STANDARD INSTALLATION)
- Contains:
  - Commands for cloning, package installation, and batch file creation

### `install_full_comfyui.json` (PRO INSTALLATION)
- Contains:
  - The complete installation script
  - Includes Triton + SageAttention setup and cache cleanup

## Architecture & Design

- **Batch-driven** architecture: the GUI generates and runs real scripts
- No admin privileges required
- Fully **customizable** via JSON
- Works **offline** (except for git/pip access)

![eng](https://github.com/user-attachments/assets/de64387c-1922-4d9a-a438-19a8c390b46c)

## 🔄 Update March 2025
- Added full GUI editor for JSON-based installers
- New LLM syntax checker using Ollama (configurable)
- Visual command editor with step management
- Cleaner layout and improved user experience

![K3U JSON](https://github.com/user-attachments/assets/6bc8da5b-1e80-4ea2-98be-b85e0c06886e)


# Beginner Guide - Setting Up ComfyUI Installer GUI

Welcome! This guide will walk you through the installation of all prerequisites needed to run the **ComfyUI Installer GUI** in both Standard and Pro modes.

---

## ✅ What You Need To Install

| Requirement | Version | Mode | Description |
|-------------|---------|------|-------------|
| Python      | 3.12.9  | All  | Required to run ComfyUI and create virtual environments |
| Git         | Latest  | All  | Required to clone the ComfyUI repository from GitHub |
| CUDA Toolkit| 12.4    | All  | Required for GPU acceleration (NVIDIA only) |
| Visual Studio Community 2022 | Latest | Pro only | Required for compiling SageAttention and Triton |

---

## 1. Install Python 3.12.9

- Go to: https://www.python.org/downloads/release/python-3129/
- Download the **Windows Installer (64-bit)**
- Launch the installer:
  - ✅ Check "Add Python to PATH"
  - ✅ Click "Install Now"

### Verify Installation:
Open **Command Prompt** and type:
```
python --version
```
You should see:
```
Python 3.12.9
```

---

## 2. Install Git

- Go to: https://git-scm.com/download/win
- Download and install Git for Windows
- Use default options during setup

### Verify Installation:
Open **Command Prompt** and type:
```
git --version
```
You should see something like:
```
git version 2.42.0.windows.1
```

---

## 3. Install CUDA Toolkit 12.4

- Go to: https://developer.nvidia.com/cuda-downloads
- Select:
  - Operating System: **Windows**
  - Version: **12.4**
  - Architecture: **x86_64**
  - Installer Type: **Network Installer** or **Local Installer**
- Complete the installation and restart your PC.

### Verify Installation:
Open **Command Prompt** and type:
```
nvcc --version
```
You should see something like:
```
Cuda compilation tools, release 12.4, V...
```

---

## 4. Install Visual Studio Community 2022 (Pro only)

- Go to: https://visualstudio.microsoft.com/vs/community/
- Click **Download**
- During installation:
  - ✅ Select **Desktop development with C++**
  - ✅ (Optional) Enable "Python Development" for convenience
- Complete setup and restart your PC.

### Verify cl.exe Compiler:
Open **Command Prompt** and type:
```
where cl.exe
```
If installed correctly, you should see a path similar to:
```
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\<version>\bin\Hostx64\x64\cl.exe
```

---

## You're Ready!
Now that everything is installed, you can launch the **ComfyUI Installer GUI** and begin installation in **Standard** or **Pro** mode.

Need help? Join the community or visit our [GitHub repo](https://github.com/Karmabu/ComfyUI-Installer-GUI)

o

## Authors & Support

- GitHub Repo: `coming soon...`
- Contact: `karma3u + chatgpt = install wizard`

> Made with ❤ using LLM + batch magic  
> by **Karm3u** and **ChatGPT**
