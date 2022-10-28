def average_positions(data):
    users = set( [user["user_name"] for user in data] )
    answers = [user["answer"] for user in data]

    average_pos = dict()
    for user in users:
        positions = []
        for answer in answers:
            positions.append(answer.index(user))
        average_pos[user] = sum(positions) / len(positions)
    
    return average_pos


def round_errors(data, correct_answer):
    users_dicts = []
    for user in data:
        name = user["user_name"]
        answer = user["answer"]
        error = sum( [abs(i - correct_answer[j]) for i,j in enumerate(answer)])
        error = round(error, 2)
        users_dicts.append({"user_name": name, "error": error})
    users_dicts.sort(key=lambda x: x["error"])

    return users_dicts


def round_scores(data, errors):
    scores = [100, 50, 25] + [0]*len(errors)
    last_user_error = errors[0]["error"]
    users_score = {}
    for user in errors:
        if user["error"] != last_user_error:
            scores.pop(0)
        users_score[user["user_name"]] = scores[0]

    return users_score


def point_distribution(data):
    for user in data: 
        user["last_turn_points"] = user["points"]
        user["answer"] = [dic["user_name"] for dic in  user["answer"]]

    #refactorizar para que funcione con este tipo de answer

    correct_answer = average_positions(data)
    errors = round_errors(data, correct_answer)
    scores = round_scores(data, errors)

    for user in data:
        user["points"] = user["last_turn_points"] + \
                                 scores[user["user_name"]]
    
    answer = [(correct_answer[name], name) for name in correct_answer]
    answer.sort()

    return data, [{"user_name":i[1], "distance":round(i[0],3)} for i in answer]