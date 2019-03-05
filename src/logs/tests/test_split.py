from django.test import TestCase

from src.split.models import SplitTypes
from src.split.splitting import prepare_logs
from src.utils.tests_utils import general_example_filepath, general_example_test_filepath, \
    general_example_train_filepath, create_test_split, create_test_log, general_example_filename, \
    general_example_train_filename, general_example_test_filename


class Split(TestCase):
    def test_split_single(self):
        training_log, test_log, _ = prepare_logs(split_single())
        self.assertEqual(4, len(training_log))
        self.assertEqual(2, len(test_log))

    def test_split_double(self):
        training_log, test_log, _ = prepare_logs(split_double())
        self.assertEqual(4, len(training_log))
        self.assertEqual(2, len(test_log))


class SplitSingle(TestCase):
    def test_size(self):
        split = split_single()
        split['config'] = {'test_size': 0.5}
        training_log, test_log, _ = prepare_logs(split)
        self.assertEqual(3, len(training_log))
        self.assertEqual(3, len(test_log))

    def test_sequential(self):
        split = split_single()
        split['config'] = {'split_type': 'split_sequential'}
        training_log, test_log, _ = prepare_logs(split)
        training_names = trace_names(training_log)
        test_names = trace_names(test_log)

        self.assertListEqual(['3', '2', '1', '6'], training_names)
        self.assertListEqual(['5', '4'], test_names)

    def test_random(self):
        split = split_single()
        split['config'] = {'split_type': 'split_random'}
        training_log1, _, _ = prepare_logs(split)
        training_log2, _, _ = prepare_logs(split)
        training_names1 = trace_names(training_log1)
        training_names2 = trace_names(training_log2)

        self.assertNotEqual(training_names1, training_names2)

    def test_temporal(self):
        split = split_single()
        split['config'] = {'split_type': 'split_temporal'}
        training_log, test_log, _ = prepare_logs(split)

        training_names = trace_names(training_log)
        test_names = trace_names(test_log)

        self.assertListEqual(sorted(['1', '2', '3', '5']), sorted(training_names))
        self.assertListEqual(sorted(['6', '4']), sorted(test_names))

    def test_strict_temporal(self):
        split = split_single()
        split['config'] = {'split_type': 'split_strict_temporal'}
        training_log, test_log, _ = prepare_logs(split)

        training_names = trace_names(training_log)
        test_names = trace_names(test_log)

        # Modified log to have only one trace here
        self.assertListEqual(['1'], sorted(training_names))
        self.assertListEqual(sorted(['6', '4']), sorted(test_names))


def trace_names(log):
    """Get trace names"""
    return [trace.attributes['concept:name'] for trace in log]


def split_single():
    return create_test_split(
        split_type=SplitTypes.SPLIT_SINGLE.value,
        original_log=create_test_log(
            log_name=general_example_filename,
            log_path=general_example_filepath))


def split_double():
    return create_test_split(
        split_type=SplitTypes.SPLIT_DOUBLE.value,
        train_log=create_test_log(
            log_name=general_example_train_filename,
            log_path=general_example_train_filepath),
        test_log=create_test_log(
            log_name=general_example_test_filename,
            log_path=general_example_test_filepath))
