import os

from flask import render_template, abort, redirect, url_for, request
from flask_login import current_user, login_required
from werkzeug.datastructures import MultiDict
from werkzeug.utils import secure_filename

from app import app, db, login_manager
from forms import GoodsForm
from models import Good, Like, Comment


@app.route('/goods')
def goods_view():
    manufacturer_par = request.args.get('manufacturer')
    category_par = request.args.get('category')
    order_par = request.args.get('order_by')

    filters = (('manufacturer', manufacturer_par), ('category', category_par))
    filters = dict(filter(lambda x: x[1] and x[1] not in ('Все производители', 'Все категории'), filters))

    categories = sorted(list({good.category for good in Good.query.all()}))
    manufacturers = sorted(list({good.manufacturer for good in Good.query.all()}))

    score_asc = 'score_asc'
    score_desc = 'score_desc'
    orders = {
        'По названию': Good.name.asc(),
        'По возрастанию цены': Good.price.asc(),
        'По убыванию цены': Good.price.desc(),
        'По возрастанию оценки': score_asc,
        'По убыванию оценки': score_desc
    }

    selectors = {
        'orders': orders.keys(),
        'manufacturers': ['Все производители'] + manufacturers,
        'categories': ['Все категории'] + categories,
    }

    if manufacturer_par in manufacturers:
        manufacturers.remove(manufacturer_par)
        selectors['manufacturers'] = [manufacturer_par, 'Все производители', *manufacturers]

    if category_par in categories:
        categories.remove(category_par)
        selectors['categories'] = [category_par, 'Все категории', *categories]

    if order_par and order_par in orders.keys():
        orders_list = list(orders.keys())
        orders_list.remove(order_par)
        selectors['orders'] = [order_par, *orders_list]
    else:
        order_par = 'По названию'

    if orders[order_par] in (score_desc, score_asc):
        goods = Good.query.filter_by(**filters).all()
        goods = sorted(goods,
                       key=lambda x: (sum([i.score for i in x.likes]) / len(x.likes)) if (len(x.likes) > 0) else 0)
        if orders[order_par] == score_desc:
            goods.reverse()
    else:
        goods = Good.query.filter_by(**filters).order_by(orders[order_par]).all()

    for i in range(len(goods)):
        goods[i].like_average = sum([x.score for x in goods[i].likes]) / len(goods[i].likes) if (
                    len(goods[i].likes) > 0) else 0

    return render_template('goods.html', goods=goods, selectors=selectors)


@app.route('/goods/<int:good_id>')
def good_view(good_id):
    like = None
    good = Good.query.filter_by(id=good_id).first()

    if current_user.is_authenticated:
        like = Like.query.filter_by(user_id=current_user.id, good_id=good_id).first()
        if like:
            like = like.score
        else:
            like = 0

    comments = Comment.query.filter_by(good_id=good_id)

    good.photo = f'photos/{good.photo}'

    return render_template('good.html', good=good, title=good.name, like=like, comments=comments)


@app.route('/goods/<int:good_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_good_view(good_id):
    if not current_user.is_admin:
        abort(403)

    good = Good.query.filter_by(id=good_id).first()
    form = GoodsForm()

    if form.is_submitted():
        good.name = form.name.data
        good.description = form.description.data
        good.category = form.category.data
        good.manufacturer = form.manufacturer.data
        good.price = form.price.data

        photo = form.photo.data
        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(
                app.config['UPLOAD_FOLDER'], 'photos', filename
            ))

            good.photo = filename

        db.session.commit()

        return redirect(url_for('good_view', good_id=good_id))

    data = {
        'name': good.name,
        'description': good.description,
        'category': good.category,
        'manufacturer': good.manufacturer,
        'price': good.price,
    }
    form = GoodsForm(formdata=MultiDict(data))

    return render_template('edit_good.html', form=form, title=f'Изменить товар {good.name}')


@app.route('/goods/<int:good_id>/delete')
@login_required
def delete_good_view(good_id):
    if not current_user.is_admin:
        abort(403)

    good = Good.query.filter_by(id=good_id).first()
    for i in Like.query.filter_by(good_id=good.id).all():
        db.session.delete(i)
    for i in Comment.query.filter_by(good_id=good.id).all():
        db.session.delete(i)

    db.session.delete(good)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/add_good', methods=['GET', 'POST'])
@login_required
def add_good_view():
    if not current_user.is_admin:
        abort(403)

    form = GoodsForm()

    if form.is_submitted():
        name = form.name.data
        description = form.description.data
        category = form.category.data
        manufacturer = form.manufacturer.data
        price = form.price.data
        photo = form.photo.data

        filename = secure_filename(photo.filename)
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], 'photos', filename
        ))

        Good.add(name, description, category, manufacturer, price, filename)
        return redirect(url_for('index'))

    return render_template("add_good.html", form=form, title="Добавить товар")


@app.route('/goods/like', methods=['POST'])
@login_required
def like_view():
    data = request.get_json()
    user_id = data['user_id']
    good_id = data['good_id']
    score = data['score']

    if like := Like.query.filter_by(user_id=user_id, good_id=good_id).first():
        like.score = score
    else:
        Like.add(user_id=user_id, good_id=good_id, score=score)
    db.session.commit()

    return "{'status': 'success'}"


@app.route('/goods/comment', methods=['POST'])
@login_required
def comment_view():
    data = request.get_json()
    user_id = data['user_id']
    good_id = data['good_id']
    comment = data['comment']

    Comment.add(user_id=user_id, good_id=good_id, comment=comment)
    db.session.commit()

    return "{'status': 'success'}"

# TODO AJAX get category
