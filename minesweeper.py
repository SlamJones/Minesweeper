#!/usr/bin/env python3

import math
import os
import time
import random

from graphics import *

settings = {
    "debug_mode": False,
    "window_x": 1000,
    "window_y": 980,
    "bg_color": "black",
    "fg_color": "white",
    "square_size": 50,
    "rows_easy": 8,
    "rows_medium": 12,
    "rows_hard": 16,
    "mines_easy": 8,
    "mines_medium": 18,
    "mines_hard": 32,
    "button_width": 250,
    "button_height": 50,
    "button_spacing": 40,
    "header_height": 50,
}

grid = []


def clearscreen():
    os.system('clear')

def init():
    clearscreen()
    print("Welcome!")
    time.sleep(1)
    clearscreen()

def main():
    to_draw = []
    buttons = []
    button_names = ["Start","Settings","Exit"]
    
    win = GraphWin("Minesweeper",settings["window_x"],settings["window_y"],autoflush=False)
    win.setBackground(settings["bg_color"])
    titleX = settings["window_x"]/2
    titleY = settings["button_height"]
    subtitleY = titleY + settings["button_spacing"] + settings["button_height"]/2
    
    title = Text(Point(titleX, titleY),"Minesweeper")
    title.setSize(30)
    subtitle = Text(Point(titleX, subtitleY),"SlamJones 2022")
    subtitle.setSize(15)
    
    for text in [title,subtitle]:
        text.setTextColor(settings["fg_color"])
        text.setStyle("bold")
        
    to_draw.append(title)
    to_draw.append(subtitle)
    
    buttons_made = 2
    rect_P1Y = subtitleY + (
        buttons_made*(settings["button_height"] + settings["button_spacing"]))
    
    for button in button_names:
        rect_P1X = titleX - settings["button_width"]/2
        rect_P2X = titleX + settings["button_width"]/2
        rect_P1Y = subtitleY + (
            buttons_made*(settings["button_height"] + settings["button_spacing"]))
        rect_P2Y = rect_P1Y + settings["button_height"]
        
        rect_centerX = (rect_P1X + rect_P2X)/2
        rect_centerY = (rect_P1Y + rect_P2Y)/2
        
        rect = Rectangle(Point(rect_P1X,rect_P1Y),Point(rect_P2X,rect_P2Y))
        rect.setFill(settings["bg_color"])
        rect.setOutline(settings["fg_color"])
        rect.setWidth(2)
        
        text = Text(Point(rect_centerX,rect_centerY),button)
        text.setTextColor(settings["fg_color"])
        
        to_draw.append(rect)
        to_draw.append(text)
        
        buttons_made += 1
        buttons.append(
            {"x1": rect_P1X, "x2": rect_P2X, "y1": rect_P1Y, "y2": rect_P2Y, "name": button, "rect": rect, "text": text})
        
    for item in to_draw:
        item.draw(win)
    win.update()
    
    clickedOn = ""
    while clickedOn != "Exit":
        click = win.getMouse()
        clickX = click.getX()
        clickY = click.getY()
        clickedOn = ""
        for button in buttons:
            if clickX >= button["x1"] and clickX <= button["x2"] and clickY >= button["y1"] and clickY <= button["y2"]:
                clickedOn = button["name"]
                flash_button(win,button,0.2)
            else:
                button["rect"].setFill(settings["bg_color"])
                button["text"].setTextColor(settings["fg_color"])
        win.update()
        if clickedOn == "Start":
            header = subtitleY
            choices = ["Easy","Medium","Hard"]
            for item in to_draw:
                item.undraw()
            win.update()

            ##### GAME FUNCTION STACK #####
            ##### Choice is the difficulty as chosen by user #####
            choice = choice_buttons(win,choices,header)
            grid,rows = generate_grid(choice)
            draw_grid(win,grid,rows,choice)
            #####
            
            for item in to_draw:
                item.draw(win)
            win.update()
        elif clickedOn == "Exit":
            break
        elif clickedOn == "Settings":
            pass
        else:
            pass
    
    ######
    
    
    win.close()


