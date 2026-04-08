import json
import os
import re
import uuid
import csv
import io
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, jsonify, flash, send_from_directory
)
from werkzeug.utils import secure_filename

import config
from models import db, Question, TestSession, TestAnswer
from database import init_db

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

init_db(app)


# ---------------------------------------------------------------------------
# Template filters
# ---------------------------------------------------------------------------

@app.template_filter("format_explanation")
def format_explanation(text):
    """Split 'Intro. (1) item. (2) item.' into intro + <ul> list."""
    # Split on (1), (2), ... patterns
    parts = re.split(r'\s*\(\d+\)\s*', text)
    items = [p.strip().rstrip('.') for p in parts if p.strip()]

    if len(items) <= 1:
        return f'<p class="explanation-intro">{text}</p>'

    intro = items[0]
    bullets = items[1:]
    li_html = ''.join(f'<li>{b}</li>' for b in bullets)
    return (
        f'<p class="explanation-intro">{intro}</p>'
        f'<ul class="explanation-list">{li_html}</ul>'
    )
# Helpers
# ---------------------------------------------------------------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


def get_exam_size():
    """Read from session-stored setting or fall back to config default."""
    return session.get("exam_size", config.EXAM_SIZE)


# ---------------------------------------------------------------------------
# User Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_test():
    user_name = request.form.get("user_name", "").strip()
    user_email = request.form.get("user_email", "").strip()

    if not user_name or not user_email:
        flash("Vui lòng nhập đầy đủ họ tên và email.", "danger")
        return redirect(url_for("index"))

    active_questions = Question.query.filter_by(active=True).all()
    exam_size = get_exam_size()

    if len(active_questions) < exam_size:
        exam_size = len(active_questions)

    if exam_size == 0:
        flash("Hiện chưa có câu hỏi nào. Vui lòng thử lại sau.", "warning")
        return redirect(url_for("index"))

    import random
    selected = random.sample(active_questions, exam_size)
    question_ids = [q.id for q in selected]

    session_id = str(uuid.uuid4())
    test_session = TestSession(
        id=session_id,
        user_name=user_name,
        user_email=user_email,
        question_ids=json.dumps(question_ids),
        current_index=0,
        score=0,
    )
    db.session.add(test_session)
    db.session.commit()

    return redirect(url_for("test_question", session_id=session_id, q_num=0))


@app.route("/test/<session_id>")
def test_redirect(session_id):
    test_session = TestSession.query.get_or_404(session_id)
    if test_session.is_complete:
        return redirect(url_for("test_result", session_id=session_id))
    return redirect(url_for("test_question", session_id=session_id, q_num=test_session.current_index))


@app.route("/test/<session_id>/q/<int:q_num>")
def test_question(session_id, q_num):
    test_session = TestSession.query.get_or_404(session_id)

    if test_session.is_complete:
        return redirect(url_for("test_result", session_id=session_id))

    question_ids = json.loads(test_session.question_ids)
    total = len(question_ids)

    # Allow viewing answered questions (but not skipping ahead)
    if q_num >= total:
        return redirect(url_for("test_result", session_id=session_id))

    question = Question.query.get_or_404(question_ids[q_num])

    # Check if this question was already answered (for back navigation)
    existing_answer = TestAnswer.query.filter_by(
        session_id=session_id, question_id=question.id
    ).first()

    return render_template(
        "test.html",
        session=test_session,
        question=question,
        q_num=q_num,
        total=total,
        existing_answer=existing_answer,
    )


