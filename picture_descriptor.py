#!/usr/bin/env python3

"""Picture Descriptor. This program scrapes a random picture description from
the University of Southern California's Digital Library (the California
Historical Society Collection, 1860-1960). Optionally, the user can view the
associated image.

Version 1.1, June 21, 2016
Tested with Python 3.5.0

TODO: Anticipate and handle exceptions, especially in get_random_desc and
get_image.
"""

import tkinter as tk
import random
from urllib import request
from PIL import Image, ImageTk

from bs4 import BeautifulSoup
from bs4 import SoupStrainer


### Constants

ID_RANGE = (0, 26223)
ITEM_URL_BASE = "http://digitallibrary.usc.edu/" \
                "cdm/singleitem/collection/p15799coll65/id/"

# Options for the USC online image viewer.
PHOTO_URL_BASE = "http://digitallibrary.usc.edu/utils/ajaxhelper/" \
                 "?CISOROOT=p15799coll65&CISOPTR="
PHOTO_URL_END = "&action=2&DMSCALE=10&DMWIDTH=800&DMHEIGHT=800"


def get_random_id():
    """Return a random integer within ID_RANGE."""
    random.seed()
    return random.randint(ID_RANGE[0], ID_RANGE[1])


class PictureDescriptor(tk.Frame):
    """Base class for the GUI.

    Defines the components and behavior of the application's main window.
    Technically, since PictureDescription is a Frame, its root is the true
    'main window' of the application, but the root is automatically
    instantiated when PictureDescriptor is.
    """

    def __init__(self, master=None):
        super().__init__(master)
        self._root().title("Picture Descriptor")
        self.config(padx=0, pady=5)
        self.grid()
        self.id = None
        self.last_image_id = None
        self.target_url = ""
        self.photo_url = ""
        self.setup_widgets()

    def setup_widgets(self):
        """Initialize and arrange components within the frame."""

        # TODO: Make the URL field a clickable link.
        # TODO: return a tuple to __init__, to keep the components 'inside' init?
        self.get_button = tk.Button(self,
                                    text="Get a Random Description",
                                    command=self.get_random_desc)
        self.get_button.grid(columnspan=2, row=0)

        self.id_text_label = tk.Label(self, text="Item ID: ")
        self.id_text_label.grid(row=1, column=0, sticky=tk.W)
        self.id_num_label = tk.Label(self, text="")
        self.id_num_label.grid(row=1, column=1, sticky=tk.W)

        self.url_text_label = tk.Label(self, text="Item URL: ")
        self.url_text_label.grid(row=2, column=0, sticky=tk.W)

        # Control variable for the text in the URL field.
        self.current_url = tk.StringVar()

        self.url_field = tk.Entry(self,
                                  width=70,
                                  textvariable=self.current_url,
                                  state="readonly")
        self.url_field.grid(row=2, column=1, sticky=tk.W)

        self.desc_frame = tk.LabelFrame(self,
                                        padx=5, pady=5,
                                        text="Description:")
        self.desc_frame.grid(columnspan=2)
        self.desc_text = tk.Text(self.desc_frame,
                                 width=60,
                                 height=15,
                                 wrap=tk.WORD)
        self.desc_text.grid()

        self.image_button = tk.Button(self,
                                      text="Show Image",
                                      command=self.show_image)
        self.image_button.grid(columnspan=2)

        # The image window is created here but hidden immediately so we can
        # show/hide the window to view an image instead of creating a new
        # window every time. Also, the window close operation is overridden
        # to hide the window instead of deleting it.
        self.image_window = tk.Toplevel()
        self.image_window.withdraw()
        self.image_window.title("")
        self.image_window.resizable(width=False, height=False)
        self.image_window.protocol("WM_DELETE_WINDOW",
                                   self.hide_image_window)

        self.canvas = tk.Canvas(self.image_window)

    def hide_image_window(self):
        """Hide the image window."""
        self.image_window.withdraw()

    def get_random_desc(self):
        """Scrape a picture description from the USC website.

        Generate a URL for the USC website using a random item ID,
        open the page, and look for the 'id="metadata_descra"' tag
        in the page's HTML. The text inside that tag should be the
        long image description, which can be extracted and passed
        to other GUI components.
        """

        self.id = get_random_id()
        # self.id = 1139 # TEST -- causes known problem with image viewer

        # Build the URLs used to scrape the description and access the image
        # viewer.
        self.target_url = ITEM_URL_BASE + str(self.id)
        self.photo_url = PHOTO_URL_BASE + str(self.id) + PHOTO_URL_END

        self.id_num_label["text"] = str(self.id)
        self.current_url.set(self.target_url)

        req = request.urlopen(self.target_url)
        html = req.read()

        soup = BeautifulSoup(html, "html.parser",
                             parse_only=SoupStrainer(id="metadata_descra"))

        long_desc = ""
        description_block = soup.find(id="metadata_descra")
        if description_block is None:
            long_desc = "No description for this item ID."
        else:
            long_desc = description_block.get_text().strip()

        # Disable text after printing the description so it can't be edited.
        self.desc_text.config(state=tk.NORMAL)
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", long_desc, None)
        self.desc_text.config(state=tk.DISABLED)

    def get_image(self):
        """Retrieve and open an image from the USC website.

        This operation relies on a URL with hardcoded options for the USC
        image viewer. The image is retrieved and then converted to a format
        usable by tkinter.
        """

        if (self.photo_url == ""):
            return None
        filename, headers = request.urlretrieve(self.photo_url,
                                                filename="digitallibrary.usc.edu.jpg")
        try:
            # Attempt to convert the downloaded image to a PhotoImage, a
            # Tkinter-usable object type.
            image = ImageTk.PhotoImage(Image.open(filename))
        except OSError as err:
            image = None
        return image

    def show_image(self):
        """Show the image for the current item ID in a new window.

        Only retrieves and updates the image if the ID has changed
        since the last time the image was shown.
        """

        if (self.id != self.last_image_id):
            self.last_image_id = self.id
            self.canvas.photoimage = self.get_image()

            self.image_window.title("Item ID: " + str(self.id))
            self.canvas.delete(tk.ALL)

            if (self.canvas.photoimage is not None):
                self.canvas.config(width=self.canvas.photoimage.width(),
                                   height=self.canvas.photoimage.height())
                self.canvas.create_image(0, 0,
                                         anchor=tk.NW,
                                         image=self.canvas.photoimage)
            else:
                self.canvas.create_text(2, 0,
                                        anchor=tk.NW,
                                        text="Error: could not load ID " +
                                        str(self.id) + " in the USC image viewer.")
            self.canvas.grid()

        # Show the window.
        self.image_window.deiconify()


if __name__ == "__main__":
    PictureDescriptor().mainloop()
