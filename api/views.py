from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from .models import CustomUser, DailyCalories
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CalorieRecordSerializer
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from django.http import HttpResponse , FileResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.utils import ImageReader
import csv


class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self , request, *args , **kwargs) :
        user = CustomUser.objects._create_user(
            username = request.data.get("username"),
            password = request.data.get("password"),
            email = request.data.get("email"),
            height = request.data.get("height"),
            weight = request.data.get("weight"),
            age = int(request.data.get("age")),
            gender = request.data.get("gender"),
            activity_factor = request.data.get("activity")
        )
        user.save()
        return Response({
            "success" :"Now login"
        })

class DailyCaloriesTrack(APIView) :
    permission_classes = [IsAuthenticated]
    def post(self , request , *args , **kwargs) :
        userid = request.user.id
        user = CustomUser.objects.get(id = userid)
        daily = DailyCalories.objects.create(user = user ,date = request.data.get("date"), consumed_calories = request.data.get("calories"))
        daily.save()
        return Response({
            "calories for today saved":"success"
        })

class CalorieRecord(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request , *args , **kwargs) :
        user_id = request.user.id
        objs = DailyCalories.objects.filter(user = CustomUser.objects.get(id = user_id))
        serializer = CalorieRecordSerializer(objs , many = True)
        return Response(serializer.data)

class GenerateReport(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)

        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        calories_goal = int(user.calories)
        objs = DailyCalories.objects.filter(user=user)

        if not objs:
            return Response({"error": "No data for this user to generate report"})


        drawing = self.plt_to_canvas([o.date for o in objs], [o.consumed_calories for o in objs], calories_goal , request.user)


        pdf.setPageSize((letter[0], letter[1]))
        pdf.drawImage(drawing, x=50, y=500, width=400, height=300)


        table_data = [["Date", "Consumed Calories"]]
        for obj in objs:
            table_data.append([str(obj.date), str(obj.consumed_calories)])

        table = Table(table_data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), 'grey'),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), 'white'),
                                   ('GRID', (0, 0), (-1, -1), 1, 'grey')]))


        table.wrapOn(pdf, 8000, 5000)
        table.drawOn(pdf, x=200, y=200)

        pdf.showPage()
        pdf.save()
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type='application/pdf')

    def plt_to_canvas(self, x_data, y_data, calories_goal, username):
        plt.figure()
        plt.plot(x_data, y_data)
        plt.axhline(y=calories_goal, color='r', linestyle='--', label='Calories Goal')
        plt.xlabel("Date")
        plt.ylabel("Consumed Calories")
        plt.title(f"Daily calories report of {username}")

        imgdata = io.BytesIO()
        plt.savefig(imgdata, format='png', bbox_inches='tight', pad_inches=0.2)
        plt.close()

        return ImageReader(imgdata)

class GenerateCSVReport(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request , *args , **kwargs) :
        user_id = request.user.id
        objs = DailyCalories.objects.filter(user = CustomUser.objects.get(id = user_id))
        fields = ["Date" , "Calories Consumed"]
        data = []
        for o in objs:
            date_string = o.date.strftime("%d-%m-%Y")
            temp = [date_string , o.consumed_calories]
            data.append(temp)
        print(data)
        with open("output.csv", "w") as file :
            csvwriter = csv.writer(file)
            csvwriter.writerow(fields)
            csvwriter.writerows(data)
        response = FileResponse(open("output.csv", 'rb'))
        response['Content-Disposition'] = f'attachment; filename="output.csv"'
        return response
