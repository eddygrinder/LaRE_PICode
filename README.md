## Objectives
This project is an integral part of the Master’s Dissertation entitled “LaRE – Expandable Remote Laboratory”.
It implements and manages a remote laboratory for electronics education, designed as a viable alternative to VISIR, with the additional commitment of being an open-source project, accessible to any educational institution regardless of geographical location.

The board matrix, the core element of the system, was developed based on a software-controlled architecture independent of proprietary platforms, ensuring that the system can be used without commercial licenses.

However, due to the current lack of support for the pyVirtualBench library on Linux systems and ARM architectures, the implementation of LaRE remains dependent on Windows systems — a factor that limits its adoption in more versatile and low-cost educational platforms.
Nevertheless, the modular architecture of LaRE enables future expansions and adaptations to different pedagogical contexts.

This dissertation partially fulfills the requirements defined in the Course Unit of Dissertation/Thesis of the 2nd year of the Master’s Degree in Electrical and Computer Engineering, specialization area in Automation and Systems.

## System Overview

The LaRE system is composed of:

* **PC (Server)** – runs a Flask-based Python web server.  
* **Raspberry Pi 5** – controls the relay matrix for switching circuits.  
* **NI VirtualBench (VB-8012)** – handles voltage, current, and waveform measurements.  
* **Web Interface** – implemented in HTML, CSS, and JavaScript for user interaction.  

Communication between the PC and Raspberry Pi is handled via **network sockets**, ensuring a simple and robust client–server connection.


## Helpful Resources
* [YouTube – Tech With Tim Flask Tutorial](https://www.youtube.com/watch?v=dam0GPOAvVI)  
* [Flask Official Documentation](https://flask.palletsprojects.com/en/stable/)  
* [pyVirtualBench Library (Armstrap)](https://github.com/armstrap/armstrap-pyvirtualbench)  
* [Armstrap Blog Post](http://armstrap.org/2015/07/27/pyvirtualbench-controlling-five-instruments-from-a-single-python-application/)


## Requirements (Windows Only)
* [NI VirtualBench hardware](http://www.ni.com/virtualbench/)
* [VirtualBench driver >= 1.1.0](https://www.ni.com/en-us/support/downloads/drivers/download.virtualbench-software.html#324215)
  Be sure to check "ANSI C Support" during installation.
    ![NiInstaller](https://github.com/armstrap/armstrap-pyvirtualbench/raw/master/images/ni-virtualbench-installer.png)
* [Python >= 3.4](https://www.python.org/downloads/).  You will need 32-bit Python support to work with the NI-provided drivers.

## Dependencies
To install the Python dependencies:
* pip install -r requirements.txt

## Licensing
This project is distributed under the terms of the GNU General Public License, version 3 (GPLv3).
It includes portions of code adapted from: armstrap/armstrap-pyvirtualbench, licensed under the MIT License (© 2015 Charles Armstrap).

See the files LICENSE and THIRD_PARTY_LICENSES.txt for full details.

## Author
Eduardo Ramalhadeiro
Master’s in Electrical and Computer Engineering – Automation and Systems
Instituto Politécnico do Porto (ISEP)
© 2025
