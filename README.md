# EFEKTA Air Quality Station 2

![EFEKTA Air Quality Station 2](https://raw.githubusercontent.com/smartboxchannel/EFEKTA_Air_Quality_Station_2/refs/heads/main/Images/1.jpg) 

## Overview

**EFEKTA Air Quality Station 2** is an air quality monitoring sensor featuring:
- **Measurements**: CO2, PM0.5, PM1.0, PM2.5, PM4, PM10, PM Size, VOC Index, NOx Index, Formaldehyde (Index C), Ozone (Index O), Temperature, Humidity, Illuminance
- **Display**: 3.2-inch TFT color display
- **Connectivity**: Zigbee 3.0

The display shows CO2, PM2.5, VOC, Formaldehyde/Ozone levels with color indicators and 24-hour historical graphs.

## Network Role

The sensor operates as a **Zigbee Router**. Optionally, it can be flashed with firmware that makes it an **End Device** (available upon request).

## Particulate Matter (PM) Sensor Features

The SPS30 sensor measures:
- **Mass concentration**: PM1, PM2.5, PM4, PM10 (µg/m³)
- **Number concentration**: PM0.5, PM1, PM2.5, PM4, PM10 (#/cm³)
- **Dominant particle size** in sampled air (PM Size)

**Auto-cleaning**: Scheduled automatic fan cleaning removes accumulated dust. Manual cleaning can also be triggered.

## VOC Compensation

Temperature and relative humidity data are used to calculate **absolute humidity**, which is fed to the VOC sensor (SGP40) in real time. This allows the VOC sensor to calculate the Volatile Organic Compound index more accurately.

## CO2 Accuracy

You can set the **altitude above sea level** for more precise CO2 measurements.

## Time Synchronization

The sensor receives time through the Zigbee network automatically. Date and time are shown on the display.

## Display Backlight

- **Adaptive backlight**: Automatically adjusts based on room illuminance
- **Night mode**: Scheduled backlight shutdown during user-defined hours

## Joystick Controls

| Action | Function |
|--------|----------|
| Press UP | Enable night mode (default: 23:00–07:00) |
| Press DOWN | Toggle adaptive backlight ON/OFF (when OFF, fixed 80% brightness) |

These basic controls work even without a Zigbee network.

## Home Assistant Integration

The sensor works with **Home Assistant** via **Zigbee2MQTT**.

## Exposed Entities (Measured Data)

| Entity | Description | Unit |
|--------|-------------|------|
| CO2 | Carbon dioxide level | ppm |
| PM2.5 | Mass concentration of particles ≤2.5 µm | µg/m³ |
| PM1 | Mass concentration of particles ≤1 µm | µg/m³ |
| PM4 | Mass concentration of particles ≤4 µm | µg/m³ |
| PM10 | Mass concentration of particles ≤10 µm | µg/m³ |
| PM Size | Dominant particle size in sampled air | µm |
| PMn 0.5 | Number concentration of particles ≤0.5 µm | #/cm³ |
| PMn 1 | Number concentration of particles ≤1 µm | #/cm³ |
| PMn 2.5 | Number concentration of particles ≤2.5 µm | #/cm³ |
| PMn 4 | Number concentration of particles ≤4 µm | #/cm³ |
| PMn 10 | Number concentration of particles ≤10 µm | #/cm³ |
| VOC index | Volatile Organic Compounds index | index point |
| NOx index | Nitrogen Oxides index | index point |
| Formaldehyde/Ozone | Formaldehyde or Ozone level | ppb |
| Temperature | Measured temperature *1 | °C |
| Humidity | Measured relative humidity *2 | % |
| Illuminance | Measured illuminance *3 | lux |
| Linkquality | Signal strength / link quality | — |

### Notes on measurements

> *1,*2 Temperature and humidity from the built-in SHT40 sensor are primarily used internally to calculate absolute humidity for the VOC sensor (SGP40). They are exposed to the network as secondary data since they are available.

> *3 Illuminance sensor is used for adaptive backlight control. Raw data is sent to the host (Zigbee2MQTT, ZHA, etc.), which recalculates it into lux. The resulting illuminance value may not precisely match real-world lux levels.

## Configurable Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| Report delay | Data reporting interval to the network | 15 seconds |
| Auto brightness | Enable/disable adaptive display brightness | Enabled |
| Night onoff backlight | Full backlight shutdown in night mode | Disabled |
| Night on backlight | Night mode start time | — |
| Night off backlight | Night mode end time | — |
| Temperature offset | Temperature adjustment (step 0.1°C) | 0 |
| Humidity offset | Humidity adjustment (step 1%) | 0 |
| Formaldehyde offset/Ozone offset | Formaldehyde/Ozone adjustment (step 1 ppb) | 0 |
| Auto clean interval | Automatic fan cleaning interval (0 = disabled) | 7 days |
| Manual clean | One-time manual fan cleaning trigger | — |
| Set altitude | Altitude above sea level for CO2 accuracy | — |
| Forced_recalibration | Manual forced calibration #1 (fresh air, 15 min → 450 ppm) | — |
| Manual_forced_recalibration | Manual forced calibration #2 (reference sensor, 15 min side-by-side) | — |
| Automatic scal | Automatic self-calibration (weekly) | Enabled |
| Factory_reset_co2 | Reset CO2 sensor to factory settings | — |

### About CO2 calibration

> *1,*2 Manual forced CO2 calibration is **optional and not recommended** for new sensors. Automatic background calibration (weekly adjustment) is enabled by default. You cannot damage the sensor by experimenting, and factory reset is always available.

## Network Join & Leave

### Join (Add to network)
1. Enable joining in Zigbee2MQTT
2. Power the sensor via USB-C
3. If the sensor is already running without a network, press and hold the side joystick button until the join message appears on the display

### Leave (Remove from network)
Press and hold the joystick button **straight in** for 10 seconds until the leave message appears. The sensor will clear all stored settings.

You can also remove the sensor from Zigbee2MQTT without using "force remove".

### Troubleshooting joining issues
Place the sensor within **1–2 meters** of the coordinator or a router with good signal strength during the joining process.

## Pollution Level Indicators

| Color | Meaning |
|-------|---------|
| 🟢 Green | Normal |
| 🟡 Yellow | Acceptable |
| 🟠 Orange | Poor |
| 🔴 Red | Dangerous |

### PM2.5 (µg/m³)

| Range | Color |
|-------|-------|
| ≤ 35 | 🟢 Green |
| > 35 … ≤ 60 | 🟡 Yellow |
| > 60 … ≤ 150 | 🟠 Orange |
| > 150 | 🔴 Red |

### CO2 (ppm)

| Range | Color |
|-------|-------|
| ≤ 650 | 🟢 Green |
| > 650 … ≤ 850 | 🟡 Yellow |
| > 850 … ≤ 1400 | 🟠 Orange |
| > 1400 | 🔴 Red |

### VOC (index point)

| Range | Color |
|-------|-------|
| < 150 | 🟢 Green |
| > 150 … ≤ 250 | 🟡 Yellow |
| > 250 … ≤ 350 | 🟠 Orange |
| > 350 | 🔴 Red |

### Formaldehyde / Ozone (ppb)

| Range | Color |
|-------|-------|
| < 50 | 🟢 Green |
| > 50 … ≤ 100 | 🟡 Yellow |
| > 100 … ≤ 150 | 🟠 Orange |
| > 150 | 🔴 Red |

## Technical Specifications

| Parameter | Value |
|-----------|-------|
| Model | EFEKTA Air Quality Station 2 |
| Protocol | ZigBee 3.0 |
| Radio module | EBYTE E18-MS1PA1-IPEX (20 dBm) |
| Main sensor | SCD40 (digital photoacoustic NDIR CO2 sensor, PASens® and CMOSens® technology) |
| Additional sensor #1 | SPS30 (MCERTS-certified PM sensor, laser scattering, anti-contamination technology, >10 year lifespan) |
| Additional sensor #2 | SGP41 (digital MEMS VOC and NOx sensor, CMOSens® Technology) |
| Additional sensor #3 | ZE08K-CH2O (electrochemical formaldehyde sensor) **or** ZE25A-O3 (electrochemical ozone sensor) |
| CO2 measurement range | 0–10000 ppm |
| CO2 accuracy (400–2000 ppm) | ±(50 ppm + 5% of reading) |
| CO2 drift (5 years, ASC enabled) | ±(5 ppm + 0.5% of reading) |
| PM measurement range | 0–1000 µg/m³ |
| PM accuracy (0–1000 µg/m³) | ±10% |
| VOC measurement range | 0–500 index points |
| Formaldehyde measurement range | 0–5000 ppb |
| Formaldehyde sensitivity | ±10 ppb |
| Ozone measurement range | 0–10000 ppb |
| Ozone sensitivity | ±10 ppb |
| Temperature sensor (SHT40) range | -40°C to +125°C |
| Temperature accuracy | ±0.25°C |
| Humidity sensor (SHT40) range | 0–100% RH |
| Humidity accuracy | ±3% |
| Enclosure dimensions | 92 × 61 × 24 mm |
| Power | USB Type-C (supports fast charging protocols) |


### Home Assistant (Zigbee2MQTT) – EFEKTA Air Quality Station 2c

### Home Assistant (Zigbee2MQTT) – EFEKTA Air Quality Station 2o
