from django.shortcuts import render, redirect
from . import models
from . import forms
from accounts import models as account_models
from django.utils import timezone
from django import forms as dforms
import random
from django.contrib.auth.hashers import make_password, check_password
#parag
from django.utils.crypto import get_random_string

# Create your views here.

def get_challenge():
    A = None
    B = None
    C = models.question()
    M = models.question.objects.all()
    C.questions = len(M)
    M = models.challenge.objects.all()
    C.challenges = len(M)
    M = account_models.user.objects.all()
    C.users = len(M)
    all_challenges = models.challenge.objects.all()
    ongoing_challenge = []
    upcoming_challenge = []
    for entry in all_challenges:
        if status(entry.slug) == 'A' and entry.type == 'O':
            ongoing_challenge.append(entry)
        elif status(entry.slug) == 'M' and entry.type == 'O':
            upcoming_challenge.append(entry)

    if len(ongoing_challenge) > 0:
        A = ongoing_challenge[0]
        for entry in ongoing_challenge:
            if entry.start_date < A.start_date:
                A = entry
            elif entry.start_date == A.start_date and entry.start_time < A.start_time:
                A = entry
        A.before_end = rem(A.slug)

    if len(upcoming_challenge) > 0:
        B = upcoming_challenge[0]
        for entry in upcoming_challenge:
            if entry.start_date < B.start_date:
                B = entry
            elif entry.start_date == B.start_date and entry.start_time < B.start_time:
                B = entry
        B.before_start = before(B.slug)

    return A, B, C

def isAdmin(request):
    username, type = authenticate(request)
    if type == 'A':
        return True
    else:
        return False

def authenticate(request):
    username = request.session.get('username')
    if username != None:
        user = account_models.user.objects.filter(username=username)
        user = user[0]
        user_type = user.user_type
        if user_type == 'standard':
            user_type = 'U'
        elif user_type == 'setter':
            user_type = 'S'
        elif user_type == 'admin':
            user_type = 'A'
        return username, user_type
    else:
        return username, None

def status(slug):
    print('lodu', ' ', slug)
    curr_date = timezone.now().date()
    curr_time = timezone.now().time()
    match = models.challenge.objects.filter(slug=slug)
    match = match[0]
    if curr_date < match.start_date:
        print('here1')
        return 'M'
    elif curr_date == match.start_date and curr_time < match.start_time:
        print('here2')
        return 'M'
    elif curr_date == match.start_date and match.start_date == match.end_date:
        if curr_time >= match.start_time and curr_time <= match.end_time:
            return 'A'
        elif curr_time > match.end_time:
            return 'C'
    elif curr_date == match.start_date and match.end_date != match.start_date:
        return 'A'
    elif curr_date > match.start_date and curr_date < match.end_date:
        return 'A'
    elif curr_date == match.end_date and curr_time <= match.end_time:
        return 'A'
    elif curr_date == match.end_date and curr_time > match.end_time:
        return 'C'
    else:
        return 'C'

def get_rank(username, challenge_slug):
    all_contestants = models.score.objects.filter(challenge_slug=challenge_slug)
    if len(all_contestants) == 0:
        return -1
    else:
        leaderboard = []
        for contestants in all_contestants:
            leaderboard.append(contestants)
        leaderboard.sort(reverse=True, key=comparator)
        rank = 1
        curr_points = leaderboard[0].score
        for i in range(len(leaderboard)):
            if leaderboard[i].score < curr_points:
                curr_points = leaderboard[i].score
                rank = i + 1
            leaderboard[i].rank = rank
            if leaderboard[i].username == username:
                return leaderboard[i].rank
        return -1

def before(slug):
    match = models.challenge.objects.filter(slug=slug)
    match = match[0]
    time = str(match.start_date) + ' ' + str(match.start_time)
    time = time.replace('-', '/')
    return time

def rem(slug):
    match = models.challenge.objects.filter(slug=slug)
    match = match[0]
    time = str(match.end_date) + ' ' + str(match.end_time)
    time = time.replace('-', '/')
    return time

def comparator(e):
    return e.score

def evaluate(A, B, points):
    print('EVALUATE')
    print(A)
    print(B)
    print(points)
    print(len(A), ' ', len(B))
    if len(A) != len(B):
        return 0
    flag = 1
    for i in range(len(A)):
        if A[i] == 'A' or A[i] == 'B' or A[i] == 'C' or A[i] == 'D':
            if A[i] != B[i]:
                flag = 0

    if flag == 0:
        return 0;
    else:
        return points

def logout_view(request):
    request.session.pop('username')
    request.session.pop('type')
    return redirect('accounts:landing')

