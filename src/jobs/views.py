import json

import django_rq
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from src.jobs import tasks
from src.jobs.job_creator import generate, generate_labelling, update
from src.jobs.models import Job, JobTypes
from src.jobs.serializers import JobSerializer
from src.predictive_model.models import PredictiveModels
from src.split.models import Split


class JobList(ListAPIView):
    """
    List all jobs, or create a new job.
    """
    serializer_class = JobSerializer

    def get_queryset(self):
        jobs = Job.objects.all()
        type = self.request.query_params.get('type', None)
        status = self.request.query_params.get('status', None)
        if type is not None:
            jobs = jobs.filter(type=type)
        elif type is not None:
            jobs = jobs.filter(status=status)
        return jobs

    # TODO remove?
    @staticmethod
    def post(request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class JobDetail(RetrieveModelMixin, GenericAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        job = self.queryset.get(pk=kwargs['pk'])
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_multiple(request):
    """No request validation"""
    payload = json.loads(request.body.decode('utf-8'))
    try:
        split = Split.objects.get(pk=payload['split_id'])
    except Split.DoesNotExist:
        return Response({'error': 'not in database'}, status=status.HTTP_404_NOT_FOUND)

    # detect either or not a predictive_model to update has been specified otherwise train a new one.
    if 'incremental_train' in payload['config'] and payload['config']['incremental_train']['base_model'] is not None:
        jobs = update(split, payload)
    elif payload['type'] in [e.value for e in PredictiveModels]:
        jobs = generate(split, payload)
    elif payload['type'] == JobTypes.LABELLING.value:
        jobs = generate_labelling(split, payload)
    else:
        return Response({'error': 'type not supported'.format(payload['type'])},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    for job in jobs:
        django_rq.enqueue(tasks.prediction_task, job.id)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data, status=201)
