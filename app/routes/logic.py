from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from app.forms import CreatePostForm, RegisterForm, LogInForm, CommentForm, ContactForm
from app.models.models import BlogPost, User, Comments

def show_post(post_id):
    form = CommentForm()

    if form.validate_on_submit():

        # add comment to the appropriate table
        # Verify if the user if logged first

        comment = request.form.get("comment")

        new_comment =  Comments(
            text=comment,
            user_id=current_user.id,
            post_id=post_id,
        )

        db.session.add(new_comment)
        db.session.commit()

    requested_post = BlogPost.query.get(post_id)
    return render_template(
        "post.html",
        post=requested_post,
        form=form,
        comments=requested_post.comments
    )

def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('blueprint.home'))

def update_post(post_id):

    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("blueprint.show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)

def create_post():

    form = CreatePostForm()
    if form.validate_on_submit():

        new_post = BlogPost(
            author=current_user.name,
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=date.today().strftime("%B %d, %Y"),
            body=form.body.data,
            img_url=form.img_url.data,
            user_id=current_user.id,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("blueprint.home"))
    return render_template("make-post.html", form=form)