def setter_view(request):
    username, type = authenticate(request)
    print(type)
    if username == None:
        return redirect('accounts:login')

    A, B, C = get_challenge()

    if request.method == 'GET':
        if type == 'U':
            entries = models.setter_request.objects.filter(username=username)
            print(len(entries))
            if len(entries) > 0:
                return render(request, 'person/setter.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'user_type': type, 'submitted': '1'})
            elif len(entries) == 0:
                form = forms.SetterRequest()
                return render(request, 'person/setter.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'user_type': type, 'form': form, 'submitted': '0'})
        elif type == 'S':
            contest_set = []
            managed = models.challenge_setter.objects.filter(setter = username)
            for entry in managed:
                curr = models.challenge.objects.filter(slug=entry.slug)
                curr = curr[0]
                curr.cs = status(entry.slug)
                contest_set.append(curr)
            form = forms.CreateChallenge()
            return render(request, 'person/setter.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'user_type': type, 'form': form, 'contests': contest_set})
        elif type == 'A':
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
    else:
        if type == 'U':
            form = forms.SetterRequest(request.POST)
            new_request = form.save(commit=False)
            new_request.username = username
            new_request.save()
            form.save_m2m()
            return redirect('person:setter')
        elif type == 'S':
            form = forms.CreateChallenge(request.POST)
            if form.is_valid():
                new_challenge = form.save(commit=False)
                new_challenge.save()
                form.save_m2m()
                setter_details = models.challenge_setter()
                setter_details.slug = form.cleaned_data['slug']
                setter_details.setter = username
                setter_details.save()
                return redirect('person:challenge', slug=form.cleaned_data['slug'])
            else:
                err = form.errors
                return render(request, 'person/setter.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'user_type': type, 'form': forms.CreateChallenge(), 'err': err})

def challenge_view(request, slug):
    username, type = authenticate(request)
    if username == None:                                                             # USER NOT LOGGED IN
        return redirect('accounts:login')
    else:
        A, B, C = get_challenge()
        match = models.challenge.objects.filter(slug=slug)                             # CONTEST DOES NOT EXIST
        if len(match) == 0:
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
        else:
            match = match[0]
            challenge_status = status(slug)
            match1 = models.challenge_setter.objects.filter(slug=slug, setter=username)    # USER A SETTER ?
            match2 = models.challenge_setter.objects.filter(slug=slug)
            if len(match1) == 0:
                challenge_user_type = 'user'
            else:
                challenge_user_type = 'setter'

            if type == 'A':
                challenge_user_type = 'admin'

    if request.method == 'GET':
        if challenge_status == 'M' and (challenge_user_type == 'setter' or challenge_user_type == 'admin'):                                                                 # CONTEST IN MAKING STATUS
            data = {'name': match.name, 'slug': match.slug, 'start_time': match.start_time, 'end_time': match.end_time, 'start_date': match.start_date, 'end_date': match.end_date, 'type': match.type, 'instructions': match.instructions}
            form = forms.challengeDetails(initial=data)
            form1 = forms.newCollaborator()
            form2 = forms.removeChallenge()
            questions = models.question.objects.filter(challenge_slug=slug)
            return render(request, 'person/challenge_details.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'curr_challenge': match, 'form': form, 'form1': form1, 'form2': form2, 'slug': match.slug, 'questions': questions, 'setters': match2, 'before': before(slug), 'user_type': challenge_user_type})
        elif challenge_status == 'M' and challenge_user_type == 'user':
            return render(request, 'person/challenge.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'challenge_name': match.name, 'instr': match.instructions, 'status': challenge_status, 'before': before(slug), 'setters': match2, 'user_type': challenge_user_type})                                                                              # CONTEST NOT IN MAKING STATUS
        elif challenge_status == 'A':
            questions = models.question.objects.filter(challenge_slug=slug)
            for question in questions:
                sub = models.submission.objects.filter(username=username, question_slug=question.slug)
                if len(sub) == 0:
                    question.solved = 0
                else:
                    question.solved = 1
            data = {'end_time': match.end_time, 'end_date': match.end_date}
            form = forms.extendChallenge(initial=data)
            return render(request, 'person/challenge.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'challenge_name': match.name, 'instr': match.instructions, 'form': form, 'status': challenge_status, 'rem': rem(slug), 'setters': match2, 'questions': questions, 'user_type': challenge_user_type})
        elif challenge_status == 'C':
            questions = models.question.objects.filter(challenge_slug=slug)
            participate = 0
            total = {}
            total['total'] = 0
            total['score'] = 0
            for question in questions:
                sub = models.submission.objects.filter(username=username, question_slug=question.slug)
                total['total'] = total['total'] + question.points
                if len(sub) == 0:
                    question.attempted = -1
                else:
                    sub = sub[0]
                    participate = 1
                    question.attempted = evaluate(question.answer, sub.answer, question.points)
                    total['score'] = total['score'] + question.attempted
            return render(request, 'person/challenge.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'slug': slug, 'participate': participate, 'challenge_name': match.name, 'instr': match.instructions, 'status': challenge_status, 'total': total, 'setters': match2, 'questions': questions, 'user_type': challenge_user_type})

    elif request.method == 'POST':

        if challenge_status == 'M' and challenge_user_type == 'setter':                                                                                 # CONTEST IN MAKING STATUS
            form = forms.challengeDetails(request.POST)
            print(form.fields)
            if form.is_valid():
                m_challenge = form.save(commit=False)
                match.type = m_challenge.type
                match.start_time = m_challenge.start_time
                match.end_time = m_challenge.end_time
                match.start_date = m_challenge.start_date
                match.end_date = m_challenge.end_date
                match.instructions = m_challenge.instructions
                match.save()
                return redirect('person:challenge', slug=slug)
            else:
                err = form.errors
                return render(request, 'person/challenge_details.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'form': form, 'slug': match.slug, 'questions': questions, 'err': err})
        elif challenge_status == 'A' and challenge_user_type == 'setter':
            form = forms.extendChallenge(request.POST)
            if form.is_valid():
                match.end_date = form.cleaned_data['end_date']
                match.end_time = form.cleaned_data['end_time']
                match.save()
                return redirect('person:challenge', slug=slug)
            else:
                questions = models.question.objects.filter(challenge_slug=slug)
                data = {'end_time': match.end_time, 'end_date': match.end_date}
                form1 = forms.extendChallenge(initial=data)
                err = form.errors.as_data()
                err = err['__all__']
                return render(request, 'person/challenge.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'challenge_name': match.name, 'form': form1, 'err': err, 'status': challenge_status, 'rem': rem(slug), 'setters': match2, 'questions': questions, 'user_type': challenge_user_type})




def new_question_view(request, challenge_slug):
    username, type = authenticate(request)
    if username == None:
        return redirect('accounts:login')
    else:
        match = models.challenge.objects.filter(slug=challenge_slug)
        if len(match) == 0:                                                                                  # CONTEST DOES NOT EXIST
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
        else:
            match = match[0]
            challenge_status = status(challenge_slug)
            match1 = models.challenge_setter.objects.filter(slug=challenge_slug, setter=username)                      # USER A SETTER ?
            if len(match1) == 0:
                challenge_user_type = 'user'
            else:
                challenge_user_type = 'setter'

            if type == 'A':
                challenge_user_type = 'admin'

    if request.method == 'GET':

        if challenge_user_type == 'user' or challenge_user_type == 'admin':
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
        elif challenge_user_type == 'setter' and challenge_status == 'M':
            form = forms.newQuestion()
            return render(request, 'person/new_question.html', {'isAdmin': isAdmin(request), 'form': form})
        elif challenge_user_type == 'setter' and (challenge_status == 'A' or challenge_status == 'C'):
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})


    elif request.method == 'POST':

        if challenge_user_type == 'setter' and challenge_status == 'M':

            form = forms.newQuestion(request.POST)
            if form.is_valid():
                new_question = form.save(commit=False)
                new_question.challenge_slug = challenge_slug
                new_question.save()
                form.save_m2m()
                return redirect('person:question', question_slug=form.cleaned_data['slug'])
            else:
                err = form.errors.as_data()
                err = err['__all__']
                return render(request, 'person/new_question.html', {'isAdmin': isAdmin(request), 'form': form, 'err': err})

def question_view(request, question_slug):
    username, type = authenticate(request)
    if username == None:
        return redirect('accounts:login')
    else:
        match = models.question.objects.filter(slug=question_slug)
        if len(match) == 0:                                                                                  # Question DOES NOT EXIST
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
        else:
            match = match[0]
            challenge_slug = match.challenge_slug
            challenge_status = status(challenge_slug)
            match1 = models.challenge_setter.objects.filter(slug=challenge_slug, setter=username)                      # USER A SETTER ?
            match2 = models.challenge.objects.filter(slug=challenge_slug)
            match2 = match2[0]
            challenge_name = match2.name
            if len(match1) == 0:
                challenge_user_type = 'user'
            else:
                challenge_user_type = 'setter'

            if type == 'A':
                challenge_user_type = 'admin'

    if request.method == 'GET':

        if challenge_status == 'M' and (challenge_user_type == 'setter' or challenge_user_type == 'admin'):
            question = match
            initial_values = []
            for item in question.answer:
                if item == 'A' or item == 'B' or item == 'C' or item == 'D':
                    initial_values.append(item)
            form = forms.manageQuestion(instance=question, initial={'answer': initial_values})
            if challenge_user_type == 'admin':
                form = forms.manageQuestionAdmin(instance=question, initial={'answer': initial_values})

            return render(request, 'person/new_question.html', {'isAdmin': isAdmin(request), 'form': form, 'question': question, 'status': challenge_status, 'user_type': challenge_user_type})

        elif challenge_status == 'M' and challenge_user_type == 'user':
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})

        elif challenge_status == 'A':
            problem = match
            curr_submission = models.submission.objects.filter(username=username, question_slug=question_slug)
            if len(curr_submission) == 0:
                form = forms.newSubmission()
            else:
                curr_submission = curr_submission[0]
                initial_values = []
                for choice in curr_submission.answer:
                    if choice == 'A' or choice == 'B' or choice == 'C' or choice == 'D':
                        initial_values.append(choice)
                form = forms.newSubmission(initial={'answer': initial_values})
            return render(request, 'person/question.html', {'isAdmin': isAdmin(request), 'type': challenge_user_type, 'challenge_name': challenge_name, 'form': form, 'problem': problem, 'status': challenge_status, 'challenge_slug': challenge_slug, 'question_slug': question_slug})

        elif challenge_status == 'C':
            problem = match
            form = forms.newSubmission()
            return render(request, 'person/question.html', {'isAdmin': isAdmin(request), 'type': challenge_user_type, 'challenge_name': challenge_name, 'form': form, 'problem': problem, 'status': challenge_status, 'challenge_slug': challenge_slug, 'question_slug': question_slug})

    elif request.method == 'POST':

        if challenge_status == 'M' and challenge_user_type == 'setter':
            form = forms.manageQuestion(request.POST)
            if form.is_valid():
                question = models.question.objects.filter(slug=question_slug)
                question = question[0]
                m_question = form.save(commit=False)
                question.name = m_question.name
                question.points = m_question.points
                question.difficulty = m_question.difficulty
                question.statement = m_question.statement
                question.option1 = m_question.option1
                question.option2 = m_question.option2
                question.option3 = m_question.option3
                question.option4 = m_question.option4
                question.tags = m_question.tags
                question.answer = m_question.answer
                question.challenge_slug = challenge_slug
                question.save()
                return redirect('person:question', question_slug=question_slug)
            else:
                err = form.errors.as_data()
                return render(request, 'person/new_question.html', {'isAdmin': isAdmin(request), 'form': form, 'err': err})

        elif challenge_status == 'A':
            form = forms.newSubmission(request.POST)
            if form.is_valid():
                new_submission = form.save(commit=False)
                curr_submission = models.submission.objects.filter(username=username, question_slug=question_slug)
                problem = match
                answers = []
                for choices in problem.answer:
                    if choices == 'A' or choices == 'B' or choices == 'C' or choices == 'D':
                        answers.append(choices)
                print(answers)
                print(len(curr_submission))
                if len(curr_submission) == 0:
                    new_submission.username = username
                    new_submission.question_slug = question_slug
                    new_submission.challenge = challenge_slug
                    new_submission.save()
                    form.save_m2m()
                    new_score = models.score.objects.filter(username=username, challenge_slug=challenge_slug)
                    if(len(new_score) == 0):
                        new_score = models.score()
                        new_score.username = username
                        new_score.challenge_slug = challenge_slug
                        new_score.score = evaluate(form.cleaned_data['answer'], answers, problem.points)
                    else:
                        new_score = new_score[0]
                        new_score.score += evaluate(form.cleaned_data['answer'], answers, problem.points)
                    new_score.save()
                else:
                    curr_submission = curr_submission[0]
                    curr_answer = []
                    for var in curr_submission.answer:
                        if var == 'A' or var == 'B' or var == 'C' or var == 'D':
                            curr_answer.append(var)

                    curr_points = evaluate(curr_answer, answers, problem.points)
                    print(curr_points)
                    curr_submission.answer = new_submission.answer
                    curr_submission.save()

                    curr_score = models.score.objects.filter(username=username, challenge_slug=challenge_slug)
                    curr_score = curr_score[0]
                    if curr_points == 0:
                        curr_score.score += evaluate(form.cleaned_data['answer'], answers, problem.points)
                    else:
                        curr_score.score -= (problem.points - evaluate(form.cleaned_data['answer'], answers, problem.points))
                    curr_score.save()

                problem = match
                curr_submission = models.submission.objects.filter(username=username, question_slug=question_slug)
                if len(curr_submission) == 0:
                    form = forms.newSubmission()
                else:
                    curr_submission = curr_submission[0]
                    initial_values = []
                    for choice in curr_submission.answer:
                        if choice == 'A' or choice == 'B' or choice == 'C' or choice == 'D':
                            initial_values.append(choice)
                    form = forms.newSubmission(initial={'answer': initial_values})
                return render(request, 'person/question.html', {'isAdmin': isAdmin(request), 'sub_msg': 'Submission Successful' ,'type': challenge_user_type, 'challenge_name': challenge_name, 'form': form, 'problem': problem, 'status': challenge_status, 'challenge_slug': challenge_slug, 'question_slug': question_slug})

        elif challenge_status == 'C' and challenge_user_type == 'user':
            form = forms.newSubmission(request.POST)
            if form.is_valid():
                problem = match
                answers = []
                for choices in problem.answer:
                    if choices == 'A' or choices == 'B' or choices == 'C' or choices == 'D':
                        answers.append(choices)
                if evaluate(form.cleaned_data['answer'], answers, 1) == 1:
                    submit_success = 1
                else:
                    submit_success = 0
                form = forms.newSubmission()
                return render(request, 'person/question.html', {'isAdmin': isAdmin(request), 'submit_success': submit_success, 'type': challenge_user_type, 'challenge_name': challenge_name, 'form': form, 'problem': problem, 'status': challenge_status, 'challenge_slug': challenge_slug, 'question_slug': question_slug})


def collaborator_view(request, challenge_slug):
    username, type = authenticate(request)
    if username == None:
        return redirect('accounts:login')

    if request.method == 'GET':

        return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})

    elif request.method == 'POST':

        form = forms.newCollaborator(request.POST)

        if form.is_valid():
            print(form.cleaned_data['setter'])
            match = models.challenge_setter.objects.filter(slug=challenge_slug, setter=form.cleaned_data['setter'])
            if len(match) == 0:
                new_setter = form.save(commit=False)
                new_setter.slug = challenge_slug
                print(new_setter)
                new_setter.save()
                form.save_m2m()
                return redirect('person:challenge', slug=challenge_slug)
            else:
                return redirect('person:challenge', slug=challenge_slug)
        else:
            return redirect('person:challenge', slug=challenge_slug)


def remove_collaborator_view(request, challenge_slug, collaborator):
    username, type = authenticate(request)
    if username == None:
        return redirect('accounts:login')

    if request.method == 'GET':

        return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})

    elif request.method == 'POST':

        if collaborator != username:
            coll = models.challenge_setter.objects.filter(slug=challenge_slug, setter=collaborator).delete()

        return redirect('person:challenge', slug=challenge_slug)

def leaderboard_view(request, challenge_slug):
    username, type = authenticate(request)
    if username == None:                                                             # USER NOT LOGGED IN
        return redirect('accounts:login')
    else:
        A, B, C = get_challenge()
        match = models.challenge.objects.filter(slug=challenge_slug)                             # CONTEST DOES NOT EXIST
        if len(match) == 0:
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
        else:
            match = match[0]
            challenge_status = status(challenge_slug)
            match1 = models.challenge_setter.objects.filter(slug=challenge_slug, setter=username)    # USER A SETTER ?
            if len(match1) == 0:
                challenge_user_type = 'user'
            else:
                challenge_user_type = 'setter'

    if request.method == 'GET':
        if challenge_status == 'C':
            all_contestants = models.score.objects.filter(challenge_slug=challenge_slug)
            if len(all_contestants) == 0:
                return render(request, 'person/leaderboard.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'challenge_name': match.name, 'user_type': challenge_user_type, 'valid': 0})
            else:
                leader = []
                for i in range(len(all_contestants)):
                    leader.append(all_contestants[i])
                leader.sort(reverse=True, key=comparator)
                rank = 1
                curr_points = leader[0].score
                for i in range(len(leader)):
                    if leader[i].score < curr_points:
                        curr_points = leader[i].score
                        rank = i + 1
                    leader[i].rank = rank
                    subs = models.submission.objects.filter(username=leader[i].username, challenge=challenge_slug)
                    leader[i].attempted = len(subs)
                return render(request, 'person/leaderboard.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'challenge_name': match.name, 'user_type': challenge_user_type, 'valid': 1, 'leader': leader, 'rank': get_rank(username, challenge_slug)})
        else:
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})

def report_view(request, challenge_slug):
    username, type = authenticate(request)
    if username == None:                                                             # USER NOT LOGGED IN
        return redirect('accounts:login')
    else:
        match = models.challenge.objects.filter(slug=challenge_slug)                             # CONTEST DOES NOT EXIST
        if len(match) == 0:
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
        else:
            match = match[0]
            challenge_status = status(challenge_slug)
            match1 = models.challenge_setter.objects.filter(slug=challenge_slug, setter=username)    # USER A SETTER ?
            if len(match1) == 0:
                challenge_user_type = 'user'
            else:
                challenge_user_type = 'setter'

            if type == 'A':
                challenge_user_type = 'admin'

    if request.method == 'GET':

        if challenge_user_type == 'setter' or challenge_user_type == 'admin':
            all_contestants = models.score.objects.filter(challenge_slug=challenge_slug)
            if len(all_contestants) == 0:
                return render(request, 'person/report.html', {'isAdmin': isAdmin(request), 'challenge_name': match.name, 'valid': 0})
            else:
                leader = []
                for i in range(len(all_contestants)):
                    leader.append(all_contestants[i])
                leader.sort(reverse=True, key=comparator)
                rank = 1
                curr_points = leader[0].score
                for i in range(len(leader)):
                    if leader[i].score < curr_points:
                        curr_points = leader[i].score
                        rank = i + 1
                    leader[i].rank = rank
                    subs = models.submission.objects.filter(username=leader[i].username, challenge=challenge_slug)
                    user_detail = account_models.user.objects.filter(username=leader[i].username)
                    leader[i].name = user_detail[0].firstname
                    leader[i].email = user_detail[0].email
                    leader[i].contact = user_detail[0].contactno
                    leader[i].attempted = len(subs)
                return render(request, 'person/report.html', {'isAdmin': isAdmin(request), 'challenge_name': match.name, 'valid': 1, 'leader': leader})
        else:
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})