@app.route("/test/<session_id>/q/<int:q_num>/submit", methods=["POST"])
def submit_answer(session_id, q_num):
    test_session = TestSession.query.get_or_404(session_id)

    if test_session.is_complete:
        return jsonify({"error": "Bài thi đã kết thúc"}), 400

    question_ids = json.loads(test_session.question_ids)
    total = len(question_ids)

    if q_num >= total:
        return jsonify({"error": "Câu hỏi không hợp lệ"}), 400

    question_id = question_ids[q_num]
    question = Question.query.get_or_404(question_id)

    # Prevent double-submit
    existing = TestAnswer.query.filter_by(session_id=session_id, question_id=question_id).first()
    if existing:
        return jsonify({
            "correct": existing.is_correct,
            "correct_answer": question.is_phishing,
            "explanation": question.explanation,
            "is_last": q_num == total - 1,
            "next_url": url_for("test_question", session_id=session_id, q_num=q_num + 1) if q_num < total - 1 else url_for("test_result", session_id=session_id),
        })

    data = request.get_json()
    user_answer = data.get("answer")  # True = phishing, False = legitimate

    if user_answer is None:
        return jsonify({"error": "Câu trả lời không hợp lệ"}), 400

    is_correct = (user_answer == question.is_phishing)

    answer = TestAnswer(
        session_id=session_id,
        question_id=question_id,
        user_answer=user_answer,
        is_correct=is_correct,
    )
    db.session.add(answer)

    if is_correct:
        test_session.score += 1

    test_session.current_index = q_num + 1
    is_last = q_num == total - 1

    if is_last:
        test_session.completed_at = datetime.utcnow()

    db.session.commit()

    next_url = (
        url_for("test_result", session_id=session_id)
        if is_last
        else url_for("test_question", session_id=session_id, q_num=q_num + 1)
    )

    return jsonify({
        "correct": is_correct,
        "correct_answer": question.is_phishing,
        "explanation": question.explanation,
        "is_last": is_last,
        "next_url": next_url,
    })


@app.route("/test/<session_id>/result")
def test_result(session_id):
    test_session = TestSession.query.get_or_404(session_id)
    question_ids = json.loads(test_session.question_ids)
    total = len(question_ids)

    # Build answer detail list
    answers = []
    for qid in question_ids:
        q = Question.query.get(qid)
        ans = TestAnswer.query.filter_by(session_id=session_id, question_id=qid).first()
        answers.append({"question": q, "answer": ans})

    pass_threshold = 0.7
    passed = (test_session.score / total) >= pass_threshold if total > 0 else False

    return render_template(
        "result.html",
        session=test_session,
        answers=answers,
        total=total,
        passed=passed,
    )


# ---------------------------------------------------------------------------
# Static uploads
# ---------------------------------------------------------------------------

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ---------------------------------------------------------------------------
# Admin Routes
# ---------------------------------------------------------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        key = request.form.get("admin_key", "").strip()
        if key == config.ADMIN_KEY:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Khóa admin không đúng. Vui lòng thử lại.", "danger")
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/")
@admin_required
def admin_dashboard():
    total_sessions = TestSession.query.count()
    completed_sessions = TestSession.query.filter(TestSession.completed_at.isnot(None)).count()
    total_questions = Question.query.filter_by(active=True).count()

    sessions = TestSession.query.order_by(TestSession.started_at.desc()).limit(50).all()

    avg_score = 0
    pass_count = 0
    if completed_sessions > 0:
        completed = TestSession.query.filter(TestSession.completed_at.isnot(None)).all()
        scores = []
        for s in completed:
            total_q = s.total_questions
            if total_q > 0:
                pct = s.score / total_q
                scores.append(pct)
                if pct >= 0.7:
                    pass_count += 1
        avg_score = round(sum(scores) / len(scores) * 100, 1) if scores else 0

    exam_size = get_exam_size()

    return render_template(
        "admin/dashboard.html",
        total_sessions=total_sessions,
        completed_sessions=completed_sessions,
        total_questions=total_questions,
        sessions=sessions,
        avg_score=avg_score,
        pass_count=pass_count,
        exam_size=exam_size,
    )


@app.route("/admin/settings", methods=["POST"])
@admin_required
def admin_settings():
    exam_size = request.form.get("exam_size", "10")
    try:
        exam_size = int(exam_size)
        if exam_size not in (5, 10, 15, 20):
            exam_size = 10
    except ValueError:
        exam_size = 10
    session["exam_size"] = exam_size
    flash(f"Đã cập nhật: mỗi bài thi sẽ có {exam_size} câu hỏi.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/questions")
