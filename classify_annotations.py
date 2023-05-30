from pathlib import Path
import jsonlines
import os


all_annotations_file = "./classified_annotation_jsonl/all_annotations.jsonl"


def write_jsonl(output_file, jsonl_content):
    with jsonlines.open(output_file, mode='w') as writer:
        writer.write_all(jsonl_content)


def combine_all_jsonl():
    folder_path = "./"

    jsonl_content = []

    for dirname in sorted(os.listdir(folder_path)):
        dir_path = Path(os.path.join(folder_path, dirname))
        if os.path.isdir(dir_path):
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path) and file_path.endswith(".jsonl"):
                    with jsonlines.open(file_path) as reader:
                        for line in reader.iter():
                            jsonl_content.append(line)

    write_jsonl(all_annotations_file, jsonl_content)


def classify_between_modern_and_pering_print():
    pering = []
    modern = []
    modern_prints = Path("./modernprints.txt").read_text(encoding='utf-8').splitlines()
    with jsonlines.open(all_annotations_file) as reader:
        for line in reader.iter():
            is_modern = False
            image_url = line['image']
            work_id = image_url.split('/')[6]
            imagegroup = (image_url.split('/')[8]).split('-')[1]
            for modern_print in modern_prints:
                work = modern_print.split(',')[0]
                if work_id == work:
                    image_group = modern_print.split(',')[1]
                    if imagegroup == image_group:
                        is_modern = True
            if is_modern:
                modern.append(line)
            else:
                pering.append(line)

    write_jsonl(f"./classified_annotation_jsonl/modern_print.jsonl", modern)
    write_jsonl(f"./classified_annotation_jsonl/pering.jsonl", pering)


def classify_as_per_work():
    curr = {}
    with jsonlines.open(all_annotations_file) as reader:
        for line in reader.iter():
            image_url = line['image']
            work_id = image_url.split('/')[6]
            if work_id in curr.keys():
                curr[work_id].append(line)
            else:
                curr[work_id] = [line]
    
    for work_id in curr:
        write_jsonl(f"./classified_annotation_jsonl/{work_id}.jsonl", curr[work_id])



if __name__ == "__main__":
    combine_all_jsonl()
    classify_between_modern_and_pering_print()
    classify_as_per_work()