def editorial_view(request, question_slug):
    username, type = authenticate(request)
    if username == None:
        return redirect('accounts:login')
    else:
        match = models.question.objects.filter(slug=question_slug)
        if len(match) == 0:                                                                                  # Question DOES NOT EXIST
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
        else:
            match = match[0]
            challenge_slug = match.challenge_slug
            challenge_status = status(challenge_slug)
            match1 = models.challenge_setter.objects.filter(slug=challenge_slug, setter=username)                      # USER A SETTER ?
            match2 = models.challenge.objects.filter(slug=challenge_slug)
            match2 = match2[0]
            challenge_name = match2.name
            if len(match1) == 0:
                challenge_user_type = 'user'
            else:
                challenge_user_type = 'setter'

            if type == 'A':
                challenge_user_type = 'admin'

    if request.method == 'GET':
        if status(challenge_slug) == 'C':
            problem = match
            form = forms.newSubmission()
            return render(request, 'person/question.html', {'isAdmin': isAdmin(request), 'editorial': 1, 'type': challenge_user_type, 'challenge_name': challenge_name, 'form': form, 'problem': problem, 'status': challenge_status, 'challenge_slug': challenge_slug, 'question_slug': question_slug})
        else:
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})


def remove_challenge_view(request, challenge_slug):
    username, type = authenticate(request)
    if username == None:                                                             # USER NOT LOGGED IN
        return redirect('accounts:login')
    else:
        match = models.challenge.objects.filter(slug=challenge_slug)                             # CONTEST DOES NOT EXIST
        if len(match) == 0:
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
        else:
            match = match[0]
            challenge_status = status(challenge_slug)
            match1 = models.challenge_setter.objects.filter(slug=challenge_slug, setter=username)    # USER A SETTER ?
            if len(match1) == 0:
                challenge_user_type = 'user'
            else:
                challenge_user_type = 'setter'

            if type == 'A':
                challenge_user_type = 'admin'

    if request.method == 'POST':

        user = account_models.user.objects.filter(username=username)
        user = user[0]
        password = request.POST['oldpassword']
        if check_password(password, user.password) == True:
            models.challenge.objects.filter(slug=challenge_slug).delete()
            models.challenge_setter.objects.filter(slug=challenge_slug).delete()
            models.question.objects.filter(challenge_slug=challenge_slug).delete()
            if challenge_user_type == 'setter':
                return redirect('person:setter')
            elif challenge_user_type == 'admin':
                return redirect('person:admin_mcqts')
        else:
            request.session['username'] = None
            return redirect('accounts:login')


