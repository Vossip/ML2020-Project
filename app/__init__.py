# coding=utf-8
import requests
import json
import os
import time
import logging
import csv
from bs4 import BeautifulSoup
from langdetect import detect
from .Document import Document
from flask import Flask
import sys
from . import config

app = Flask(__name__)
URL = "https://services-api.lexisnexis.com/v1/News?"
expand = "&$expand=Document"
top = "&$top=50"
filter = "&$filter=SearchType eq LexisNexis.ServicesApi.SearchType'Boolean' and GroupDuplicates eq LexisNexis.ServicesApi.GroupDuplicates'HighSimilarity'"
accessToken = 'Bearer xxxxxxxxx'
search = "$search="

term_1 = " W/25 ((conflicts of interest) OR (conjur!) OR (conniv!) OR (conspir!) OR (contraband) OR (contraven!) OR (convict!) OR (copycat) OR (correctional) OR (correctiv!) OR (corrupt!) OR (counterfei!) OR (court case) OR (cover up) OR (cozen!) OR (crime!) OR (crimin!) OR (cronism) OR (crony!) OR (crook) OR (crooke!) OR (culpab!) OR (culprit) OR (custody) OR (cyber terror!) OR (cybercrim!) OR (cyberfraud!) OR (cybergang) OR (cyberheist) OR (cyberpira!) OR (cybersabot!) OR (cyberscam) OR (cyberspy!) OR (cyberterror!) OR (cyberthreat) OR (dacoit!) OR (damag!) OR (dangerous!) OR (debar!) OR (deceit!) OR (deceiv!) OR (decept!) OR (defendant!) OR (defraud!) OR (denounc!) OR (denunciat!) OR (detain!) OR (detention) OR (dirty money) OR (disbar!) OR (disciplinary) OR (disciplining) OR (disguis!) OR (dishonest!) OR (disloyal!) OR (disobey!) OR (disservic!) OR (dissimulat!) OR (election W/2 fraud) OR (election W/2 rig!) OR (embargo!) OR (embezzl!) OR (encroach!) OR (endamag!) OR (endanger!) OR (enforc!) OR (escapee) OR (espionag!) OR (exacti!) OR (extort!) OR (extrajudic!) OR (extralegal) OR (fabricat!) OR (faker!) OR (false accounting) OR (false flag) OR (false witness) OR (falsif!) OR (favoritism) OR (favouritism) OR (felon!) OR (fined) OR (fines) OR (flagitious) OR (forcible) OR (forensic) OR (forfeit!) OR (forge!) OR (frame up) OR (fraud!) OR (fugitiv!) OR (gang) OR (gangste!) OR (graft) OR (grievanc!) OR (guerrilla) OR (guilt!) OR (Hacker) OR (hacking) OR (hacktivis!) OR (house arrest) OR (hurt!) OR (ill-gotten) OR (illegal!) OR (illegitim!) OR (illicit!) OR (immoral!) OR (impeach!) OR (impost!) OR (imprison!) OR (impugn!) OR (impunity) OR (incarcerat!) OR (incriminat!) OR (inculpat!) OR (indemnif!) OR (indict!) OR (influence peddl!) OR (infraction!) OR (infring!) OR (injunction W/2 freez!) OR (injustic!) OR (inmate) OR (inside* job) OR (inside* deal!) OR (inside* trad!) OR (insolven!) OR (investigat!) OR (jail!) OR (judged w/8 court) OR (judged w/8 jury) OR (judgment) OR (judicial) OR (justice W/2 obstruct!) OR (justice W/2 serv!) OR (Kick-back) OR (kickback) OR (larcen!) OR (latitat!) OR (launder!) OR (law-break!) OR (lawbreak!) OR (lawless!) OR (lawsuit) OR (lebanese loop) OR (legal action) OR (legal conflict) OR (litig!) OR (machinat!) OR (Maffia) OR (mafia) OR (mafios!) OR (maladministrat!) OR (malefact!) OR (malefic!) OR (malfeas!) OR (malice) OR (malicious) OR (malversation) OR (manipulat!) OR (Market w/2 manipulat!) OR (meddl!) OR (misappropriat!) OR (misbrand!) OR (misconduc!) OR (misdeed) OR (misdemean!) OR (misfeas!) OR (mishandle) OR (mislead!) OR (mismanag!) OR (misrepresent!) OR (misus!) OR (mobster!) OR (mug shot) OR (mulct!) OR (narco!) OR (ndrangheta) OR (nefario!) OR (nepotis!) OR (noncomplian!) OR (oathbreach!) OR (oathbreak!) OR (offenc!) OR (offend!) OR (omerta) OR (omertà) OR (order W/2 freez!) OR (outlaw!) OR (outrag!) OR (overthrow!) OR (palter!) OR (parole) OR (peculat!) OR (pecuniary) OR (penal!) OR (penalty) OR (penitent!) OR (perfid!) OR (perjur!) OR (perpetrat!) OR (phone W/2 tapp!) OR (phoney OR phony) OR (piracy) OR (plagia!) OR (plea) OR (ponzi) OR (prevaricat!) OR (prison!) OR (prisoner) OR (probat!) OR (prohibit!) OR (proscribe!) OR (prosecut!) OR (protection money) OR (public enem!) OR (punish!) OR (putsch) OR (Pyramid organi!) OR (Pyramid schem!) OR (racketee!) OR (rake off) OR (rearraign!) OR (recidiv!) OR (red-handed) OR (redress!) OR (reprehend!) OR (reprehensibl!) OR (repriev!) OR (retaliat!) OR (reveng!) OR (revolving door) OR (rigg!) OR (ringlead!) OR (rip off) OR (rogue) OR (sabot!) OR (sanction!) OR (scam!) OR (scandal!) OR (scelerat!) OR (search warrant) OR (sedition) OR (seiz!) OR (sentenc! PRE/2 to) OR (sham) OR (shlenter!) OR (sleeper cell) OR (slush fund!) OR (smuggl!) OR (spy!) OR (steal! OR stole!) OR (suborn!) OR (subvers!) OR (subvert!) OR (sued) OR (swindl!) OR (taint!) OR (tamper!) OR (tax W/1 evas!) OR (tax W/2 evad!) OR (telefelon!) OR (telefraud))"
term_2 = " W/25 ((telephone W/2 tapp!) OR (terror!) OR (theft!) OR (tort) OR (traffic of influence) OR (traffick!) OR (traitor!) OR (transgress!) OR (treacher!) OR (treason!) OR (triad) OR (trial) OR (unauthoriz!) OR (under oath W/2 lie!) OR (under oath W/2 lying) OR (undue) OR (unlaw!) OR (usur!) OR (usurp!) OR (verdict) OR (violat!) OR (vitiat!) OR (vote W/2 buy!) OR (warrant) OR (white collar crim!) OR (wrong do!) OR (wrongdo!) OR (yakuza) OR (was fined) OR (a w/2 fine w/3 gav!) OR (a w/2 fine w/3 giv!) OR (a w/2 fine w/3 receiv!) OR (abet!) OR (abscond!) OR (abus!) OR (accomplice) OR (accus!) OR (adulter!) OR (agiotage) OR (allegation) OR (allege!) OR (amerce!) OR (amerci!) OR (apprehend!) OR (apprehension) OR (arraign!) OR (arrest!) OR (arrogat!) OR (asset! freez!) OR (at fault) OR (attack!) OR (attentat!) OR (bad faith) OR (bail) OR (ban OR banned) OR (bankrupt!) OR (barratry) OR (bench warrant) OR (betray!) OR (bid W/2 rig!) OR (biopiracy) OR (black-market!) OR (blacklist!) OR (blame!) OR (blood diamond) OR (bogus) OR (books W/2 fiddl!) OR (bootleg!) OR (breach!) OR (brib!) OR (carceral) OR (cease and desist) OR (charged with) OR (charges W/2 press!) OR (cheat!) OR (civil action) OR (clandestin!) OR (class action) OR (collud!) OR (collusi!) OR (complaint) OR (complicity) OR (complot!) OR (con artist) OR (conceal!) OR (condemn!) OR (Confiscat!) OR (conflict diamond) OR (conflict mineral) OR (conflict of interest))"

