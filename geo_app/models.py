from django.db import models


class UploadFile(models.Model):

    """This model is for the file"""
    file_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='files')

    def __str__(self):
        return f'{self.file_type} Data'


class Details(models.Model):

    """This model will hold the project details"""

    project_name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    affiliated_agency = models.CharField(max_length=500)
    description = models.TextField()
    project_start_time = models.DateField()
    project_completion_time = models.DateField()
    total_budget = models.IntegerField()
    completion_percentage = models.FloatField()
    issue_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Details of {self.project_name} "


class Coordinates(models.Model):

    """This one holds coordinates information for a project."""

    details = models.ForeignKey(Details, on_delete=models.CASCADE)

    lng = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)





class CountAnn(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'User visited { self.count}'


class Agency(models.Model):
    agency_code = models.CharField(max_length=20)
    agency_type = models.CharField(max_length=30)
    agency_name = models.CharField(max_length=200)
    agency_description = models.CharField(max_length=300)
    projects_running = models.IntegerField(default=0)
    max_running_project = models.IntegerField(default=0)
    yearly_funding = models.IntegerField(default=0)
    location_limit = models.IntegerField(default=0)
    spent = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.agency_name} type = {self.agency_type}'


class Projects(models.Model):
    project_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)
    executing_agency = models.ForeignKey(Agency, on_delete=models.DO_NOTHING)
    cost = models.IntegerField()
    timespan = models.IntegerField()
    project_id = models.CharField(max_length=20)
    goal = models.CharField(max_length=200)
    start_date = models.DateField()
    completion = models.FloatField()
    actual_cost = models.FloatField()

    issue_count = models.IntegerField(default=0)


class Proposal(models.Model):
    project_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)
    executing_agency = models.ForeignKey(Agency, on_delete=models.DO_NOTHING)
    cost = models.IntegerField()
    timespan = models.IntegerField()
    project_id = models.CharField(max_length=20)
    goal = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)
    proposal_date = models.DateField()

    hold = models.BooleanField(default=True)
    recommendation = models.CharField(max_length=200, null=True, blank=True)


class Components(models.Model):
    project = models.CharField(max_length=20)
    executing_agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    component_id = models.CharField(max_length=30)
    depends_on = models.CharField(max_length=30, null=True, blank=True)
    component_type = models.CharField(max_length=50)
    budget_ratio = models.FloatField()

    is_project = models.BooleanField(default=False)


class Constraints(models.Model):
    code = models.CharField(max_length=20)
    max_limit = models.IntegerField()
    constraint_type = models.CharField(max_length=80)

    def __str__(self):
        return f'{self.code}s constraint on {self.constraint_type}'


class Locations(models.Model):
    location = models.CharField(max_length=100)
    max_count = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.location} {self.max_count}'


class Issue(models.Model):

    """Holds issue data and it's parent project."""

    details = models.ForeignKey(Projects, on_delete=models.CASCADE)
    issue = models.CharField(max_length=200)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f' Issue of {self.details.project_name}'