def remove_question_view(request, question_slug):
    username, type = authenticate(request)
    if username == None:
        return redirect('accounts:login')
    else:
        match = models.question.objects.filter(slug=question_slug)
        if len(match) == 0:                                                                                  # Question DOES NOT EXIST
            return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
        else:
            match = match[0]
            challenge_slug = match.challenge_slug
            challenge_status = status(challenge_slug)
            match1 = models.challenge_setter.objects.filter(slug=challenge_slug, setter=username)                      # USER A SETTER ?
            match2 = models.challenge.objects.filter(slug=challenge_slug)
            match2 = match2[0]
            challenge_name = match2.name
            if len(match1) == 0:
                challenge_user_type = 'user'
            else:
                challenge_user_type = 'setter'

            if type == 'A':
                challenge_user_type = 'admin'

    ques = models.question.objects.filter(slug=question_slug)
    if len(ques) != 0 and (challenge_user_type == 'setter' or challenge_user_type == 'admin'):
        ques.delete()
        return redirect('person:challenge', slug=challenge_slug)
    else:
        return redirect('person:setter')

#Parag
def account_view(request, profile_slug):
    if request.method == 'GET':
        if request.session.get('username') != None:
            user_account = account_models.user.objects.filter(username = profile_slug)
            user_account = user_account[0]
            is_setter = 0
            contestset = []
            challenge_status = []
            user_type = user_account.user_type
            if user_type == 'S':
                is_setter = 1
                x = models.challenge_setter.objects.filter(setter = profile_slug)
                print(x)
                for entry in x:
                    y = models.challenge.objects.filter(slug = entry.slug)
                    z = status(entry.slug)
                    y = y[0]
                    y.status = z
                    print(y.name, ' ', y.status)
                    print(y.start_time, ' ', y.start_date)
                    if y not in contestset:
                        contestset.append(y)


            editable = 0
            if request.session.get('username') == profile_slug:
                editable = 1

            contest = []
            contest_flag = 0
            contest_message = "has not yet participated in any of the challenges!"
            subarray = models.score.objects.filter(username = profile_slug)
            for sub in subarray:
                curr = models.challenge.objects.filter(slug = sub.challenge_slug)
                curr = curr[0]
                curr.rank = get_rank(profile_slug, curr.slug)
                contest_flag = 1
                contest.append(curr)


            form  = forms.AccountForm(request.FILES or None, instance = user_account)
            form.fields['username'].widget = dforms.TextInput(attrs={'readonly': ''})
            form.fields['email'].widget = dforms.TextInput(attrs={'readonly': ''})
            form.fields['firstname'].widget = dforms.TextInput(attrs={'readonly': ''})
            form.fields['lastname'].widget = dforms.TextInput(attrs={'readonly': ''})
            form.fields['contactno'].widget = dforms.NumberInput(attrs={'readonly': ''})
            form.fields['bio'].widget = dforms.TextInput(attrs={'readonly': ''})
            sub = models.submission.objects.filter(username = request.session.get('username'))
            return render(request, 'person/user_account.html', {'isAdmin': isAdmin(request), 'contest_message' : contest_message, 'contest_flag' : contest_flag, 'user_account':user_account,'form' : form, 'number' : len(sub), 'editable' : editable, 'is_setter' : is_setter, 'contest' : contest, 'contestset' : contestset, 'profile_slug' : profile_slug})
        else:
            return redirect('accounts:login')
    else:
        print("HERE")

