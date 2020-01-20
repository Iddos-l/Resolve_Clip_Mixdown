#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script export the current clip in timeline using an output
# preset named: 'MIXDOWN' and import the new file to bin.
#
# Iddos, Bootqe color studio, iddolahman@gmail.com

import os, sys, time, ntpath
from pathlib import Path
from timecode_utils import frames2TC
from python_get_resolve import GetResolve

# Getting resolve data
resolve = GetResolve()
if resolve == None:
    sys.exit(-1)

FPS = int(float(resolve.GetProjectManager().GetCurrentProject().GetSetting('timelineFrameRate')))
mediaStorage = resolve.GetMediaStorage()
proj = resolve.GetProjectManager().GetCurrentProject()
clip = proj.GetCurrentTimeline().GetCurrentVideoItem()

# Getting the clip source path and creating 'Mixdown' folder if not exists
base, ext = os.path.splitext(clip.GetName())
mixdownName = base + '_Mixdown_' + frames2TC(clip.GetStart(), FPS)
parrentFolder = Path(os.path.dirname(clip.GetMediaPoolItem().GetClipProperty()['File Path']))
destFolder = Path(str(parrentFolder) + '/Mixdown')
Path(destFolder).mkdir(parents=True, exist_ok=True)

# Loading output preset and setting up parameters
proj.LoadRenderPreset('MIXDOWN')
proj.SetRenderSettings({
    "MarkIn":clip.GetStart(),
    "MarkOut": clip.GetEnd()-1,
    "CustomName": mixdownName,
    "TargetDir": str(destFolder)})

# Render
proj.AddRenderJob()
proj.StartRendering(len(proj.GetRenderJobs()))

while proj.IsRenderingInProgress():
    time.sleep(1)

# Import the new render output to bin
os.chdir(destFolder)
dest = os.getcwd()
files = mediaStorage.GetFiles(dest)

for f in files.values():
    base = ntpath.basename(f)
    name, ex = os.path.splitext(base)
    if name == mixdownName:
        mediaStorage.AddItemsToMediaPool(f)
        break

# Go to Edit
resolve.OpenPage('edit')
