from sportal import app, db
from flask import render_template, request, redirect, url_for, flash
from sportal.models import User, Course
from sportal.form import RegisterForm, LoginForm, UpdateProfile, UpdateAccount, UpdatePassword, EnrollForm, UnenrollForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return render_template('home.html')

# @app.route('/admin')
# def adminpage():
#     form = AdminLogin()
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard'))
#     else:
#         return render_template('admin.html', form=form)

@app.route('/admin')
def userspage():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/delete/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    user_to_delete = User.query.get(id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User deleted successfully!", category='info')
    return redirect(url_for('userspage'))

@app.route('/register', methods=['GET', 'POST'])
def registerpage():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(fname=form.fname.data,
                              lname=form.lname.data,
                              username=form.username.data,
                              email=form.email.data,
                              password_hash=form.password.data,
                              gender=form.gender.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash("Account Created! You are now logged in", category='success')
        return redirect(url_for('dashboard'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There is an error: {err_msg}', category='danger')

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'You are now logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username or Password incorrect', category='danger')
    
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', form=form)


# When user is already logged in 
# These pages can only be accessed after logging in
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    enroll_form = EnrollForm()
    unenroll_form = UnenrollForm()
    if enroll_form.validate_on_submit():
        selected_course = enroll_form.courses.data
        course = Course.query.filter_by(course_name=selected_course).first()
        if course:
            current_user.course = course.id
            db.session.commit()
            return redirect(url_for('dashboard'))
    
    if unenroll_form.validate_on_submit():
        if current_user.course:
            current_user.course = None
            db.session.commit()
            return redirect(url_for('dashboard'))

    enrolled = Course.query.filter_by(id=current_user.course).first()
    return render_template('dashboard.html', enroll_form=enroll_form, unenroll_form=unenroll_form, enrolled=enrolled)

@app.route('/dashboard/progress')
def user_progress():
    if current_user.is_authenticated:
        progress = [
            {'id':1, 'semester':'I', 'marks':364, 'total':500, 'percent':72.8, 'gpa':3.01},
            {'id':2, 'semester':'II', 'marks':363, 'total':500, 'percent':72.6, 'gpa':2.99},
            {'id':3, 'semester':'III', 'marks':335, 'total':500, 'percent':67, 'gpa':2.91},
            {'id':4, 'semester':'IV', 'marks':379, 'total':500, 'percent':75.8, 'gpa':3.12}
        ]
        return render_template('user-progress.html', progress=progress)
    else:
        flash('Please login first!', category='warning')
        return redirect(url_for('loginpage'))

@app.route('/dashboard/settings', methods=['GET', 'POST'])
def user_settings():
    update_profile  = UpdateProfile()
    update_account  = UpdateAccount()
    update_password = UpdatePassword()
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    if current_user.is_authenticated:
        user_to_update = User.query.get(current_user.id)

        if update_profile.validate_on_submit():
            user_to_update.fname  = update_profile.fname.data
            user_to_update.lname  = update_profile.lname.data
            user_to_update.gender = update_profile.gender.data
            db.session.commit()
            flash('Changes to Profile Updated Successfully!', category='success')
            return redirect(url_for('dashboard'))        
            
        if update_account.validate_on_submit():
            user_to_update.username = update_account.username.data
            user_to_update.email    = update_account.email.data
            db.session.commit()
            flash('Account Updated Successfully!', category='success')
            return redirect(url_for('dashboard'))       

        if update_password.validate_on_submit():
            if user_to_update.check_password_correction(attempted_password=update_password.curr_pass.data):
                user_to_update.password_hash = update_password.con_new_pass.data
                db.session.commit()
                flash('Password Changed!', category='success')
                return redirect(url_for('dashboard'))
            else:
                flash('Password is incorrect!', category='danger')

        if update_profile.errors != {} or update_account.errors != {} or update_password.errors != {}:
            not_err = "This field is required."
            for err_msg in update_profile.errors.values():
                if err_msg[0] != not_err:
                    flash(err_msg[0], category='danger')
            for err_msg in update_account.errors.values():
                if err_msg[0] != not_err:
                    flash(err_msg[0], category='danger')
            for err_msg in update_password.errors.values():
                if err_msg[0] != not_err:
                    flash(err_msg[0], category='danger')

        return render_template('user-settings.html', update_profile=update_profile, update_account=update_account, update_password=update_password, user_to_update=user_to_update, months=months)
    else:
        flash('Please login first', category='warning')
        return redirect(url_for('loginpage'))

@app.route('/logout')
def logoutpage():
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out!", category="info")
    
    return redirect(url_for('homepage'))



