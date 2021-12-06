import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow

from parser_commands import create_parser


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=[message_texts])
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases,
        messages=[message]
    )
    intents_client.create_intent(request={"parent": parent, "intent": intent})


def get_list_intents(project_id):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    intents = intents_client.list_intents(request={"parent": parent})
    intent_name = []
    for intent in intents:
        intent_name.append(intent.display_name)
    return intent_name


def load_intents(project_id, file_questions):
    with open(file_questions, encoding='utf-8') as file_questions:
        questions = json.load(file_questions)
    intents = get_list_intents(project_id)
    for intent, scenario in questions.items():
        training_phrases_parts = scenario['questions']
        message_texts = scenario['answer']
        if intent not in intents:
            create_intent(project_id, intent, training_phrases_parts,
                          message_texts)


if __name__ == '__main__':
    load_dotenv()

    file_path = 'questions.json'

    parser = create_parser(file_path)
    args = parser.parse_args()
    project = args.project
    file_questions = args.file

    load_intents(project, file_questions)
