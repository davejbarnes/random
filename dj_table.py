# definitions of character sets for drawing tables 
import sys

#  Dictionary of strings of characters, indexed as such:

#   012 3
#   ├─┼─┤
#
#   4 5 6
#   │ │ │       this is an example of a 
#               'light subheader'
#   789 10
#   ├─┼─┤


#   0 1 2
#   ┃ ╋ ┃       this is a 'bold crossed' row


#Headers:
table_header = {"boldbold": "┏━┳┓┃┃┃┣━╋┫",
                "boldlight": "┏━┳┓┃┃┃┡━╇┩",
                "lightlight": "┌─┬┐│││├─┼┤",
                "doublelight": "╒═╤╕│││╞═╪╡",
                "roundlight": "╭─┬╮│││├─┼┤"
               }

#Subheaders:
table_subheader = {"boldbold": "┣━╋┫┃┃┃┣━╋┫",
                   "boldlight": "┢━╈┪┃┃┃┡━╇┩",
                   "lightlight": "├─┼┤│││├─┼┤",
                   "doublelight": "╞═╪╡│││╞═╪╡"
                  }

#Footers:
table_footer = {"boldbold": "┣━╋┫┃┃┃┗━┻┛",
                "boldlight": "┢━╈┪┃┃┃┗━┻┛",
                "lightlight": "├─┼┤│││└─┴┘",
                "doublelight": "╞═╪╡│││╘═╧╛",
                "roundlight": "├─┼┤│││╰─┴╯"
               }

#Tops
table_top = {"boldbold": "┏━┳┓",
             "boldlight": "┍━┯┑",
             "lightlight": "┌─┬┐",
             "doublelight": "╒═╤╕",
             "roundlight": "╭─┬╮"
            }

#Rows:
table_row = {"bold": "┃┃┃",
             "light": "│││",
             "boldcross": "┃╋┃",
             "lightcross": "├┼┤"
            }

#Deviders:
table_devider = {"bold": "┣━╋┫",
                 "light": "├─┼┤│││└─┴┘"
                }

#Ends
table_end = {"boldbold": "┗━┻┛",
             "boldlight": "┕━┷┙",
             "lightlight": "└─┴┘",
             "doublelight": "╘═╧╛",
             "roundlight": "╰─┴╯"
            }


def draw_part(chars: str, values: list, widths: list):
    cols = len(widths)
    # draw the top line
    out_line = (chars[0])
    for col in range(cols):

        for i in range(0,widths[col]):
            out_line += chars[1]
        if col < cols -1 :
            out_line += chars[2]
    out_line += chars[3]
    print(out_line)

    # draw the line with values
    out_line = chars[4]
    for id, value in enumerate(values):
        out_line += value
        padding = " " * (widths[id] - len(value))
        out_line += padding
        out_line += chars[5]
    print(out_line)

    # draw the bottom line
    out_line = (chars[7])
    for col in range(0, cols):
        for i in range(0,widths[col]):
            out_line += chars[8]
        if col < cols -1 :
            out_line += chars[9]
    out_line += chars[10]
    print(out_line)

def draw_data_row(chars: str, values: list, widths: list, id: int) -> str:
    cols = len(widths)
    err_line = ""
    if cols != len(values):
        err_line = "Wrong number of columns for line " + str(id) + ": got " + str(len(values)) + ", expected " + str(cols) + ": Values " + str(values)
    else:
        out_line = chars[0]
        for col in range(cols):
            out_line += values[col]
            padding = " " * (widths[col] - len(values[col]))
            out_line += padding
            if col < cols -1 :
                out_line += chars[1]
        out_line += chars[2]
        print(out_line)
    return err_line


def draw_row(chars: str, widths: list):
    cols = len(widths)
    out_line = (chars[0])
    for col in range(0, cols):
        for i in range(0,widths[col]):
            out_line += chars[1]
        if col < cols -1 :
            out_line += chars[2]
    out_line += chars[3]
    print(out_line)


