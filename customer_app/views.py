from django.shortcuts import render
from datetime import date, timedelta
from django.db.models import Count
from .models import Customer, Interaction

# Landing page: list all customers
def index(request):
    customers = Customer.objects.all()
    return render(request, "index.html", {"customers": customers})

# Create a new customer
def create_customer(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        social_media = request.POST.get("social_media", "")
        Customer.objects.create(
            name=name, email=email, phone=phone, address=address, social_media=social_media
        )
        return render(request, "add.html", {"msg": "Successfully Saved a Customer"})
    return render(request, "add.html")

# Record an interaction
def interact(request, cid):
    channels = Interaction.CHANNEL_CHOICES
    directions = Interaction.DIRECTION_CHOICES
    context = {"channels": channels, "directions": directions}
    if request.method == "POST":
        customer = Customer.objects.get(id=cid)
        channel = request.POST["channel"]
        direction = request.POST["direction"]
        summary = request.POST["summary"]
        Interaction.objects.create(
            customer=customer,
            channel=channel,
            direction=direction,
            summary=summary
        )
        context["msg"] = "Interaction Success"
    return render(request, "interact.html", context)

# Show interactions in last 30 days
def summary(request):
    thirty_days_ago = date.today() - timedelta(days=30)
    interactions = Interaction.objects.filter(interaction_date__gte=thirty_days_ago)
    count = interactions.count()
    interactions = interactions.values("channel", "direction").annotate(count=Count('channel'))
    return render(request, "summary.html", {"interactions": interactions, "count": count})

def submit(request):
    # Placeholder for submission logic
    return render(request, "submit.html")

def show_exam_result(request):
    # Placeholder for exam result logic
    return render(request, "exam_result.html")
