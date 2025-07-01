# PIO Flasher - GUI Tool for PlatformIO

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