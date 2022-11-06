#Import Flask
from flask import render_template, jsonify, flash, redirect, url_for, session
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

#ALL PAGES
#Tegral
@app.route("/")
def tg_page(): 
    #redirect if not logged
    if not session.get('dashboard_user'):
        return redirect(url_for('login_page'))
    #generate db table
    model_tegral.create_myob_db()  
    date_axis = sales_axis = pipe_axis = year_axis = [0] 
    #get tg sales
    data_sales = model_tegral.get_data('sales')  
    if data_sales:
        date_axis = [row[2] for row in data_sales] 
        sales_axis = [row[1] for row in data_sales] 

    #get tg pipe
    data_pipe = model_tegral.get_data('pipeline')
    if data_pipe:  
        pipe_axis = [row[1] for row in data_pipe] 
    
    #get year target
    data_year_target = model_tegral.get_data('yeartarget')   
    if data_year_target:
        year_axis = [row[1] for row in data_year_target]

    invoice_yesterday_dollar = sales_invoice_dollar = month_potential_dollar = pipeline_dollar = sample_sent = refresh_flag = 0     
    
    #tegral invoice yesterday
    invoice_yesterday = model_tegral.get_myob_invoice_data_yesterday() - model_tegral.get_myob_invoice_data_before_yesterday()
    
    #convert to dollar
    invoice_yesterday_dollar =  "${:,.2f}".format(invoice_yesterday)

    #sales invoice
    sales_invoice_dollar = "${:,.2f}".format(model_tegral.get_myob_invoice_data_today())

    #month potential
    month_potential_dollar = "${:,.2f}".format(model_tegral.get_myob_month_potential())

    #pipeline variable for tegral
    pipeline = model_tegral.get_myob_orders_computed_pipeline()//1.1
    pipeline_dollar = "${:,.2f}".format(pipeline)

    #sample sent
    sample_sent = model_tegral.get_myob_invoice_sample_sent()

    #refresh flag
    refresh_flag = model_tegral.get_refresh_flag()
    
    #pipedrive
    pipedrive=pipe.get_pipedrive_count(41)

    #email contacts
    email_contacts=model_tegral.get_email_contact_count()

    #render template    
    return render_template('tegral.html', date_axis=date_axis, sales_axis=sales_axis, pipe_axis=pipe_axis, year_axis=year_axis, 
    invoice_yesterday=invoice_yesterday_dollar, sales_invoice=sales_invoice_dollar, month_potential=month_potential_dollar, pipeline=pipeline_dollar,
    pipedrive=pipedrive, sample_sent=sample_sent, email_contacts=email_contacts, refresh_flag=refresh_flag, userlogin=session.get('dashboard_user'), title='Tegral Dashboard')

#Purific Dashboard
@app.route("/purific")
def pr_page(): 
    #redirect if not logged
    if not session.get('dashboard_user'):
        return redirect(url_for('login_page'))
    #generate db table
    model_purific.create_myob_db()   
    date_axis = sales_axis = pipe_axis = year_axis = [0] 
    #get tg sales
    data_sales = model_purific.get_data('sales')  
    if data_sales:
        date_axis = [row[2] for row in data_sales] 
        sales_axis = [row[1] for row in data_sales] 

    #get tg pipe
    data_pipe = model_purific.get_data('pipeline')
    if data_pipe:  
        pipe_axis = [row[1] for row in data_pipe] 
    
    #get year target
    data_year_target = model_purific.get_data('yeartarget')   
    if data_year_target:
        year_axis = [row[1] for row in data_year_target]
    invoice_yesterday_dollar = sales_invoice_dollar = month_potential_dollar = pipeline_dollar = sample_sent = refresh_flag = 0

    #tegral invoice yesterday
    invoice_yesterday = model_purific.get_myob_invoice_data_yesterday() - model_purific.get_myob_invoice_data_before_yesterday()
    
    #convert to dollar
    invoice_yesterday_dollar =  "${:,.2f}".format(invoice_yesterday)

    #sales invoice
    sales_invoice_dollar = "${:,.2f}".format(model_purific.get_myob_invoice_data_today())

    #month potential
    month_potential_dollar = "${:,.2f}".format(model_purific.get_myob_month_potential())

    #pipeline variable for tegral
    pipeline = model_purific.get_myob_orders_computed_pipeline()//1.1
    pipeline_dollar = "${:,.2f}".format(pipeline)

    #sample sent
    sample_sent = model_purific.get_myob_invoice_sample_sent()

    #refresh flag
    refresh_flag = model_purific.get_refresh_flag()

    #pipedrive
    pipedrive=pipe.get_pipedrive_count(41)

    #email contacts
    email_contacts=model_tegral.get_email_contact_count()

    #render template    
    return render_template('purific.html', date_axis=date_axis, sales_axis=sales_axis, pipe_axis=pipe_axis, year_axis=year_axis, 
    invoice_yesterday=invoice_yesterday_dollar, sales_invoice=sales_invoice_dollar, month_potential=month_potential_dollar, pipeline=pipeline_dollar,
    pipedrive=pipedrive, sample_sent=sample_sent, email_contacts=email_contacts, refresh_flag=refresh_flag, userlogin=session.get('dashboard_user'), title='Purific Dashboard')


