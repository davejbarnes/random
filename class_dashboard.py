class dashboard:

    def __init__(self, dash_title, cols, width: int = 0):
        self.dash_title = dash_title
        self.cols = cols
        self.width = width
        self.__panes = {}
        self.__panes_order = []
        self.__rendered_panes = []
        self.__max_width = width
        self.__terminal_width = self.__get_terminal_width()


    def __get_max_width(self):
        # return the maximum width of a line in all defined panes
        max_width = 0
        for pane in self.__panes:
            for line in self.__panes[pane]:
                for l in line.split("\n"):
                    l = l.replace("\t", "    ")
                    max_width = len(l) if len(l) > max_width else max_width
        return max_width


    def __get_terminal_width(self):
        # what it says!
        import os
        columns, _ = os.get_terminal_size(0)
        return int(columns)


    def __render_pane(self, title):
        # Render a single pane taking into acount the width available
        pane = []
        len_title = len(title)
        raw_lines = self.__panes[title]
        text_lines = []
        # Deal with new lines and tabs
        for line in raw_lines:
            split_lines = line.split("\n")
            for split_line in split_lines:
                split_line = split_line.replace("\t", "    ")
                text_lines.append(split_line)

        # Work out the width for every pane.  Use max_width if no width
        # was specified for the dashboard.  Minimum width has to be able
        # to draw the longest pane title at least.
        max_width = self.__max_width if self.width == 0 else self.width
        width = max_width if max_width >= len(title) + 5 else len(title) + 5
        # We don't want the terminal to wrap, so limit to auto_width
        auto_width = (self.__terminal_width // self.cols) - self.cols - 2 #+ int((self.__terminal_width % self.cols) / self.cols) - int(self.cols / 2 ) - self.cols - 1
        width = auto_width if width > auto_width else width
        # Ensure dashbord width is up to date so padding of panes
        # works correctly
        self.width = width

        # Work out the maximum width for each text line so we can crop
        # or pad as appropriate, and make sure we take into account the
        # minimum width of the title
        width_text = 0
        for text_line in text_lines:
            l = len(text_line)
            width_text = l if l > width_text else width_text
        if width_text < width or width_text > width:
            width_text = width
        if width_text < len_title:
            width_text = len_title + 8

        # Some variables to use when rendering the lines
        E = "\033[1m"  # Emphasise
        R = "\033[0m"  # Reset
        L = "─" * len_title  # Top line over title
        M = "─" * (width_text - len_title - 5)  # Line after title
        N = " " * (width_text - len_title - 4)  # padding after title bump
        S = " " * (width_text + 2)  # Blank line
        Y = "─" * (width_text + 2)  # Bottom line
        # Render the pane
        # Render the title lines
        pane.append("    ╭─" + L + "─╮" + N)
        pane.append("╭───╯ " + E + title + R + " ╰" + M + "╮")
        pane.append("│" + S + "│")
        for text_line in text_lines:
            # Do we need to crop?
            if len(text_line) > width_text:
                text_line = text_line[0:width_text-2] + ".."
            line_len = len(text_line)
            # Do we need to pad?
            if line_len == width_text:
                pane.append("│ " + text_line + " │")
            else:
                X = " " * (width_text - line_len)
                pane.append("│ " + text_line + X + " │")
        # Add the bottom
        pane.append("│" + S + "│")
        pane.append("╰" + Y + "╯")

        return pane

    
    def __render_panes(self):
        # Iterate through the defined panes and render them using the 
        # list to get the order correct
        self.__rendered_panes = []
        for pane_key in self.__panes_order:
            self.__rendered_panes.append(self.__render_pane(pane_key))


    def display_dashboard(self, fit_width: bool = False):
        # As it says - diaplay the dashboard using defined panes
        # If fit_width is true we'll use all the terminal width
        # and ignore the dashboard's setting
        print("Dashboard - ", self.dash_title, "Fit width is", fit_width)
        self.__terminal_width = self.__get_terminal_width()
        if fit_width:
            self.width = (self.__terminal_width // self.cols) + 2
        self.__max_width = self.__get_max_width()
        self.__render_panes()
        num_panes = len(self.__panes)
        blank = " " * (self.width + 4)
        for first_pane in range(0, num_panes, self.cols):
            # Find the max height of panes in this row so we can add
            # appropriate blanks for panes with different heights
            height = 0
            for r in range(0, self.cols):
                try:
                    h = len(self.__rendered_panes[first_pane + r])
                    height = h if h > height else height
                except:
                    pass
            row = ""
            # Combine each line in the panes on this row, adding
            # blanks to keep the row height consistent
            for h in range(0, height):
                for r in range(0, self.cols):
                    try:
                        _ = self.__rendered_panes[first_pane + r]
                        try:
                            row += self.__rendered_panes[first_pane + r][h]
                        except:
                            row += blank
                    except:
                        pass
                row += "\n"
            print(row)
                

    def create_pane(self, title):
        # Add a new pane if the title doesn't already exist
        # Returns the index of the new pane or -1 if it fails
        if title not in self.__panes_order:
            self.__panes_order.append(title)
            self.__panes[title] = []
            return len(self.__panes_order)
        return -1


    def append_pane_text(self, title, text):
        # Add a line of text to a pane given the pane title
        try:
            self.__panes[title].append(text)
            return True
        except:
            # Pane isn't defined
            return False
