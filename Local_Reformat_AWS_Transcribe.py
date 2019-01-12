import json
import Reformat

file_name =
reformatted_file_name = f'{file_name} - Reformatted'
with open(file_name, 'r') as f:
    data = f.read()
    contents = json.loads(data)
    individual_words_details = contents['results']['items']
    try:
        total_speakers = contents['results']['speaker_labels']['speakers']
        segments = contents['results']['speaker_labels']['segments']
    except KeyError:
        total_speakers = 1
        keep_punctuation = Reformat.combine_punctuation(individual_words_details)
        new_list = []
        for item in keep_punctuation:
            new_list.append(item['alternatives'][0]['content'])

        Reformat.create_document(new_list,reformatted_file_name, total_speakers)
        exit()

    keep_punctuation = Reformat.combine_punctuation(individual_words_details)
    new_list = []
    for item in segments:
        for segment in item['items']:
            for word in keep_punctuation:
                for k, v in word.items():
                    if k == 'start_time' and v == segment['start_time']:
                        word_dict = {
                            "start_time": segment['start_time'],
                            "end_time": segment['end_time'],
                            "speaker_label": segment['speaker_label'],
                            "content": word['alternatives'][0]['content'],
                            "confidence": word['alternatives'][0]['confidence']
                        }
                        new_list.append(word_dict)

    Reformat.create_document(new_list,reformatted_file_name,total_speakers)



