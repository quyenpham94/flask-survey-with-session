from flask import Flask, render_template, redirect, request, flash, session
from surveys import satisfaction_survey as survey


app = Flask(__name__)

# key name is used to store something in the session
# put here as constants so we're guaranteed to be consistent in our spelling of these
RESPONSES_KEY="responses"

app.config['SECRET_KEY'] = "never-tell"

@app.route('/home')
def home_page():
    responses = []
    return render_template('home_page.html')

@app.route('/')
def survey_page():
    
    return render_template('survey_page.html', survey=survey)

@app.route('/start', methods=["POST"])
def start_survey():

    session[RESPONSES_KEY]=[]

    return redirect('/questions/0')


@app.route('/questions/<int:number>')
def question_page(number):

    responses = session.get(RESPONSES_KEY)

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    if (len(responses) is None):
        return redirect('/')
    if (len(responses) != number):
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[number]
    return render_template("question.html", question_num=number, question=question)

@app.route('/answer', methods=["POST"])
def answer_page():
    # responses = []

    # get the choice from customer
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY]=responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    if (len(responses) != len(survey.questions)):
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def complete():
    return render_template('complete.html')
