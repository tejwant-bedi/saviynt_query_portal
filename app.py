import os
from flask import Flask, flash, render_template, request, redirect, url_for, session, Response
from sqlalchemy import or_,asc
from extensions import db
import pandas as pd
import re
from glossary_data import glossary_data
from functools import wraps
from datetime import timedelta
import csv
from io import StringIO

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.permanent_session_lifetime = timedelta(minutes=10)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB limit
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "saviynt123")

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.permanent = True
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid credentials"

    return render_template("admin_login.html", error=error)

@app.before_request
def refresh_admin_session():
    if session.get("admin"):
        session.permanent = True

@app.route("/admin-logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("dashboard"))

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper

def normalize_text(value):
    if not value:
        return ""
    # Remove leading/trailing spaces
    value = value.strip()
    # Replace multiple spaces with single space
    value = re.sub(r'\s+', ' ', value)
    # Convert to lowercase
    return value.lower()

def clean_text(value):

    if not value:
        return ""
    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)
    return value

def clean_query_text(query_text):
    if not query_text:
        return ""

    query_text = query_text.replace('\r\n', '\n').replace('\r', '\n')

    lines = [line.strip() for line in query_text.split('\n')]

    lines = [line for line in lines if line]

    query_text = '\n'.join(lines)

    query_text = re.sub(r'[ \t]+', ' ', query_text)

    return query_text.strip()

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

    modules = (
        db.session.query(Query.module)
        .distinct()
        .order_by(asc(Query.module))
        .all()
    )
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
@admin_required
def add_query():
    if request.method == "POST":
        try:
            # 1. Get and clean input
            module = clean_text(request.form.get("module", ""))
            name = clean_text(request.form.get("name", ""))
            description = clean_text(request.form.get("description", ""))
            comments = clean_text(request.form.get("comments", ""))
            query_text = clean_query_text(request.form.get("query_text", ""))
            dynamic_input=clean_text(request.form.get("dynamic_input"))
            execute_in=request.form.get("execute_in")

            # 2. Validation
            if not name or not query_text:
                flash("Name and Query Text are required.")
                return redirect(url_for("add_query"))
            allowed_scopes = ["Data Analyzer, Analytics", "Analytics"]
            if execute_in not in allowed_scopes:
                flash("Invalid value for 'Execute in'")
                return redirect(url_for("add_query"))

            # 3. Normalize name for duplicate check
            # Removes extra spaces and ignores case
            normalized_name = re.sub(r"\s+", " ", name).strip().lower()

            # Check existing queries
            existing_queries = Query.query.all()
            for q in existing_queries:
                existing_normalized = re.sub(r"\s+", " ", q.name).strip().lower()
                if existing_normalized == normalized_name:
                    flash("A query with this name already exists.")
                    return redirect(url_for("add_query"))

            # 4. Create new query
            new_query = Query(
                module=module,
                name=name,
                description=description,
                query_text=query_text,
                comments=comments,
                dynamic_input=dynamic_input,
                execute_in=execute_in
            )

            db.session.add(new_query)
            db.session.commit()

            flash("Query added successfully!")
            return redirect(url_for("manage"))

        except Exception as e:
            db.session.rollback()
            print("Add query error:", e)
            flash("Failed to add query due to a system error.")

            return redirect(url_for("add_query"))

    return render_template("add.html")

# ===============================
# MANAGE PAGE 
# ===============================

@app.route("/manage")
@admin_required
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

# ===============================
# QUERIES_TABLE
# ===============================

@app.route("/queries_table")
@admin_required
def queries_table():
    queries = Query.query.order_by(Query.id.desc()).all()

    if not queries:
        return "<h2>No records found.</h2>"

    columns = [column.name for column in Query.__table__.columns]

    return render_template(
        "queries_table.html",
        queries=queries,
        columns=columns
    )

# ===============================
# DELETE FROM QUERIES_TABLE
# ===============================

@app.route("/delete_queries_table/<int:id>", methods=["POST"])
@admin_required
def delete_queries_table(id):
    query = Query.query.get_or_404(id)

    try:
        db.session.delete(query)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Delete error:", e)

    return redirect(url_for("queries_table"))

# ===============================
# EDIT QUERY
# ===============================

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_query(id):
    query = Query.query.get_or_404(id)

    if request.method == "POST":
        allowed_scopes = ["Data Analyzer, Analytics", "Analytics"]
        execute_in = request.form.get("execute_in")

        if execute_in not in allowed_scopes:
            flash("Invalid value for 'Execute in'")
            return redirect(url_for("edit_query", id=id))
        
        query.module = clean_text(request.form["module"])
        query.name = clean_text(request.form["name"])
        query.description = clean_text(request.form["description"])
        query.query_text = clean_query_text(request.form["query_text"])
        query.execute_in = clean_text(request.form["execute_in"])
        query.dynamic_input = clean_text(request.form["dynamic_input"])
        query.comments = clean_text(request.form["comments"])

        db.session.commit()

        return redirect(url_for("manage"))

    return render_template("edit.html", query=query)

