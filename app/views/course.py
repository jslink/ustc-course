from flask import Blueprint,render_template,abort,redirect,url_for,request,abort
from app.models import Course
from app.forms import ReviewForm

course = Blueprint('course',__name__)

@course.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    print(per_page)
    courses_page = Course.query.paginate(page,per_page=per_page)
    return render_template('course-index.html',pagination=courses_page)

@course.route('/<int:course_id>/')
#@course.route('/<int:course_id>/<course_name>/')
def view_course(course_id,course_name=None):
    course = Course.query.get(course_id)
    if not course:
        abort(404)
    #if course_name != course.name:
    #    return redirect(url_for('.view_course',course_id=course_id,course_name=course.name))

    related_courses = Course.query.filter_by(name=course_name).all()
    teacher = course.teacher
    if teacher:
        same_teacher_courses = teacher.courses
    else:
        same_teacher_courses = None
    return render_template('course.html',
            course=course,
            related_courses=related_courses,
            teacher=teacher,
            same_teacher_courses=same_teacher_courses)

#@course.route('/<int:course_id>/<course_name>/reviews/')
@course.route('/<int:course_id>/reviews/')
def review(course_id,course_name=None):
    course = Course.query.get(course_id)
    if not course:
        abort(404)
    #if course_name != course.name:
    #    return redirect(url_for('.review',course_id=course_id,course_name=course.name))

    reviews = course.reviews.paginate(page=1,per_page=10)
    if reviews.total:
        str = ''
        for item in reviews.items:
            str += item.content + '<a href=' + url_for('review.edit_review', review_id=item.id) +'>Edit</a><br>'
        return str
    else:
        return 'No reviews'


'''deprecated. See review.py.
@course.route('/<int:course_id>/<course_name>/review/edit',methods=['GET','POST'])
def edit_review(course_d,course_name=None):
    course = Course.query.get(course_id)
    if not course:
        return 404
    if course_name != course.name:
        return redirect(url_for('.edit_review',course_id=course_id,course_name=course.name))
    '''



@course.route('/new/',methods=['GET','POST'])
@course.route('/<int:course_id>/edit/',methods=['GET','POSt'])
def edit_course(course_id=None):
    if course_id:
        course = Course.query.get(course_id)
    else:
        course = Course()
    if not course:
        abort(404)
    course_form = CourseForm(request.form, course)
    if course_form.validate_on_submit():
        course_form.populate_obj(course)
        course = course.save()
        flash('course saved')
        return redirect('.view_course', course_id=course.id, course_name=course.name)
    return render_tempalte('edit-course.html', form=course_form)
