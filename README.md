# Image Classification of Lettuce Seeds
> **Note**: The code is very messy. Feel free to modularize and improve.
## Publication
https://www.wcse.org/index.php?m=content&c=index&a=show&catid=26&id=1300

## Installation
Steps to install and run the project:


### 1. Create a project folder
Create a dedicated folder for this project and navigate into it:
```bash
mkdir lettuce_project
cd lettuce_project
```

### 2. Get Code

#### Option A: Clone the repository using Git (recommended)
```bash
git clone https://github.com/yourusername/lettuce-seed-classifier.git
cd lettuce-seed-classifier
```

#### Option B: Download as ZIP

- Click the green **Code** button → **Download ZIP**
- Extract the ZIP file into your `lettuce_project` folder
- Open Command Prompt in the extracted folder

### 3. Install python 3.9
Download from: 
https://www.python.org/downloads/release/python-390/

### 4. Setup virtual environemnt
```bash
py -3.9 -m venv venv

source venv/bin/activate
```

### 5. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage
### 1. Run the main.py file
```bash
py main.py
```
### 2. Capture
- Click the Capture button to open the camera
- Press the space bar to capture the image or esc button to quit
- Save the file with any name or click cancel to classify without saving image
### 3. Classify
- Click the Classify button to predict the variety

