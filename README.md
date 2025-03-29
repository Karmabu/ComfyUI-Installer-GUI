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

---

## Authors & Support

- GitHub Repo: `coming soon...`
- Contact: `karma3u + chatgpt = install wizard`

> Made with ❤ using LLM + batch magic  
> by **Karm3u** and **ChatGPT**
