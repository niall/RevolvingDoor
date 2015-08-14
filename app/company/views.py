from . import company
from flask import render_template, flash, redirect, url_for
from app.models import Company, Site, SiteManager, Job, Role
from .forms import NewSiteForm, NewManagerForm, NewCompanyForm, NewJobForm
from flask.ext.login import login_required
from .. import db
from app.reg.utils import map_lookup

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
    cmp = Company.query.filter_by(**kwargs).first_or_404()
    managers = cmp.managers
    sites = cmp.sites.all()
    return render_template('company/company-profile.html', company=cmp, sites=sites, manager=managers)

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
        return redirect(url_for('company.company_profile', type='name', value=cmp.name))

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
        return redirect(url_for('company.company_profile', type='name', value=cmp.name))

    return render_template('company/add-site.html', form=form, name=cmp.name)

@company.route('/site/<id>')
def site_profile(id):
    site = Site.query.filter_by(id=id).first_or_404()
    cmp = Company.query.filter_by(id=site.company_id).first_or_404()
    map_url = map_lookup(site.postcode)
    jobs = site.jobs
    return render_template('company/site-profile.html', site=site, company=cmp, jobs=jobs, map_url=map_url)

@company.route('/<type>/<value>/new-job', methods=['GET', 'POST'])
def new_job(type, value):
    kwargs = {type: value}
    cmp = Company.query.filter_by(**kwargs).first_or_404()
    form = NewJobForm()

    form.site.choices = [(g.id, g.name) for g in cmp.sites.order_by('name')]
    form.role.choices = [(g.id, g.name) for g in Role.query.order_by('name')]
    if form.validate_on_submit():
        new_job=Job(
            site_id=form.site.data,
            role_id=form.role.data,
            start_date=form.start_date.data
        )
        db.session.add(new_job)
        flash('New ' + cmp.name + ' Job Added: ' + form.number.data)
        return redirect(url_for('company.site_profile', id=form.site.data))

    return render_template('company/add-job.html', form=form, company=cmp)

"""
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

"""