#  
Python scripts to get playlist information from YouTube

## 1. Create Virtual Environment 

The name of the python virtual I use for windows is 'venv', and 'linvenv' for linux.

### 1.1 Command to create virtual environment
```bash
# To create the virtual environment use the command
python -m venv <venv-name>

# for Win 
python -m venv venv
source ./venv/Scripts/activate

#for linux
python -m venv linvenv
source ./linvenv/bin/activate
```

### 1.2 Check pip tool is using the venv dir
```
pip --version
```
```bash
# print pip binary location before activate virtual environment
cool@TrailGate:/mnt/e/repo/vidory/YTPlayLister$ pip --version
pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)

# ctivate virtual environment
cool@tTrailGate:/mnt/e/repo/vidory/YTPlayLister$ . ./linvenv/bin/activate

# print pip binary location after activate virtual environment
(linvenv) cool@TrailGate:/mnt/e/repo/vidory/YTPlayLister$ pip --version
pip 20.0.2 from /mnt/e/repo/vidory/ytplaylister/linvenv/lib/python3.8/site-packages/pip (python 3.8)
```

## 2. Install the packages in the venv

```bash
pip install pandas
pip install argparse
pip install dotenv
pip install --upgrade google-api-python-client
pip install --upgrade google-auth-oauthlib google-auth-httplib2
```

### Sample Python code for youtube.playlistItems.list
- See instructions for running these [code samples](ttps://developers.google.com/explorer-help/code-samples#python)