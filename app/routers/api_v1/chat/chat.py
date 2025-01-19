from fastapi import APIRouter, Path, Body, Depends
from app.gemini import TextGeneration
from app.routers.api_v1.chat.models import ChatMessage, TextMessages
from typing import Annotated
from app.dependencies import DbConnection
from fastapi.background import BackgroundTasks


chat_router = APIRouter()

def get_pet_info(pet_id, collections: Annotated[DbConnection, Depends()]):
    pet_info = collections.petsCollection.find_one({'_id': pet_id})
    daily_info = collections.trackingCollection.find({'pet_id': pet_id}).to_list()[:7]
    return {
        "pet_info": pet_info,
        "daily_info": daily_info
    }



@chat_router.post('/')
async def chat_start(chatMessage: Annotated[ChatMessage, Body()], pet_info: Annotated[get_pet_info, Depends()]):
    """
        Description
        Create a New Chat & responds with Chat Response & chatId

        Request Body

            - message: User Message
    """
    print(pet_info)
    t = TextGeneration(instruction=pet_info, model=3)
    return t.start_chat(chatMessage.message)

@chat_router.post('/{chat_id}')
async def continue_chat(chat_id: Annotated[str, Path()], chatMessage: Annotated[ChatMessage, Body()]):
    """
        Description
        Resume the Existing Chat & Responds according to previous Chat

        Path Parameter

            - chatId: Chat Id which was received after Starting the Chat

        Request Body

            - message: User Message
    """
    t = TextGeneration()
    return t.continue_chat(chatId=chat_id, user_message=chatMessage.message)

# @chat_router.post('/text')
# async def text_generation(textMessage: Annotated[TextMessages, Body()]):
#     t = TextGeneration()
#     return t.generate_text(textMessage.message)

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from typing import Annotated
import tempfile
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import matplotlib.pyplot as plt
import io
import numpy as np

def create_trend_graph(dates, values, title, ylabel):
    """Create a graph for trend analysis"""
    plt.figure(figsize=(8, 4))
    plt.plot(dates, values, marker='o')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot to memory
    img_data = io.BytesIO()
    plt.savefig(img_data, format='png', dpi=300)
    img_data.seek(0)
    plt.close()

    # Convert to ReportLab Image
    img = Image(img_data, width=6 * inch, height=3 * inch)
    return img


