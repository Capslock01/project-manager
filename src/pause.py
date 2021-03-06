"""Handles pausing a project."""

from flask import redirect
from flask import g
from flask import url_for
from src import app
from src import db
from src.login import require_login


@app.route('/pause/<pid>')
@require_login()
def pause(pid: int) -> str:
    """Create start entry for project with given pid."""

    if validate_pause(pid):
        # Set end value for entry
        update = """UPDATE entry SET "end"=NOW()
                    WHERE
                        project_id=:pid
                        AND "end" IS NULL
                        AND start IS NOT NULL"""
        db.session.execute(update, {'pid': pid})
        # Set state from 'running' to 'active'
        update = 'UPDATE project SET state=1 WHERE id=:pid'
        db.session.execute(update, {'pid': pid})
        db.session.commit()
    return redirect(url_for('manager'))


def validate_pause(pid: int) -> bool:
    """Check if project with pid can be paused."""

    # Validate pid
    query = 'SELECT * FROM project WHERE user_id=:uid AND id=:pid'
    project = db.session.execute(
        query,
        {
            'uid': g.user[0],
            'pid': pid
        }
    ).fetchone()
    if project is None:
        return False

    # Check if project is running
    query = """SELECT *
               FROM entry
               WHERE project_id=:pid
                   AND start IS NOT NULL
                   AND "end" IS NULL
               ORDER BY id DESC"""
    entry = db.session.execute(query, {'pid': pid}).fetchone()
    # example entry:
    # (1, 1, datetime.datetime(2022, 6, 10, 21, 47, 34, 798696), None, None)
    if entry is None:
        return False
    # Has start, but no end time -> running
    if entry[3] is None and entry[2] is not None:
        return True
    return False
