from kandinsky import *
from ion import *
from time import *
import micropython as mp
from microtext import *

# Version : v1.0

drawed = False

mounth_names = [None, "Janvier", "Fe"+chr(769)+"vrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aou"+chr(770)+"t", "Septembre", "Octobre", "Novembre", "De"+chr(769)+"cembre"]

# Get color palette of the current theme
color_palette = get_palette()

# Exit using KEY_ONOFF to allow the usage of KEY_BACK
mp.kbd_intr(KEY_ONOFF)

events=[
("Pre"+chr(769)+"sidentielle 2022", "24/4/2022"),
("Nouvelle anne"+chr(769)+"e", "1/1/****"),
("Fe"+chr(770)+"te du travail", "1/5/****"),
("Paix 1945", "5/5/****"),
("Jour des morts", "1/11/****"),
("Armistice", "11/11/****"),
("Noe"+chr(776)+"l", "25/12/****"),
# Add your own date!
#("Name", "da/mo/year"),
# ** or ***** for any day/mounth/year
]

def get_week_day(day,mounth,years):
  c = (14-mounth)//12
  a = years-c
  m = mounth+12*c-2
  j = [6, 0, 1, 2, 3, 4, 5][(day+a+a//4-a//100+a//400+(31*m)//12)%7]
  return j


def get_mounth_lenght(mounth, years):
  return [None, 31, 28+(years%4==0 and years%400!=0), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mounth]

def draw_day(day, mounth, years, selected=False):
  global drawed

  if drawed and selected:
    fill_rect(0, 195, 320, 27, color_palette['HomeBackground'])
    drawed = False

  important = False
  for event in events:
    l_event = event[1].split("/")
    if (l_event[0] in [str(day),"{:0>2}".format(str(day)),"**"]) and (l_event[1] in [str(mounth),"{:0>2}".format(str(mounth)),"**"]) and (l_event[2] in [str(years),"****"]):
      important = True
      if selected:
        draw_string(event[0], 20, 198, color_palette['AccentText'], color_palette['HomeBackground'])
        drawed = True

  wd = get_week_day(day, mounth, years)
  x = 43+wd*33
  y = 65+(day-wd-2)//7*25
  if selected:
    fill_rect(x, y, 30, 25, color_palette['AccentText'])
    fill_rect(x+2, y+2, 26, 21, color_palette['HomeBackground'])
  else:
    fill_rect(x, y, 30, 25, color_palette['HomeBackground'])
  if important:
    draw_string("{:0>2}".format(day), x+5, y+3, color_palette['AccentText'], color_palette['HomeBackground'])
  else:
    draw_string("{:0>2}".format(day), x+5, y+3, color_palette['PrimaryText'], color_palette['HomeBackground'])


def draw_mounth(mounth, years, selected=0):
  fill_rect(0, 0, 320, 222, color_palette['HomeBackground'])
  draw_string("{:^20}".format(mounth_names[mounth]+" "+str(years)), 60, 0, color_palette['PrimaryText'], color_palette['HomeBackground'])
  for i in range(8):
    fill_rect(40+i*33, 20, 3, 175, color_palette['PrimaryText'])
  for i in range(7):
    draw_string(["Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"][i],48+i*33,23,(200,)*3, color_palette['HomeBackground'])
  for i in range(get_mounth_lenght(mounth, years)):
    draw_day(i+1, mounth, years, (i+1)==selected)


class Window():
  def pop_up(self, title):
    # Draw the countours of the window
    draw_line(39, 19, 274, 19, 'black')
    draw_line(39, 19, 39, 231, 'black')
    draw_line(274, 19, 274, 231, 'black')
    # Draw the background of the window
    fill_rect(40, 30, 234, 200, color_palette['HomeBackground'])
    fill_rect(40, 20, 234, 10, color_palette['Toolbar'])

    dms(title, 45, 21)

  def button(self, x, y, text, selected=False, size_factor=1):
    """
    selected: If true, contours and text colors become color_palette['AccentText'].
    size_factor (float): The default button size is multiplied by it.
    """
    x_size = 60*size_factor
    y_size = 20*size_factor
    # Draw_the countours of the button
    draw_line(x-1, y-1, x+x_size+2, y-1, 'black' if not selected else color_palette['AccentText'])
    draw_line(x-1, y+y_size+1, x+x_size+2, y+y_size+1, 'black' if not selected else color_palette['AccentText'])
    draw_line(x-1, y-1, x-1, y+y_size+2, 'black' if not selected else color_palette['AccentText'])
    draw_line(x+x_size+1, y, x+x_size+1, y+y_size+1, 'black' if not selected else color_palette['AccentText'])
  
  def ask(self, title):
    fill_rect(0, 0, 320, 222, 'blue')
    self.button(10, 10, "nop")
    while not keydown(KEY_OK):
      pass
    return True


def get_today():
    year, mounth, day, hour, minutes, seconds, a, b = localtime()
    return (int(day), int(mounth), int(year))


def main():
  quit = False
  selected, mounth, years = get_today()
  draw_mounth(mounth, years, selected)
  while not quit:
    while not (keydown(KEY_RIGHT) or keydown(KEY_LEFT) or keydown(KEY_UP) or keydown(KEY_DOWN) or keydown(KEY_OK) or keydown(KEY_HOME) or keydown(KEY_BACK)):
      pass

    if keydown(KEY_UP):
      draw_day(selected, mounth, years, False)
      selected -= 7

    elif keydown(KEY_DOWN):
      draw_day(selected, mounth, years, False)
      selected += 7

    if keydown(KEY_LEFT):
      draw_day(selected, mounth, years, False)
      selected -= 1

    elif keydown(KEY_RIGHT):
      draw_day(selected, mounth, years, False)
      selected += 1

    if keydown(KEY_HOME):
      selected, mounth, years = get_today()
      draw_mounth(mounth, years, selected)

    if keydown(KEY_OK):
      w.pop_up("Events on {}/{}/{}".format(selected, mounth, years))
      while not keydown(KEY_BACK):
        pass
      draw_mounth(mounth, years, selected)

    if keydown(KEY_BACK):
      quit = w.ask("Quit")
      break

    if selected > get_mounth_lenght(mounth, years):
      selected %= get_mounth_lenght(mounth, years)
      mounth += 1
      if mounth > 12:
        mounth = 1
        years += 1
      draw_mounth(mounth, years, selected)

    if selected < 1:
      mounth -= 1
      if mounth < 1:
        mounth = 12
        years -= 1
      selected = (selected-1) % get_mounth_lenght(mounth, years)+1
      draw_mounth(mounth, years, selected)

    draw_day(selected, mounth, years, True)
    sleep(0.1)


w = Window()
main()
