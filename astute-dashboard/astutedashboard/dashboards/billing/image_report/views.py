#
# Copyright 2017 NephoScale
#

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from horizon import exceptions
from horizon import forms
from horizon import tables
from horizon import tabs
#from datetime import timedelta, date
import datetime
from django.http import HttpResponse

from astutedashboard.common import \
    get_discount_types, \
    get_discounts, \
    get_discount_mappings, \
    get_discount_mapping, \
    get_billing_plan_mappings, \
    get_billing_plan_mapping, \
    get_projects, \
    get_plans, \
    get_image_list, \
    get_image_count, \
    get_image_name, \
    get_image_usage_report
    
from astutedashboard.dashboards.billing.image_report \
    import forms as panel_forms
from astutedashboard.dashboards.billing.image_report \
    import tables as panel_tables

class IndexView(generic.TemplateView):
    #table_class = panel_tables.BillingPlanMappingsTable
    template_name = 'billing/image_report/index.html'
    page_title = _("SQL Image Usage Report")

    def get_data(self):
        period_from = self.request.session.get('image_filter_period_from')
        period_to = self.request.session.get('image_filter_period_to')
        abc = get_image_usage_report(self.request,
            period_from=period_from,
            period_to=period_to,
            verbose=True)

        print '**********************/*****************'
        print abc
        print '**********************/*****************'
        return abc

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['admin_image_report_filter_endpoint'] = 'search_filter'
        context['image_filter_period_from'] = self.request.session.get('image_filter_period_from') or ''
        context['image_filter_period_to'] = self.request.session.get('image_filter_period_to') or ''
        abc = get_image_usage_report(self.request,
            period_from=context['image_filter_period_from'],
            period_to=context['image_filter_period_to'],
            verbose=True)
        context['abc'] = abc
        image_data = get_image_count(self.request)
        original_image_list = get_image_list(self.request)
        #print '++++++++++++++++++++++'
        #print original_image_list
        #print '++++++++++++++++++++++'
        user_data = {}
        user_data1 = {}
        for date in image_data:
            for user in image_data[date]:
                start = datetime.datetime.strptime("2018-04-05", "%Y-%m-%d")
                end = datetime.datetime.strptime("2018-04-11", "%Y-%m-%d")
                date_array = (start + datetime.timedelta(days=x) for x in range(0, (end-start).days))
                report_date_list = []
 
                #start_dt = date(2018, 4, 01)
                #start_dt = str(start_dt)
                #start_dt = '2018-04-01'
                #end_dt = date(2018, 4, 12)
                #delta = end_dt - start_dt # timedelta
#                for i in range(delta.days + 1):
#                    dateVal = d1 + timedelta(days=i)
                #end_dt = '2018-04-12'
                #for dt in self.daterange(start_dt, end_dt):
                #    print(dt.strftime("%Y-%m-%d"))
                image_name = get_image_name(self.request, user)
                #print image_name
                if user not in user_data:
                    user_data[user] = {}
                    user_data1[image_name] = {}

                user_data[user][date] = image_data[date][user]
                user_data1[image_name][date] = image_data[date][user]


                for date_object in date_array:
                    date_val = date_object.strftime("%Y-%m-%d")
                    report_date_list.append(date_val)
                    #print '*******'
                    #print date_val
                #for dt in self.daterange(start_dt, end_dt):
                #    date_val = dt.strftime("%Y-%m-%d")
                #for i in range(delta.days + 1):
                #    dateVal = start_dt + timedelta(days=i)
                    if date_val not in user_data1[image_name]:
                        user_data1[image_name][date_val] = '0.0'

                #print user_data1
                #print '&&&&&&&&&&&&&&&&&&&&&&&new'
                #user_data[image_name][date] = image_data[date][user]
                #user_data[image_name] = user_data.pop('user')
                #user_data[image_name] = user_data[user]
                #del user_data[user]
                #print user_data

        #print '---------------------------------------------'
        #print user_data
        #print '---------------------------------------------' 
        #print user_data1
        context['report_date_list'] = report_date_list
        context['user_data']  = user_data
        context['user_data1'] = user_data1
        #print '**********************'
        #print context
        return context


def search_filter(request):
    period_from = request.POST.get('period_from') or request.GET.get('period_from')
    period_to = request.POST.get('period_to') or request.GET.get('period_to')

    print '++++++++++++++++++++++++++++++++'
    print period_from
    print period_to
    print '+++++++++++++++++++++++++++++++'

    if period_from:
        request.session['image_filter_period_to'] = period_from
    else:
        try:
            del request.session['image_filter_period_from']
        except KeyError:
            pass

    if period_to:
        request.session['image_filter_period_to'] = period_to
    else:
        try:
            del request.session['image_filter_period_to']
        except KeyError:
            pass

    # force session save
    request.session.modified = True
    return HttpResponse(200)


