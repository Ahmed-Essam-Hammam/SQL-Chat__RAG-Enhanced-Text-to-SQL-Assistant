from chains import answer_chain


def get_natural_response(question, data):
    return answer_chain.invoke({
        "question": question,
        "data": data
    }).strip()
