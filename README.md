Luigi AWS Cookiecutter
======================

A cookiecutter template to create Luigi workflow on AWS. This template was
developed as a part of a final project for CSCI-E29 Advanced Python for Data
Science course. The project includes three parts:

1) Extending cookiecutter functionality to allow template developers configure
the templates with flexible updating of prompts to user 
(see below in Cookiecutter with extra prompts functionality section).

2) Design a template for Luigi workflow on AWS using this functionality - this
repo. Flexible design allows to ask user specific questions and generate a big
portion of a code for Luigi workflow including user sepcific ExternalTasks and
BatchTasks definitions.

3) Generate an example of a project using this template. This template was used
to generate code for Luigi workflow for automated update and analysis of
biological models available at https://github.com/dianakolusheva/emmaa/blob/luigi/emmaa/luigi/tasks.py 
Please note that this example is still work in progress and will be updated in
the future. It is linked here to demonstrate how a project might look like and
not to provide an actual working and tested code.

Cookiecutter with extra prompts functionality
---------------------------------------------

This template is built using cookiecutter version with extra prompts
functionality available at https://github.com/dianakolusheva/cookiecutter/tree/extra_prompts
The changes on that branch include updating [prompt.py](https://github.com/dianakolusheva/cookiecutter/blob/421d49b6f45f370aa5e4d98a1d01ff7ffe59caea/cookiecutter/prompt.py#L190-L331)
by adding a function `prompt_in_loop_for_config` and modifying `prompt_for_config`
function. This new functionality is useful if you want to prompt user multiple
times with the same sets of questions depending on their previous input.
For example, in this template, I ask users how many BatchTasks they want to run
and then loop that many times through set of questions about individual task.

Instructions for template developers to create new templates using [cookiecutter/extra_prompts](https://github.com/dianakolusheva/cookiecutter/tree/extra_prompts) branch
-------------------------------------------------------------------------

Install [cookiecutter/extra_prompts](https://github.com/dianakolusheva/cookiecutter/tree/extra_prompts) branch from source. You can generate your template from scratch
or use this [cookiecutter template](https://github.com/eviweb/cookiecutter-template)
for creating a... cookiecutter template...

Create a cookiecutter.json with the prompts you want to ask the user. To define
a loop, add a key-value pair to the cookiecutter.json where the key starts with
'loop_' (e.g. 'loop_number_of_batch_tasks') and the value is a dictionary (I'll
be referring to it as loop dictionary to avoid confusion with cookiecutter dictionary). Don't
worry about readability, the 'loop_' part will be stripped out before showing to user.
You can provide a default value for number of iterations by putting 'default' in
your loop dictionary (if not provided, it defaults to 1). Other key-value pairs
in your loop dictionary should be the questions and default values (or jinja2
patterns for rendering default values) you want to ask during one iteration.
Default values can be of any types supported by regular cookiecutter (simple
variable, list of options, dictionary, etc.)
If you want the default value to be incremented at each iteration, add '_iter'
to the end of your question. For example, 'name_of_batch_task_iter' ends with
'_iter' and the default value for this question changes at each iteration
(BatchTask_1, BatchTask_2, etc.) The part '_iter' is also stripped out before
showing to user. Questions without '_iter' have teh save default value at every
iteration. 

Note that you can have nested loops too. To do that, simply add a key starting
with 'loop_' and a new loop dictionary as a value inside first level loop dictionary.
For example, see how parameter loop is nested inside batch tasks loop:

```    
"loop_number_of_batch_jobs": {
        "default": 1,
        "name_of_batch_task_iter": "BatchTask",
        "loop_number_of_parameters": {
            "default": 0,
            "name_of_parameter_iter" : "param",
            "type_of_parameter": [
                "Parameter",
                "OptionalParameter",
                "DateParameter",
                "BoolParameter",
                "IntParameter",
                "other"]
        },
        "output_s3_path": "s3://somepath/"
    }
```


Instructions on using this template to generate AWS Luigi workflow
------------------------------------------------------------------
### Requirements

Install [cookiecutter/extra_prompts](https://github.com/dianakolusheva/cookiecutter/tree/extra_prompts) branch from source.

### Usage

Generate a new Cookiecutter template layout: `cookiecutter gh:dianakolusheva/cookiecutter-luigi-aws`
or call it from python: 

```
from cookiecutter.main import cookiecutter
cookiecutter('cookiecutter-luigi-aws/')
```

Answer all prompts specifying the details of your desired workflow, e.g. your
external dependencies on S3 (Luigi ExternalTask) and AWS Batch Jobs (Luigi BatchTask)
you want to run. After you answer all the questions, a new directory will be generated
in you current working directory with the name that you selected.
You will find a file `tasks.py` which contains a skeleton of your Luigi workflow.
It should already have class definitions for the tasks in your workflow.
You will need to add run methods by adding specific steps you want your batch
jobs to do and probably modify some other details (e.g. if s3 path of the target
is a result of joining initial path and parameter values).

License
-------
This project is licensed under the terms of the [MIT License](/LICENSE)
