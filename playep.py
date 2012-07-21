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

def normalize_episode(input_str):
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

def episode_matches(ep_str, directory, recursive=False):
  if not recursive:
    filenames = os.listdir(directory)
  else:
    filenames = []
    for root, dirs, files in os.walk(directory):
      for filename in files:
        filenames.append('%s/%s' % (root, filename))
  candidates = filter(is_this_a_movie_file,
                      filter(lambda n: n.upper().find(ep_str) != -1, filenames))
  return candidates

def find_by_episode(ep_str):
  search_subs = False
  cwd = os.getcwd()
  candidates = episode_matches(ep_str, cwd)
  if not candidates:
    print "can't find episode " + ep_str + " in this folder."
    search_subs = confirm("search subdirectories?", True)
  if search_subs:
    candidates = episode_matches(ep_str, cwd, recursive=True)
  return candidates

def find_by_both(search_strs, ep_str):
  search_subs = False
  cwd = os.getcwd()
  episode_candidates = episode_matches(ep_str, cwd)
  candidates = filter(lambda c: all([c.lower().find(term) != -1 for term in search_strs]), episode_candidates)
  if not candidates:
    print "can't find %s %s in this folder." % (' '.join(search_strs), ep_str)
    search_subs = confirm("search subdirectories?", True)
  if search_subs:
    episode_candidates = episode_matches(ep_str, cwd, recursive=True)
    candidates = filter(lambda c: all([c.lower().find(term) != -1 for term in search_strs]), episode_candidates)
  return candidates

def confirm(prompt, resp=False):
  if resp:
    prompt = '%s %s/%s: ' % (prompt, 'Y', 'n')
  else:
    prompt = '%s %s/%s: ' % (prompt, 'y', 'N')
  while True:
    ans = raw_input(prompt)
    if not ans:
      return resp
    if ans.upper() == 'Y':
      return True
    if ans.upper() == 'N':
      return False

def main(args):
  if len(args) == 2:
    episode_input = args[1]
    episode_str = normalize_episode(episode_input)
    movie_files = find_by_episode(episode_str)
    if not movie_files:
      print "unable to find episode %s!" % episode_str
      exit()
    if len(movie_files) > 1:
      print "found several matching movie files:"
      for filename in movie_files:
        print filename
      print "maybe supply a series name or a season?"
      exit()
  else:
    search_terms = args[1:-1]
    episode_input = args[-1]
    search_strs = [term.lower() for term in search_terms]
    episode_str = normalize_episode(episode_input)
    movie_files = find_by_both(search_strs, episode_str)
    if not movie_files:
      print "unable to find %s %s!" % (' '.join(search_strs), episode_str)
      exit()
    if len(movie_files) > 1:
      print "found several matching movie files:"
      for filename in movie_files:
        print filename
      print "try to narrow down your arguments."
      exit()

  movie_file = movie_files[0]
  print "found file %s. opening with %s..." % (movie_file, movie_player_of_choice)
  os.execlp(movie_player_of_choice, movie_player_of_choice, movie_file)

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print """Usage: 'playep.py [term1 term2 ..] episode' where episode has a"
format similar to the following (all these will open episode 5):
  '5', 'S01E05', 'e5', 's1e5'
Specifying the season is optional, and if omitted is disregarded
when searching for the right file.
Optionally, additional search terms can be added to distinguish
the sought file (typically, the name of the series).
All search terms must be present in the file name.
Example:
  'playep.py br ba s2e1', 'playep.py suits 5'

The script initially searches the current directory, and if no
match is found, asks if the user wants to search all subdirectories as well.
The movie player to use is selected by changing the
'movie_player_of_choice' variable in playep."""
  else:
    main(sys.argv)
