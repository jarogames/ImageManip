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




Comments
===========



22.4.2018 i switched off the heatpump

  - next time we could 1/ do a homomorph transform of the image and 2/ ocr 
  after which would be cleaner than to have all in this commandline
  
  - i did tests with feature recognition to make the homomorph trans. 
  automaticaly (based on a pretransformed picture). But the pictures
  were sometimes too dark without any features other than SS numbers
  
  
