# Copyright 2013 - Mirantis, Inc.
# Copyright 2015 - StackStorm, Inc.
# Copyright 2015 Huawei Technologies Co., Ltd.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from oslo_log import log as logging
from pecan import hooks
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from mistral.api import access_control as acl
from mistral.api.controllers.v2 import resources
from mistral import context
from mistral.db.v2 import api as db_api
from mistral.utils import rest_utils

LOG = logging.getLogger(__name__)


class ReportController(rest.RestController, hooks.HookController):
    """ReportController will return a generated report"""

    @rest_utils.wrap_wsme_controller_exception
    @wsme_pecan.wsexpose(resources.Report, wtypes.text)
    def get(self, ident):
        acl.enforce('report:get', context.ctx())

        LOG.info("Generating Report information "
                 "for execution id: {}".format(ident))
        db_model = db_api.get_report(ident)

        return resources.Report.from_dict(db_model.to_dict())
