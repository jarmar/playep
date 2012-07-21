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

`playep.py [term1 term2 ..]episode`, where `episode` represents an episode.
Here's some examples that all open episode five:

    playep.py 5
    playep.py E05
    playep.py e5

You only need to specify the season if it's necessary to distinguish the right 
episode (i.e. with more than one season in the same folder). Then you can write:

    playep.py s2e4

You can also supply additional search terms that will all be required to be
present in the filename. Examples:

    playep.py br ba s2e1
    playep.py suits 5

playep will first search the current directory, and if no matches are found,
walk through all subdirectories if the user so wants.

## Todo

The recursive search walks all subdirectories to the bottom. It would be better
to recurse in a more restrictive manner. The easiest way to do this would be
to stop at the first file that matches the arguments, but this would lead to
ambiguous arguments executing the first matching file, rather than the unique
matching file.

Make the 's' optional when specifying a season (allowing e.g. "2e4") (yes, 
we're being *really* lazy here)