def choice_buttons(win,choices,header):
    to_draw = []
    buttons = []
    
    centerX = settings["window_x"]/2
    P1X = centerX - settings["button_width"]/2
    P2X = centerX + settings["button_width"]/2
    P1Y = header
    P2Y = header + settings["button_height"]
    for choice in choices:
        P1Y = P2Y + settings["button_spacing"]
        P2Y = P1Y + settings["button_height"]
        button_rect = Rectangle(Point(P1X,P1Y),Point(P2X,P2Y))
        button_rect.setFill(settings["bg_color"])
        button_rect.setOutline(settings["fg_color"])
        button_rect.setWidth(2)
        button_centerY = (P1Y + P2Y)/2
        button_text = Text(Point(centerX,button_centerY),choice)
        button_text.setTextColor(settings["fg_color"])
        to_draw.append(button_rect)
        to_draw.append(button_text)
        buttons.append(
            {"name": choice, "x1": P1X, "x2": P2X, "y1": P1Y, "y2": P2Y, "rect": button_rect, "text": button_text,})
        
    for item in to_draw:
        item.draw(win)
    win.update()
    ####################
    click = win.getMouse()
    clickX = click.getX()
    clickY = click.getY()
    for button in buttons:
        if clickX >= button["x1"] and clickX <= button["x2"] and clickY >= button["y1"] and clickY <= button["y2"]:
            choice = button["text"].getText()
            flash_button(win,button,0.2)
        else:
            button["rect"].setFill(settings["bg_color"])
            button["text"].setTextColor(settings["fg_color"])
            choice = "Easy"
    ####################
    for item in to_draw:
        item.undraw()
    win.update()
    choice = choice.lower()
    return(choice)
    
    
def generate_grid(difficulty):
    difficulty = difficulty.lower()
    mines = settings["mines_"+difficulty]
    rows = settings["rows_"+difficulty]
    buttons = settings["rows_"+difficulty]**2

    button_list = []
    grid = [1,1]
    
    for i in range(buttons):
        button = {"x": grid[0], "y": grid[1], "mined":False, "clicked":False,}
        button_list.append(button)
        
        if grid[0] == rows:
            grid[0] = 1
            grid[1] += 1
        else:
            grid[0] += 1
        
    for i in range(mines):
        button = random.choice(button_list)
        while button["mined"]:
            button = random.choice(button_list)
        button["mined"] = True
    
    if settings["debug_mode"]:
        for button in button_list:
            print(str(button))
        print("{} buttons generated from {} x {}".format(
            str(len(button_list)),str(rows),str(rows)))
    return(button_list,rows)


