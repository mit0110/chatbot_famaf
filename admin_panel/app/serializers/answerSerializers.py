
def answerEntity(answer) -> dict:
    return {
        "id": str(answer["_id"]),
        "content": answer["content"],
        "category": answer.get("category"),
        "created_at": answer["created_at"],
        "updated_at": answer["updated_at"]
    }


def populatedAnswerEntity(answer) -> dict:
    return {
        "id": str(answer["_id"]),
        "content": answer["content"],
        "category": answer.get("category"),
        "created_at": answer["created_at"],
        "updated_at": answer["updated_at"]
    }


def answerListEntity(answers) -> list:
    return [populatedAnswerEntity(answer) for answer in answers]