from google import genai

client = genai.Client(api_key="AIzaSyDwFlz5ipw_QpHzTi1akcHrdy-HgM5wKfQ")

def get_summary(text):
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Give me a summary about:" + text,)
    return response

def get_qna(text):
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Give me a list of frequent questions and answers about:" + text,)
    return response

def get_quiz(text):
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Give me a multiple choice quiz that has similar answers and traps about:" + text,)
    return response

response = get_quiz("machine learning")
print(response.text)