def edit_view(request, profile_slug):
    if request.method == 'GET':
        if request.session.get('username') != None:
            user_account = account_models.user.objects.filter(username = profile_slug)
            user_account = user_account[0]

            if request.session.get('username') != profile_slug:
                return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})

            form  = forms.AccountForm(instance = user_account)
            form1 = forms.ChangePassword()
            form.fields['username'].widget = dforms.TextInput(attrs={'readonly': ''})
            form.fields['email'].widget = dforms.TextInput(attrs={'readonly': ''})
            sub = models.submission.objects.filter(username = request.session.get('username'))
            return render(request, 'person/edit_user_account.html', {'isAdmin': isAdmin(request), 'user_account':user_account, 'form' : form, 'form1' : form1, 'profile_slug' : profile_slug})
        else:
            return redirect('accounts:login')
    elif request.method == 'POST':
        user_account = account_models.user.objects.filter(username = profile_slug)
        user_account = user_account[0]
        form = forms.AccountForm(request.POST, request.FILES or None, instance=user_account)
        if form.is_valid():
            form.save()
            return redirect('person:profile', profile_slug = profile_slug)
        else:
            err = "Contact number is not valid"
            form1 = forms.ChangePassword()
            return render(request, 'person/edit_user_account.html', {'isAdmin': isAdmin(request), 'user_account': user_account, 'form': form, 'form1': form1, 'profile_slug': profile_slug, 'err': err})


