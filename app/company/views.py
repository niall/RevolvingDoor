from . import company
from flask import render_template, flash, redirect, url_for
from app.models import Company, Site, SiteManager
from .forms import NewSiteForm, NewManagerForm, NewCompanyForm
from flask.ext.login import login_required
from .. import db

@company.route('/')
@login_required
def company_index():
    companies = Company.query.order_by(Company.name.asc())
    return render_template('company/index.html', companies=companies)

@company.route('/new', methods=['GET', 'POST'])
def new_company():
    form = NewCompanyForm()
    if form.validate_on_submit():
        new_company = Company(form.name.data)
        db.session.add(new_company)
        flash('New Company Added: '+ new_company.name)
        return redirect(url_for('company.company_index'))
    return render_template('company/add-company.html', form=form)

@company.route('/<type>/<value>')
def company_profile(type, value):
    kwargs = {type: value}
    company = Company.query.filter_by(**kwargs).first_or_404()
    manager = company.managers
    return render_template('company/company-profile.html', company=company, manager=manager)

@company.route('/<type>/<value>/new-manager', methods=['GET', 'POST'])
def new_manager(type, value):
    kwargs = {type: value}
    cmp = Company.query.filter_by(**kwargs).first_or_404()
    form = NewManagerForm()
    if form.validate_on_submit():
        new_manager = SiteManager(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            company_id=cmp.id
        )
        db.session.add(new_manager)
        flash('New Manager for ' + cmp.name + ' Added: ' + new_manager.name)
        return redirect(url_for('company.company_index'))

    return render_template('company/add-manager.html', form=form, company=cmp)

@company.route('/<type>/<value>/new-site', methods=['GET', 'POST'])
def new_site(type, value):
    kwargs = {type: value}
    cmp = Company.query.filter_by(**kwargs).first_or_404()
    form = NewSiteForm()
    form.site_manager.choices = [(g.id, g.name) for g in SiteManager.query.filter_by(company_id=cmp.id).order_by('name')]
    if form.validate_on_submit():
        new_site = Site(
            name=form.name.data,
            address=form.address.data,
            start_time=form.start_time.data,
            company_id=cmp.id
        )
        manager = SiteManager.query.filter_by(id=form.site_manager.data).first()
        db.session.add(new_site)
        db.session.commit()
        manager.site_id = new_site.id
        db.session.add(manager)
        flash(cmp.name + ' Site Added: ' + new_site.name)
        return redirect(url_for('company.company_index'))

    return render_template('company/add-site.html', form=form, name=cmp.name)

@company.route('/site/<id>')
def site_profile(id):
    site = Site.query.filter_by(id=id).first_or_404()
    cmp = Company.query.filter_by(id=site.company_id).first_or_404()
    return render_template('company/site-profile.html', site=site, company=cmp)