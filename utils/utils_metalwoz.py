import json
import os
import pandas as pd

from .utils_function import get_input_example


def read_langs_turn(args, dial_files, max_line=None, ds_name=""):
    print(("Reading from {} for read_langs_turn".format(ds_name)))

    data = []

    cnt_lin = 1
    df = pd.read_excel(
        os.path.join(args["data_path"], "Translated", "train_dumpdata_tod_metalwoz_translated_tokenized.xlsx"),
        dtype=str,
    )
    dict_translated = dict(zip(df["text"], df["trans_tokenized"]))
    del df
    number_of_dials = 0
    number_of_turns = 0
    for dial_file in dial_files:

        f_dials = open(dial_file, "r")
        dials = f_dials.readlines()
        number_of_dials += len(dials)
        for dial in dials:
            dialog_history = []
            dial_dict = json.loads(dial)
            number_of_turns += len(dial_dict["turns"])
            for ti, turn in enumerate(dial_dict["turns"]):
                if turn.strip() not in dict_translated:
                    print("turn = ", turn.strip())
                turn = dict_translated.get(turn.strip(), turn.strip()).strip()

                if ti % 2 == 0:
                    turn_sys = turn.lower().strip()
                else:
                    turn_usr = turn.lower().strip()
                    data_detail = get_input_example("turn")
                    data_detail["ID"] = "{}-{}".format(ds_name, cnt_lin)
                    data_detail["turn_id"] = ti % 2
                    data_detail["turn_usr"] = turn_usr
                    data_detail["turn_sys"] = turn_sys
                    data_detail["dialog_history"] = list(dialog_history)

                    if not args["only_last_turn"]:
                        data.append(data_detail)

                    dialog_history.append(turn_sys)
                    dialog_history.append(turn_usr)

            if args["only_last_turn"]:
                data.append(data_detail)

            cnt_lin += 1
            if max_line and cnt_lin >= max_line:
                break
    print("number_of_dials = ", number_of_dials)
    print("number_of_turns = ", number_of_turns)
    return data


def read_langs_dial(file_name, ontology, dialog_act, max_line=None, domain_act_flag=False):
    print(("Reading from {} for read_langs_dial".format(file_name)))

    raise NotImplementedError


def prepare_data_metalwoz(args):
    ds_name = "MetaLWOZ"

    example_type = args["example_type"]
    max_line = args["max_line"]

    onlyfiles = [
        os.path.join(args["data_path"], "metalwoz/dialogues/{}".format(f))
        for f in os.listdir(os.path.join(args["data_path"], "metalwoz/dialogues/"))
        if ".txt" in f
    ]

    _example_type = "dial" if "dial" in example_type else example_type
    pair_trn = globals()["read_langs_{}".format(_example_type)](args, onlyfiles, max_line, ds_name)
    pair_dev = []
    pair_tst = []

    print("Read {} pairs train from {}".format(len(pair_trn), ds_name))
    print("Read {} pairs valid from {}".format(len(pair_dev), ds_name))
    print("Read {} pairs test  from {}".format(len(pair_tst), ds_name))

    meta_data = {"num_labels": 0}

    return pair_trn, pair_dev, pair_tst, meta_data
