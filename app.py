import os
from flask import Flask, flash, render_template, request, redirect, url_for
from sqlalchemy import or_
from extensions import db
import pandas as pd

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB limit

# ===============================
# DATABASE CONFIG
# ===============================
database_url = os.getenv("DATABASE_URL")
if os.getenv("DATABASE_URL"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///queries.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from models import Query


# ===============================
# DASHBOARD
# ===============================

@app.route("/")
def dashboard():
    total_queries = Query.query.count()
    total_modules = db.session.query(Query.module).distinct().count()
    recent_queries = Query.query.order_by(Query.created_at.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_queries=total_queries,
        total_modules=total_modules,
        recent_queries=recent_queries
    )


# ===============================
# SEARCH PAGE
# ===============================

@app.route("/search")
def search_page():
    keyword = request.args.get("keyword")
    results = []

    if keyword:
        results = Query.query.filter(
            or_(
                Query.name.ilike(f"%{keyword}%"),
                Query.module.ilike(f"%{keyword}%"),
                Query.description.ilike(f"%{keyword}%"),
                Query.query_text.ilike(f"%{keyword}%")
            )
        ).order_by(Query.created_at.desc()).all()

    return render_template("search.html", results=results, keyword=keyword)


# ===============================
# MODULES PAGE
# ===============================

@app.route("/modules")
def modules():
    selected_module = request.args.get("module")

    # Get all unique modules
    modules = db.session.query(Query.module).distinct().all()
    modules = [m[0] for m in modules]

    queries = []

    if selected_module:
        queries = Query.query.filter_by(module=selected_module) \
                              .order_by(Query.created_at.desc()) \
                              .all()

    return render_template(
        "modules.html",
        modules=modules,
        selected_module=selected_module,
        queries=queries
    )

# ===============================
# ADD QUERY
# ===============================

@app.route("/add", methods=["GET", "POST"])
def add_query():
    if request.method == "POST":
        new_query = Query(
            module=request.form["module"],
            name=request.form["name"],
            description=request.form["description"],
            query_text=request.form["query_text"],
            comments=request.form["comments"]
        )

        db.session.add(new_query)
        db.session.commit()

        return redirect(url_for("manage"))

    return render_template("add.html")


# ===============================
# MANAGE PAGE (EDIT/DELETE + SEARCH)
# ===============================

@app.route("/manage")
def manage():
    keyword = request.args.get("keyword")

    if keyword:
        queries = Query.query.filter(
            or_(
                Query.name.ilike(f"%{keyword}%"),
                Query.module.ilike(f"%{keyword}%")
            )
        ).order_by(Query.created_at.desc()).all()
    else:
        queries = Query.query.order_by(Query.created_at.desc()).all()

    return render_template("manage.html", queries=queries, keyword=keyword)

@app.route("/debug")
def debug():
    queries = Query.query.all()

    if not queries:
        return "<h2>No records found.</h2>"

    # Get column names dynamically
    columns = [column.name for column in Query.__table__.columns]

    html = """
    <h1>Full Query Table</h1>
    <div style="overflow-x:auto;">
    <table border="1" cellpadding="8" cellspacing="0">
        <thead>
            <tr>
    """

    # Header row
    for col in columns:
        html += f"<th>{col}</th>"

    html += "</tr></thead><tbody>"

    # Data rows
    for q in queries:
        html += "<tr>"
        for col in columns:
            value = getattr(q, col)
            html += f"<td>{value}</td>"
        html += "</tr>"

    html += "</tbody></table></div>"

    return html

# ===============================
# EDIT QUERY
# ===============================

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_query(id):
    query = Query.query.get_or_404(id)

    if request.method == "POST":
        query.module = request.form["module"]
        query.name = request.form["name"]
        query.description = request.form["description"]
        query.query_text = request.form["query_text"]
        query.comments = request.form["comments"]

        db.session.commit()

        return redirect(url_for("manage"))

    return render_template("edit.html", query=query)

# ===============================
# BULK UPLOAD (ENTERPRISE)
# ===============================
@app.route("/bulk_upload", methods=["GET", "POST"])
def bulk_upload():
    if request.method == "POST":
        file = request.files.get("file")

        # 1. File presence check
        if not file or file.filename == "":
            flash("Please select a file to upload.")
            return redirect(url_for("bulk_upload"))

        filename = file.filename.lower()

        # 2. File type validation
        if not (filename.endswith(".csv") or filename.endswith(".xlsx")):
            flash("Invalid file type. Please upload a CSV or XLSX file.")
            return redirect(url_for("bulk_upload"))

        try:
            # 3. Read file (with encoding handling)
            if filename.endswith(".csv"):
                try:
                    df = pd.read_csv(file, encoding="utf-8")
                except UnicodeDecodeError:
                    file.seek(0)
                    df = pd.read_csv(file, encoding="latin1")
            else:
                df = pd.read_excel(file)

            # 4. Empty file check
            if df.empty:
                flash("The uploaded file is empty.")
                return redirect(url_for("bulk_upload"))

            # Normalize column names
            df.columns = df.columns.str.strip().str.lower()

            # 5. Required columns validation
            required_columns = {"name", "query_text"}
            missing_columns = required_columns - set(df.columns)

            if missing_columns:
                flash(f"Missing required columns: {', '.join(missing_columns)}")
                return redirect(url_for("bulk_upload"))

            added_count = 0
            duplicate_count = 0
            skipped_count = 0

            # 6. Process rows
            for _, row in df.iterrows():
                name = str(row.get("name", "")).strip()
                query_text = str(row.get("query_text", "")).strip()

                # Skip invalid rows
                if not name or not query_text or name.lower() == "nan":
                    skipped_count += 1
                    continue

                # Duplicate check (by name)
                existing = Query.query.filter_by(name=name).first()
                if existing:
                    duplicate_count += 1
                    continue

                new_query = Query(
                    module=str(row.get("module", "")).strip(),
                    name=name,
                    description=str(row.get("description", "")).strip(),
                    query_text=query_text,
                    comments=str(row.get("comments", "")).strip()
                )

                db.session.add(new_query)
                added_count += 1

            # 7. Commit once
            db.session.commit()

            # 8. Success summary
            flash(
                f"Upload completed: {added_count} added, "
                f"{duplicate_count} duplicates skipped, "
                f"{skipped_count} invalid rows skipped."
            )

        except Exception as e:
            db.session.rollback()
            print("Bulk upload error:", e)  # Server log
            flash("Upload failed due to a system error. Please check the file format and try again.")

        return redirect(url_for("bulk_upload"))

    return render_template("bulk_upload.html")

# ===============================
# APP START
# ===============================

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)