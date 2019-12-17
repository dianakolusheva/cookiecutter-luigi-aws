import os
from datetime import date, timedelta
from luigi import ExternalTask, Parameter, DateParameter
from luigi.contrib.batch import BatchTask
from luigi.contrib.s3 import S3Target
from luigi.format import Nop

from emmaa.model import EmmaaModel
from emmaa.model_tests import run_model_tests_from_s3, \
    update_model_manager_on_s3
from emmaa.analyze_tests_results import generate_model_stats_on_s3


class SavedEmmaaModel(ExternalTask):
    S3_DATA_ROOT = 's3://emmaa/models'

    model_name = Parameter()
    last_updated = DateParameter()

    def output(self):
        return S3Target(
            path=os.path.join(
                self.S3_DATA_ROOT, self.model_name, self.last_updated)+'.pkl',
            format=Nop)


class Config(ExternalTask):
    S3_DATA_ROOT = 's3://emmaa/models'

    model_name = Parameter()

    def output(self):
        return S3Target(
            path=os.path.join(
                self.S3_DATA_ROOT, self.model_name, 'config.json'), format=Nop)


class TestFile(ExternalTask):
    S3_DATA_ROOT = 's3://emmaa/tests'

    test_corpus = Parameter()

    def output(self):
        return S3Target(
            path=os.path.join(self.S3_DATA_ROOT, self.test_corpus), format=Nop)


class TestResults(ExternalTask):
    S3_DATA_ROOT = 's3://emmaa/results'

    model_name = Parameter()
    date_created = DateParameter()

    def output(self):
        return S3Target(
            path=os.path.join(
                self.S3_DATA_ROOT, self.model_name, self.date_created)+'.json',
            format=Nop)


class Stats(ExternalTask):
    S3_DATA_ROOT = 's3://emmaa/stats'

    model_name = Parameter()
    date_created = DateParameter()

    def output(self):
        return S3Target(
            path=os.path.join(
                self.S3_DATA_ROOT, self.model_name, self.date_created)+'.json',
            format=Nop)


class UpdateModel(BatchTask):
    S3_OUTPUT_ROOT = 's3://emmaa/models'

    model_name = Parameter()

    def requires(self):
        yesterday = date.today() - timedelta(days=1)
        return [SavedEmmaaModel(model_name=self.model_name,
                                last_updated=yesterday),
                Config(model_name=self.model_name)]

    def run(self):
        em = EmmaaModel.load_from_s3(self.model_name)
        em.get_new_readings()
        em.save_to_s3()
        em.update_to_ndex()

    def output(self):
        return S3Target(
            path=os.path.join(self.S3_OUTPUT_ROOT,
                              (self.model_name + date.today().to_isoformat())),
            format=Nop)


class UpdateMM(BatchTask):
    S3_OUTPUT_ROOT = 's3://emmaa/results'

    model_name = Parameter()

    def requires(self):
        return SavedEmmaaModel(
            model_name=self.model_name, last_updated=date.today())

    def run(self):
        update_model_manager_on_s3(self.model_name)

    def output(self):
        return S3Target(path=os.path.join(self.S3_OUTPUT_ROOT, self.model_name),
                        format=Nop)


class RunTests(BatchTask):
    S3_OUTPUT_ROOT = 's3://emmaa/results'

    model_name = Parameter()
    test_name = Parameter()

    def requires(self):
        {'model_manager': UpdateMM(self.model_name),
         'test_corpus': (self.test_name)}

    def run(self):
        run_model_tests_from_s3(self.model_name, self.test_name)

    def output(self):
        return S3Target(path=os.path.join(self.S3_OUTPUT_ROOT, self.model_name),
                        format=Nop)


class GenerateStats(BatchTask):
    S3_OUTPUT_ROOT = 's3://emmaa/stats'

    model_name = Parameter()

    def requires(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        return {
            'latest_test_results': TestResults(
                model_name=self.model_name,
                date_created=today),
            'previous_test_results': TestResults(
                model_name=self.model_name,
                date_created=yesterday),
            'previous_stats': Stats(
                model_name=self.model_name,
                date_created=yesterday)
        }

    def run(self):
        generate_model_stats_on_s3(self.model_name)

    def output(self):
        return S3Target(path=os.path.join(self.S3_OUTPUT_ROOT, self.model_name),
                        format=Nop)