#Login Dashboard
@app.route("/login", methods=['GET', 'POST'])
def login_page(): 
    #redirect if logged
    if session.get('dashboard_user'):
        return redirect(url_for('tg_page'))
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


#Combined Dashboard
@app.route("/combined")
def cm_page(): 
    #redirect if not logged
    if not session.get('dashboard_user'):
        return redirect(url_for('login_page'))
    #generate db table
    combined.create_table_db()   

    #refresh data
    combined.refresh() 

    date_axis = sales_axis = pipe_axis = year_axis = [0] 
    invoice_yesterday_dollar = sales_invoice_dollar = month_potential_dollar = pipeline_dollar = sample_sent = 0
    #get tg sales
    data_sales = combined.get_data('sales')  
    if data_sales:
        date_axis = [row[2] for row in data_sales] 
        sales_axis = [row[1] for row in data_sales] 

    #get tg pipe
    data_pipe = combined.get_data('pipeline')
    if data_pipe:  
        pipe_axis = [row[1] for row in data_pipe] 
    
    #get year target
    data_year_target = combined.get_data('yeartarget')   
    if data_year_target:
        year_axis = [row[1] for row in data_year_target] 

    #tegral invoice yesterday
    invoice_yesterday = model_tegral.get_myob_invoice_data_yesterday() - model_tegral.get_myob_invoice_data_before_yesterday()

    #purific invoice yesterday
    invoice_yesterday_purific = model_purific.get_myob_invoice_data_yesterday() - model_purific.get_myob_invoice_data_before_yesterday()


    #invoice yesterday variable combined
    invoice_yesterday_combined = invoice_yesterday + invoice_yesterday_purific

    #convert to dollar
    invoice_yesterday_dollar =  "${:,.2f}".format(invoice_yesterday_combined)

    #sales invoice
    sales_invoice_dollar = "${:,.2f}".format(model_purific.get_myob_invoice_data_today() + model_tegral.get_myob_invoice_data_today())

    #month potential
    month_potential_dollar = "${:,.2f}".format(model_purific.get_myob_month_potential() + model_tegral.get_myob_month_potential())

    #pipeline variable for purific
    pipeline_pr = model_purific.get_myob_orders_computed_pipeline()//1.1

    #pipeline variable for tegral
    pipeline_tg = model_tegral.get_myob_orders_computed_pipeline()//1.1

    pipeline_dollar = "${:,.2f}".format(pipeline_tg + pipeline_pr)

    #sample sent
    sample_sent = model_purific.get_myob_invoice_sample_sent() + model_tegral.get_myob_invoice_sample_sent()

    #pipedrive
    pipedrive=pipe.get_pipedrive_count(41)

    #email contacts
    email_contacts=model_tegral.get_email_contact_count()

    #render template    
    return render_template('combined.html', date_axis=date_axis, sales_axis=sales_axis, pipe_axis=pipe_axis, year_axis=year_axis, 
    invoice_yesterday=invoice_yesterday_dollar, sales_invoice=sales_invoice_dollar, month_potential=month_potential_dollar, pipeline=pipeline_dollar,
    pipedrive=pipedrive, sample_sent=sample_sent, email_contacts=email_contacts, userlogin=session.get('dashboard_user'), title='Combined Dashboard')


