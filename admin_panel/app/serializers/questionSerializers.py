from app.serializers.answerSerializers import answerEntity

def populatedQuestionEntity(question) -> dict:
    return {
        "id": str(question["_id"]),
        "content": question["content"],
        "category": question.get("category"),
        "image": question.get("image"),
        "answers": [answerEntity(answer) for answer in question.get("answers", [])],
        "created_at": question["created_at"],
        "updated_at": question["updated_at"]
    }


def questionListEntity(questions) -> list:
    return [populatedQuestionEntity(question) for question in questions]