import os

os.system('pip install -r systems\\commons\\requirements.txt')
os.system('pyinstaller --onefile -w systems\\test.py')

os.rename("dist\\SERVER.exe", "SERVER.exe")

