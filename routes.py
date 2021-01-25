from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import Permissions, Transaction, User
from datetime import datetime
from app import db
import locale
from sqlalchemy.sql.functions import sum

# set locale so we can play with currency formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

main = Blueprint('main', __name__)


# global filter to format currency per locale
@main.app_template_filter()
def format_currency(value):
    return locale.currency(value, symbol=True, grouping=True)


@main.route('/')
def index():
    return render_template('index.html')  # TODO: maybe route this to the account or approval page if logged in


@main.route('/admin')
@login_required
def admin():
    if current_user.permission == Permissions.admin:
        return render_template('admin.html', name=current_user.name, users=User.query.all())
    else:
        return redirect(url_for('auth.login'))  # user isn't an admin - redirect to login page
                                                # TODO: maybe route back to index instead


@main.route('/modify_user', methods=['POST'])
@login_required
def modify_user():
    user = User.query.get(request.form.get('user_id'))
    user_name = request.form.get('name')
    permission = Permissions(int(request.form.get('permission')))
    email = request.form.get('email')
    password = request.form.get('password')
    msg = 'Updated '
    danger = ''

    if user_name and user.name != user_name:
        user.name = user_name
        msg += 'Name, '
    if permission and user.permission != permission:
        if (user.permission == Permissions.admin and
                permission != Permissions.admin and
                User.query.filter_by(permission=Permissions.admin).count() == 1):
            danger = "Cannot remove the only admin's permissions."
        else:
            user.permission = permission
            msg += 'Permissions, '
    if email and user.email != email:
        user.email = email
        msg += 'Email, '
    if password:
        user.password = generate_password_hash(password, method='sha256')
        msg += 'Password, '

    if msg == 'Updated ':  # we didn't update anything
        flash(f'{danger} No changes made for {user_name}.', 'is-danger' if danger else 'is-warning')
    else:
        db.session.commit()
        flash(f'{danger} {msg[:-2]} for {user_name}.', 'is-danger' if danger else 'is-success')

    return redirect(url_for('main.admin'))


@main.route('/account')
@login_required
def account():
    transaction_sum = Transaction.query.with_entities(sum(Transaction.amount).label(
        'balance')).filter(Transaction.user_id == current_user.id)  # ,
    # Transaction.approved is True)
    balance = 0
    if transaction_sum:
        balance = transaction_sum[0][0] if transaction_sum[0][0] is not None else 0
    return render_template('account.html', name=current_user.name,
                           transactions=Transaction.query.filter_by(
                               user_id=current_user.id).order_by(Transaction.date.desc()),
                           balance=balance)


@main.route('/deposit', methods=['POST'])
@login_required
def deposit():
    amount = request.form.get('amount')
    memo = request.form.get('memo')

    try:
        amount = round(float(amount), 2)
    except ValueError:
        flash(f'{amount}  is not a valid deposit amount', 'is-danger')
        return redirect(url_for('main.account'))

    if memo == '':
        flash(f'Please enter a memo for this deposit', 'is-danger')
        return redirect(url_for('main.account'))

    transaction = Transaction(date=datetime.now(), amount=abs(amount),
                              memo=memo, approved=False, user_id=current_user.id)
    db.session.add(transaction)
    db.session.commit()

    flash(f"Approval for a deposit of ${amount:.2f} is pending in {current_user.name}'s account", 'is-success')

    return redirect(url_for('main.account'))


@main.route('/withdraw', methods=['POST'])
@login_required
def withdraw():
    amount = request.form.get('amount')
    memo = request.form.get('memo')

    try:
        amount = round(float(amount), 2)
    except ValueError:
        flash(f'{amount}  is not a valid withdrawal amount', 'is-danger')
        return redirect(url_for('main.account'))

    if memo == '':
        flash(f'Please enter a memo for this withdrawal', 'is-danger')
        return redirect(url_for('main.account'))

    transaction = Transaction(date=datetime.now(), amount=abs(amount) * -1.0,
                              memo=memo, approved=False, user_id=current_user.id)
    db.session.add(transaction)
    db.session.commit()

    flash(f"Approval for a withdrawal of ${amount:.2f} is pending in {current_user.name}'s account", 'is-success')

    return redirect(url_for('main.account'))
