import tkinter as tk
import WaveBox.App as App
import WaveBox.history as history

if __name__ == '__main__':
    
    App.work_space_loc = history.get_last()
    
    while App.live:
        App.run()

