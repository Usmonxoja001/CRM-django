import os
import django
import random
from django.utils import timezone

# 1. Django sozlamalarini ulash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm_project.settings")
django.setup()

# 2. Model va foydalanuvchilarni import qilish
from contacts.models import Contact
from leads.models import Lead
from deals.models import Deal
from tasks.models import Tasks
from django.contrib.auth.models import User

# 3. Superuserni olish
user = User.objects.filter(is_superuser=True).first()
if not user:
    raise Exception("Superuser topilmadi. Avval createsuperuser qiling!")

# 4. Tasodifiy ma’lumotlar
first_names = ["Ali", "Vali", "Hasan", "Husan", "Bobur"] * 6
last_names = ["Karimov", "Toshpulatov", "Xasanov", "Norqulov", "Akramov"] * 6
companies = ["Nuron IT", "Mega Soft", "TechnoHub", "PDP", "Inha"] * 6
positions = ["Manager", "Developer", "Analyst", "Designer", "Intern"]
addresses = ["Toshkent", "Samarqand", "Buxoro", "Farg‘ona", "Namangan"]
lead_titles = [f"Lead #{i+1}" for i in range(30)]
lead_desc = ["Yirik loyiha", "Aloqa o‘rnatildi", "Kutilmoqda", "Tavsiya asosida", "Sinov bosqichi"]

def clean_phone(phone):
    return phone.replace(" ", "").replace("-", "")

contacts, leads, deals, tasks = [], [], [], []

# 5. Ma’lumotlarni yaratish
for i in range(30):
    first = first_names[i]
    last = last_names[i]
    company = companies[i]
    position = random.choice(positions)
    address = random.choice(addresses)
    email = f"{first.lower()}.{last.lower()}@{company.lower().replace(' ', '')}.uz"
    phone = clean_phone(f"+998{random.randint(900000000, 999999999)}")

    contact = Contact.objects.create(
        first_name=first,
        last_name=last,
        email=email,
        phone=phone,
        company=company,
        position=position,
        address=address,
        source=random.choice(['website', 'referral', 'social_media', 'email', 'other']),
        notes=random.choice([
            "Eng yirik mijoz", "Potensial yangi mijoz",
            "Hamkorlik bo‘yicha muzokara", "Doimiy buyurtmachi", ""
        ]),
        assigned_to=user,
        created_by=user
    )
    contacts.append(contact)

    lead = Lead.objects.create(
        contact=contact,
        title=lead_titles[i],
        status=random.choice(['new', 'contacted', 'qualified', 'unqualified', 'converted']),
        priority=random.choice(['low', 'medium', 'high']),
        description=random.choice(lead_desc),
        estimated_value=random.randint(5000, 90000),
        assigned_to=user,
        created_by=user
    )
    leads.append(lead)

    deal = Deal.objects.create(
        title=f"{lead_titles[i]} bitimi",
        contact=contact,
        lead=lead,
        stage=random.choice(['discovery', 'proposal', 'negotiation', 'closed_won', 'closed_lost']),
        amount=random.randint(4000, 80000),
        expected_close_date=timezone.now().date() + timezone.timedelta(days=random.randint(5, 60)),
        probability=random.choice([40, 50, 60, 70, 80, 90]),
        description=lead_desc[i % len(lead_desc)],
        assigned_to=user,
        created_by=user
    )
    deals.append(deal)

    task = Task.objects.create(
        title=f"{lead_titles[i]} vazifasi",
        description=f"{lead_titles[i]} uchun vazifa bajarilishi kerak.",
        status=random.choice(['not_started', 'in_progress', 'completed', 'deferred']),
        priority=random.choice(['low', 'medium', 'high']),
        due_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
        contact=contact,
        lead=lead,
        deal=deal,
        assigned_to=user,
        created_by=user
    )
    tasks.append(task)

# 6. Natija
print("✅ Bazaga 30 ta contact, lead, deal va task muvaffaqiyatli qo'shildi!")
