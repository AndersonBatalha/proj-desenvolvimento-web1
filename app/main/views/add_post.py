from ..forms import PostForm
from app.models import Post, Usuario
from app.main import main
from app import db
from slugify import slugify

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .upload_file import allowed_extension, upload

@main.route('/add_post', methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        if request.method == "POST":
            if allowed_extension(request.files['imagem'].filename):
                post = Post(
                    titulo=form.titulo.data,
                    texto=form.texto.data,
                    imagem='uploads/'+form.imagem.data.filename,
                    slug=slugify(form.titulo.data),

                    id_autor=current_user.id,
                    autor=Usuario.query.get(current_user.id)
                )
                db.session.add(post)
                db.session.commit()
                upload()
                flash('Postagem adicionada', category='success')
                return redirect(url_for('main.posts'))
            else:
                flash('Apenas arquivos de imagem são válidos', category='warning')

    return render_template('forms/add_post.html', form=form)