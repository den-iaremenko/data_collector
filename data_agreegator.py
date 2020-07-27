import requests
import csv

from bs4 import BeautifulSoup
from time import sleep, time
from datetime import datetime
from loguru import logger
from git import Repo


date = datetime.now()
logger.add(f"file_{date.day}_{date.month}_{date.hour}_{date.minute}.log", retention="10 days")


class CsvFiles:

    def __init__(self):
        self.dou = "dou.csv"
        self.nbu = "nbu.csv"
        self.ukrsib = "ukrsib.csv"

    @staticmethod
    def dou_fields():
        return ['t', "h_t", 'java', '.net', 'php', 'c++', 'qa',
                'project manager', 'product manager', 'analyst',
                'за рубежом', 'python', 'ruby', 'ios/macos',
                'android', 'front end', 'дизайн', 'маркетинг',
                'devops', 'начинающим']

    @staticmethod
    def nbu_fields():
        return ["t", "h_t", "e", "d"]

    @staticmethod
    def ukrsib_fields():
        return ["h_t", "t", "e_b", "e_s", "d_b", "d_s", "e_card_b", "e_card_s", "d_card_b", "d_card_s"]


csv_files = CsvFiles()


def run():
    nbu_data = get_nbu_data()
    ukrsib_data = get_ukrsib()
    dou_data = get_data_from_dou()
    if nbu_data:
        write_to_csv(csv_files.nbu, csv_files.nbu_fields(), nbu_data)
    write_to_csv(csv_files.ukrsib, csv_files.ukrsib_fields(), ukrsib_data)
    write_to_csv(csv_files.dou, csv_files.dou_fields(), dou_data)
    git_push()


def create_col_names(file_name, field_names):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        csvfile.close()


def write_to_csv(file_name, field_names, data_to_write):
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writerow(data_to_write)
        csvfile.close()


def git_push():
    PATH_OF_GIT_REPO = r'.git'  # make sure .git folder is properly configured
    COMMIT_MESSAGE = 'new data'
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
        logger.info("All Data is pushed")
    except:
        logger.warning("Some error occured while pushing the code")


def get_data_from_dou():
    dou = {
        "h_t": datetime.now(),
        "t": time(),
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = requests.get("https://jobs.dou.ua/", headers=headers)
    data = BeautifulSoup(data.content, "html.parser")
    main_table = data.find(class_="b-recent-searches")
    all_cats = main_table.find_all(class_="cat")
    for cat in all_cats:
        dou[cat.find(class_="cat-link").text.lower()] = cat.find("em").text
        # print(cat.find("em").text)
        # print(cat.find(class_="cat-link").text)
        # print("\n")
    logger.info(dou)
    return dou


def get_ukrsib():
    def get_values(parent_element):
        buy = parent_element.find(class_="rate__buy").find("p").text.replace("'", "").strip()
        sale = parent_element.find(class_="rate__sale").find("p").text.replace("'", "").strip()
        return [buy, sale]

    ukrsib = {
        "h_t": datetime.now(),
        "t": time(),
        "e_b": 0,
        "e_s": 0,
        "d_b": 0,
        "d_s": 0,
        "e_card_b": 0,
        "e_card_s": 0,
        "d_card_b": 0,
        "d_card_s": 0,
    }
    data = requests.get("https://my.ukrsibbank.com/en/personal/")
    data = BeautifulSoup(data.content, "html.parser")
    usd_nal = data.find(id="NALUSD")
    euro_nal = data.find(id="NALEUR")
    usd_card = data.find(id="BNUAHUSD")
    euro_card = data.find(id="BNUAHEUR")
    ukrsib["d_b"] = float(get_values(usd_nal)[0])
    ukrsib["d_s"] = float(get_values(usd_nal)[1])
    ukrsib["e_b"] = float(get_values(euro_nal)[0])
    ukrsib["e_s"] = float(get_values(euro_nal)[1])
    ukrsib["e_card_b"] = float(get_values(euro_card)[0])
    ukrsib["e_card_s"] = float(get_values(euro_card)[1])
    ukrsib["d_card_b"] = float(get_values(usd_card)[0])
    ukrsib["d_card_s"] = float(get_values(usd_card)[1])
    logger.info(ukrsib)
    return ukrsib


def get_nbu_data():
    nbu = {
        "h_t": datetime.now(),
        "t": time(),
        "e": None,
        "d": None
    }
    retry = 5
    data = None
    while retry:
        try:
            data = requests.get("https://bank.gov.ua")
            if int(data.status_code) == 200:
                retry = 0
        except Exception as e:
            logger.error(f"Error: {e} ")
            retry = retry - 1
    if not data:
        logger.error("Error for NBU")
        return
    data = BeautifulSoup(data.content, "html.parser")
    main_container = data.find(id="container-3")
    all_left_cols = main_container.find_all(class_="col-xs-4")
    current_values = []
    for col_data in all_left_cols:
        if col_data.find(class_="value-full"):
            current_values.append(col_data.find(class_="value-full").find("small").text)
    nbu["e"] = float(current_values[0].replace(",", ".").strip())
    nbu["d"] = float(current_values[1].replace(",", ".").strip())
    logger.info(nbu)
    return nbu


if __name__ == "__main__":
    sec_to_wait = 60
    while True:
        curr_datetime = datetime.now()
        logger.info(f"Current time: {curr_datetime.hour}:{curr_datetime.minute}:{curr_datetime.second}")
        if curr_datetime.hour in [9, 10, 12, 14, 18, 20] and curr_datetime.minute == 00:
            run()
        sleep(sec_to_wait)













    # create_col_names("ukrsib.csv", CsvFiles.ukrsib_fields())
    # with open("nbu.csv") as csvf:
    #     f = csv.DictReader(csvf)
    #     for i in f:
    #         new_i = i.copy()
    #         new_i["h_t"] = datetime.fromtimestamp(int(i["t"]))
    #         new_i["e"] = float(i["e"].replace(",", ".").strip())
    #         new_i["d"] = float(i["d"].replace(",", ".").strip())
    #         print(new_i)
    #         write_to_csv("nbu.csv", CsvFiles.nbu_fields(), new_i)

    # with open("ukrsib.csv") as csvf:
    #     f = csv.DictReader(csvf)
    #     for i in f:
    #         new_i = {}
    #         new_i["t"] = i["t"]
    #         new_i["h_t"] = datetime.fromtimestamp(int(i["t"]))
    #         new_i["e_b"] = float(i["e"].split(",")[0].replace("'", "")[1:])
    #         new_i["e_s"] = float(i["e"].split(",")[1].replace("'", "")[:-1])
    #         new_i["d_b"] = float(i["d"].split(",")[0].replace("'", "")[1:])
    #         new_i["d_s"] = float(i["d"].split(",")[1].replace("'", "")[:-1])
    #         new_i["e_card_b"] = float(i["e_card"].split(",")[0].replace("'", "")[1:])
    #         new_i["e_card_s"] = float(i["e_card"].split(",")[1].replace("'", "")[:-1])
    #         new_i["d_card_b"] = float(i["d_card"].split(",")[0].replace("'", "")[1:])
    #         new_i["d_card_s"] = float(i["d_card"].split(",")[1].replace("'", "")[:-1])
    #         print(new_i)
    #         write_to_csv("ukrsib.csv", CsvFiles.ukrsib_fields(), new_i)