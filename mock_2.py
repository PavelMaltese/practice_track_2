import pandas as pd
import numpy as np
import random

n_students = 5000
subjects = ['Math', 'Physics', 'Programming', 'English']

data = []

def generate_student_type():
    r = random.random()
    if r < 0.05:
        return "top"
    elif r < 0.20:
        return "good"
    elif r < 0.75:
        return "average"
    else:
        return "weak"

def grade_by_type(student_type):
    if student_type == "top":
        return 'A'
    elif student_type == "good":
        return random.choices(['A','B','C'], [0.6,0.3,0.1])[0]
    elif student_type == "average":
        return random.choices(['A','B','C','D','E','F'],
                              [0.1,0.3,0.3,0.15,0.1,0.05])[0]
    else:
        return random.choices(['C','D','E','F'],
                              [0.2,0.3,0.3,0.2])[0]

def attendance_by_type(student_type):
    if student_type == "top":
        return np.random.normal(90, 7)
    elif student_type == "good":
        return np.random.normal(82, 13)
    elif student_type == "average":
        return np.random.normal(70, 15)
    else:
        return np.random.normal(50, 20)

def ontime_by_type(student_type):
    if student_type == "top":
        return np.random.normal(95, 7)
    elif student_type == "good":
        return np.random.normal(85, 13)
    elif student_type == "average":
        return np.random.normal(70, 15)
    else:
        return np.random.normal(50, 20)


for student_id in range(1, n_students + 1):

    student_type = generate_student_type()


    gender = random.choices(['M', 'F'], [0.67, 0.33])[0]

    base_age = random.choice([18, 19])
    if random.random() < 0.1:
        base_age += random.randint(1, 3)

    expelled = False

    for sem_index in range(1, 9):

        if expelled:
            break

        course = (sem_index - 1) // 2 + 1

        year = 2023 + (sem_index - 1) // 2
        semester = 1 if sem_index % 2 == 1 else 2
        semester_name = f"{year}_{semester}"

        age = base_age + (sem_index - 1) // 2


        base_attendance = attendance_by_type(student_type)
        base_ontime = ontime_by_type(student_type)


        if gender == 'F':
            base_attendance *= 1.2
            base_ontime *= 1.2

        base_attendance = max(0, min(100, base_attendance))
        base_ontime = max(0, min(100, base_ontime))

        retakes_total = 0
        expelled_this_semester = False

        for subject in subjects:

            expelled_now = 0


            attendance = np.clip(np.random.normal(base_attendance, 5), 0, 100)
            ontime = np.clip(np.random.normal(base_ontime, 7), 0, 100)

            exam_grade = grade_by_type(student_type)

            retake_grade = None
            commission_grade = None

            if exam_grade == 'F':
                retakes_total += 1

                if student_type == "top":
                    retake_grade = 'B'
                elif student_type == "good":
                    retake_grade = random.choice(['A','B','C'])
                elif student_type == "average":
                    retake_grade = random.choice(['B','C','D','F'])
                else:
                    retake_grade = random.choice(['C','D','F'])

                if retake_grade == 'F':
                    if student_type in ["top", "good"]:
                        commission_grade = random.choice(['C','D'])
                    elif student_type == "average":
                        commission_grade = random.choice(['C','D','F'])
                    else:
                        commission_grade = random.choice(['D','F'])

                    if commission_grade == 'F':
                        expelled_this_semester = True
                        expelled_now = 1

            data.append({
                'student_id': student_id,
                'gender': gender,
                'course': course,
                'age': age,
                'semester': semester_name,
                'subject': subject,
                'exam_grade': exam_grade,
                'retake_grade': retake_grade,
                'commission_grade': commission_grade,
                'attendance_percent': round(attendance, 1),
                'assignments_on_time_percent': round(ontime, 1),
                'retakes_count_semester': retakes_total,
                'expelled': expelled_now,
                'student_type': student_type
            })

        if expelled_this_semester:
            expelled = True


df = pd.DataFrame(data)
df.to_excel("student_dataset_realistic_2.xlsx", index=False)

print("Готово: student_dataset_realistic.xlsx")