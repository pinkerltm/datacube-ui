# Copyright 2016 United States Government as represented by the Administrator
# of the National Aeronautics and Space Administration. All Rights Reserved.
#
# Portion of this code is Copyright Geoscience Australia, Licensed under the
# Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License
# at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# The CEOS 2 platform is licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.shortcuts import render
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.forms.models import model_to_dict

import json
from datetime import datetime, timedelta

from apps.dc_algorithm.models import Satellite, Area, Application
from .forms import AdditionalOptionsForm, DataSelectionForm
from .tasks import run

from collections import OrderedDict

from apps.dc_algorithm.views import (ToolView, SubmitNewRequest, GetTaskResult, SubmitNewSubsetRequest, CancelRequest,
                                     UserHistory, ResultList, OutputList, RegionSelection, TaskDetails)


class RegionSelection(RegionSelection):
    """Creates the region selection page for the tool by extending the RegionSelection class

    Extends the RegionSelection abstract class - tool_name is the only required parameter -
    all other parameters are provided by the context processor.

    See the dc_algorithm.views docstring for more information
    """
    tool_name = 'coastal_change'


class CoastalChangeTool(ToolView):
    """Creates the main view for the custom mosaic tool by extending the ToolView class

    Extends the ToolView abstract class - required attributes are the tool_name and the
    generate_form_dict function.

    See the dc_algorithm.views docstring for more details.
    """

    tool_name = 'coastal_change'
    task_model_name = 'CoastalChangeTask'

    def generate_form_dict(self, satellites, area):
        forms = {}
        for satellite in satellites:
            forms[satellite.pk] = {
                'Data Selection':
                AdditionalOptionsForm(
                    datacube_platform=satellite.datacube_platform, auto_id="{}_%s".format(satellite.pk)),
                'Geospatial Bounds':
                DataSelectionForm(area=area,
                    time_start=satellite.date_min,
                    time_end=satellite.date_max,
                    auto_id="{}_%s".format(satellite.pk))
            }
        return forms


class SubmitNewRequest(SubmitNewRequest):
    """
    Submit new request REST API Endpoint
    Extends the SubmitNewRequest abstract class - required attributes are the tool_name,
    task_model_name, form_list, and celery_task_func

    Note:
        celery_task_func should be callable with .delay() and take a single argument of a TaskModel pk.

    See the dc_algorithm.views docstrings for more information.
    """
    tool_name = 'coastal_change'
    task_model_name = 'CoastalChangeTask'
    #celery_task_func = create_cloudfree_mosaic
    celery_task_func = run
    form_list = [DataSelectionForm, AdditionalOptionsForm]


class GetTaskResult(GetTaskResult):
    """
    Get task result REST API endpoint
    Extends the GetTaskResult abstract class, required attributes are the tool_name
    and task_model_name

    See the dc_algorithm.views docstrings for more information.
    """
    tool_name = 'coastal_change'
    task_model_name = 'CoastalChangeTask'


class SubmitNewSubsetRequest(SubmitNewSubsetRequest):
    """
    Submit new subset request REST API endpoint
    Extends the SubmitNewSubsetRequest abstract class, required attributes are
    the tool_name, task_model_name, celery_task_func, and task_model_update_func.

    See the dc_algorithm.views docstrings for more information.
    """
    tool_name = 'coastal_change'
    task_model_name = 'CoastalChangeTask'

    celery_task_func = run

    def task_model_update_func(self, task_model, **kwargs):
        """
        Basic funct that updates a task model with kwargs. In this case only the date
        needs to be changed, and results reset.
        """
        # This is not supported for coastal change.
        pass


class CancelRequest(CancelRequest):
    """
    Cancel request REST API endpoint
    Extends the CancelRequest abstract class, required attributes are the tool
    name and task model name. This will not kill running queries, but will
    disassociate it from the user's history.
    """
    tool_name = 'coastal_change'
    task_model_name = 'CoastalChangeTask'


class UserHistory(UserHistory):
    """
    Generate a template used to display the user's history
    Extends the QueryHistory abstract class, required attributes are the tool
    name and task model name. This will list all queries that are complete, have a
    OK status, and are registered to the user.
    """
    tool_name = 'coastal_change'
    task_model_name = 'CoastalChangeTask'


class ResultList(ResultList):
    """
    Generate a template used to display any number of existing queries and metadatas
    Extends the ResultList abstract class, required attributes are the tool
    name and task model name. This will list all queries that are complete, have a
    OK status, and are registered to the user.
    """
    tool_name = 'coastal_change'
    task_model_name = 'CoastalChangeTask'


class OutputList(OutputList):
    """
    Generate a template used to display any number of existing queries and metadatas
    Extends the OutputList abstract class, required attributes are the tool
    name and task model name. This will list all queries that are complete, have a
    OK status, and are registered to the user.
    """
    tool_name = 'coastal_change'
    task_model_name = 'CoastalChangeTask'


class TaskDetails(TaskDetails):
    """
    Generate a template used to display the full task details for any
    given task.
    Extends the TaskDetails abstract class, required attributes are the tool
    name and task model name.
    """
    tool_name = 'coastal_change'
    task_model_name = 'CoastalChangeTask'
