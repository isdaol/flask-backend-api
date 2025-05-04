from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from forms import ItemForm, UploadFileForm
from models import Item, db
from flask_login import login_required, current_user
import os
from config import Config
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    items = Item.query.all()
    return render_template('main/index.html', items=items)

@main_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, description=form.description.data)
        db.session.add(item)
        db.session.commit()
        flash('Элемент успешно создан!', 'success')
        return redirect(url_for('main.index'))
    return render_template('main/create.html', title='Создать', form=form)

@main_bp.route('/item/<int:item_id>')
def read(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('main/read.html', item=item)

@main_bp.route('/update/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update(item_id):
    item = Item.query.get_or_404(item_id)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        db.session.commit()
        flash('Элемент успешно обновлен!', 'success')
        return redirect(url_for('main.read', item_id=item.id))
    return render_template('main/update.html', title='Редактировать', form=form, item=item)  

@main_bp.route('/delete/<int:item_id>', methods=['POST'])
@login_required
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Элемент успешно удален!', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            flash(f'Файл "{filename}" успешно загружен!', 'success')
            return redirect(url_for('main.index'))
    return render_template('main/upload.html', title='Загрузка файла', form=form)

@main_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search']
        results = Item.query.filter(db.or_(Item.name.contains(search_term), Item.description.contains(search_term))).all()
        return render_template('main/index.html', items=results, search_term=search_term)
    return render_template('main/search.html', title='Поиск')