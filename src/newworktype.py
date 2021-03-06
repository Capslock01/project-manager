"""Module for creating a new worktype."""

import datetime
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from src import app
from src import db
from src.login import require_login


@app.route('/new_worktype', methods=['GET', 'POST'])
@require_login()
def new_worktype():
    """Create new worktypes."""

    if request.method == 'GET':
        return render_template('newworktype.html')

    if create_worktype():
        flash('Worktype created successfully.')
        return redirect(url_for('manager'))
    return redirect(url_for('new_worktype'))


def create_worktype() -> bool:
    """Create worktype for all users to use."""

    # Get data from form
    name = request.values.get('name', '').strip()
    rounding = request.values.get('rounding', '0').strip()
    rounding_unit = int(request.values.get('rounding_unit'))
    minimum = request.values.get('minimum', '0').strip()
    min_unit = int(request.values.get('min_unit'))
    price = request.values.get('price', '0').strip()

    # Validate worktype name
    if 4 > len(name) > 128:
        flash('Invalid name length!')
        return False
    query_worktype = 'SELECT * FROM work_type WHERE name = :name'
    worktype = db.session.execute(query_worktype, {'name': name}).fetchone()
    if worktype is not None:
        flash('Worktype name is already taken.')
        return False

    # Validate numerical values
    try:
        minimum = int(minimum)
        rounding = int(rounding)
        price = round(float(price), 2)  # Round just in case
    except ValueError:
        flash('Only use integers for rounding and minimum, '
              'and decimal for price!')
        return False

    # Set rounding and minimum to correct units
    if rounding_unit == 1:
        rounding = datetime.timedelta(minutes=rounding)
    elif rounding_unit == 2:
        rounding = datetime.timedelta(hours=rounding)

    if min_unit == 1:
        minimum = datetime.timedelta(minutes=minimum)
    elif min_unit == 2:
        minimum = datetime.timedelta(hours=minimum)

    # Create new worktype
    insert = """INSERT INTO work_type
                    (name, rounding, minimum, price)
                VALUES
                    (:name, :rounding, :minimum, :price)"""
    db.session.execute(
        insert,
        {
            'name': name,
            'rounding': rounding,
            'minimum': minimum,
            'price': price
        }
    )
    db.session.commit()
    return True
