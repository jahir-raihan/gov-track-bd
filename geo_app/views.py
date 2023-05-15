from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import UploadDetailsForm
from .models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
import pandas as pd


def get_time_range(objs):

    """Returns The Lowest time bound , and Highest time bounds for filtering in frontend."""

    start_dates = set()
    end_dates = set()
    for obj in objs:
        s = int(str(obj.start_date).split('-')[0])
        start_dates.add(s)
        end_dates.add(s + obj.timespan)

    return sorted(start_dates), sorted(end_dates)


@login_required
def home(request):

    """Main Driver Function for User data visualization and filtering with necessary information."""
    if not request.user.is_authenticated:
        cnt = CountAnn.objects.get(id=1)
        cnt.count += 1
        cnt.save()
    details = []
    category = {}
    start_dates, end_dates = get_time_range(Projects.objects.all())
    i = 0

    for data in Projects.objects.all():  # Getting details and category
        try:
            category[data.executing_agency.id].append(i)
        except:
            category[data.executing_agency.id] = [i]
        i += 1
        details.append(data)
    print(category)
    print(details)
    # When request  is POST

    if request.method == 'POST':    # When we filter in frontend it will send an POST request to backend

        filtered_details = []
        final_f_details = []
        if request.POST['category'] == '':
            for data in details:
                start = int(str(data.start_date).split('-')[0])
                filtered_details.append([data.project_name, data.id,start,
                                         start + int(data.timespan)])

        else:
            for idx in category[int(request.POST['category'])]:
                d_p = details[idx]
                start = int(str(d_p.start_date).split('-')[0])
                filtered_details.append([d_p.project_name, d_p.id, start,
                                         start + d_p.timespan])
        print(len(details))
        print(len(filtered_details))

        # Conditions for time range based filtering

        srt_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if srt_date != '' and end_date != '':
            for data in filtered_details:
                if data[2] >= int(srt_date) and data[3] <= int(end_date):
                    final_f_details.append(data)
        elif srt_date != '':
            for data in filtered_details:
                if data[2] >= int(srt_date):
                    final_f_details.append(data)
        elif end_date != '':
            for data in filtered_details:
                if data[3] <= int(end_date):
                    final_f_details.append(data)
        else:
            final_f_details = filtered_details

        data = {
            'details': final_f_details,
        }
        return JsonResponse(data)

    # When request is GET
    category = Agency.objects.all()
    context = {
        'details': details,
        'category': category,
        'start_dates': start_dates,
        'end_dates': end_dates
    }
    return render(request, 'home.html', context)


def get_percentage_amount_time(data):

    """This function calculates remaining time percentage against (end time - curr working days)"""

    start_date = datetime.strptime(str(data.project_start_time), '%Y-%m-%d')
    end_date = datetime.strptime(str(data.project_completion_time), '%Y-%m-%d')
    est_days = (end_date - start_date).days
    curr_date = datetime.now()

    time_remaining = (end_date - curr_date).days / est_days * 100
    return round(time_remaining, 2) if time_remaining > 0 else 0


from datetime import timedelta
@login_required
def get_details(request):

    """This Function will return the Project details along with location data in a viewable format."""

    if request.method == 'POST':    # When request is POST then we'll return coordinates and project details
        dp = Projects.objects.get(id=int(request.POST['project_id']))
        dt = datetime.strptime(f'{dp.start_date}', '%Y-%m-%d')
        dt2 = dt + timedelta(days=364*dp.timespan)
        print(dt2)
        project = [dp.project_name, dp.executing_agency.agency_name, dp.goal, dt.strftime('%d %B, %Y'),
                   dt2.strftime('%d %B, %Y'), f'<b>BDT  {dp.cost} crore</b>', f'<b>{dp.completion} %</b>',
                   dp.id,f'<b>{ dp.location } </b>']

        coordinates = [[dp.lat, dp.lng]]
        # pct_time = f'<b>{get_percentage_amount_time(dp)} % </b>   [Based on Estimated Date and Completed Days]'
        l_c = len(coordinates)
        data = {
            'project': project,
            'coordinates': coordinates,
            'l_c': l_c,
            # 'pct_time': pct_time,
            'csrf': request.META['CSRF_COOKIE']
        }
        return JsonResponse(data)


from django.http import HttpResponse
from django.template import loader


