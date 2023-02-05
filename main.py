from math import factorial

from docxtpl import DocxTemplate
from csv import reader
from utils import ExamClass

from datetime import date

x = date.today()

if x.month > 8:
    academic_year = f"{x.year} - {x.year + 1}"
else:
    academic_year = f"{x.year - 1} - {x.year}"

doc = DocxTemplate("templates/repartition_template.docx")

context = dict(academic_year=academic_year, semestre='premier',
               date=x.strftime('%d/%m/%Y'),
               date_heure=f"{x.strftime('%d/%m/%Y')} 8h00 - 11h00")

base = [tuple(i) for i in reader(open("templates/base_issea.csv", encoding='utf8'))]
base = base[1:]

Amphi_1_G = ExamClass(code_name='Amphi_1_G', nrows=10, ncols=5)
Amphi_1_D = ExamClass(code_name='Amphi_1_D', nrows=10, ncols=5)
ISEL1_G = ExamClass(code_name='ISEL1_G', nrows=5, ncols=3)
ISEL1_D = ExamClass(code_name='ISEL1_D', nrows=5, ncols=3)
ISE2_G = ExamClass(code_name='ISE2_G', nrows=6, ncols=3)
ISE2_D = ExamClass(code_name='ISE2_D', nrows=6, ncols=3)
AS1_G = ExamClass(code_name='AS1_G', nrows=6, ncols=3)
AS1_D = ExamClass(code_name='AS1_D', nrows=5, ncols=3)
ISEL2_G = ExamClass(code_name='ISEL2_G', nrows=3, ncols=3)
ISEL2_D = ExamClass(code_name='ISEL2_D', nrows=3, ncols=3)
Amphi_2_G = ExamClass(code_name='Amphi_2_G', nrows=10, ncols=5)
Amphi_2_D = ExamClass(code_name='Amphi_2_D', nrows=10, ncols=5)

all_classes = [Amphi_1_G, Amphi_1_D, ISEL1_G, ISEL1_D, ISE2_G, ISE2_D,
               AS1_G, AS1_D, ISEL2_G, ISEL2_D, Amphi_2_G, Amphi_2_D]

for ec in all_classes[:-2]:
    ec.attributes_places(base)
    ec.print_names(context)

doc.render(context)
doc.save("generated_doc.docx")
