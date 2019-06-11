import os
from ..forms import EditPostForm
from app.models import Post, Usuario
from app.main import main
from app import db
from slugify import slugify

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .upload_file import allowed_extension, upload

@main.route('/edit_post/<slug>', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    post = Post.query.filter_by(slug=slug).first()
    form = EditPostForm(post=post)
    if form.validate_on_submit():
        if request.method == "POST" and (
            form.titulo.data != request.form['titulo'] or \
            form.texto.data != request.form['texto']
        ):
            post.titulo = form.titulo.data = request.form['titulo']
            post.texto = form.texto.data = request.form['texto']
            post.slug = slugify(form.titulo.data)
            post.id_autor = current_user.id
            post.autor = Usuario.query.get(current_user.id)
            if request.files['imagem']:
                if (allowed_extension(request.files['imagem'].filename)):
                    img = request.files['imagem'].filename
                    post.imagem = os.path.join('uploads/', img)
                    upload()
                else:
                    flash('Apenas arquivos de imagem são válidos', category='warning')
            db.session.commit()
            flash('Alterado com sucesso!', category='success')
        return redirect(url_for('main.posts'))

    return render_template('forms/edit_post.html', form=form, post=post)