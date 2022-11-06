#Import Flask
from flask import jsonify, redirect, url_for, session
from datetime import timedelta
import os
#Import main app
from __main__ import app

app.secret_key = os.urandom(32)
app.permanent_session_lifetime = timedelta(days=30)

#Import all class models
from models import *
model_tegral = Brands('tegral')
model_purific = Brands('purific')
combined = CombinedBrands()
form_process = Forms()
pipe = Pipedrive()

#Import forms
from forms import LoginForm, ProductCategoryForm, ProductCategoryDeleteForm, ProductCategoryEditForm, MonthlyTargetForm, ChangePassForm


#AJAX CALLS
#tegral ajax
@app.route('/tg_add_invoice')
def tg_add_invoice():
    try:
        model_tegral.refresh()
        er_message = 'SUCCESS'
    except:
        er_message = 'FAILED'
    return jsonify(result=er_message)

#purific ajax
@app.route('/pr_add_invoice')
def pr_add_invoice():
    try:
        model_purific.refresh()
        er_message = 'SUCCESS'
    except:
        er_message = 'FAILED'
    return jsonify(result=er_message)

#tegral product ajax
@app.route('/tg_product_refresh')
def tg_product_refresh():
    try:
        model_tegral.refresh_product()
        er_message = 'SUCCESS'
    except:
        er_message = 'FAILED'
    return jsonify(result=er_message)

#Login ajax process
@app.route("/login-process/", methods=['POST'])
def login_process():
    form = LoginForm()
    if form.validate_on_submit():
        username_check = form_process.check_username(form.username.data)
        password_check = form_process.check_password(form.username.data, form.password.data)
        if username_check and password_check:
            session["dashboard_user"] = username_check
            return jsonify(result='success')
    return jsonify(result='Invalid Username/Password!')

#logout URL
@app.route("/logout")
def logout():
    session.pop("dashboard_user", None)
    return redirect(url_for('login_page'))

#logout URL
@app.route("/category-process/", methods=['POST'])
def add_product_category_process():
    form = ProductCategoryForm()
    if form.validate_on_submit():
        cat_name = form.category_name.data
        product_ids = form.product_ids.data
        fy_actual = form.fy_actual.data
        new_growth = form.new_growth.data
        growth_portions = form.growth_portions.data
        if not fy_actual.isdigit():
            return jsonify(result='FY_ACTUAL_INVALID')
        if not new_growth.isdigit():
            return jsonify(result='NEW_GROWTH_INVALID')
        if not growth_portions.isdigit():
            return jsonify(result='GROWTH_PORTIONS_INVALID')
        if cat_name and product_ids:
            if model_tegral.check_product_category_exists(cat_name):
                return jsonify(result='DUPLICATE')
            model_tegral.insert_product_categories(cat_name, product_ids.upper(), fy_actual, new_growth, growth_portions)
            return jsonify(result='SUCCESS')
    return jsonify(result='ERROR')

#Edit product category process
@app.route("/edit-category-process/", methods=['POST'])
def edit_product_category_process():
    form = ProductCategoryEditForm()
    if form.validate_on_submit():
        category_id = form.category_id.data
        cat_name = form.category_name.data
        product_ids = form.product_ids.data
        fy_actual = form.fy_actual.data
        new_growth = form.new_growth.data
        growth_portions = form.growth_portions.data
        if not fy_actual.isdigit():
            return jsonify(result='FY_ACTUAL_INVALID')
        if not new_growth.isdigit():
            return jsonify(result='NEW_GROWTH_INVALID')
        if not growth_portions.isdigit():
            return jsonify(result='GROWTH_PORTIONS_INVALID')
        if category_id:
            model_tegral.update_product_categories(category_id, cat_name, product_ids.upper(), fy_actual, new_growth, growth_portions)
            return jsonify(result='SUCCESS')
    return jsonify(result='ERROR')


#Update month target process tegral
@app.route("/tg-update-month-target-process/", methods=['POST'])
def tg_update_month_target_process():
    form = MonthlyTargetForm()
    if form.validate_on_submit():
        jan = form.jan.data
        feb = form.feb.data
        mar = form.mar.data
        apr = form.apr.data
        may = form.may.data
        june = form.june.data
        july = form.july.data
        aug = form.aug.data
        sept = form.sept.data
        oct = form.october.data
        nov = form.nov.data
        dec = form.dec.data
        if jan:
            model_tegral.update_monthly_target(jan, 1)
        if feb:
            model_tegral.update_monthly_target(feb, 2)
        if mar:
            model_tegral.update_monthly_target(mar, 3)
        if apr:
            model_tegral.update_monthly_target(apr, 4)
        if may:
            model_tegral.update_monthly_target(may, 5)
        if june:
            model_tegral.update_monthly_target(june, 6)
        if july:
            model_tegral.update_monthly_target(july, 7)
        if aug:
            model_tegral.update_monthly_target(aug, 8)
        if sept:
            model_tegral.update_monthly_target(sept, 9)
        if oct:
            model_tegral.update_monthly_target(oct, 10)
        if nov:
            model_tegral.update_monthly_target(nov, 11)
        if dec:
            model_tegral.update_monthly_target(dec, 12)
            
        return jsonify(result='SUCCESS')
    return jsonify(result='ERROR')

#Update month target process purific
@app.route("/pr-update-month-target-process/", methods=['POST'])
def pr_update_month_target_process():
    form = MonthlyTargetForm()
    if form.validate_on_submit():
        jan = form.jan.data
        feb = form.feb.data
        mar = form.mar.data
        apr = form.apr.data
        may = form.may.data
        june = form.june.data
        july = form.july.data
        aug = form.aug.data
        sept = form.sept.data
        oct = form.october.data
        nov = form.nov.data
        dec = form.dec.data
        if jan:
            model_purific.update_monthly_target(jan, 1)
        if feb:
            model_purific.update_monthly_target(feb, 2)
        if mar:
            model_purific.update_monthly_target(mar, 3)
        if apr:
            model_purific.update_monthly_target(apr, 4)
        if may:
            model_purific.update_monthly_target(may, 5)
        if june:
            model_purific.update_monthly_target(june, 6)
        if july:
            model_purific.update_monthly_target(july, 7)
        if aug:
            model_purific.update_monthly_target(aug, 8)
        if sept:
            model_purific.update_monthly_target(sept, 9)
        if oct:
            model_purific.update_monthly_target(oct, 10)
        if nov:
            model_purific.update_monthly_target(nov, 11)
        if dec:
            model_purific.update_monthly_target(dec, 12)
            
        return jsonify(result='SUCCESS')
    return jsonify(result='ERROR')

@app.route("/delete-product-process/", methods=['GET', 'POST'])
def delete_product_category():
    form = ProductCategoryDeleteForm()
    if form.validate_on_submit():
        cat_id = form.cat_id.data
        if cat_id:
            model_tegral.delete_product_categories(cat_id)
            return jsonify(result='SUCCESS')
    return jsonify(result='ERROR')


@app.route("/password-change-process/", methods=['GET', 'POST'])
def password_change_process():
    form = ChangePassForm()
    if form.validate_on_submit():
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password == confirm_password:
            if session.get('dashboard_user'):
                form_process.change_password(session.get('dashboard_user'), password)
                return jsonify(result='SUCCESS')
    return jsonify(result='ERROR')