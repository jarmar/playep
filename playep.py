#!/usr/bin/python

import os
import sys
import re

### 'config' ###
movie_player_of_choice = 'vlc'
################

known_movie_types = ['mkv', 'avi', 'mp4']

def cwd_filenames():
  cwd = os.getcwd()
  return os.listdir(cwd)

def make_sense_of_input(input_str):
  regex = '((?<=S)[0-9]+)?E?([0-9]+)'
  input_str = input_str.upper()
  m = re.search(regex, input_str)
  if not m:
    print "error: couldn't parse that into an episode number."
    exit()
  season  = m.group(1)
  episode = m.group(2)
  if len(episode) < 2:
    episode = '0' + episode
  if season:
    if len(season) < 2:
      season = '0' + season
    return 'S' + season + 'E' + episode
  else:
    return 'E' + episode

def is_this_a_movie_file(pathname):
  i = pathname.rfind('.')
  extension = pathname[i + 1:]
  return extension in known_movie_types

def find_that_file(ep_str):
  filenames = cwd_filenames()
  candidates = filter(is_this_a_movie_file,
                      filter(lambda n: n.upper().find(ep_str) != -1, filenames))
  if not candidates:
    print "error: can't find episode " + ep_str + " in this folder."
    exit()
  if len(candidates) > 1:
    print "error: it seems " + ep_str + " is not conclusive, found " +\
          "several matching movie files:"
    for filename in candidates:
      print filename
    exit()
  return candidates[0]

if __name__ == '__main__':
  try:
    input_str = sys.argv[1]
  except:
    print "Usage: 'playep.py <episode>' where <episode> has a format similar"
    print "to the following (all these will open episode 5):"
    print "'5', 'S01E05', 'e5', 's1e5'"
    print "Specifying the season is optional, and if omitted is disregarded"
    print "when searching for the right file."
    print "The movie player to use is selected by changing the"
    print "'movie_player_of_choice' variable in playep."
    exit()
  ep_str   = make_sense_of_input(input_str)
  filename = find_that_file(ep_str)
  print "found file '" + filename + "'. opening with '" +\
      movie_player_of_choice + "'..."
  os.execlp(movie_player_of_choice, movie_player_of_choice, filename)
