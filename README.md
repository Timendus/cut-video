# Video cutting script

Do you need to cuts parts from a video on a regular basis? For example so you
can upload individual presentations from a longer live-streamed meeting? Just
tell this script what to cut out and set it loose.

## Dependencies

Here's the brew summary, adapt to your own package manager:

```bash
brew install python3 ffmpeg
```

## Installation

```bash
pip install git+https://github.com/timendus/cut-video
```

Or if you prefer pipx:

```bash
pipx install git+https://github.com/timendus/cut-video
```

## Uninstalling

```bash
pip uninstall cut-video
```

Or:

```bash
pipx uninstall cut-video
```

## Usage

Create a text file defining the cuts you want to make. The file should contain
two columns, one with start and optional end times and one with descriptions of
the parts. The columns are separated by whitespace:

```
# TIME(S)         DESCRIPTION
# -------         -----------
00:00             Welcome
01:48-08:55       New colleagues
08:51-10:52       Agenda
```

Empty lines and lines starting with a `#` will be ignored. If only a starting
time is given, the end time will default to the start time of the next part (or
the end of the video). Start time and end time should be noted in `hh:mm:ss` or
`mm:ss` or `ss`. Parts may overlap.

Then run `cut-video`, passing in the source video and the text file you just
created:

```bash
cut-video ~/Videos/my-video.mp4 ~/Videos/my-video.cuts
```

This will create a directory `~/Videos/my-video/`, based on the file name of the
source video, and put all the parts you specified in there. In this example:

```
~/Videos/my-video/01 Welcome.mp4
~/Videos/my-video/02 New colleagues.mp4
~/Videos/my-video/03 Agenda.mp3
```

If you run the command again, ffmpeg will ask for each file if you wish to
overwrite it or skip it. If you want to overwrite all files, you can pass
`--overwrite` as the third argument to `cut-video`:

```bash
cut-video ~/Videos/my-video.mp4 ~/Videos/my-video.cuts --overwrite
```
