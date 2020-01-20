#!/usr/bin/env python3

def frames2TC (frames, fps, offset=0):
    h = str(int((frames + offset) / (fps*3600)))
    m = str(int(frames / (fps*60)) % 60)
    s = str(int((frames % (fps*60))/fps))
    f = str(int(frames % (fps*60) % fps))
    return f'{h.zfill(2)}-{m.zfill(2)}-{s.zfill(2)}-{f.zfill(2)}'

if __name__ == '__main__':
    main()
