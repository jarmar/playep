## What's this?

A simple script that allows for quick opening of TV series episodes from a 
terminal; by taking a short string, parsing it as an episode number (and 
optionally a season), turning it into the common E00 (or S00E00) format, 
and trying to open a matching movie file in the current directory.

## Install

Place `playep.py` somewhere along your PATH. Optionally change the 
`media_player_of_choice` variable inside `playep.py` to your preferred media 
player. The default is `vlc`.

## Usage

`playep <episode>`, where `<episode>` represents an episode. Here's some 
examples that all open episode five:

    playep 5
    playep E05
    playep e5

You only need to specify the season if it's necessary to distinguish the right 
episode (i.e. with more than one season in the same folder). Then you can write:

    playep s2e4

## Todo

Make the 's' optional when specifying a season (allowing e.g. "2e4") (yes, 
we're being *really* lazy here)