def redirecter_view(request):
    if request.method == 'GET':
        if request.session.get('username') != None:
            return redirect('person:profile', profile_slug=request.session.get('username'))
        else:
            return redirect('accounts:login')

def change_password(request, profile_slug):
    if request.method == 'POST':
        user_account = account_models.user.objects.filter(username = profile_slug)
        user_account = user_account[0]
        is_setter = 0
        contestset = []
        challenge_status = []
        user_type = user_account.user_type
        print(user_type)
        if user_type == 'S':
                is_setter = 1
                x = models.challenge_setter.objects.filter(setter = profile_slug)
                for entry in x:
                    y = models.challenge.objects.filter(slug = entry.slug)
                    y[0].status = status(entry.slug)
                    contestset.append(y[0])

        editable = 0
        if request.session.get('username') == profile_slug:
            editable = 1

        contest = []
        subarray = models.submission.objects.filter(username = request.session.get('username'))
        for sub in subarray:
            curr = models.challenge.objects.filter(slug = sub.challenge)
            curr = curr[0]
            if curr not in contest:
                contest.append(curr)


        form  = forms.AccountForm(request.FILES or None, instance = user_account)
        form.fields['username'].widget = dforms.TextInput(attrs={'readonly': ''})
        form.fields['email'].widget = dforms.TextInput(attrs={'readonly': ''})
        form.fields['firstname'].widget = dforms.TextInput(attrs={'readonly': ''})
        form.fields['lastname'].widget = dforms.TextInput(attrs={'readonly': ''})
        form.fields['contactno'].widget = dforms.NumberInput(attrs={'readonly': ''})
        form.fields['bio'].widget = dforms.TextInput(attrs={'readonly': ''})
        sub = models.submission.objects.filter(username = request.session.get('username'))

        form1 = forms.ChangePassword(request.POST)
        #form = forms.AccountForm(request.POST, request.FILES or None, instance=user_account)
        #form1.data['username'] = request.session.get('username')
        if form1.is_valid():
            user_account = account_models.user.objects.filter(username = profile_slug)
            user_account = user_account[0]
            if check_password(form1.cleaned_data['oldpassword'], user_account.password):
                token = get_random_string(length=8)
                user_account.user_token = make_password(token)
                user_account.password = make_password(form1.cleaned_data['password1'])
                user_account.save()
                #form1.save()
            else:
                #print("here")

                err = "Current Password Do Not Match With Your Actual Password"
                return render(request, 'person/edit_user_account.html', {'isAdmin': isAdmin(request), 'user_account':user_account, 'form' : form, 'form1' : form1, 'profile_slug' : profile_slug, 'err': err})

            return render(request, 'person/user_account.html', {'isAdmin': isAdmin(request), 'user_account':user_account,'form' : form, 'number' : len(sub), 'editable' : editable, 'is_setter' : is_setter, 'contest' : contest, 'contestset' : contestset, 'success': 'Password reset successful', 'profile_slug' : profile_slug})
            #return render(request, 'person/edit_user_account.html', {'user_account':user_account, 'form' : form, 'form1' : form1, 'profile_slug' : profile_slug, 'success': 'Password reset successful'})
        else:
            #print("haha")
            err = form1.errors.get_json_data()
            print(err['password2'][0]['message'])
            err = err['password2'][0]['message']
            return render(request, 'person/edit_user_account.html', {'isAdmin': isAdmin(request), 'user_account':user_account, 'form' : form, 'form1' : form1, 'profile_slug' : profile_slug, 'err': err})
    else:
        return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})

