#
# Copyright 2017 NephoScale
#


from django.utils.translation import ugettext_lazy as _

import horizon
from astutedashboard.dashboards.billing import dashboard

class ImageUsageMappings(horizon.Panel):
    name = _("Image Usage Report")
    slug = "image_usage_report"

dashboard.M1AstutePanels.register(ImageUsageMappings)
