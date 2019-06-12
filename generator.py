import argparse
import shutil

from scripts.gSheetDownloader import ExcelGenerator
from scripts.json_generator import JsonGenerator

DEFAULT_EXCEL_PATH = "excels"
DEFAULT_JSON_PATH = "jsons"

parser = argparse.ArgumentParser("Generate json from google sheet or excels")

parser.add_argument("--local", "-l", dest="local", help="Indicate if local files will be used")
parser.add_argument("--output", "-o", dest="output", help="The output folder for json", default=DEFAULT_JSON_PATH)
parser.add_argument("--online", dest="online", default="1xBtO-_FBtojVlSMJZhgH0XmCGMLD2sIt",
                    help="The folder id of the Google Drive scenarios root folder")
parser.add_argument("--save-online", "-s", dest="store", action="store_true", help="Save excel files on disk")

if __name__ == '__main__':
    args = parser.parse_args()

    if args.local:
        JsonGenerator(args.local, args.output)
    else:
        ExcelGenerator(root_folder_id=args.online, excel_path=DEFAULT_EXCEL_PATH)
        JsonGenerator(DEFAULT_EXCEL_PATH, args.output)
        if not args.store:
            print ("Deleting temporary excel files")
            shutil.rmtree(DEFAULT_EXCEL_PATH)



    print("Generation complete, see the folder", args.output)