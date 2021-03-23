#!/envbin/python3
## for mouse actions
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from concurrent.futures import ThreadPoolExecutor ## to do 3 things later
import random       ## for randint() and choice()
import time         ## for sleep()
import UPL          ## Cross stdlib

keyboard = KeyboardController()
mouse = MouseController()

def do_actions(keys=[], hold=False, press_count=1, mode="keyboard") -> None:
    print(mode)
    if mode == "keyboard":
        if hold:
            for i in range(press_count):
                for key in keys:
                    keyboard.press(key)
                    time.sleep(1)
                    keyboard.release(key)
        else:
            for i in range(press_count):
                keyboard.type(''.join(keys))
    
    elif mode == "mouse":
        mouse_btn = keys[0] ## only 1 inpt
        mouse_btn = Button.left if mouse_btn == "left" else Button.right

        mouse.click(mouse_btn, press_count)

    elif mode == "mouse_move":
        mouse.move(keys[0], keys[1])

    elif mode == "action":
        action = keys[0]
        if action == "mine_down":
            mouse.move(0, 0)
            mouse.press(Button.right)
            time.sleep(press_count)
            mouse.release(Button.right)

        elif action == "sound":
            sound = keys[1]
            UPL.upl_sound.playsound(sound)
            
        elif action == "walk_jump":
            keyboard.press("w")
            keyboard.press(Key.space)
            time.sleep(press_count)
            keyboard.release("w")
            keyboard.relase(Key.space)

        elif action == "sprint":
            keyboard.press('w')
            keyboard.press(Key.shift)
            time.sleep(press_count)
            keyboard.relase('w')
            keyboard.release(Key.shift)

    elif mode == "gui":
        tmp = ''
        prompt = ''.join(keys)
        while tmp != prompt:
            tmp = UPL.gui.prompt(title="Type it!", text=prompt)
        
        say_words("good job")
    return

def say_words(words="What am I doing?") -> None:
    UPL.upl_sound.speech(words)
## main func takes dict returns nothing
def main(json_data:dict) -> None:
    
    ## set local vars that are called often
    ## timing stuff
    min_time_dif = json_data['min_time_dif']
    max_time_dif = json_data['max_time_dif']
    
    ## actions that will be called later
    action_calls = json_data['actions']

    ## init wait
    time.sleep(random.randint(10, 100))

    ## we will be in this func forever
    while True:
        
        ## getting a random item from action_calls

        action_name = random.choice(list(action_calls.keys()))
        action = action_calls[action_name]
        print(f"running {action_name}")

        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(say_words, (action["say"]))
            do_actions(action["keys"], action["hold"],action["count"] ,action["mode"])

        ## wait for next event (rand number from 100, 600 in default config) (seconds)
        time.sleep(random.randint(min_time_dif, max_time_dif))
   

## SCRIPT STARTS HERE ##
if __name__ == "__main__":

    print("Welcome to BeepBopStuff\nCode by: Cross\nName by: Ash")
    
    ## basic json stuff
    json_file = "conf.json" ## made to ref later
    json_data = UPL.Core.file_manager.getData_json(json_file) ## getting all json data (dict)

    ## main func call (expects int)
    main(json_data)