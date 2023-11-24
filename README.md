# Home Monitoring System

## Tech Stack

- Backend
    - Python, Django, MySQL, OpenCV, nginx, ECS
- Frontend
    - Vue, Axios, Element plus, Rellax, Kinesis, Echarts
- Models
    - PyTorch, Tensorflow

## Module

- User Management
    - ORM framework
    - model: face recognition + blinking detection for dynamic face login
- Pedestrian and Pet Recognition
    - model: object detection
- Emotion Recognition
    - model: micro expression recognition + emotion recognition
- Intrusion Detection
    - model: face recognition
    - Video Storage: H.264 encoded MP4 video before and after intrusion
- Model Service
    - model: image captioning + 3D to 2D model + fall detection
- Disabilities Friendly
    - model: gesture recognition
    - Self-defined gestures

## Docs

Requirement Analysis Document, Design Document, Testing Document, User Manual.

## Project Structure

'family_monitor_server/' is the project container.

Under 'user/' are functionalities related to users.

Under 'recognition/' are functionalities related to models.

Under 'model/' are various models. If a model contains multiple files, please create a subfolder.

## Installation Steps

Below requires the command line working directory to be in the root folder of this repository.

### Prepare Python Virtual Environment

#### Create Virtual Environment

```bash
python -m venv venv
```

#### Activate Virtual Environment

**Windows**

```powershell
.\venv\Scripts\activate.bat
```

**Linux**

```bash
source ./venv/bin/activate
```

When the command prompt displays (venv), it signifies that the virtual environment has been successfully activated.

### Install Required Dependencies

#### One-click installation via requirements.txt, after entering the virtual environment in the previous step (venv), run the following command in the command line

```bash
pip install -r requirements.txt
```

### Database

```bash
Copy db_setting.cnf to the project root directory.
```

[//]: # (### 数据库迁移（对数据模型的修改）)

[//]: # (```bash)

[//]: # (py manage.py makemigrations)

[//]: # (```)

[//]: # (```bash)

[//]: # (py manage.py migrate)

[//]: # (```)

### Model Configuration

Copy the models sent in the group to the specified directory.

- Place model_U.pth under model/emotional_recognition/
- After extracting model.zip, place the four files in model/microexpression_recognition/model/
- Place shape_predictor_68_face_landmarks.dat under model/isLive/gaze_tracking/trained_models/
- Place checkpoint.pt under model/gaze_vector/
- Place weight389123791.pth and weight493084032.pth under /model/image_caption/models/
- Place the 'Models' folder from the extracted Fall_Models under /model/fall-detect-track/