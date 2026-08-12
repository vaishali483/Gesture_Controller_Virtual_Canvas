# Gesture-Controlled Virtual Canvas

A real-time computer vision project that lets users draw in the air using hand gestures captured through a webcam.

## Features

* Real-time hand tracking using **MediaPipe Hands**
* Draw on a virtual canvas using the **index finger**
* Select drawing colours using **thumb gestures**
* Clear the canvas using a **fist gesture**
* Live webcam and drawing overlay using **OpenCV**

The implementation tracks hand landmarks from the webcam feed and uses simple gesture rules to control drawing behaviour.

## Tech Stack

* Python
* OpenCV
* MediaPipe
* NumPy

## Installation

```bash
git clone <your-repository-url>
cd <repository-name>

python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python air_drawing.py
```

Allow webcam access when prompted.

Press **Q** to exit the application.

## Gesture Controls

| Gesture                        | Action        |
| ------------------------------ | ------------- |
| Index finger raised            | Draw          |
| Thumb open near colour palette | Change colour |
| Fist                           | Clear canvas  |

## Project Purpose

This project demonstrates practical computer vision, real-time video processing, hand landmark tracking, gesture recognition, and rapid prototyping in Python.
