import boto3
import json


def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    for item in event.get('Records'):
        name = item['s3']['object']['key']
        data = s3_client.get_object(Bucket='', Key=name) #put your bucket name in the "Bucket" variable
        contents = json.loads(data['Body'].read())
        individual_words_details = contents['results']['items']
        total_speakers = contents['results']['speaker_labels']['speakers']
        segments = contents['results']['speaker_labels']['segments']
        key = name
        s3_resource = boto3.resource('s3')
        bucket_name = '' #put your output bucket name in this variable
        local_file = f'/tmp/{name}.txt'

    combine_punctuation = []
    for word in individual_words_details:
        if word['type'] == 'pronunciation':
            combine_punctuation.append(word)
        else:
            combine_punctuation[-1]['alternatives'][0]['content'] += word['alternatives'][0]['content']

    new_list = []
    for item in segments:
        for segment in item['items']:
            for word in combine_punctuation:
                for k, v in word.items():
                    if k == 'start_time' and v == segment['start_time']:
                        new_dict = {
                            "start_time": segment['start_time'],
                            "end_time": segment['end_time'],
                            "speaker_label": segment['speaker_label'],
                            "content": word['alternatives'][0]['content'],
                            "confidence": word['alternatives'][0]['confidence']
                        }
                        new_list.append(new_dict)

    def create_document(new_list):
        with open(local_file, 'a+') as file:
            speaker = 'spk_0'
            line = []
            if total_speakers > 1:
                for item in new_list:
                    if item['speaker_label'] == speaker:
                        line.append(item['content'])
                    else:
                        sentence = ' '.join(line)
                        file.write(f'{speaker}: {sentence}\n')
                        print('\n')
                        del line
                        line = []
                        speaker = item['speaker_label']
            else:
                for item in new_list:
                    line.append(item['content'])
                sentence = ' '.join(line)
            file.write(f'{speaker}: {sentence}')
        s3_resource.meta.client.upload_file(local_file, bucket_name, key)

    create_document(new_list)
