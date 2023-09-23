from kandinsky import *
from ion import *
from time import *
import micropython as mp

# Version : v1.0

drawed = False

mounth_names = [None, "Janvier", "Fe"+chr(769)+"vrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aou"+chr(770)+"t", "Septembre", "Octobre", "Novembre", "De"+chr(769)+"cembre"]

# Get color palette of the current theme
color_palette = get_palette()

# Exit using KEY_ONOFF to allow the usage of KEY_BACK
mp.kbd_intr(KEY_ONOFF)


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


def get_today():
    year, mounth, day, hour, minutes, seconds, a, b = localtime()
    return (int(day), int(mounth), int(year))


def start():
  selected, mounth, years = get_today()
  draw_mounth(mounth, years, selected)
  while not keydown(KEY_ONOFF):
    while not (keydown(KEY_RIGHT) or keydown(KEY_LEFT) or keydown(KEY_UP) or keydown(KEY_DOWN) or keydown(KEY_EXE) or keydown(KEY_HOME)):
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

#Pour les interresses, les "+chr(xxx)+"
#permette d'avoir des accents.
#"e"+chr(768) => accent aigu
#"e"+chr(769) => accent grave
#+770 => accent circonflexe
#776 => tremas

# == Vous pouvez changer les  ==
# == couleurs au tout debut ! ==

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
start()