def create_detailed_pet_report(data, output_filename="detailed_pet_health_report.pdf"):
    """Generate a detailed PDF report for veterinary review based on pet health data"""

    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12
    )

    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8
    )

    # Title Page
    elements.append(Paragraph("Comprehensive Veterinary Health Report", title_style))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    elements.append(PageBreak())

    # Pet Information Section
    elements.append(Paragraph("1. Pet Information", heading_style))

    pet_info = data['pet_info']
    current_age = datetime.now().year - datetime.strptime(pet_info['dob'], '%Y-%m-%d %H:%M:%S').year

    pet_details = [
        ["Name:", pet_info['name']],
        ["Breed:", pet_info['breed']],
        ["Date of Birth:", datetime.strptime(pet_info['dob'], '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y')],
        ["Age:", f"{current_age} years"],
        ["Weight:", f"{pet_info['weight']} kg"],
        ["Gender:", "Male" if pet_info['gender'] == 'M' else "Female"],
        ["Neutered/Spayed:", "No" if not pet_info['reproduction'] else "Yes"],
        ["Pregnancy Status:", "Yes" if pet_info['pregnancy'] else "No"]
    ]

    pet_table = Table(pet_details, colWidths=[2 * inch, 4 * inch])
    pet_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(pet_table)
    elements.append(Spacer(1, 20))

    # Medical History Section
    elements.append(Paragraph("2. Medical History", heading_style))

    # Allergies
    elements.append(Paragraph("2.1 Allergies", subheading_style))
    if pet_info['allergies']:
        allergy_data = [[
            "Allergy",
            "Date Identified",
            "Duration"
        ]]
        for allergy in pet_info['allergies']:
            allergy_date = datetime.strptime(allergy['date'], '%Y-%m-%d %H:%M:%S')
            duration = (datetime.now() - allergy_date).days
            allergy_data.append([
                allergy['name'],
                allergy_date.strftime('%B %d, %Y'),
                f"{duration} days"
            ])
        allergy_table = Table(allergy_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
        allergy_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(allergy_table)
    else:
        elements.append(Paragraph("No known allergies", styles['Normal']))
    elements.append(Spacer(1, 15))

    # Vaccinations
    elements.append(Paragraph("2.2 Vaccination History", subheading_style))
    if pet_info['vaccine']:
        vaccine_data = [["Vaccine", "Date Administered", "Age at Administration"]]
        for vaccine in pet_info['vaccine']:
            vaccine_date = datetime.strptime(vaccine['date'], '%Y-%m-%d %H:%M:%S')
            birth_date = datetime.strptime(pet_info['dob'], '%Y-%m-%d %H:%M:%S')
            age_at_vaccine = (vaccine_date - birth_date).days // 365
            vaccine_data.append([
                vaccine['name'],
                vaccine_date.strftime('%B %d, %Y'),
                f"{age_at_vaccine} years"
            ])
        vaccine_table = Table(vaccine_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
        vaccine_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(vaccine_table)
    else:
        elements.append(Paragraph("No vaccination records found", styles['Normal']))

    elements.append(PageBreak())

    # Daily Health Monitoring
    elements.append(Paragraph("3. Daily Health Monitoring", heading_style))

    # Prepare data for graphs
    dates = [datetime.strptime(day['datentime'], '%Y-%m-%d %H:%M:%S').strftime('%m/%d')
             for day in data['daily_info']]

    # Weight trend
    elements.append(Paragraph("3.1 Weight Trend Analysis", subheading_style))
    weights = [day['weight'] for day in data['daily_info']]
    weight_img = create_trend_graph(dates, weights, 'Weight Trend', 'Weight (kg)')
    elements.append(weight_img)
    elements.append(Spacer(1, 15))

    # Temperature trend
    elements.append(Paragraph("3.2 Temperature Trend Analysis", subheading_style))
    temps = [day['temperature'] for day in data['daily_info']]
    temp_img = create_trend_graph(dates, temps, 'Temperature Trend', 'Temperature (°C)')
    elements.append(temp_img)
    elements.append(Spacer(1, 15))

    # Daily records table
    elements.append(Paragraph("3.3 Daily Health Records", subheading_style))
    daily_headers = [
        "Date",
        "Weight\n(kg)",
        "Temp\n(°C)",
        "Water\n(L)",
        "Walking\n(hrs)",
        "Sleep\n(hrs)",
        "Mood\n(1-5)",
        "Behavior"
    ]

    daily_data = [[
        datetime.strptime(day['datentime'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),
        f"{day['weight']:.1f}",
        f"{day['temperature']:.1f}",
        f"{day['water_intake']:.1f}",
        f"{day['walking']:.1f}" if day['walking'] is not None else "N/A",
        f"{day['sleep_time']:.1f}",
        str(day['mood_indicator']),
        day['behavior']
    ] for day in data['daily_info']]

    daily_table = Table([daily_headers] + daily_data, colWidths=[0.9 * inch, 0.7 * inch, 0.7 * inch,
                                                                 0.7 * inch, 0.7 * inch, 0.7 * inch,
                                                                 0.7 * inch, 2 * inch])
    daily_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (-1, 1), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    elements.append(daily_table)

    # Detailed Notes Section
    elements.append(PageBreak())
    elements.append(Paragraph("4. Daily Observation Notes", heading_style))
    for day in data['daily_info']:
        date_str = datetime.strptime(day['datentime'], '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y')
        elements.append(Paragraph(f"Date: {date_str}", subheading_style))

        diet_info = day['diet'][0] if day['diet'] else {'food': 'No food recorded', 'amount': 0, 'notes': 'No notes'}
        notes_data = [
            ["Behavior:", day['behavior']],
            ["Food Type:", diet_info['food']],
            ["Food Amount:", f"{diet_info['amount']}g"],
            ["Diet Notes:", diet_info['notes']],
            ["General Notes:", day['notes']]
        ]

        notes_table = Table(notes_data, colWidths=[1.5 * inch, 4.5 * inch])
        notes_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ]))
        elements.append(notes_table)
        elements.append(Spacer(1, 15))

    # Build PDF
    doc.build(elements)
@chat_router.get('/report')
async def get_report(pet_data: Annotated[dict, Depends(get_pet_info)]):
    """
    Generate and return a PDF report for a pet.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        temp_path = tmp_file.name
    create_detailed_pet_report(pet_data, temp_path)
    return FileResponse(
        path=temp_path,
        filename='detailed_pet_health_report.pdf',
        media_type='application/pdf',
    )
