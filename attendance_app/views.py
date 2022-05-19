from django.http import Http404, JsonResponse
from django.shortcuts import render, render_to_response, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models import Count
from .models import Stream, Subject, Semester, Student, Attendance, StudentAttendance

def index(request):
    if request.user.is_authenticated() == False:
        return redirect('login')
    context = {}
    return render(request, 'index.html', {})

def dashboard(request):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}
    context['total_students'] = Student.objects.count()

    return render(request, 'dashboard.html', context)

def manage_stream(request, action=None, stream_id=None):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}

    if stream_id is not None:
        stream = get_object_or_404(Stream, pk=stream_id)
        context['stream'] = stream

    if action == "view":
        context['readonly'] = 1

    elif action == "delete":
        stream.delete()
        request.session['message'] = 'Record delete successfully.'
        return redirect('manage_stream')

    if request.method == 'POST':
        if action == "edit":
            stream = Stream.objects.get(pk=stream_id)
            request.session['message'] = 'Record update successfully.'
        else:
            stream = Stream()
            request.session['message'] = 'Record save successfully.'

        stream.name = request.POST['txtStreamName']
        stream.save()
        return redirect('manage_stream')

    all_stream = Stream.objects.all()
    context['all_stream'] = all_stream
    return render(request, 'manage_stream.html', context)

def manage_semester(request, action=None, semester_id=None):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}

    if semester_id is not None:
        semester = get_object_or_404(Semester, pk=semester_id)
        context['semester'] = semester

    if action == "view":
        context['readonly'] = 1

    elif action == "delete":
        semester.delete()
        request.session['message'] = 'Record delete successfully.'
        return redirect('manage_semester')

    if request.method == 'POST':
        if action == "edit":
            semester = Semester.objects.get(pk=semester_id)
            request.session['message'] = 'Record update successfully.'
        else:
            semester = Semester()
            request.session['message'] = 'Record save successfully.'

        semester.stream = Stream.objects.get(pk=request.POST['cmbStreamId'])
        semester.name = request.POST['txtSemesterName']
        semester.save()
        return redirect('manage_semester')

    all_stream = Stream.objects.all()
    context['all_stream'] = all_stream

    all_semester = Semester.objects.all()
    context['all_semester'] = all_semester
    return render(request, 'manage_semester.html', context)

def manage_subject(request, action=None, subject_id=None):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}

    if subject_id is not None:
        subject = Subject.objects.get(pk=subject_id)
        all_semester = Semester.objects.all()
        context['subject'] = subject
        context['all_semester'] = all_semester

    if action == "view":
        context['readonly'] = 1

    elif action == "delete":
        subject.delete()
        request.session['message'] = 'Record delete successfully.'
        return redirect('manage_subject')

    if request.method == 'POST':
        if action == "edit":
            subject = Subject.objects.get(pk=subject_id)
            request.session['message'] = 'Record update successfully.'
        else:
            subject = Subject()
            request.session['message'] = 'Record save successfully.'

        subject.stream = Stream.objects.get(pk=request.POST['cmbStreamId'])
        subject.semester = Semester.objects.get(pk=request.POST['cmbSemesterId'])
        subject.name = request.POST['txtSubjectName']
        subject.save()
        return redirect('manage_subject')

    all_stream = Stream.objects.all()
    context['all_stream'] = all_stream

    all_subject = Subject.objects.all()
    context['all_subject'] = all_subject
    return render(request, 'manage_subject.html', context)

def ajax_get_semesters(request):
    stream_id = request.POST['stream_id'];
    stream = Stream.objects.get(pk=stream_id)
    semesters = Semester.objects.filter(stream=stream)
    str_option = ""
    str_option = "<option value="">Select Semester</option>"
    for semester in semesters:
        str_option += "<option value='" + str(semester.pk) + "'>" + semester.name + "</option>"
    return HttpResponse(str_option)

def ajax_get_subjects(request):
    semester_id = request.POST['semester_id'];
    semester = Semester.objects.get(pk=semester_id)
    subjects = Subject.objects.filter(semester=semester)
    str_option = ""
    str_option = "<option value="">Select Subject</option>"
    for subject in subjects:
        str_option += "<option value='" + str(subject.pk) + "'>" + subject.name + "</option>"
    return HttpResponse(str_option)

def ajax_get_students(request):
    semester_id = request.POST['semester_id'];
    semester = Semester.objects.get(pk=semester_id)
    students = Student.objects.filter(semester=semester)
    str_option = ''
    for student in students:
        str_option += '<div class="input-group">'
        str_option += '<span class="input-group-addon"><input type="checkbox" name="chkStudentId[]" class="minimal chk-student" value="' + str(student.pk) + '"></span>'
        str_option += '<P class="form-control text-capitalize">' + student.firstname + ' ' + student.middlename + ' ' + student.lastname + '</P>'
        str_option += '</div>'

    return HttpResponse(str_option)