def get_data_in_csvf(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="reports.csv"'},
    )

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    proj = Projects.objects.get(pk=692)

    rows = [[proj.project_name], [proj.location], [proj.lat], [proj.lng], [proj.executing_agency.agency_name],
            [proj.cost], [proj.timespan], [proj.project_id], [proj.goal], [proj.start_date], [proj.completion],
            [proj.actual_cost]]
    for proj in Projects.objects.all():
        rows[0].append(proj.project_name)
        rows[1].append(proj.location)
        rows[2].append(proj.lat)
        rows[3].append(proj.lng)
        rows[4].append(proj.executing_agency.agency_name)
        rows[5].append(proj.cost)
        rows[6].append(proj.timespan)
        rows[7].append(proj.project_id)
        rows[7].append(proj.goal)
        rows[8].append(proj.start_date)
        rows[9].append(proj.completion)
        rows[10].append(proj.actual_cost)

    t = loader.get_template('reports.csv')
    c = {'data': rows}
    response.write(t.render(c))
    return response

import csv
from django.http import HttpResponse

def get_data_in_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    proj = Projects.objects.get(pk=692)

    rows = [[proj.project_name], [proj.location], [proj.lat], [proj.lng], [proj.executing_agency.agency_name],
            [proj.cost], [proj.timespan], [proj.project_id], [proj.goal], [proj.start_date], [proj.completion],
            [proj.actual_cost]]
    for proj in Projects.objects.all():
        rows[0].append(proj.project_name)
        rows[1].append(proj.location)
        rows[2].append(proj.lat)
        rows[3].append(proj.lng)
        rows[4].append(proj.executing_agency.agency_name)
        rows[5].append(proj.cost)
        rows[6].append(proj.timespan)
        rows[7].append(proj.project_id)
        rows[7].append(proj.goal)
        rows[8].append(proj.start_date)
        rows[9].append(proj.completion)
        rows[10].append(proj.actual_cost)

    writer.writerow(rows[0])
    writer.writerow(rows[1])
    writer.writerow(rows[2])
    writer.writerow(rows[3])
    writer.writerow(rows[4])
    writer.writerow(rows[5])
    writer.writerow(rows[6])
    writer.writerow(rows[7])
    writer.writerow(rows[8])
    writer.writerow(rows[9])
    writer.writerow(rows[10])



    return response
# Excluded
# This function is excluded right now , because of the csv file format


def get_file_upload_options(user):
    lst = ['Proposal File', 'Component', 'Agencies', 'Projects', 'Constraints']

    if user.is_EXEC:
        return lst[0:2]
    if user.is_SYSADMIN:
        return lst


def read_the_file(file, file_type):
    if file_type == 'Projects':
        data = pd.read_csv(file)
        length = data.shape[0]
        for i in range(length):
            agency = Agency.objects.get(agency_code=data['exec'][i])
            l = data['location'][i].strip()
            obj = Projects(project_name=data['name'][i], location=l, lat=data['latitude'][i],
                           lng=data['longitude'][i], executing_agency=agency, cost=data['cost'][i],
                           timespan=data['timespan'][i], project_id=data['project_id'][i], goal=data['goal'][i],
                           start_date=data['start_date'][i],
                           completion=data['completion'][i],
                           actual_cost=data['actual_cost'][i])

            try:
                loc = Locations.objects.filter(locations=l)[0]
                loc.count += 1
                loc.save()
            except:
                loc = Locations(location=l)
                loc.count += 1
                loc.save()

            agency.projects_running += 1
            agency.yearly_funding += data['cost'][i]
            agency.save()
            obj.save()

    elif file_type == 'Proposal File':
        data = pd.read_csv(file)
        length = data.shape[0]
        for i in range(length):
            agency = Agency.objects.get(agency_code=data['exec'][i])
            obj = Proposal(project_name=data['name'][i], location=data['location'][i], lat=data['latitude'][i],
                           lng=data['longitude'][i], executing_agency=agency, cost=data['cost'][i],
                           timespan=data['timespan'][i], project_id=data['project_id'][i], goal=data['goal'][i],
                           proposal_date=data['proposal_date'][i])
            obj.save()

    elif file_type == 'Component':

        # This part of the program is giving error.

        # csv_data = file
        #data = data.fillna('No Value')
        # Getting error at budget ratio.
        # print(data.head())
        # length = data.shape[0]
        pass

    elif file_type == 'Agencies':
        data = pd.read_csv(file)
        length = data.shape[0]
        for i in range(length):

            obj = Agency(agency_code=data['code'][i], agency_type=data['type'][i], agency_name=data['name'][i],
                         agency_description=data['description'][i])
            obj.save()

    elif file_type == 'Constraints':
        data = pd.read_csv(file)
        length = data.shape[0]
        for i in range(length):

            obj = Constraints(code=data['code'][i], max_limit=int(data['max_limit'][i]), constraint_type=data['constraint_type'][i])
            obj.save()
            cons = data['constraint_type'][i]
            if cons == 'executing_agency_limit':
                agency = Agency.objects.get(agency_code=data['code'][i])
                agency.max_running_project = int(data['max_limit'][i])
                agency.save()
            elif cons == 'location_limit':
                try:
                    loc = Locations.objects.get(location=data['code'][i])
                    loc.max_count = int(data['max_limit'][i])
                    loc.save()
                except:
                    loc = Locations.objects.create(location=data['code'][i])
                    loc.count += 1
                    loc.max_count = int(data['max_limit'][i])
                    loc.save()
            else:
                agency = Agency.objects.get(agency_code=data['code'][i])
                agency.max_yearly_funding = int(data['max_limit'][i])
                agency.save()


