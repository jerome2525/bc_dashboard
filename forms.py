from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

#Product Category form
class ProductCategoryForm(FlaskForm):
    category_name = StringField('Category Name *', validators=[DataRequired()])
    product_ids = TextAreaField(u'Product IDs *',validators=[DataRequired(), Length(max=200)], render_kw={"placeholder": "TT21,TT20,TT23 no spacing between comma please"})
    fy_actual = StringField('FY Actual *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    new_growth = StringField('New Growth *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    growth_portions = StringField('Growth Portions*', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})

#Product Category delete form
class ProductCategoryDeleteForm(FlaskForm):
    cat_id = HiddenField('Cat ID *', validators=[DataRequired()])

#Product Category form Edit
class ProductCategoryEditForm(FlaskForm):
    category_id = HiddenField('Category ID *', validators=[DataRequired()])
    category_name = StringField('Category Name *', validators=[DataRequired()])
    product_ids = TextAreaField(u'Product IDs *',validators=[DataRequired(), Length(max=200)], render_kw={"placeholder": "TT21,TT20,TT23 no spacing between comma please"})
    fy_actual = StringField('FY Actual *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    new_growth = StringField('New Growth *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    growth_portions = StringField('Growth Portions*', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})


#Product Category form Edit
class MonthlyTargetForm(FlaskForm):
    jan = StringField('January *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    feb = StringField('February *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    mar = StringField('March *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    apr = StringField('April *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    may = StringField('May *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    june = StringField('June *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    july = StringField('July *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    aug = StringField('August *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    sept = StringField('September *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    october = StringField('October *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    nov = StringField('November *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})
    dec = StringField('December *', validators=[DataRequired()], render_kw={"placeholder": "please use plain number no comma, dot is valid"})


#Product Category form Edit
class ChangePassForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