# ===============================
# BULK UPLOAD 
# ===============================
@app.route("/bulk_upload", methods=["GET", "POST"])
@admin_required
def bulk_upload():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            flash("Please select a file to upload.")
            return redirect(url_for("bulk_upload"))

        filename = file.filename.lower()

        if not (filename.endswith(".csv") or filename.endswith(".xlsx")):
            flash("Invalid file type. Please upload a CSV or XLSX file.")
            return redirect(url_for("bulk_upload"))

        try:
            # Read file
            if filename.endswith(".csv"):
                try:
                    df = pd.read_csv(file, encoding="utf-8")
                except UnicodeDecodeError:
                    file.seek(0)
                    df = pd.read_csv(file, encoding="latin1")
            else:
                df = pd.read_excel(file)

            if df.empty:
                flash("The uploaded file is empty.")
                return redirect(url_for("bulk_upload"))

            # Normalize column names
            df.columns = df.columns.str.strip().str.lower()

            required_columns = {"name", "query_text"}
            missing_columns = required_columns - set(df.columns)

            if missing_columns:
                flash(f"Missing required columns: {', '.join(missing_columns)}")
                return redirect(url_for("bulk_upload"))

            added_count = 0
            duplicate_count = 0
            skipped_count = 0
            row_errors = []

            # Load existing queries once
            existing_queries = Query.query.all()
            existing_set = {
                (normalize_text(q.name), normalize_text(q.module))
                for q in existing_queries
            }

            allowed_scopes = ["Data Analyzer, Analytics", "Analytics"]

            # Process rows
            for index, row in df.iterrows():
                row_number = index + 2  # +2 because Excel header is row 1

                try:
                    name = clean_text(str(row.get("name", "")))
                    module = clean_text(str(row.get("module", "")))
                    query_text = clean_query_text(str(row.get("query_text", "")))
                    description = clean_text(str(row.get("description", "")))
                    comments = clean_text(str(row.get("comments", "")))
                    dynamic_input = clean_text(str(row.get("dynamic_input", "")))
                    execute_in = clean_text(str(row.get("execute_in", "")))

                    # Validation: name/query
                    if not name or name.lower() == "nan":
                        skipped_count += 1
                        row_errors.append(f"Row {row_number}: Missing query name")
                        continue

                    if not query_text or query_text.lower() == "nan":
                        skipped_count += 1
                        row_errors.append(f"Row {row_number}: Missing query_text")
                        continue

                    # Duplicate check
                    key = (normalize_text(name), normalize_text(module))
                    if key in existing_set:
                        duplicate_count += 1
                        row_errors.append(f"Row {row_number}: Duplicate (name + module)")
                        continue

                    # Execute scope validation
                    if execute_in and execute_in not in allowed_scopes:
                        skipped_count += 1
                        row_errors.append(
                            f"Row {row_number}: Invalid Execute in value -> '{execute_in}'"
                        )
                        continue

                    # Insert
                    new_query = Query(
                        module=module,
                        name=name,
                        description=description,
                        query_text=query_text,
                        comments=comments,
                        dynamic_input=dynamic_input,
                        execute_in=execute_in
                    )

                    db.session.add(new_query)
                    existing_set.add(key)
                    added_count += 1

                except Exception as row_error:
                    skipped_count += 1
                    row_errors.append(
                        f"Row {row_number}: System error -> {str(row_error)}"
                    )

            db.session.commit()

            # Summary
            flash(
                f"Upload completed: {added_count} added, "
                f"{duplicate_count} duplicates, "
                f"{skipped_count} skipped."
            )

            # Store row errors (limit to avoid huge UI)
            if row_errors:
                session["bulk_errors"] = row_errors[:100]
            else:
                session.pop("bulk_errors", None)

        except Exception as e:
            db.session.rollback()
            print("Bulk upload error:", e)
            flash("Upload failed due to a system error.")

        return redirect(url_for("bulk_upload"))

    # GET request
    errors = session.pop("bulk_errors", None)
    return render_template("bulk_upload.html", errors=errors)

# ===============================
# GLOSSARY
# ===============================

@app.route("/glossary")
def glossary():
    
    selected_section = request.args.get("section")

    sections = sorted(glossary_data.keys())
    items = glossary_data.get(selected_section)

    return render_template(
        "glossary.html",
        sections=sections,
        selected_section=selected_section,
        items=items
    )
    
@app.route("/export", methods=["GET", "POST"])
@admin_required
def export_queries():

    # 👉 If user clicks download
    if request.method == "POST":

        queries = Query.query.all()

        output = StringIO()

        # Excel UTF-8 fix
        output.write('\ufeff')

        writer = csv.writer(
            output,
            delimiter=",",
            quoting=csv.QUOTE_ALL
        )

        # Exact bulk upload header
        writer.writerow([
            "module",
            "name",
            "description",
            "dynamic_input",
            "execute_in",
            "query_text",
            "comments"
        ])

        for q in queries:
            query_text = q.query_text.replace("\u00A0", " ") if q.query_text else ""

            writer.writerow([
                q.module,
                q.name,
                q.description,
                q.dynamic_input,
                q.execute_in,
                query_text,
                q.comments
            ])

        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": "attachment; filename=queries_export.csv"
            }
        )

    return render_template("export.html")

# ===============================
# APP START
# ===============================

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
    
