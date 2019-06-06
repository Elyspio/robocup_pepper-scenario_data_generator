import json
import os
import sys
import xlrd

scenarios_excels_directory = './scenarios'
jsons_path = './dist'
global_excels_path = './global.xlsx'


old_cell_value = xlrd.sheet.Sheet.cell_value


def strip_entry_python2(self, row, col):

    raw_value = old_cell_value(self, row, col)
    if type(raw_value) == unicode:
        raw_value = raw_value.strip()
    return raw_value

def strip_entry_python3(self, row, col):

    raw_value = old_cell_value(self, row, col)
    if type(raw_value) == str:
        raw_value = raw_value.strip()
    return raw_value

if sys.version_info[0] == 3:
    xlrd.sheet.Sheet.cell_value = strip_entry_python3
elif sys.version_info[0] == 2:  
    xlrd.sheet.Sheet.cell_value = strip_entry_python2


def add_arguments(sheet, arguments, row, index):
    """
    :param row: the actual row in sheet
    :type row int

    :param sheet: the scenario sheet
    :type sheet xlrd.sheet.Sheet

    :param arguments: the array that will contain arguments
    :type arguments dict

    :param index: the index of the current argument
    :type index int

    :rtype dict
    """

    if sheet.ncols > index + 1:
        key = sheet.cell_value(row, index)
        value = sheet.cell_value(row, index + 1)
        if key != "" and value != "":
            arguments[key] = value
            return add_arguments(sheet, arguments, row, index + 2)
    return arguments


def get_nb_useful_cols(sheet, row=0, col=0):
    if sheet.cell_value(row, col) == "":
        return 0
    return 1 + get_nb_useful_cols(sheet, row, col + 1)


def create_global():
    global_book = xlrd.open_workbook(global_excels_path)
    print ("--- Global ---")

    def use_sheet(book, sheet_name, json_path):
        """
        :param book: the book of global.xlsx
        :type book xlrd.book.Book

        :param sheet_name: the name of sheet
        :type sheet_name str

        :param json_path: the name of the json that will be created in folder json
        :type json_path str
        """
        sheet = book.sheet_by_name(sheet_name)
        data = []
        cols = []

        nb_cols = get_nb_useful_cols(sheet, 0,  0)

        for col in range(0, nb_cols):
            cols.append(sheet.cell_value(1, col))

        for row in range(2, sheet.nrows):
            obj = {}
            for index, col in enumerate(cols):

                raw_value = sheet.cell_value(row, index)
                if(type(raw_value) == str):
                    raw_value = raw_value

                obj[col] = sheet.cell_value(row, index)
            data.append(obj)

        with open(os.path.join(jsons_path, json_path), 'w') as data_file:
            data_file.write(json.dumps(data))
            # print( "File " + json_path + ": \033[0;32mOK\033[0;0m")
            print("{0:10} {1:50} \033[0;32m{2}\033[0;0m".format(
                "File", json_path, "OK"))

    use_sheet(global_book, "Drinks", "drinks.json")
    use_sheet(global_book, "Locations", "locations.json")
    use_sheet(global_book, "People", "people.json")
    print ("")
# noinspection PyShadowingNames


def create_scenario(file_xlsx):
    workbook = xlrd.open_workbook(file_xlsx)

    # region sheet Meta
    sheet_meta = workbook.sheet_by_name('Meta')
    scenario_name = sheet_meta.cell_value(1, 0)
    json_key = sheet_meta.cell_value(1, 1)
    scenario_duration = sheet_meta.cell_value(1, 2)
    # endregion

    # region scenario.json

    steps_sheet = workbook.sheet_by_name('Steps')
    steps = []
    # start at 1 to ignore title line
    for i in range(1, steps_sheet.nrows):


        if steps_sheet.cell_value(i, 3) != "":
            arguments = add_arguments(steps_sheet, {}, i, 7)

            steps.append({
                'name': steps_sheet.cell_value(i, 3),
                'id': steps_sheet.cell_value(i, 4),
                'eta': steps_sheet.cell_value(i, 5),
                'action': steps_sheet.cell_value(i, 6),
                'arguments': arguments
            })

    # Create scenario folder

    if not os.path.exists((os.path.join(jsons_path, json_key))):
        os.mkdir((os.path.join(jsons_path, json_key)))

    with open(os.path.join(jsons_path, json_key, "scenario.json"), 'w') as scenario_file:

        scenario_file.write(json.dumps({
            'steps': steps,
            'duration': scenario_duration,
            'name': scenario_name
        }))
        print("{0:10} {1:50} \033[0;32m{2}\033[0;0m".format(
            "File", scenario_name + "/scenario.json", "OK"))

    # endregion

    # region speech.json
    speech_sheet = workbook.sheet_by_name('Speech')
    speech = []

    for i in range(1, steps_sheet.nrows):
        speech.append({
            "step": speech_sheet.cell_value(i, 0),
            "toSay": speech_sheet.cell_value(i, 1)
        })

    with open(os.path.join(jsons_path, json_key, 'speech.json'), 'w') as speech_file:
        speech_file.write(json.dumps(speech))
        print("{0:10} {1:50} \033[0;32m{2}\033[0;0m".format(
            "File", scenario_name + "/speech.json", "OK"))

    # endregion

    # region variables.json
    var_sheet = workbook.sheet_by_name('Variables')
    variables = []
    nb_rows = var_sheet.nrows

    for row in range(1, nb_rows):
        nb_useful_cols = get_nb_useful_cols(var_sheet, row, 2)
        obj = {}
        for col in range(0, nb_useful_cols):
            obj[str(var_sheet.cell_value(row, col))
                ] = var_sheet.cell_value(row, col+1)
        variables.append(obj)

    with open(os.path.join(jsons_path, json_key, 'variables.json'), 'w') as var_file:
        var_file.write(json.dumps(variables))
        print("{0:10} {1:50} \033[0;32m{2}\033[0;0m".format(
            "File", scenario_name + "/variables.json", "OK"))

    # endregion

    print("{0:10} {1:50} \033[0;32m{2}\033[0;0m".format(
        "Scenario", scenario_name, "OK"))


if __name__ == '__main__':

    if not os.path.exists(jsons_path):
        os.mkdir(jsons_path)

    create_global()
    print ("--- Scenarios --- ")
    for scenario_file in [f for f in os.listdir(scenarios_excels_directory) if
                          f.endswith('.xlsx') and not f.startswith("~")]:
        create_scenario(os.path.join(
            scenarios_excels_directory, scenario_file))
    print("")
    print("--- Generation completed ---")
    print("see dist/")
