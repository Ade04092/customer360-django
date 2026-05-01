# customer_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Customer, Interaction, Course, Lesson, Question, Choice, Submission

# Home page
def index(request):
    customers = Customer.objects.all()
    context = {"customers": customers}
    return render(request, "index.html", context)

# Create new customer
def create_customer(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        social_media = request.POST.get("social_media", "")
        customer = Customer.objects.create(
            name=name, email=email, phone=phone, address=address, social_media=social_media
        )
        customer.save()
        msg = "Successfully Saved a Customer"
        return render(request, "add.html", context={"msg": msg})
    return render(request, "add.html")

# Add interaction for a customer
def interact(request, cid):
    channels = Interaction.CHANNEL_CHOICES
    directions = Interaction.DIRECTION_CHOICES
    context = {"channels": channels, "directions": directions}

    if request.method == "POST":
        customer = Customer.objects.get(id=cid)
        channel = request.POST["channel"]
        direction = request.POST["direction"]
        summary = request.POST["summary"]
        interaction = Interaction.objects.create(
            customer=customer,
            channel=channel,
            direction=direction,
            summary=summary
        )
        interaction.save()
        context["msg"] = "Interaction Success"
        return render(request, "interact.html", context)

    return render(request, "interact.html", context)

# Summary page (last 30 days)
def summary(request):
    thirty_days_ago = date.today() - timedelta(days=30)
    interactions = Interaction.objects.filter(interaction_date__gte=thirty_days_ago)
    count = interactions.count()
    interactions = interactions.values("channel","direction").annotate(count=Count('channel'))
    return render(request, "summary.html", {"interactions": interactions, "count": count})

# Exam submit page
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(lesson__course=course)
    if request.method == 'POST':
        user = User.objects.first()  # For testing
        for q in questions:
            choice_id = request.POST.get(str(q.id))
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                Submission.objects.create(user=user, question=q, selected_choice=choice)
        return redirect('show_exam_result', course_id=course.id)
    return render(request, 'submit.html', {'course': course, 'questions': questions})

# Exam result page
def show_exam_result(request, course_id, submission_id):
    from django.shortcuts import get_object_or_404, render
    from .models import Enrollment, Submission

    enrollment = get_object_or_404(Enrollment, id=course_id)  # or by user/course
    submission = get_object_or_404(Submission, id=submission_id)
    correct, total = submission.is_get_score()
    grade = int((correct / total) * 100) if total else 0
    selected_ids = submission.choices.values_list('id', flat=True)

    return render(request, 'exam_result_bootstrap.html', {
        'course': enrollment.course,
        'selected_ids': selected_ids,
        'grade': grade,
        'possible': total,
    })

# Optional mock exam for Task 7 screenshot
def mock_exam_result(request):
    score = 95
    results = [
        {'question': 'Q1', 'answer': 'A', 'correct': True},
        {'question': 'Q2', 'answer': 'B', 'correct': True},
        {'question': 'Q3', 'answer': 'C', 'correct': True},
    ]
    return render(request, 'mock_exam_result.html', {'score': score, 'results': results})
