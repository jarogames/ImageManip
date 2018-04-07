ssocr
==========
OCR for 7-segmented LED displays


verbose and debug image; `-d -1` means decide on number of digits by itself
FIRST ROTATE AND SHEAR then `crop x y dx dy`  y is from top

```
./ssocr-2.16.3/ssocr -v -D -d -1  rotate 1 shear 47 crop 350 390 170 120  2016-03-02-105013.jpg
```


Threshold implies the line thickness,  mono, invert, erosion;

```
./ssocr-2.16.3/ssocr -v -D -d -1  rotate 1 shear 47 crop 390 390 140 110  -t 95  make_mono invert erosion  2016-03-02-105013.jpg
```
