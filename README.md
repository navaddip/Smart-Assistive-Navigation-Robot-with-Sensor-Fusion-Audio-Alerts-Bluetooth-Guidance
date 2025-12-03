# Smart Assistive Navigation Robot

A Raspberry Pi-based autonomous navigation robot featuring 180° ultrasonic scanning, obstacle detection and avoidance, PWM motor control, and Bluetooth alerts for safe mobility assistance.

---

## 🚀 Features

- **180° Environmental Scanning** - Servo-controlled ultrasonic sensor sweeps left, center, and right
- **Real-time Obstacle Detection** - Detects and avoids obstacles dynamically
- **PWM Motor Control** - Smooth speed control using L298N motor driver
- **Bluetooth Alerts** - Sends notifications when obstacles are detected
- **Smart Navigation** - Intelligent left/right decision-making based on clearance
- **Safe Operation** - Immediate stopping and smooth movement logic

---

## 🛠️ Hardware Components

| Component | Description |
|-----------|-------------|
| Raspberry Pi 3/4 | Main controller |
| HC-SR04 | Ultrasonic distance sensor |
| SG90 | Servo motor for scanning |
| L298N | Dual H-bridge motor driver |
| DC Motors (2x) | Drive motors |
| HC-05 | Bluetooth communication module |
| Battery Pack | Power supply |

---

## 📁 Project Structure
```
Smart-Navigation-Robot/
├── OAC.py                    # Basic obstacle avoidance control
├── raspberrypi.py            # Full system with Bluetooth + PWM + scanning
├── README.md                 # Project documentation
└── videos/
    ├── path_navigation.mp4   # Navigation demonstration
    └── voice_feedback.mp4    # Bluetooth alert demo
```

---

## ⚙️ Installation

### Step 1: Install Required Packages
```bash
# Start pigpio daemon
sudo pigpiod

# Install system packages
sudo apt-get update
sudo apt-get install pigpio python3-pigpio

# Install Python libraries
pip3 install RPi.GPIO
pip3 install pigpio
pip3 install pyserial
pip3 install opencv-python
```

### Step 2: Enable Serial for Bluetooth
```bash
sudo raspi-config
```

Navigate to:
1. **Interface Options** → **Serial Port**
2. **Disable** login shell over serial
3. **Enable** hardware serial port
4. Reboot: `sudo reboot`

### Step 3: Pair Bluetooth Module
```bash
# Scan for Bluetooth devices
bluetoothctl
scan on
# Note the HC-05 MAC address
pair [MAC_ADDRESS]
trust [MAC_ADDRESS]
connect [MAC_ADDRESS]
exit
```

---

## 🎮 How to Run

### Basic Obstacle Avoidance
```bash
python3 OAC.py
```

### Full System (with Bluetooth Alerts + PWM + Scanning)
```bash
python3 raspberrypi.py
```

### Stop the System

Press `Ctrl + C` to stop the script safely.

### Stop pigpio Daemon
```bash
sudo killall pigpiod
```

---

## 🔄 How It Works
```
┌─────────────────────────────────────────┐
│  1. Servo rotates to scan angles        │
│     (Left → Center → Right)             │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  2. Ultrasonic sensor measures          │
│     distance at each angle              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  3. Obstacle detected?                  │
│     (Distance < threshold)              │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        │ YES         │ NO
        ▼             ▼
┌───────────────┐  ┌──────────────┐
│ • Stop motors │  │ Continue     │
│ • Send alert  │  │ forward      │
│ • Scan sides  │  │ movement     │
│ • Turn clear  │  └──────────────┘
│   direction   │
└───────────────┘
```

### Decision Logic

1. **Scan Phase**: Servo rotates ultrasonic sensor to measure distances
2. **Detection Phase**: Compare distances against safety threshold
3. **Alert Phase**: Send Bluetooth notification if obstacle detected
4. **Decision Phase**: Compare left vs right clearance
5. **Action Phase**: Turn toward clearer path
6. **Resume Phase**: Continue forward navigation with PWM speed control

---

## 📹 Demo Videos

### Path Navigation
[![Path Navigation](https://img.icons8.com/ios-filled/100/video.png)](videos/path_navigation.mp4)



### Bluetooth Voice Feedback
[![Voice Feedback](https://img.icons8.com/ios-filled/100/video.png)](videos/voice_feedback.mp4)
---

## 🔌 Wiring Diagram

### HC-SR04 Ultrasonic Sensor
```
VCC  → 5V
GND  → GND
TRIG → GPIO 23
ECHO → GPIO 24
```

### SG90 Servo Motor
```
VCC    → 5V
GND    → GND
Signal → GPIO 18
```

### L298N Motor Driver
```
IN1 → GPIO 17
IN2 → GPIO 27
IN3 → GPIO 22
IN4 → GPIO 10
ENA → GPIO 4 (PWM)
ENB → GPIO 25 (PWM)
```

### HC-05 Bluetooth Module
```
VCC → 5V
GND → GND
TX  → RX (GPIO 15)
RX  → TX (GPIO 14)
```

---

## ⚠️ Important Notes

- **Safety First**: Test in a controlled environment before real-world use
- **Flat Surface**: Best performance on level ground
- **Power Supply**: Ensure adequate battery capacity for motors and Pi
- **Wiring**: Double-check all connections before powering on
- **Bluetooth Pairing**: Module must be paired with receiving device
- **GPIO Permissions**: May require `sudo` for GPIO access
- **Distance Calibration**: Adjust threshold values based on environment

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Servo not moving | Check pigpio daemon is running: `sudo pigpiod` |
| No Bluetooth connection | Verify pairing and serial port configuration |
| Motors not responding | Check L298N connections and power supply |
| Ultrasonic errors | Ensure TRIG/ECHO pins are correctly wired |
| Permission denied | Run with `sudo` or add user to gpio group |

---

## 🔧 Configuration

Edit these values in `raspberrypi.py` to customize behavior:
```python
# Distance threshold (cm)
OBSTACLE_DISTANCE = 30

# Motor speed (0-100)
MOTOR_SPEED = 70

# Scan angles
LEFT_ANGLE = 180
CENTER_ANGLE = 90
RIGHT_ANGLE = 0

# Turn duration (seconds)
TURN_TIME = 0.5
```

---

## 📚 Dependencies

- Python 3.7+
- RPi.GPIO
- pigpio
- pyserial
- opencv-python (optional, for camera integration)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open-source and available for academic and personal use. Feel free to modify and distribute.

---

## 👨‍💻 Author

Created as an assistive navigation solution for enhanced mobility and safety.

---

## 🌟 Acknowledgments

- Raspberry Pi Foundation for excellent documentation
- HC-SR04 and L298N community resources
- Open-source robotics community

---

**Made with ❤️ for accessible robotics**
