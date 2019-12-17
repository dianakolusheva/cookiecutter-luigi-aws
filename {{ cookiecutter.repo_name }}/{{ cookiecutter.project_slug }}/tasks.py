import os
from luigi import ExternalTask, Parameter
from luigi.contrib.batch import BatchTask
from luigi.contrib.s3 import S3Target
from luigi.format import Nop


{% set number_of_external_tasks = cookiecutter.number_of_external_tasks['value'] | int %}
{% for i in range(number_of_external_tasks) %}
{% set current_task = cookiecutter.number_of_external_tasks[i] %}
class {{ current_task['name_of_external_task'] }}(ExternalTask):
    S3_DATA_ROOT = {{ current_task['s3_path'] }}
    {% set number_of_parameters = current_task.number_of_parameters.value | int %}
    {% for j in range(number_of_parameters) -%}
    {%- set current_param = current_task['number_of_parameters'][j] -%}
    {% if current_param['type_of_parameter'] != 'other' %}
    {{ current_param['name_of_parameter'] }} = {{ current_param["type_of_parameter"] }}()
    {% else %}
    {{ current_param['name_of_parameter'] }} = Parameter()  # Put your desired parameter type here
    {% endif %}
    {%- endfor %}
    def output(self):
        return S3Target(path=self.S3_DATA_ROOT, format=Nop)  # Modify your path and/or add extra parameters here
{% endfor %}

{% set number_of_batch_jobs = cookiecutter.number_of_batch_jobs['value'] | int %}
{% for i in range(number_of_batch_jobs) %}
{% set current_task = cookiecutter.number_of_batch_jobs[i] %}
class {{ current_task['name_of_batch_task'] }}(BatchTask):
    S3_OUTPUT_ROOT = {{ current_task['output_s3_path'] }}
    {% set number_of_parameters = current_task.number_of_parameters.value | int %}
    {% for j in range(number_of_parameters) -%}
    {%- set current_param = current_task['number_of_parameters'][j] -%}
    {% if current_param['type_of_parameter'] != 'other' %}
    {{ current_param['name_of_parameter'] }} = {{ current_param["type_of_parameter"] }}()
    {% else %}
    {{ current_param['name_of_parameter'] }} = Parameter()  # Put your desired parameter type here
    {% endif %}
    {%- endfor %}
    def requires(self):
        # put requirements for your task as one of 
        # 1) single task as SomeTask()
        # 2) list of tasks as [Task1(), Task2()]
        # 3) dict of tasks as {'image': Task1(), 'text': Task2()}
        pass
    def run(self):
        # do something cool here using output of your required tasks as
        # input().do_something and save to this task's output as output().do_something
        pass
    def output(self):
        return S3Target(path=self.S3_OUTPUT_ROOT, format=Nop)  # Modify your path and/or add extra parameters here
{% endfor %}