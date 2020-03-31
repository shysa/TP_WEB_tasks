from django.shortcuts import render
from paginator.paginate import paginate


def index(request):
    context = {}
    questions = []
    for i in range(1, 300):
        questions.append({
            'title': 'question ' + str(i),
            'id': i,
            'text': '''Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante
                        sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis.
                        Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in
                        faucibus''',
            'tags': ['tag' + str(i), 'tag' + str(i), 'tag' + str(i), 'tag' + str(i), 'tag' + str(i)],
            'comments': str(i),
            'rating': str(i),
        })

    context = paginate(questions, request)

    return render(request, 'index.html', context)


def question(request, question_id):
    comments = []
    question = {
        'title': 'question',
        'id': question_id,
        'text': '''Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante
                            sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis.
                            Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in
                            faucibus''',
        'tags': ['tag' + str(1), 'tag' + str(2), 'tag' + str(3)],
        'comments': str(5),
        'rating': str(10),
    }
    for i in range(5):
        comments.append({
            'id': i,
            'text': '''Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante
                            sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis.
                            Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in
                            faucibus''',
            'rating': str(i),
        })

    context = {'question': question, 'comments': comments}

    return render(request, 'question.html', context)


def tag(request, tag):
    context = {}
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': 'question ' + str(i),
            'id': i,
            'text': '''Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante
                            sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis.
                            Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in
                            faucibus''',
            'tags': [tag, 'tag' + str(i)],
            'comments': str(i),
            'rating': str(i),
        })

    context = paginate(questions, request)
    context['tag'] = tag

    return render(request, 'index.html', context)


def hot(request):
    context = {}
    questions = []
    for i in range(1, 300):
        questions.append({
            'title': 'question ' + str(i),
            'id': i,
            'text': '''Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante
                            sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis.
                            Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in
                            faucibus''',
            'tags': ['tag' + str(i), 'tag' + str(i), 'tag' + str(i), 'tag' + str(i), 'tag' + str(i)],
            'comments': str(i),
            'rating': i,
        })

    questions.sort(key=lambda question: question['rating'], reverse=True)

    context = paginate(questions, request)

    return render(request, 'index.html', context)


def ask(request):
    return render(request, 'ask.html')


def profile(request):
    return render(request, 'profile.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')