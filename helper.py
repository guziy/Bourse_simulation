__author__ = 'san'

data_path_format = "data/Titre%d.csv"
index_path = "data/Index.csv"
out_data_filename_format = "Titre%d.csv"


def change_line(line, new_day_index):
    fields = line.split(",")
    fields[0] = "Today-%d" % new_day_index
    return ",".join(fields)

def create_input_file_for_the_day(simulation_day = 0, nItems = 10, nRecordsPerFile = 260):
    """
    creates the input timeseries for the day_of_year containing the data for the
    current day and for the 259 preceding ones for each item
    """
    for i in xrange(nItems):
        f = open(data_path_format % i)
        lines = f.readlines()
        f.close()
        the_title = lines.pop(0)

        new_lines = lines[-nRecordsPerFile - simulation_day: len(lines) - simulation_day]

        new_lines = map(lambda x: change_line(x[1],  x[0]), enumerate(new_lines) )
        new_lines.insert(0, the_title)

        f = open(out_data_filename_format % i, mode = "w")
        f.writelines(new_lines)
        f.close()




    pass


if __name__ == "__main__":
    create_input_file_for_the_day()