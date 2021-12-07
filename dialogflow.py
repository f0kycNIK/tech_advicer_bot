from google.cloud import dialogflow


def detect_intent_text(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    answer = response.query_result.fulfillment_text
    intent_flag = response.query_result.intent.is_fallback
    return answer, intent_flag