def manage_student(request, action=None, student_id=None):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}

    if student_id is not None:
        student = Student.objects.get(pk=student_id)
        context['student'] = student
        all_semester = Semester.objects.all()
        context['all_semester'] = all_semester

    if action == "view":
        context['readonly'] = 1

    elif action == "delete":
        student.delete()
        request.session['message'] = 'Record delete successfully.'
        return redirect('manage_student')

    if request.method == 'POST':
        if action == "edit":
            student = Student.objects.get(pk=student_id)
            request.session['message'] = 'Record update successfully.'
        else:
            student = Student()
            request.session['message'] = 'Record save successfully.'

        student.firstname = request.POST['txtFirstName']
        student.middlename = request.POST['txtMiddleName']
        student.lastname = request.POST['txtLastName']
        student.address = request.POST['txtAddress']
        student.phone = request.POST['txtPhone']
        student.mobile = request.POST['txtMobile']
        student.semester = Semester.objects.get(pk=request.POST['cmbSemesterId'])
        student.enrollment_no = request.POST['txtEnrollmentNo']
        student.status = True if request.POST['rdoStatus'] == "1" else False
        student.save()
        # return redirect('manage_student')

    all_stream = Stream.objects.all()
    context['all_stream'] = all_stream

    all_student = Student.objects.all()
    context['all_student'] = all_student
    return render(request, 'manage_student.html', context)

def manage_attendance(request, action=None, attendance_id=None):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}

    if attendance_id is not None:
        attendance = Attendance.objects.get(pk=attendance_id)
        context['attendance'] = attendance
        all_student_attendance = StudentAttendance.objects.filter(attendance=attendance)
        context['all_student_attendance'] = all_student_attendance
        all_semester = Semester.objects.all()
        context['all_semester'] = all_semester
        all_subject = Subject.objects.all()
        context['all_subject'] = all_subject

    if action == "view":
        context['readonly'] = 1

    elif action == "delete":
        attendance.delete()
        request.session['message'] = 'Record delete successfully.'
        return redirect('manage_attendance')

    if request.method == 'POST':
        if action == "edit":
            attendance = Attendance.objects.get(pk=attendance_id)
            student_attendance = StudentAttendance.objects.filter(attendance=attendance)
            student_attendance.delete()
            request.session['message'] = 'Record update successfully.'
        else:
            attendance = Attendance()
            request.session['message'] = 'Record save successfully.'

        attendance.date = datetime.strptime(str.strip(request.POST['txtDate']), '%d/%m/%Y')
        subject = Subject.objects.get(pk=request.POST['cmbSubjectId'])
        attendance.subject = subject
        attendance.save()

        all_student = Student.objects.filter(semester=subject.semester)
        for student in all_student:
            status = False
            for chk_student in request.POST.getlist('chkStudentId[]'):
                if str(student.pk) == str(chk_student):
                    status = True
            student_attendance = StudentAttendance()
            student_attendance.attendance = attendance
            student_attendance.student = student
            student_attendance.status = status
            student_attendance.save()

        return redirect('manage_attendance')

    all_stream = Stream.objects.all()
    context['all_stream'] = all_stream

    all_attendance = Attendance.all()
    context['all_attendance'] = all_attendance
    return render(request, 'manage_attendance.html', context)

def manage_student_promotion(request):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}
    if request.method == 'POST':
        semester = Semester.objects.get(pk=request.POST['cmbSemesterId'])
        all_student = Student.objects.filter(semester=semester)
        new_semester = Semester.objects.get(pk=request.POST['cmbNewSemesterId'])
        for student in all_student:
            for chk_student in request.POST.getlist('chkStudentId[]'):
                if str(student.pk) == str(chk_student):
                    student = Student.objects.get(pk=student.pk)
                    student.semester_id = new_semester.pk
                    student.save()
        return redirect('manage_student_promotion')

    all_stream = Stream.objects.all()
    context['all_stream'] = all_stream
    return render(request, 'manage_student_promotion.html', context)

def student_attendance_report(request):
    if request.user.is_authenticated() == False:
        return redirect('login')

    context = {}
    if request.method == 'POST':
        date = request.POST['txtDate']
        date = datetime.strptime(str.strip(date), '%d/%m/%Y')
        date = date.strftime('%Y-%m-%d')
        semester = Semester.objects.get(pk=request.POST['cmbSemesterId'])
        all_student = Student.objects.filter(semester_id=semester)
        all_subject = Subject.objects.filter(semester_id=semester.pk)
        context['all_subject'] = all_subject
        all_attendance = Attendance.objects.filter(date=date).filter(subject_id__in = all_subject)
        all_student_attendance = StudentAttendance.objects.filter(attendance_id__in = all_attendance)
        context['all_student_attendance'] = all_student_attendance

        cntx = {}
        for student in all_student:
             cntx[student.pk] = {'date' : date, 'student_name' : student.firstname}

        context['first_part'] = cntx

        main_cntx = {}
        for student in all_student:
            sub_cntx = {}
            sub_cntx['date'] = date
            sub_cntx['student_name'] = student.firstname + ' ' + student.middlename + ' ' + student.lastname

            cntx = {}
            for subject in all_subject:
                attendance = Attendance.objects.filter(date=date).filter(subject_id = subject.pk)
                all_stu_atndnc = StudentAttendance.objects.filter(attendance_id = attendance).filter(student_id = student.pk)
                for atndnc in all_stu_atndnc:
                    cntx[subject.pk] = atndnc.status

            sub_cntx['status'] = cntx
            main_cntx[student.pk] = sub_cntx

        context['second_part'] = main_cntx

    all_stream = Stream.objects.all()
    context['all_stream'] = all_stream
    return render(request, 'student_attendance_report.html', context)

def test(request):
    return render(request, 'index.html', {})