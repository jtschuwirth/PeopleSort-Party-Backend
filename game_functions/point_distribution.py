def clean_data(data):
    users = [*filter(lambda x: "answer" in x and len(x["answer"]) > 0, data)]
    for user in users:
        user["answer"] = [*map(lambda x: x["user_name"], user["answer"])]
    return users


def average_positions(data):
    users = set( data[0]["answer"] )
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


def round_scores(errors):
    scores = [100, 50, 25] + [0]*len(errors)
    last_user_error = errors[0]["error"]
    users_score = {}
    i = 1
    for user in errors:
        if user["error"] != last_user_error:
            scores.pop(0)
            i += 1
        users_score[user["user_name"]] = scores[0]

    return users_score


def point_distribution(table, data):
    for user in data: 
        user["last_turn_points"] = user["points"]

    clean_user_list = clean_data(data)
    if len(clean_user_list) < 1:
        raise ValueError("Ningún usuario entregó answer")

    correct_answer = average_positions(clean_user_list)
    errors = round_errors(clean_user_list, correct_answer)
    scores = round_scores(errors)

    for user in clean_user_list:
        user["points"] = user["last_turn_points"] + \
                         scores[user["user_name"]]
        table.update_item(
           Key={'connection_id': user["connection_id"]},
           UpdateExpression = f"ADD points :p",
           ExpressionAttributeValues={
               ':p': scores[user["user_name"]]
           })
    
    answers = [(correct_answer[name], name) for name in correct_answer]
    answers.sort()

    j = 1
    last_user_avg_pos = answers[0][0]
    c_answer =[]
    for answer in answers:
        if answer[0] > last_user_avg_pos:
            j += 1
        c_answer.append({ "user_name": answer[1], 
                          "distance": j
            }
        )

    return data, c_answer