def delete_pic(request, profile_slug):
    if request.method == 'GET':
        user_account = account_models.user.objects.filter(username = profile_slug)
        user_account = user_account[0]
        is_setter = 0
        contestset = []
        challenge_status = []
        user_type = user_account.user_type
        print(user_type)
        if user_type == 'S':
            is_setter = 1
            x = models.challenge_setter.objects.filter(setter = profile_slug)
            for entry in x:
                y = models.challenge.objects.filter(slug = entry.slug)
                y[0].status = status(entry.slug)
                contestset.append(y[0])

        editable = 0
        if request.session.get('username') == profile_slug:
            editable = 1

        contest = []
        subarray = models.submission.objects.filter(username = request.session.get('username'))
        for sub in subarray:
            curr = models.challenge.objects.filter(slug = sub.challenge)
            curr = curr[0]
            if curr not in contest:
                contest.append(curr)

        form  = forms.AccountForm(request.FILES or None, instance = user_account)
        form.fields['username'].widget = dforms.TextInput(attrs={'readonly': ''})
        form.fields['email'].widget = dforms.TextInput(attrs={'readonly': ''})
        form.fields['firstname'].widget = dforms.TextInput(attrs={'readonly': ''})
        form.fields['lastname'].widget = dforms.TextInput(attrs={'readonly': ''})
        form.fields['contactno'].widget = dforms.NumberInput(attrs={'readonly': ''})
        form.fields['bio'].widget = dforms.TextInput(attrs={'readonly': ''})
        sub = models.submission.objects.filter(username = request.session.get('username'))

        if user_account.image != None:
            user_account.image = None
        user_account.save()
        return render(request, 'person/user_account.html', {'isAdmin': isAdmin(request), 'user_account':user_account,'form' : form, 'number' : len(sub), 'editable' : editable, 'is_setter' : is_setter, 'contest' : contest, 'contestset' : contestset, 'success': 'Profile Picture Deleted Successfully', 'profile_slug' : profile_slug})

