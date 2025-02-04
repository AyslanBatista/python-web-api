from blog.auth import create_user
from blog.posts import (
    delete_post_by_slug,
    get_all_posts,
    get_post_by_slug,
    new_post,
    update_post_by_slug,
)
from flask import Blueprint, Flask, abort, redirect, render_template, request, url_for
from flask_simplelogin import get_username, login_required
from blog.utils import slugify

bp = Blueprint("post", __name__, template_folder="templates")


@bp.route("/")
def index():
    posts = get_all_posts()
    return render_template("index.html.j2", posts=posts)


@bp.route("/<string:slug>")
def detail(slug):
    post = get_post_by_slug(slug)
    if not post:
        return abort(404, "Post not found")

    return render_template("post.html.j2", post=post)


@bp.route("/new", methods=["GET", "POST"])
@login_required()
def new():
    error_message = None
    title = ""
    content = ""

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        username = get_username()

        try:
            slug = new_post(title, content, username)
            return redirect(url_for("post.detail", slug=slug))
        except ValueError as e:
            error_message = str(e)

    return render_template(
        "form.html.j2",
        error_message=error_message,
        title=title,
        content=content,
    )


@bp.route("/register", methods=["GET", "POST"])
def register():
    error_message = None
    
    if request.method == "POST":
        try:
            user = create_user(
            username=request.form.get("username"),
            password=request.form.get("password"),
            )
            return render_template("usuario-criado.html.j2", user=user)
        except ValueError as e:
            error_message = str(e)
            
    return render_template("register.html.j2", error_message=error_message)


@bp.route('/logout', methods=["GET"])
@login_required
def logout():
    from flask_simplelogin import logout

    logout()

@bp.route("/post/<slug>/edit", methods=["GET", "POST"])
@login_required()
def edit(slug):
    post = get_post_by_slug(slug)

    if not post:
        return "Post não encontrado", 404
    
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if title == post["title"]:
            update_data = {"content": content}
            update_post_by_slug(slug, update_data)
        else:
            update_data = {"title": title, "content": content}
            update_post_by_slug(slug, update_data)
        
        new_slug = slugify(title)
        return redirect(url_for("post.detail", slug=new_slug or slug))

    return render_template("edit_post.html.j2", post=post)

@bp.route("/post/<slug>/delete", methods=["POST"])
@login_required()
def delete(slug):
    post = get_post_by_slug(slug)

    if not post:
        return "Post não encontrado", 404

    # Garantir que apenas o autor pode deletar
    if post["username"] != get_username():
        return "Acesso negado", 403

    delete_post_by_slug(slug)
    
    return redirect("/")


def configure(app: Flask):
    app.register_blueprint(bp)
