from django.test import TestCase
import datetime
from django.utils import timezone 
from django.urls import reverse

# Create your tests here.


from .models import Question
class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_recently_published() returns False with future pub_date
        """
        time= timezone.now() + datetime.timedelta(days=30)
        future_question= Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time= timezone.now() + datetime.timedelta(days=1, seconds=1)
        old_question= Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recently_question(self):
        """
        was_recently_published() returns False with pub_date  within last day
        """
        time= timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question= Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    create a question wit the given 'question_text' and publish the 
    given number of 'days' offset to now (negative for question published 
    in the past, positive for question yet to be published),
    """
    time=timezone.now() + datetime.timezone(days=days)
    return Question.objects.create(question_text=question_test, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        if no question exists, appropriate message displayed
        """
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
        def test_past_question(self):
            """
            Question with a pub_date in the past are displayed on the index page.
            """
            question=create_question(question_test="past question.", days=-30)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(response.context['latest_question_list'],[question],)
        def test_future_question(self):
            """
            Question with a future pub_date ain't displayed
            """
            question=create_question(question_text='future question', days=30)
            response=self.client.get(reverse('polls:index'))
            self.assertContains(response, "no polls are available.") 
            self.assertquerysetEqual(response.context['latest_question_list'], [])
        def test_future_question_and_past_question(self):
            """
            Even if both past and future questions exist, only past questions                                                                                                  
            """
            question=create_question(question_text="past questiion.",days=-30)
            create_question(question_text="future question.", days=30)
            response=self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(response.context["latest_question_list"], [question],)
def test_two_past_questions(self):
    """
    the question index page may display multiple questions.
    """
    question1=create_question(question_text="past question 1.", days=-30)
    question2=create_question(question_text="past question 2.", days=-5)
    response=self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1])
class DetailViewTests(TestCase):
    def test_future_question(self):
        """
        the detail view of a question with a pub_date in the future returns 404
        """
        future_question = create_question(question_text='future questiom', days=5)
        url=reverse('polls:detail', args=(future_question.id,))
        response=self.client.get(url)
        self.assertEqual(response.status_code, 404)
    def test_past_question(self):
        """
        the detail view of a question with past pub_date displays question's text
        """
        past_question=create_question(question_text="past question", days=-5)
        url = reverse('polls:detail', args=(past_question.id))
        response = self.client.get(url)
        self.assertcontain(response, past_question.question_text)
        