def contest_view(request):
    username, type = authenticate(request)
    if username == None:
        return redirect('accounts:login')

    A, B, C = get_challenge()

    if request.method == 'GET':
        open_challenge = models.challenge.objects.filter(type = 'O')
        ongoing_challenge = []
        upcoming_challenge = []
        archived_challenge = []
        ongoing = False
        upcoming = False
        archived = False
        for i in open_challenge:
            cs = status(i.slug)
            if cs == 'A':
                ongoing = True
                ongoing_challenge.append(i)
            elif cs == 'M':
                upcoming = True
                upcoming_challenge.append(i)
            elif cs == 'C':
                archived = True
                archived_challenge.append(i)

        success1 = "No Ongoing Challenges"
        success2 = "No Upcoming Challenges"
        success3 = "No Challenges held"
        return render(request, 'person/contests.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'success3': success3, 'success1' : success1, 'success2' : success2, 'archived': archived, 'upcoming' : upcoming, 'ongoing' : ongoing, 'ongoing_challenge' : ongoing_challenge, 'upcoming_challenge' : upcoming_challenge, 'archived_challenge': archived_challenge})

#pravin
def practice_view(request):
    username, type = authenticate(request)
    if username == None:
        return redirect('accounts:login')
    else:
        A, B, C = get_challenge()
        if request.method == 'GET':
            completed = []
            questions = models.question.objects.all()
            for i in range(len(questions)):
                if status(questions[i].challenge_slug) == 'C':
                    completed.append(questions[i])
            args = {'isAdmin': isAdmin(request), 'questions':completed, 'A': A, 'B': B, 'C': C}
            return render(request, 'person/practice.html',args)

        else:
            completed = []
            questions = models.question.objects.all()

            if request.method=='POST':
                query1= request.POST.get("search_item")
                query2 = request.POST.get("search_tag")
                query3 = request.POST.get("difficulty")
                #print("aaaaaaaaaaaaaaaaaa",query2)
                questions = questions.filter(name__icontains=query1)
                questions = questions.filter(tags__icontains=query2)
                questions = questions.filter(difficulty__icontains=query3)
                for i in range(len(questions)):
                    if status(questions[i].challenge_slug) == 'C':
                        completed.append(questions[i])
                args = {'isAdmin': isAdmin(request), 'questions':completed, 'A': A, 'B': B, 'C': C}

                return render(request,'person/practice.html',args)

#mradul
def admin_view(request):
    username, type = authenticate(request)
    if username == None:
        return redirect('accounts:login')

    if type != 'A':
        return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})

    A, B, C = get_challenge()

    if request.method == 'GET':
        all_setters = account_models.user.objects.filter(user_type='S')
        setters = []
        for users in all_setters:
            curr = users
            curr.noc = len(models.challenge_setter.objects.filter(setter=curr.username))
            setters.append(curr)
        sr = models.setter_request.objects.all()
        challenges = models.challenge.objects.all()
        upcoming = []
        for challenge in challenges:
            if status(challenge.slug) == 'M':
                upcoming.append(challenge)

        return render(request, 'person/admin.html', {'isAdmin': isAdmin(request), 'A': A, 'B': B, 'C': C, 'user_type': type, 'sr': sr, 'upcoming': upcoming, 'setters': setters})
    else:
        id = request.POST["id"]
        username = request.POST["username"]
        action = request.POST["action"]

        if action == "1":
            user = account_models.user.objects.filter(username=username)
            user = user[0]
            user.user_type = 'S'
            user.save()
            models.setter_request.objects.filter(username=username).delete()
        elif action == "0":
            models.setter_request.objects.filter(username=username).delete()
        return redirect('person:admin_mcqts')

def random_question_view(request):
    username, type = authenticate(request)
    print(type)
    if username == None:
        return redirect('accounts:login')
    if request.method == 'GET':
        upcoming = []
        all_ques = models.question.objects.all()
        for entry in all_ques:
            if status(entry.challenge_slug) == 'C':
                upcoming.append(entry)

        index = random.randint(0, len(upcoming) - 1)
        return redirect('person:question', question_slug=upcoming[index].slug)

def remove_setter_view(request, setter_name):
    if request.method == 'POST':
        user = account_models.user.objects.filter(username=setter_name)
        user = user[0]
        user.user_type = 'U'
        user.save()
        return redirect('person:admin_mcqts')
    else:
        return render(request, 'person/not_found.html', {'isAdmin': isAdmin(request)})
