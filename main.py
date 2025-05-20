# main
"""
    run generic and main file
"""

from fileHandler import FileHandler

if __name__ == '__main__':
    fileHandler = FileHandler()
    text = fileHandler.pullFile()
    analysis = fileHandler.analyzeCode(text)