@admin_required
def admin_questions():
    questions = Question.query.order_by(Question.created_at.desc()).all()
    return render_template("admin/questions.html", questions=questions)


@app.route("/admin/questions/add", methods=["GET", "POST"])
@admin_required
def admin_question_add():
    if request.method == "POST":
        image_path = None
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                image_path = filename

        question = Question(
            title=request.form["title"],
            scenario_type=request.form["scenario_type"],
            content=request.form["content"],
            image_path=image_path,
            is_phishing=request.form["is_phishing"] == "true",
            explanation=request.form["explanation"],
            active=request.form.get("active") == "on",
        )
        db.session.add(question)
        db.session.commit()
        flash("Đã thêm câu hỏi mới.", "success")
        return redirect(url_for("admin_questions"))

    return render_template("admin/question_form.html", question=None, action="add")


@app.route("/admin/questions/<int:qid>/edit", methods=["GET", "POST"])
@admin_required
def admin_question_edit(qid):
    question = Question.query.get_or_404(qid)

    if request.method == "POST":
        question.title = request.form["title"]
        question.scenario_type = request.form["scenario_type"]
        question.content = request.form["content"]
        question.is_phishing = request.form["is_phishing"] == "true"
        question.explanation = request.form["explanation"]
        question.active = request.form.get("active") == "on"

        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                question.image_path = filename

        db.session.commit()
        flash("Đã cập nhật câu hỏi.", "success")
        return redirect(url_for("admin_questions"))

    return render_template("admin/question_form.html", question=question, action="edit")


@app.route("/admin/questions/<int:qid>/delete", methods=["POST"])
@admin_required
def admin_question_delete(qid):
    question = Question.query.get_or_404(qid)
    db.session.delete(question)
    db.session.commit()
    flash("Đã xóa câu hỏi.", "success")
    return redirect(url_for("admin_questions"))


@app.route("/admin/questions/<int:qid>/toggle", methods=["POST"])
@admin_required
def admin_question_toggle(qid):
    question = Question.query.get_or_404(qid)
    question.active = not question.active
    db.session.commit()
    status = "kích hoạt" if question.active else "ẩn"
    flash(f"Đã {status} câu hỏi.", "success")
    return redirect(url_for("admin_questions"))


@app.route("/admin/questions/import", methods=["GET", "POST"])
@admin_required
def admin_import():
    if request.method == "POST":
        # JSON import
        if "json_data" in request.form and request.form["json_data"].strip():
            try:
                items = json.loads(request.form["json_data"])
                count = _import_questions(items)
                flash(f"Đã nhập {count} câu hỏi từ JSON.", "success")
                return redirect(url_for("admin_questions"))
            except (json.JSONDecodeError, KeyError) as e:
                flash(f"Lỗi JSON: {e}", "danger")

        # CSV import
        elif "csv_file" in request.files:
            file = request.files["csv_file"]
            if file and file.filename:
                stream = io.StringIO(file.stream.read().decode("utf-8-sig"))
                reader = csv.DictReader(stream)
                items = list(reader)
                try:
                    count = _import_questions(items)
                    flash(f"Đã nhập {count} câu hỏi từ CSV.", "success")
                    return redirect(url_for("admin_questions"))
                except KeyError as e:
                    flash(f"Thiếu cột: {e}", "danger")

    return render_template("admin/import.html")


def _import_questions(items):
    count = 0
    for item in items:
        is_phishing_val = item.get("is_phishing", "true")
        if isinstance(is_phishing_val, bool):
            is_phishing = is_phishing_val
        else:
            is_phishing = str(is_phishing_val).lower() in ("true", "1", "yes", "phishing")

        q = Question(
            title=item["title"],
            scenario_type=item.get("type", item.get("scenario_type", "text")),
            content=item["content"],
            is_phishing=is_phishing,
            explanation=item["explanation"],
            active=True,
        )
        db.session.add(q)
        count += 1
    db.session.commit()
    return count


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