def draw_grid(win,grid,rows,difficulty):
    to_draw = []
    buttons = []
    
    container_width = settings["square_size"]*rows
    container_height = container_width
    centerX = settings["window_x"]/2
    centerY = settings["window_y"]/2 + settings["header_height"]
    
    P1X = centerX - container_width/2
    P2X = centerX + container_width/2
    P1Y = centerY - container_height/2
    P2Y = centerY + container_height/2
    
    cont_P1X = P1X
    cont_P2X = P2X
    cont_P1Y = P1Y
    cont_P2Y = P2Y
    
    container = Rectangle(Point(P1X,P1Y),Point(P2X,P2Y))
    container.setFill(settings["bg_color"])
    container.setOutline(settings["fg_color"])
    container.setWidth(4)
    to_draw.append(container)
    
    #### Draw top GUI ####
    cP1X = centerX - settings["square_size"]*0.75
    cP2X = centerX + settings["square_size"]*0.75
    cP1Y = settings["button_spacing"]/2
    cP2Y = cP1Y + settings["square_size"]*1.5
    
    center_button = Rectangle(Point(cP1X,cP1Y),Point(cP2X,cP2Y))
    center_button.setFill(settings["bg_color"])
    center_button.setOutline(settings["fg_color"])
    center_button.setWidth(3)
    to_draw.append(center_button)
    
    center_text = Text(Point(centerX,(cP1Y+cP2Y)/2),"X")
    center_text.setTextColor(settings["fg_color"])
    center_text.setStyle("bold")
    center_text.setSize(16)
    to_draw.append(center_text)
    
    menu_button = {"rect": center_button, "text": center_text, "x1": cP1X, "y1": cP1Y, "x2": cP2X, "y2": cP2Y, "flag": False,}
    
    for i in range(rows):
        P1X += settings["square_size"]
        #P1Y += settings["square_size"]
        P2X += settings["square_size"]
        #P2Y += settings["square_size"]
        gridline_x = Line(Point(P1X,P1Y),Point(P1X,P2Y))
        gridline_x.setFill(settings["fg_color"])
        gridline_x.setOutline(settings["fg_color"])
        to_draw.append(gridline_x)
    
    P1X = centerX - container_width/2
    P2X = centerX + container_width/2
    P1Y = centerY - container_height/2
    P2Y = centerY + container_height/2
        
    for i in range(rows):
        #P1X += settings["square_size"]
        P1Y += settings["square_size"]
        #P2X += settings["square_size"]
        P2Y += settings["square_size"]
        gridline_y = Line(Point(P1X,P1Y),Point(P2X,P1Y))
        gridline_y.setFill(settings["fg_color"])
        gridline_y.setOutline(settings["fg_color"])
        to_draw.append(gridline_y)
    
    P1X = centerX - container_width/2
    P2X = centerX + container_width/2
    P1Y = centerY - container_height/2
    P2Y = centerY + container_height/2
    
    #######  GRIDS HAVE BEEN DRAWN  #######
    #######   NOW TO DRAW BUTTONS   #######
    ####### HOW TO GET X1,X2,Y1,Y2? #######
    
    ### P1X, P1Y is upper-left corner ###
    ### P2X, P2Y should only be calculated from P1X and P1Y ###
    
    for y in range(rows):
        for x in range(rows):
            P2X = P1X + settings["square_size"]
            P2Y = P1Y + settings["square_size"]

            button_centerX = (P1X+P2X)/2
            button_centerY = (P1Y+P2Y)/2

            button = Rectangle(Point(P1X,P1Y),Point(P2X,P2Y))
            button.setFill(settings["fg_color"])
            if settings["debug_mode"]:
                print("Button: x:{}->{}   y:{}->{}".format(
                    str(P1X),str(P2X),str(P1Y),str(P2Y)))
            button_text = Text(Point(button_centerX,button_centerY),"")
            button_text.setTextColor(settings["bg_color"])  
            
            button_all = {"rect": button, "text": button_text, "x1": P1X, "y1": P1Y, "x2": P2X, "y2": P2Y, "mined": False, "clicked": False, "adjacent": 0}
            buttons.append(button_all)

            ### Set P1 for next button ###
            P1X += settings["square_size"]
            #P1Y += settings["square_size"]
          

            to_draw.append(button)
            to_draw.append(button_text)
        P1X = centerX - container_width/2
        P1Y += settings["square_size"]
                           
                    
    
    for item in to_draw:
        item.draw(win)
    win.update()
    
    key = ""
    
    if settings["debug_mode"]:
        print(str(len(buttons))+" buttons made")

    ##### SET A FEW BUTTONS AS MINED #####
    difficulty = difficulty.lower()
    mines = settings["mines_"+difficulty]
    
    for i in range(mines):
        button = random.choice(buttons)
        while button["mined"]:
            button = random.choice(buttons)
        button["mined"] = True
        
        
    ##### For the rest of the buttons, 
    ##### assign a number that equals the 
    ##### number of adjacent mines
    ##### But how??
    ##### Somehow it counts blank squares(outside play area)
    ##### in the mine count per square
    
    ##### Take each button individually
    ##### If Taken button is NOT mined
    ##### Check it against every other button
    ##### If checked button is adjacent to Taken button, +1 to adjacent
    for button in buttons:
        if not button["mined"]:
            centerX = (button["x1"] + button["x2"]) / 2
            centerY = (button["y1"] + button["y2"]) / 2
            
            for check_button in buttons:
                if check_button["mined"]:
                #if check_button is not button:
                    ##### Test LEFT #####
                    testX = centerX - settings["square_size"]
                    if (testX >= check_button["x1"] and testX <= check_button["x2"] and centerY >= check_button["y1"] and centerY <= check_button["y2"]):
                        button["adjacent"] += 1

                    ##### Test RIGHT #####
                    testX = centerX + settings["square_size"]
                    if (testX >= check_button["x1"] and testX <= check_button["x2"] and centerY >= check_button["y1"] and centerY <= check_button["y2"]):
                        button["adjacent"] += 1

                    ##### Test ABOVE #####
                    testY = centerY - settings["square_size"]
                    if (centerX >= check_button["x1"] and centerX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                        button["adjacent"] += 1

                    ##### Test BELOW #####
                    testY = centerY + settings["square_size"]
                    if (centerX >= check_button["x1"] and centerX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                        button["adjacent"] += 1
                        
                    ##### Test UPPER-LEFT #####
                    testX = centerX - settings["square_size"]
                    testY = centerY - settings["square_size"]
                    if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                        button["adjacent"] += 1

                    ##### Test UPPER-RIGHT #####
                    testX = centerX + settings["square_size"]
                    testY = centerY - settings["square_size"]
                    if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                        button["adjacent"] += 1
                        
                    ##### Test LOWER-LEFT #####
                    testX = centerX - settings["square_size"]
                    testY = centerY + settings["square_size"]
                    if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                        button["adjacent"] += 1

                    ##### Test LOWER-RIGHT #####
                    testX = centerX + settings["square_size"]
                    testY = centerY + settings["square_size"]
                    if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                        button["adjacent"] += 1
    
    
    
    
    #####
    ##### PLAYER INPUT STACK #####
    while key == "":
        key = win.checkKey()
        click = win.checkMouse()
        try:
            clickX = click.getX()
            clickY = click.getY()
        except:
            clickX = 0
            clickY = 0
        if click != None and settings["debug_mode"]:
            print(str(click))
        ### CHECK IF PLAYER CLICKED FLAG BUTTON ###
        if clickX >= menu_button["x1"] and clickX <= menu_button["x2"] and clickY >= menu_button["y1"] and clickY <= menu_button["y2"]:
            if not menu_button["flag"]:
                menu_button["text"].setTextColor(settings["bg_color"])
                menu_button["text"].setText("?")
                menu_button["rect"].setFill(settings["fg_color"])
                
                menu_button["flag"] = True
            else:
                menu_button["text"].setTextColor(settings["fg_color"])
                menu_button["text"].setText("X")
                menu_button["rect"].setFill(settings["bg_color"])
                
                menu_button["flag"] = False
        ### THEN CHECK IF PLAYER CLICKED A GRID BUTTON ###
        for button in buttons:
            if clickX >= button["x1"] and clickX <= button["x2"] and clickY >= button["y1"] and clickY <= button["y2"] and not button["clicked"]:
                if settings["debug_mode"]:
                    print("Clicked on {}".format(str(button)))
                if menu_button["flag"]:
                    button["text"].setText("?")
                    win.update()
                else:
                    #flash_button(win,button,0.0001)
                    button["rect"].setFill(settings["bg_color"])
                    button["text"].setTextColor(settings["fg_color"])
                    if button["mined"]:
                        button["text"].setText(":(")
                        win.update()
                        key = "Escape"
                        time.sleep(0.2)
                        for button in buttons:
                            if button["mined"]:
                                button["text"].setText("X")
                        win.update()
                        show_info_box(win,"KaBoom!  You lose!",1.5)
                    elif button["adjacent"] == 0:
                        check_adjacent(win,buttons,button)
                        reveal_borders(win,buttons)
                    else:
                        button["text"].setText(str(button["adjacent"]))
                    button["clicked"] = True
        win.update()
        victory = check_victory(win,buttons)
        if victory:
            key = "Escape"
    ##### END PLAYER INPUT STACK #####
    #####
    
    for item in to_draw:
        item.undraw()
    win.update()
    
    
def check_victory(win,buttons):
    count = 0
    mines = 0
    for button in buttons:
        if button["mined"]:
            mines += 1
        if not button["clicked"]:
            count += 1
    if mines == count:
        for button in buttons:
            if not button["clicked"]:
                button["text"].setText("X")
        win.update()
        show_info_box(win,"You win!  Well played!",0)
        return(True)
    return(False)
    
    
def check_adjacent(win,buttons,button):
    to_reveal = []    
    centerX = (button["x1"] + button["x2"]) / 2
    centerY = (button["y1"] + button["y2"]) / 2
        
    for check_button in buttons:
        if not check_button["clicked"] and check_button["adjacent"] == 0:
            #if check_button is not button:
            ##### Test LEFT #####
            testX = centerX - settings["square_size"]
            if (testX >= check_button["x1"] and testX <= check_button["x2"] and centerY >= check_button["y1"] and centerY <= check_button["y2"]):
                to_reveal.append(check_button)

            ##### Test RIGHT #####
            testX = centerX + settings["square_size"]
            if (testX >= check_button["x1"] and testX <= check_button["x2"] and centerY >= check_button["y1"] and centerY <= check_button["y2"]):
                to_reveal.append(check_button)

            ##### Test ABOVE #####
            testY = centerY - settings["square_size"]
            if (centerX >= check_button["x1"] and centerX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                to_reveal.append(check_button)

            ##### Test BELOW #####
            testY = centerY + settings["square_size"]
            if (centerX >= check_button["x1"] and centerX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                to_reveal.append(check_button)
                        
            ##### Test UPPER-LEFT #####
            testX = centerX - settings["square_size"]
            testY = centerY - settings["square_size"]
            if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                to_reveal.append(check_button)

            ##### Test UPPER-RIGHT #####
            testX = centerX + settings["square_size"]
            testY = centerY - settings["square_size"]
            if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                to_reveal.append(check_button)
                        
            ##### Test LOWER-LEFT #####
            testX = centerX - settings["square_size"]
            testY = centerY + settings["square_size"]
            if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                to_reveal.append(check_button)

            ##### Test LOWER-RIGHT #####
            testX = centerX + settings["square_size"]
            testY = centerY + settings["square_size"]
            if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                to_reveal.append(check_button)
                
    for item in to_reveal:
        flash_button(win,item,0)
        item["clicked"] = True
        check_adjacent(win,buttons,item)
    win.update()
    
    
    ###### Recieves a list of all buttons
    ###### Determine which buttons have been clicked and have 0 adjacent mined buttons
    ###### Gather a list of all buttons adjacent to determined buttons
    ###### Reveal list
    
def reveal_borders(win,buttons):
    to_reveal = []
    for button in buttons:
        if button["clicked"] and button["adjacent"] == 0:
            for check_button in buttons:
                centerX = (button["x1"] + button["x2"]) / 2
                centerY = (button["y1"] + button["y2"]) / 2
                #if check_button is not button:
                ##### Test LEFT #####
                testX = centerX - settings["square_size"]
                if (testX >= check_button["x1"] and testX <= check_button["x2"] and centerY >= check_button["y1"] and centerY <= check_button["y2"]):
                    to_reveal.append(check_button)

                ##### Test RIGHT #####
                testX = centerX + settings["square_size"]
                if (testX >= check_button["x1"] and testX <= check_button["x2"] and centerY >= check_button["y1"] and centerY <= check_button["y2"]):
                    to_reveal.append(check_button)

                ##### Test ABOVE #####
                testY = centerY - settings["square_size"]
                if (centerX >= check_button["x1"] and centerX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                    to_reveal.append(check_button)

                ##### Test BELOW #####
                testY = centerY + settings["square_size"]
                if (centerX >= check_button["x1"] and centerX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                    to_reveal.append(check_button)

                ##### Test UPPER-LEFT #####
                testX = centerX - settings["square_size"]
                testY = centerY - settings["square_size"]
                if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                    to_reveal.append(check_button)

                ##### Test UPPER-RIGHT #####
                testX = centerX + settings["square_size"]
                testY = centerY - settings["square_size"]
                if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                    to_reveal.append(check_button)

                ##### Test LOWER-LEFT #####
                testX = centerX - settings["square_size"]
                testY = centerY + settings["square_size"]
                if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                    to_reveal.append(check_button)

                ##### Test LOWER-RIGHT #####
                testX = centerX + settings["square_size"]
                testY = centerY + settings["square_size"]
                if (testX >= check_button["x1"] and testX <= check_button["x2"] and testY >= check_button["y1"] and testY <= check_button["y2"]):
                    to_reveal.append(check_button)
            
    for item in to_reveal:
        flash_button(win,item,0)
        item["text"].setTextColor("white")
        if item["adjacent"] > 0:
            item["text"].setText(str(item["adjacent"]))
        item["clicked"] = True
    win.update()
    
    
def show_info_box(win,text,timer):
    to_draw = []
    centerX = settings["window_x"]/2
    centerY = settings["window_y"]/2
    
    P1X = centerX - settings["button_width"]
    P2X = centerX + settings["button_width"]
    P1Y = centerY - settings["button_height"]
    P2Y = centerY + settings["button_height"]
    
    box = Rectangle(Point(P1X,P1Y),Point(P2X,P2Y))
    box.setFill(settings["bg_color"])
    box.setOutline(settings["fg_color"])
    box.setWidth(3)
    
    text = Text(Point(centerX,centerY),text)
    text.setTextColor(settings["fg_color"])
    text.setStyle("bold")
    
    to_draw.append(box)
    to_draw.append(text)
    
    for item in to_draw:
        item.draw(win)
    win.update()
    
    if timer == 0:
        win.getMouse()
    else:
        time.sleep(timer)

    for item in to_draw:
        item.undraw()
    win.update()
    
    
def flash_button(win,button,flash_time):
    button["rect"].setFill(settings["fg_color"])
    button["text"].setTextColor(settings["bg_color"])
    if flash_time > 0:
        win.update()
        time.sleep(flash_time)
    button["rect"].setFill(settings["bg_color"])
    button["text"].setTextColor(settings["fg_color"])
    if flash_time > 0:
        win.update()
        
        
def farewell():
    clearscreen()
    print("Farewell!")
    clearscreen()
    
    

init()
main()
farewell()