# Reformat-AWS-Transcribe-Output
This project is to reformat AWS Transcribe output into a more human readable format both on your local machine or in AWS Lambda

# Usage

## Local
To run locally you will need the Reformat.py, and Local_Reformat_AWS_Transcribe.py files on your machine. Reformat.py contains 2 functions.
The first is `combine_punctuation` which takes punctuation items and concatenates them to the word preceeding them so they do not get
dropped during documentation. The reason this was necessary was that punctuation does not have time stamps needed during second function,
`create_document`

The create_document function takes 3 variables: "new_list"(new list of words created from "combine_punctuation"), "reformatted_file_name",
and "total_speakers". This function organizes the words to their speaker and creates a new document that looks more like a conversation 
than a JSON file. 

## Lambda
The Lambda_Reformat_AWS_Transcribe file can be copy pasted, or imported into Lambda. It is written to trigger from S3 events and has two 
fields you will need to edit. The first is the Bucket name that will contain your AWS Transcribe output, and the second is the bucket 
where you would like your new document to be put. 

## Both
Once you have your new document, you can open it in Notpad, Notepad++, or your preferred text editor. If you copy / paste the entire file 
into a Word document it will create a blank like between each speaker segment. 