def draw_table(data: str, header_style: str = "boldlight", row_style: str = 'light',
    footer_style: str = 'none', end_style: str = "roundlight", delimiter: str = ";",
    devider: bool = False):

    table_data = data.splitlines()
    cols = len(table_data[1].split(delimiter))
    field_widths = [1] * cols
    num_lines = 0
    errors = []

    for line in table_data:
        cells = line.split(delimiter)
        num_lines += 1
        if len(cells) > cols:
            print("Fuck")
            continue
        for id, cell in enumerate(cells):
            if len(cell) >= field_widths[id]:
                field_widths[id] = len(cell) + 1

    for id, line in enumerate(table_data):
        anyerr = ""
        if id == 0 and header_style != "none":
            fields = line.split(delimiter)
            draw_part(table_header[header_style], fields, field_widths)
        elif id == 0 and header_style == "none":
            fields = line.split(delimiter)
            draw_row(table_top[row_style + row_style], field_widths)
            anyerr = draw_data_row(table_row[row_style], fields, field_widths, id)
        elif id == num_lines -1 and footer_style != 'none':
            fields = line.split(delimiter)
            draw_part(table_footer[footer_style], fields, field_widths)
        else:
            fields = line.split(delimiter)
            anyerr = draw_data_row(table_row[row_style], fields, field_widths, id)
            if id != num_lines -1 and devider and footer_style == 'none':
                draw_row(table_devider[row_style], field_widths)
            if id != num_lines -2 and devider and footer_style != 'none':
                draw_row(table_devider[row_style], field_widths)
        if anyerr != "":
            errors.append(anyerr)
    if footer_style == 'none':
        draw_row(table_end[end_style], field_widths)
    if len(errors) > 0:
        for error in errors:
            print(error)


# fake = "id;state;host_name;service_description;service_alert\n"
# fake += "143;2;dc01-web01;uptime_status;CRIT: Host uptime is 0:30\n"
# fake += "146;2;dc03-web01;uptime_status;CRIT: Host uptime is 0:25\n"

def parse_args() -> list:
    arguments = sys.argv
    num_args = len(arguments)
    valid_parameters = True
    error_list = []

    header = False
    footer = False
    devider = False
    header_style = "none"
    row_style = "light"
    footer_style = "none"
    end_style = "none"
    delimiter = ";"     # default for LiveStatus output ;)
    devider = False

    for index, arg in enumerate(arguments):
        if index == 0:
            continue
        if arg in ["h=bold", "h=light", "h=double", "h=round", "-h=bold", "-h=light", "-h=double", "-h=round"]:
            header = True
            header_style = arg.split("=")[1]
            continue
        if arg in ["t=bold", "t=light", "-t=bold", "-t=light"]:
            row_style = arg.split("=")[1]
            continue
        if arg == '-D=1' or arg == 'D=1':
            devider = True
            continue
        if arg in ["f=bold", "f=light", "f=double", "f=round", "-f=bold", "-f=light", "-f=double", "-f=round"]:
            footer = True
            footer_style = arg.split("=")[1]
            continue
        if arg in ["e=bold", "e=light", "e=double", "e=round", "-e=bold", "-e=light", "-e=double", "-e=round"]:
            end_style = arg.split("=")[1]
            continue

        if arg[0:2] == "d=":
            delimiter = arg[2]
            #print("Delimiter is", delimiter)
            continue
        if arg[0:3] == "-d=":
            delimiter = arg[3]
            #print("Delimiter is", delimiter)
            continue

        valid_parameters = False
        error_list.append(arg + " is not a valid argument")
    if header_style != 'none':
        header_style += row_style

    if end_style != 'none':
        end_style += row_style

    if footer_style != 'none':
        footer_style += row_style

    return [header, header_style, row_style, footer, footer_style, end_style, devider, delimiter, devider, error_list]

options = parse_args()

opt_header = options[0]
opt_header_style = options[1]
opt_row_style = options[2]
opt_footer = options[3]
opt_footer_style = options[4]
opt_end_style = options[5]
opt_devider = options[6]
opt_delimiter = options[7]
opt_devider = options[8]
error_list = options[9]

if opt_end_style == 'none':
    if opt_header_style == 'none':
        opt_end_style = opt_row_style + opt_row_style
    else:
        opt_end_style = opt_header_style

if len(error_list) > 0:
    for error in error_list:
        print(error)
    exit(1)


rawdata = ""
for line in sys.stdin:
    rawdata += line

draw_table(data = rawdata, header_style=opt_header_style, row_style=opt_row_style,
            footer_style=opt_footer_style, end_style=opt_end_style, delimiter=opt_delimiter,
            devider=opt_devider)