#Product Dashboard
@app.route("/products")
def tg_products(): 
    #redirect if not logged
    if not session.get('dashboard_user'):
        return redirect(url_for('login_page'))

    #title of the page
    title='Monthly Product Dashboard'
    
    #set default variable data for axis
    product_name_axis_month = product_sales_axis_month = product_month_target_axis_month = [0]
    
    #create db table for products
    model_tegral.create_myob_product_db()

    #refresh flag
    refresh_flag = model_tegral.get_product_refresh_flag()

    #monthly
    # get tg sales send to graph
    data_sales_month = model_tegral.get_product_monthly_base_cat('total') 
    data_name_month = model_tegral.get_product_monthly_base_cat('category') 
    data_month_target = model_tegral.get_product_monthly_base_cat('month_target') 
    if data_sales_month and data_name_month and data_month_target:
        product_name_axis_month = [row[0] for row in data_name_month] 
        product_sales_axis_month = [row[0] for row in data_sales_month] 
        product_month_target_axis_month = [row[0] for row in data_month_target] 


    #render template    
    return render_template('products.html', product_name_axis_month=product_name_axis_month, product_sales_axis_month=product_sales_axis_month, product_month_target_axis_month=product_month_target_axis_month, userlogin=session.get('dashboard_user'), refresh_flag=refresh_flag, title=title)

#Product Dashboard
@app.route("/products-yearly")
def tg_products_yearly(): 
    #redirect if not logged
    if not session.get('dashboard_user'):
        return redirect(url_for('login_page'))

    #title of the page
    title='Yearly Product Dashboard'
    
    #set default variable data for axis
    product_name_axis_yearly = product_sales_axis_yearly = product_month_target_axis_yearly = [0]
    
    #create db table for products
    model_tegral.create_myob_product_db()

    #yearly
    data_sales_yearly = model_tegral.get_product_yearly_base_cat('total') 
    data_name_yearly = model_tegral.get_product_yearly_base_cat('category') 
    data_year_target = model_tegral.get_product_yearly_base_cat('year_target')
    if data_sales_yearly and data_name_yearly and data_year_target:
        product_name_axis_yearly = [row[0] for row in data_name_yearly] 
        product_sales_axis_yearly = [row[0] for row in data_sales_yearly] 
        product_month_target_axis_yearly = [row[0] for row in data_year_target] 


    #render template    
    return render_template('products-yearly.html', product_name_axis_year=product_name_axis_yearly, product_sales_axis_year=product_sales_axis_yearly, product_month_target_axis_year=product_month_target_axis_yearly, userlogin=session.get('dashboard_user'), title=title)


#Product add category
@app.route("/products/addcategory")
def add_category(): 
    #redirect if not logged
    if not session.get('dashboard_user'):
        return redirect(url_for('login_page'))
    form = ProductCategoryForm()
    del_form = ProductCategoryDeleteForm()
    
    #get cat list
    cat_list = model_tegral.get_product_category_list()
    #render template    
    return render_template('add-product-category.html', title='Add Product Category', form=form, cat_list=cat_list, del_form=del_form, userlogin=session.get('dashboard_user'))


