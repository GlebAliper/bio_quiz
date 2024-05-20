import uuid


def get_quizzes():
    quizzes = []
    with open('./data/quiz.csv', 'r', encoding='UTF-8') as f:
        for i, line in enumerate(f.readlines()[1:]):
            id, name, description, image = line.strip().split(';')
            quizzes.append(
                [
                    id,
                    name,
                    description,
                    image
                ]
            )
        return quizzes


def get_users_stats():
    stats = []
    with open('./data/user.csv', 'r', encoding='UTF-8') as f:
        for i, line in enumerate(f.readlines()[1:]):
            name, email, games, answers, correct_answers, percent = line.strip().split(';')
            stats.append(
                [
                    name,
                    games,
                    answers,
                    correct_answers,
                    round(float(percent), 2)
                ]
            )
        return stats


def get_quiz(quiz_id):
    quiz = []
    questions = []
    with open('./data/quiz.csv', 'r', encoding='UTF-8') as f:
        for i, line in enumerate(f.readlines()[1:]):
            id, name, description, image = line.strip().split(';')
            if int(id) == quiz_id:
                quiz.append(id)
                quiz.append(name),
                quiz.append(description),
                quiz.append(image)

    with open('./data/quiz_question.csv', 'r', encoding='UTF-8') as f:
        for i, line in enumerate(f.readlines()[1:]):
            id, q_id, question, answer_1, answer_2, answer_3, answer_4, correct_answer = line.strip().split(';')

            if int(q_id) == quiz_id:
                questions.append(
                    [
                        id,
                        question,
                        answer_1,
                        answer_2,
                        answer_3,
                        answer_4
                    ]
                )

    return quiz, questions


def make_result(user_name, user_email, game_answers):
    game_answers_total = 0
    game_correct_answers = 0
    with open('./data/quiz_question.csv', 'r', encoding='UTF-8') as f:
        for i, line in enumerate(f.readlines()[1:]):
            id, q_id, question, answer_1, answer_2, answer_3, answer_4, correct_answer = line.strip().split(';')
            if id in game_answers:
                game_answers_total += 1
                if game_answers[id] == correct_answer:
                    game_correct_answers += 1

    with open('./data/user.csv', 'r', encoding='UTF-8') as f:
        users = []
        new_user = True
        for i, line in enumerate(f.readlines()[1:]):
            name, email, games, answers, correct_answers, percent = line.strip().split(
                ';')
            if user_name == name:
                new_user = False
                email = user_email
                games = int(games) + 1
                answers = int(answers) + game_answers_total
                correct_answers = int(correct_answers) + game_correct_answers
                percent = 100 * correct_answers / answers
                users.append(
                    [
                        name,
                        email,
                        games,
                        answers,
                        correct_answers,
                        percent
                    ]
                )
            else:
                users.append(
                    [
                        name,
                        email,
                        games,
                        answers,
                        correct_answers,
                        percent
                    ]
                )
        if new_user:
            users.append(
                [
                    user_name,
                    user_email,
                    1,
                    game_answers_total,
                    game_correct_answers,
                    100 * game_correct_answers / game_answers_total
                ]
            )
        users.sort(key=lambda x: float(x[-1]), reverse=True)
    with open('./data/user.csv', 'w', encoding='UTF-8') as f:
        lines = ['name;email;games;answers;correct_answers;percent\n']
        for user in users:
            lines.append(';'.join(map(str, user)) + "\n")
        f.writelines(lines)

    return game_correct_answers, 100 * game_correct_answers / game_answers_total


def save_quiz(q_name, q_description, questions, answers, image):
    data_quizzes = []
    if image:
        image_type = image.content_type.split(sep='/')[1]
        image_name = 'static/images_store/' + str(uuid.uuid4()) + '.' + image_type
        with open(image_name, 'wb+') as f:
            f.write(image.read())
    else:
        image_name = 'static/images_store/default.jpg'
    with open('./data/quiz.csv', 'r', encoding='UTF-8') as f:
        max_id = 0
        for i, line in enumerate(f.readlines()[1:]):
            id, name, description, image = line.strip().split(';')
            max_id = max(int(id), max_id)
            data_quizzes.append([
                id,
                name,
                description,
                image
            ])
        quiz_id = max_id + 1

        data_quizzes.append([
            quiz_id,
            q_name,
            q_description,
            image_name
        ])
    with open('./data/quiz.csv', 'w', encoding='UTF-8') as f:
        lines = ['id;name;description;image\n']
        for quiz in data_quizzes:
            lines.append(';'.join(map(str, quiz)) + "\n")
        f.writelines(lines)

    data_questions = []
    with open('./data/quiz_question.csv', 'r', encoding='UTF-8') as f:
        max_id = 0
        for i, line in enumerate(f.readlines()[1:]):
            id, q_id, question, answer_1, answer_2, answer_3, answer_4, correct_answer = line.strip().split(';')

            max_id = max(int(id), max_id)

            data_questions.append(
                [
                    id,
                    q_id,
                    question,
                    answer_1,
                    answer_2,
                    answer_3,
                    answer_4,
                    correct_answer
                ]
            )
        max_id += 1

    for key, val in questions.items():
        data_questions.append([
            max_id,
            quiz_id,
            val,
            answers.get(key).get('0'),
            answers.get(key).get('1'),
            answers.get(key).get('2'),
            answers.get(key).get('3'),
            answers.get(key).get('correct_answer'),
        ])
        max_id += 1
    with open('./data/quiz_question.csv', 'w', encoding='UTF-8') as f:
        lines = ['id,quiz_id;question;answer_1;answer_2;answer_3;answer_4;correct_answer\n']
        for question in data_questions:
            lines.append(';'.join(map(str, question)) + "\n")
        f.writelines(lines)