@login_required
def upload_details(request):

    """ This view uploads  files of different categories based on conditions and type provided."""
    if request.user.is_authenticated and (request.user.is_SYSADMIN or request.user.is_EXEC):

        option = get_file_upload_options(request.user)
        if request.method == 'POST':
            form = UploadDetailsForm(request.POST, request.FILES)

            if form.is_valid():
                fs = form.save()
                path = fs.file.url[1:]

                read_the_file(path, request.POST['file_type'])


                return render(request, 'user/register_other_roles_refresh.html', {'msg': 'Uploaded File Successfully !'})

        elif request.user.is_MOP:
            return render(request, 'admin/project_request.html')

        else:
            return render(request, 'upload-files.html', {'options': option})
    return redirect('home')


# End Excluded

def issue_form(request):

    """This one stores issues of a particular ongoing project, and counts it."""

    if request.method == 'POST':    # When request is POST
        det = Projects.objects.get(id=int(request.POST['id']))   # Get project object from database
        det.issue_set.create(issue=request.POST['issue'], rating=int(request.POST['rate']))   # Create Issue for the details
        det.issue_count += 1    # And increase the count of issues for this details object

        det.save()  # Finally save
    return HttpResponse('Success')  # This line doesn't make any sense


@login_required
def admin(request):

    """View specially for admin users, admin can search a project
        by title, agency or sort them by count of issues they have"""
    if request.user.is_authenticated and (request.user.is_SYSADMIN or request.user.is_EXEC):

        if request.method == 'POST':
            key = request.POST['keyword']
            if key == '' and 'sort' in request.POST:
                result = sorted(Projects.objects.all(), key=lambda x: x.issue_count, reverse=True)   # Sorting by issue

            elif key != '' and 'sort' in request.POST:
                data_points = Projects.objects.filter(
                    Q(project_name__startswith=key))
                result = sorted(data_points, key=lambda x: x.issue_count, reverse=True)
            else:
                result = Projects.objects.filter(
                    Q(project_name__startswith=key))
            final_result = []
            for data in result:
                final_result.append([data.project_name, data.id, data.issue_count])

            data = {
                'projects': final_result
            }
            return JsonResponse(data)

        return render(request, 'admin-page.html')
    return redirect('home')


@login_required
def get_admin_vizes(request):

    """Returns Map Geo Location for given  coordinates"""

    if request.method == 'POST':
        dp = Projects.objects.get(id=int(request.POST['id']))
        coordinates = [[dp.lat, dp.lng]]
        l_c = len(coordinates)
        data = {
            'coordinates': coordinates,
            'l_c': l_c
        }
        return JsonResponse(data)


# MOP section


def proposal_approval(request):
    if request.user.is_MOP:

        if request.method == 'POST':
            if request.POST['approval'] == 'decline':
                proposal = Proposal.objects.get(id=int(request.POST['id']))
                proposal.hold = True
                proposal.save()
                data = {
                    'id': proposal.id,
                    'template': '<p style="text-align:center">Proposal on Hold ! </p>'
                }
                return JsonResponse(data)
            else:

                p = Proposal.objects.get(id=int(request.POST['id']))
                p.approved = True
                p.save()
                proj_id = p.project_id[:3]+'j' + p.project_id[4:]
                project = Projects(project_name=p.project_name, location=p.location, lat=p.lat,
                                   lng=p.lng, executing_agency=p.executing_agency, cost=p.cost,
                                   timespan=p.timespan, project_id=proj_id, goal=p.goal,
                                   start_date=request.POST['date'],
                                   completion=0,
                                   actual_cost=0)
                try:
                    loc = Locations.objects.get(location=p.location)
                    loc.count += 1
                    loc.save()

                except:
                    loc = Locations(location=p.location)
                    loc.count += 1
                    loc.save()

                project.save()

                data = {
                    'id': p.id,
                    'template': '<p style="text-align:center">Proposal Approved ! </p>'
                }
                return JsonResponse(data)

        un_approved_projects = Proposal.objects.filter(approved=False)



        context = {
            'proposals': un_approved_projects,


        }
        return render(request, 'proposals.html', context)
