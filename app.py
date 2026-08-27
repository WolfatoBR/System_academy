from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///academia.db"
db = SQLAlchemy(app)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    duracao_dias = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(255))

    def __repr__(self):
        return f"<Plano {self.nome}"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    data_cadastro = db.Column(db.DateTime, server_default=db.func.now())

    plano_id = db.Column(db.Integer, db.ForeignKey("plan.id"), nullable=True)
    plano = db.relationship("Plan", backref="alunos")

    def __repr__(self):
        return f"<Aluno {self.nome}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/alunos/novo", methods=["GET", "POST"])
def new_students():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]

        aluno = Student(nome=nome, email=email, telefone=telefone)
        db.session.add(aluno)
        db.session.commit()

        return redirect(url_for("list_students"))

    return render_template("new_student.html")

@app.route("/alunos/editar/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    aluno = Student.query.get_or_404(id)

    if request.method == "POST":
        aluno.nome = request.form["nome"]
        aluno.email = request.form["email"]
        aluno.telefone = request.form["telefone"]

        db.session.commit()
        return redirect(url_for("list_students"))

    return render_template("edit_student.html", aluno=aluno)

@app.route("/alunos/excluir/<int:id>", methods=["POST"])
def delete_student(id):
    aluno = Student.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for("list_students"))

@app.route("/alunos")
def list_students():
    alunos = Student.query.all()
    return render_template("list_students.html", alunos=alunos)

if __name__ == "__main__":
    app.run(debug=True)