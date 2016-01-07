## Picture Descriptor

University of Southern California (USC)'s Digital Library has some fantastic photo collections, including the enormous California Historical Society Collection, 1860-1960. Most, if not all, of the photographs in this collection have lengthy and precise descriptions of the scene or object in the photograph. This program generates a random item ID, finds the item on the USC website, then scrapes the description from that item's page. Optionally, the user can choose to view the associated image.

#### Usage:
* Windows: run "picture_descriptor.exe" inside the /dist folder.
* Other: if you have a python interpreter installed, load and run "picture_descriptor.py" manually. On Unix-like systems, you may be able to simply run it like a script.  
NOTE: This program was tested with Python 3.5.0 and may not work with older versions.

#### Inspiration:
Based on an idea from the intfiction.org forums, seen here:  
http://www.intfiction.org/forum/viewtopic.php?f=6&t=18987&start=40

Yes, the name is a misnomer. The program itself isn't describing anything, it's just pulling text from the website.  

This program is intended as a fun inspirational tool for creative writing, or as a visualization exercise. If you are interested in seriously browsing USC's collections, please do so at their website:  
http://digitallibrary.usc.edu/cdm/collections

#### Known Issues:
* The images are pulled using the USC's online image viewer with a hardcoded scaler value. I chose a medium value that seems to work well with most images in my tests, but some images will appear much larger or smaller than others.

* Item IDs are randomly generated from a range based on the lowest and highest item IDs I was able to find. Some IDs within this range do not have a description.
