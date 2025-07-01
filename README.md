# PIO Flasher - GUI Tool for PlatformIO

## Project Description

PIO Flasher is a graphical tool for working with PlatformIO projects that simplifies the process of working with microcontrollers. The application provides a convenient interface for performing basic operations without using the command line.

**Main features:**
- Device flashing
- Uploading files to FS
- Full flash memory erase
- Console output of command execution results
- Dark theme support

## Installation

### Windows
1. Make sure you have Python 3 installed
2. Run the `install.cmd` file
3. The application will start automatically after installing requirements

### Linux
1. Open a terminal
2. Grant execution rights to the script:
   ```bash
   chmod +x install.sh
   ```
3. Run the script:
   ```bash
   sudo ./install.sh
   ```

## Requirements
- Python 3.x
- PlatformIO
- PyQt5

## Usage

1. Launch the application via `main.py` or use the installation scripts
2. Specify the path to the PlatformIO project:
   - Enter the path manually in the text field
   - Or click "..." to select a folder via the dialog window
3. Select the desired operation:
   - **Flash! →** - flashing
   - **Upload data in board FS →** - upload files to the file system
   - **Erase flash [X]** - full flash memory erase
4. Monitor the operation progress in the console output

## Possible Issues and Solutions

**Issue:** PlatformIO commands do not execute  
**Solution:** Make sure PlatformIO is correctly installed and added to PATH

**Issue:** Errors related to PyQt5  
**Solution:** Reinstall PyQt5: `pip3 install --force-reinstall PyQt5`

**Issue:** The application does not start on Linux  
**Solution:** Make sure all requirements are installed:
```bash
sudo apt install python3-pyqt5
sudo ./install.sh
```

## Compatibility
- Windows 10/11
- Linux (with graphical environment)
- Supported microcontrollers: all compatible with PlatformIO