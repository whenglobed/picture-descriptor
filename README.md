## Picture Descriptor

University of Southern California (USC)'s Digital Library has some fantastic photo collections, including the enormous California Historical Society Collection, 1860-1960. Most, if not all, of the photographs in this collection have lengthy and precise descriptions of the scene or object in the photograph. This program generates a random item ID, finds the item on the USC website, then scrapes the description from that item's page. Optionally, the user can choose to view the associated image.

#### Usage
Windows users can simply run "picture\_descriptor\_win32.exe", found in the Releases section.  

For other operating systems, you have to download and run "picture\_descriptor.py" with a Python interpreter on your machine (Unix-like machines should be able to run it like a script, assuming Python is installed). This program has only been tested with Python 3.5.0, and the following Python modules are also required:

* Beautiful Soup 4
* Pillow
* Tkinter, if your Python installation doesn't have it by default  

#### Screenshots:
![control panel](screenshots/picture_descriptor_screenshot1.png&raw=true)
![image viewer](screenshots/picture_descriptor_screenshot2.jpg&raw=true)

#### Inspiration:
Picture Descriptor is based on an idea from the intfiction.org forums, seen here:  
http://www.intfiction.org/forum/viewtopic.php?f=6&t=18987&start=40

Yes, the name is a misnomer. The program itself isn't describing anything, it's just pulling text from the website.  

This program is intended as a fun inspirational tool for creative writing, or as a visualization exercise. If you are interested in seriously browsing USC's collections, please do so at their website:  
http://digitallibrary.usc.edu/cdm/collections

#### Known Issues:
* The images are pulled using the USC's online image viewer with a hardcoded scaler value. I chose a medium value that seems to work well with most images in my tests, but some images will appear much larger or smaller than others.

* Item IDs are randomly generated from a range based on the lowest and highest item IDs I was able to find. Some IDs within this range do not have a description.

* Currently, the program stores a copy of the most recent image in whatever folder the program is run from. This is messy and should be cleaned up in the future.