#Tegral Add Monthly Target
@app.route("/add-monthly-target")
def add_monthly_target(): 
    #redirect if not logged
    if not session.get('dashboard_user'):
        return redirect(url_for('login_page'))
    
    #Tegral
    jan = model_tegral.get_default_month_fields(1)
    feb = model_tegral.get_default_month_fields(2)
    march = model_tegral.get_default_month_fields(3)
    apr = model_tegral.get_default_month_fields(4)
    may = model_tegral.get_default_month_fields(5)
    jun = model_tegral.get_default_month_fields(6)
    jul = model_tegral.get_default_month_fields(7)
    aug = model_tegral.get_default_month_fields(8)
    sept = model_tegral.get_default_month_fields(9)
    oct = model_tegral.get_default_month_fields(10)
    nov = model_tegral.get_default_month_fields(11)
    dec = model_tegral.get_default_month_fields(12)
    form = MonthlyTargetForm(jan=jan, feb=feb, mar=march, apr=apr, may=may, june=jun, july=jul, aug=aug, sept=sept, october=oct, nov=nov, dec=dec)

    #Purific
    pur_jan = model_purific.get_default_month_fields(1)
    pur_feb = model_purific.get_default_month_fields(2)
    pur_march = model_purific.get_default_month_fields(3)
    pur_apr = model_purific.get_default_month_fields(4)
    pur_may = model_purific.get_default_month_fields(5)
    pur_jun = model_purific.get_default_month_fields(6)
    pur_jul = model_purific.get_default_month_fields(7)
    pur_aug = model_purific.get_default_month_fields(8)
    pur_sept = model_purific.get_default_month_fields(9)
    pur_oct = model_purific.get_default_month_fields(10)
    pur_nov = model_purific.get_default_month_fields(11)
    pur_dec = model_purific.get_default_month_fields(12)
    pur_form = MonthlyTargetForm(jan=pur_jan, feb=pur_feb, mar=pur_march, apr=pur_apr, may=pur_may, june=pur_jun, july=pur_jul, aug=pur_aug, sept=pur_sept, october=pur_oct, nov=pur_nov, dec=pur_dec)
    
    #render template    
    return render_template('tegral-add-monthly-target.html', title='Monthly Target', tegral_title='Tegral Monthly Target', purific_title='Purific Monthly Target', form=form, pur_form=pur_form, userlogin=session.get('dashboard_user') )


#Product add category
@app.route("/products/editcategory/<category_id>")
def edit_category(category_id): 
    #redirect if not logged
    if not session.get('dashboard_user'):
        return redirect(url_for('login_page'))
    product_ids_default = model_tegral.get_default_product_fields( 'product_ids', category_id )
    category_name_default = model_tegral.get_default_product_fields( 'product_category', category_id )
    fy_actual_default = model_tegral.get_default_product_fields( 'fy_actual', category_id )
    new_growth_default = model_tegral.get_default_product_fields( 'new_growth', category_id )
    growth_portion_default = model_tegral.get_default_product_fields( 'growth_portions', category_id )
    form = ProductCategoryEditForm(category_id=category_id, category_name=category_name_default, product_ids=product_ids_default, fy_actual=fy_actual_default, new_growth=new_growth_default, growth_portions=growth_portion_default)
    return render_template('edit-product-category.html', title='Edit Product Category', form=form, userlogin=session.get('dashboard_user'))

#Sales Team Dashboard
@app.route("/sales-team")
def sales_team(): 
    #redirect if not logged
    if not session.get('dashboard_user'):
        return redirect(url_for('login_page'))

    #title of the page
    title='Sales Team Dashboard'
    
    #set default variable data for axis
    callers_axis = success_call_axis = attempted_call_axis = voicemail_call_axis = [0]
    try:
        #create db table for products
        pipe.create_db()
        #refresh data
        pipe.refresh()
    except:
        return redirect(url_for('login_page'))

    #monthly
    # get tg sales send to graph
    callers = pipe.get_caller_graph('caller_name')
    success_call = pipe.get_caller_graph('success_status')
    attempted_call = pipe.get_caller_graph('attempt_status')
    voicemail_call = pipe.get_caller_graph('voicemail_status')
    if callers and success_call and attempted_call and voicemail_call:
        callers_axis = [row[0] for row in callers] 
        success_call_axis = [row[0] for row in success_call] 
        attempted_call_axis = [row[0] for row in attempted_call] 
        voicemail_call_axis = [row[0] for row in voicemail_call] 

    #render template    
    return render_template('sales-team.html', callers_axis = callers_axis, success_call_axis=success_call_axis, attempted_call_axis=attempted_call_axis,voicemail_call_axis=voicemail_call_axis,title=title,userlogin=session.get('dashboard_user'))


#Sales Team Dashboard
@app.route("/profile")
def profile(): 
    form = ChangePassForm()
    #redirect if not logged
    #if not session.get('dashboard_user'):
        #return redirect(url_for('login_page'))
    return render_template('profile.html', title='Profile', form=form, userlogin=session.get('dashboard_user'))
