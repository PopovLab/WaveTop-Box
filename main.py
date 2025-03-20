import tkinter as tk
import WaveBox.App as App
import WaveBox.History as History

if __name__ == '__main__':
    
    App.work_space_loc = History.get_last()
    
    while App.live:
        App.run()

