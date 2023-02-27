pyinstaller -w --clean -F -n RainbowPiano -i "NONE" --distpath .\ .\main_gui.py
rmdir /S /Q .\build\
del /F /S /Q .\*.spec