terms = [term_1, term_2]

AM_path = os.getcwd() + "/AdverseMedia_13.11.20/AM"
NAM_path = os.getcwd() + "/AdverseMedia_13.11.20/NAM"
UC_path = os.getcwd() + "/AdverseMedia_13.11.20/UC"


def create_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    log_format = logging.Formatter(
        "%(asctime)-15s - %(levelname)s - %(thread)d - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(log_format)
    log.addHandler(ch)
    return log


log = create_logger(__name__)


def sleep(request_counter, entity_counter, articles_total):
    if request_counter != 0:
        if request_counter % 7 == 0:
            print_mid_results(request_counter, entity_counter, articles_total)
            for i in range(60):
                print(i, end=' ')
                time.sleep(1)
            print('\n')
        if request_counter % 275 == 0:
            print_mid_results(request_counter, entity_counter, articles_total)
            for i in range(3600):
                print(i, end=' ')
                time.sleep(1)
            print('\n')
        if request_counter % 3500 == 0:
            print_mid_results(request_counter, entity_counter, articles_total)
            for i in range(43200):
                print(i, end=' ')
                time.sleep(1)
            print('\n')


def print_mid_results(request_counter, entity_counter, articles_total):
    print("==================================")
    print("Number of request made: ", request_counter)
    print("Number of entities processed: ", entity_counter)
    print("Number of articles made: ", articles_total)
    print("==================================")


def print_result_count(count, name, articles_counter, term_count):
    print("==================================")
    print("Entity: ", name)
    print("Total number of articles left to query: ", count - term_count)
    print("Total number of articles queried: ", articles_counter)
    print("==================================")
    UC_list = os.listdir(UC_path)
    NAM_list = os.listdir(NAM_path)
    AM_list = os.listdir(AM_path)
    print("############################")
    print("Amount of AM: ", len(AM_list))
    print("Amount of NAM: ", len(NAM_list))
    print("Amount of UC: ", len(UC_list))
    print("############################")


def entites(file_name):
    with open(os.getcwd() + "/app/" + file_name, encoding="utf8", mode='r') as csv_file:
        file = csv.reader(csv_file, delimiter=';')

        names = []

        line_count = 0
        for row in file:
            if len(row) == 0:
                break
            names.append(row[0])
            line_count += 1

        print("Total number of entites: ", len(names))
    return names


def make_sub_dir(path, language):
    sub_directory = path + "/" + language
    try:
        os.mkdir(sub_directory)
    except OSError:
        pass
    else:
        print("Successfully created the directory %s" % sub_directory)
    return sub_directory


@app.route("/start", methods=["GET"])
def main():
    names = entites(config.ENTITIES)
    counter, articles_counter = 0, 0
    entity_counter = 0
    request_counter = 0
    for name in names:
        entity_counter += 1
        counter = 0
        # entity_directory = os.getcwd() + "/AdverseMedia_13.11.20/" + name
        # try:
        #     os.mkdir(entity_directory)
        # except OSError:
        #     continue
        print("=====================")
        print("Entity: ", name)
        for term in terms:
            term_count = 0
            new_name = '"' + name + '"'
            query = URL + search + new_name + term + expand + top + filter
            print("--------------------")
            print("Query: ", query)

            counter, articles_counter, request_counter = start_working(query, name, counter, articles_counter, request_counter, entity_counter, term_count)
    print(articles_counter)


def start_working(query, name, counter, articles_counter, request_counter, entity_counter, term_count):
    if counter >= 500:
        return counter, articles_counter, request_counter
    sleep(request_counter, entity_counter, articles_counter)
    response = make_query(query)
    request_counter += 1
    if response.status_code != 200:
        print(response.raise_for_status())
    if response is not None and response.content is not None:
        json_obj = json.loads(response.content)
        if 'value' in json_obj:
            for news in json_obj['value']:
                if 'Document' in news \
                        and news['Document'] is not None \
                        and 'Content' in news['Document'] \
                        and news['Document']['Content'] is not None:

                    document = Document(name)
                    document.set_content(news['Document']['Content'])

                    soup = BeautifulSoup(document.get_content(), features="html.parser")

                    document.set_body(soup.findAll("nitf:body"))
                    document.set_title(" ".join([elem.get_text() for elem in soup.findAll("title")]))
                    document.set_published(" ".join([elem.get_text() for elem in soup.findAll("published")]))
                    document.set_updated(" ".join([elem.get_text() for elem in soup.findAll("updated")]))
                    document.set_id(" ".join([elem.get_text() for elem in soup.findAll("id")]))

                    text = " ".join([elem.get_text() for elem in document.get_body()])
                    detection_result = detect(text)
                    if detection_result == "en":
                        data = create_ml_query(document)
                        ml_article_response = make_request_ml(data)
                        response_data = ml_article_response.json()

                        article = response_data["article"]
                        if article != '':
                            document.set_cleaned_article(response_data["article"])
                            document.set_raw_cleaned_article(response_data["article_html"])

                            data_2 = create_ml_predict_query(document)
                            ml_predict_response = make_request_ml_predict(data_2)
                            response_data_2 = ml_predict_response.json()
                            document.set_prediction_class(response_data_2["data"]["prediction_class"])
                            document.set_prediction_score(response_data_2["data"]["prediction_score"])

                            filename = name + "_" + str(counter) + '.json'
                            data = document.get_data()

                            if document.get_prediction_class() == "Uncertain":
                                with open(UC_path + "/" + filename, "w") as outfile:
                                    json.dump(data, outfile)
                            elif document.get_prediction_class() == "Non-negative":
                                with open(NAM_path + "/" + filename, "w") as outfile:
                                    json.dump(data, outfile)
                            else:
                                with open(AM_path + "/" + filename, "w") as outfile:
                                    json.dump(data, outfile)

                            # html_file = open(entity_directory + "/" + filename, "w")
                            # html_file.write(text)
                            # html_file.close()

                            print(filename)
                            counter += 1
                            term_count += 1
                            articles_counter += 1
        if '@odata.nextLink' in json_obj:
            query = json_obj['@odata.nextLink']
            print_result_count(json_obj['@odata.count'], name, articles_counter, term_count)
            counter, articles_counter, request_counter = start_working(query, name, counter, articles_counter, request_counter, entity_counter, term_count)
    return counter, articles_counter, request_counter


def make_query(query):
    return requests.get(query, headers={'Authorization': accessToken,
                                            'Content-Type': 'application/x-www-form-urlencoded'})


def create_ml_query(document):
    data = {}
    data["keyword"] = document.get_name()
    data["keywordLocal"] = None
    data["surroundingSentences"] = 2
    data["country"] = None
    data["document"] = document.get_content()
    data["documentWithValues"] = document.get_content()
    data["weightMain"] = 2
    data["weightSurrounding"] = 1
    data["relevance"] = 5
    return json.dumps(data)


def make_request_ml(data):
    query = "http://127.0.0.1:5000/article"
    return requests.post(url=query, headers={'Content-Type': 'application/json'}, data=data)


def create_ml_predict_query(document):
    data = {}
    data["document"] = [document.get_cleaned_article()]
    return json.dumps(data)


def make_request_ml_predict(data):
    query = "http://127.0.0.1:5000/predict"
    return requests.post(url=query, headers={'Content-Type': 'application/json'}, data=data)
