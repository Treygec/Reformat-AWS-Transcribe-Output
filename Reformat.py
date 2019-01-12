#this file is just for Local_Reformat to make that code cleaner and more readable

def create_document(list_of_words, document_name, total_speakers):
    filename = document_name
    with open(filename, 'a+', encoding='utf-8') as file:
        speaker = 'spk_0'
        line = []
        if total_speakers > 1:
            for item in list_of_words:
                if item['speaker_label'] == speaker:
                    line.append(item['content'])
                else:
                    sentence = ' '.join(line)
                    file.write(f'{speaker}: {sentence}\n')
                    file.write('\n')
                    del line
                    line = []
                    speaker = item['speaker_label']
        else:
            for item in list_of_words:
                line.append(item)
                sentence = ' '.join(line)
            file.write(f'{speaker}: {sentence}')


def combine_punctuation(list_of_items):
    combined_punctuation = []
    for item in list_of_items:
        if item['type'] == 'pronunciation':
            combined_punctuation.append(item)
        else:
            combined_punctuation[-1]['alternatives'][0]['content'] += item['alternatives'][0]['content']
    return combined_punctuation
