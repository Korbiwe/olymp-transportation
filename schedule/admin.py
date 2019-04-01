from flask import flash

from core.admin import BaseAdminModelView
from core.models import db
from schedule.models import Driver, Vehicle

from schedule.models import ScheduleEntry, Driver, Stop, Route, VehicleType, Park, Vehicle


class EntryAdmin(BaseAdminModelView):
    def validate_form(self, form):
        if not form.time_start.data or not form.time_end.data or not form.driver.data:
            return super(EntryAdmin, self).validate_form(form)

        if form.time_start.data > form.time_end.data:
            flash("Start time can't be greater than end time")
            return False

        if form.driver.data.type_id != form.vehicle.data.type_id:
            flash(f'This driver is not allowed to drive this vehicle!')
            return False

        return super(EntryAdmin, self).validate_form(form)


def init(admin):
    admin.add_view(EntryAdmin(ScheduleEntry, db.session))
    admin.add_view(BaseAdminModelView(Driver, db.session))
    admin.add_view(BaseAdminModelView(Stop, db.session))
    admin.add_view(BaseAdminModelView(Route, db.session))
    admin.add_view(BaseAdminModelView(VehicleType, db.session))
    admin.add_view(BaseAdminModelView(Park, db.session))
    admin.add_view(BaseAdminModelView(Vehicle, db.session))
