#
# Copyright (C) 2017-2018 Maha Farhat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Test core shell functionality for the pipeline
"""

import os
import time

from chore import get_job_manager
from django.test import override_settings
from extratest.base import ExtraTestCase

from apps.pipeline.models import Pipeline, Program, ProgramFile

DIR = os.path.dirname(__file__)
FIX = os.path.join(DIR, 'fixtures')

class ProgramTest(ExtraTestCase):
    """Test the loading of programs and how they make commands"""
    def setUp(self):
        super().setUp()
        self.files = [
            ProgramFile.objects.create(name='file', store='test_{}.txt'.format(name))\
                for name in ('one', 'two')]

        self.program = Program(name='test', keep=False,
                               command_line='ls -l ${file} > @{file}')
        self.program.save()
        self.program.files.set([self.files[0]])

    def test_no_input_error(self):
        """Test input error"""
        self.program.files.set([])
        with self.assertRaises(ValueError):
            dict(self.program.prepare_files())

    def test_no_output_error(self):
        """Test output error"""
        dict(self.program.prepare_files(file=str(self.files[0].store.file)))
        self.program.command_line = 'ls -l ${file} > @{output}'

        with self.assertRaises(ValueError):
            dict(self.program.prepare_files(file=str(self.files[0].store.file)))

    def test_io_output(self):
        """Test the processing of io"""
        self.program.command_line = 'A @{B} C ${D} E @{F} G ${H}'
        inputs = [('$', '', '', 'D', '', 9, 13), ('$', '', '', 'H', '', 23, 27)]
        outputs = [('@', '', '', 'B', '', 2, 6), ('@', '', '', 'F', '', 16, 20)]
        # Inputs are always first in the io
        self.assertEqual(list(self.program.io()), inputs + outputs)
        self.assertEqual(list(self.program.io(outputs=False)), inputs)
        self.assertEqual(list(self.program.io(inputs=False)), outputs)

    def test_program(self):
        """Test the program"""
        output = '/tmp/test_one.txt'
        files = dict(self.program.prepare_files(output_dir='/tmp'))
        self.assertEqual(files[('$', 'file', 6, 13)], str(self.files[0].store.file))
        self.assertEqual(files[('@', 'file', 16, 23)], output)

        cmd = self.program.prepare_command(files)
        self.assertEqual(cmd, "ls -l %s > %s" % (self.files[0].store.file, output))

    def test_prefix_suffix(self):
        """Test the use of prefix and suffix in command"""
        output = '/tmp/out_one.ls'
        self.files[0].name = 'foo'
        self.files[0].save()
        self.program.command_line = 'ls -l $test_{foo}.txt > @out_{foo}.ls'
        files = dict(self.program.prepare_files(output_dir='/tmp'))
        self.assertEqual(files[('@', 'foo', 24, 37)], output)
        cmd = self.program.prepare_command(files)
        self.assertEqual(cmd, "ls -l %s > %s" % (self.files[0].store.file, output))

    def test_bin_directory(self):
        """Test the use of the custom BIN directory"""
        with self.settings(PIPELINE_BIN=FIX):
            self.program.command_line = 'sh ${bin}test.sh ${file}'
            for filename in dict(self.program.prepare_files(output_dir='/tmp')).values():
                self.assertTrue(os.path.isfile(filename), "File doesn't exist: %s" % filename)

    def test_brand_new_output(self):
        """Test the use of outputs with a new name"""
        self.program.command_line = 'ls > @{foo}.sam'
        files = dict(self.program.prepare_files(output_dir='/tmp', foo='gah.txt'))
        self.program.prepare_command(files)

    def test_command_combination(self):
        """New lines are considered command combinators"""
        self.program.command_line = 'ls\nwc\nls'
        files = dict(self.program.prepare_files(output_dir='/tmp'))
        cmd = self.program.prepare_command(files)
        self.assertEqual(cmd, "ls && wc && ls")

    def test_prepare_from_list(self):
        """Prepare commands from a list"""
        self.program.files.set([self.files[0], self.files[1]])
        self.program.command_line = 'ls ${file}_one.txt ${file}_two.txt '\
                                     + '${file}_one.ps ${file}_two.ps'
        files = list(self.program.prepare_files(output_dir='/tmp',\
                        file=['/tmp/in_one.ps', '/tmp/in_two.ps']))

        self.assertEqual(files, [
            (('$', 'file', 3, 18), str(self.files[0].store.file)),
            (('$', 'file', 19, 34), str(self.files[1].store.file)),
            (('$', 'file', 35, 49), '/tmp/in_one.ps'),
            (('$', 'file', 50, 64), '/tmp/in_two.ps'),
        ])


class PipelineTest(ExtraTestCase):
    """Test pipeline features"""
    def setUp(self):
        super().setUp()
        self.pipeline = Pipeline.objects.create(name='TEST')
        self.file = ProgramFile(name='file', store='test_one.txt')
        self.filename = str(self.file.store.file)
        self.dir = os.path.dirname(self.filename)

    def setup_pipeline(self, *programs):
        """Setup a list of programs in the pipeline"""
        wait = 'sleep 0.01 && '
        self.programs = [Program.objects.create(name=a, \
            command_line=wait + b) for a, b in programs]
        for pos, program in enumerate(self.programs):
            self.pipeline.programs.create(order=pos, program=program)

    def assertProgram(self, result, inputs, outputs, data=None): # pylint: disable=invalid-name
        """Assert that creating a program produces the right data"""
        def content(filename):
            """Read in the filename and return content"""
            with open(filename, 'r') as fhl:
                return fhl.read()
        outputs = outputs if isinstance(outputs, list) else [outputs]
        inputs = inputs if isinstance(inputs, list) else [inputs]
        self.assertEqual(result.input_files, "\n".join(inputs))
        self.assertEqual(result.output_files, "\n".join(outputs))
        if data is not None:
            ret = '---'.join([content(filename) for filename in outputs])
            self.assertEqual(ret, data)

        self.assertTrue(result.is_submitted)
        self.assertTrue(result.is_complete)
        self.assertEqual(result.error_text, None)
        self.assertFalse(result.is_error)

        self.assertGreater(result.input_size, 0)
        self.assertGreater(result.output_size, 0)
        self.assertGreater(result.duration, 0)

    @override_settings(PIPELINE_MODULE='chore.fake.FakeJobManager')
    def test_pipeline(self):
        """Test the pipeline generation"""
        self.setup_pipeline(
            ('A', 'ls -l ${file}.txt > @{file}.ls'),
            ('B', 'wc ${file}.ls > @{file}.c'),
            ('C', 'ls -l ${file}.txt ${file}.ls ${file}.c > @{file}.out'),
            ('D', 'wc ${file}.out > @{file}.out'),
        )
        result = self.pipeline.run("pipe", output_dir=self.dir, file=self.filename)
        limit = 40
        while not result.update_all():
            if limit == 40:
                get_job_manager().run_all()
            elif limit == 35:
                get_job_manager().finish_all()
            time.sleep(0.2)
            limit -= 1
            self.assertTrue(limit > 0, "Pipeline test timed out.")

        results = list(result.programs.all())
        self.assertEqual(len(results), 4)
        filename = self.filename[:-4] + ".%s"
        self.assertProgram(results[0], self.filename, filename % "ls")
        self.assertProgram(results[1], filename % "ls", filename % "c")
        #self.assertProgram(results[2], [
        #    filename % "ls", self.filename, filename % "c"], filename % "out")
        self.assertProgram(results[3], filename % "out", filename % "out")

    @override_settings(PIPELINE_MODULE='chore.fake.FakeJobManager')
    def test_duration(self):
        """Test the duration during a run"""
        self.assertEqual(type(get_job_manager()).__name__, 'FakeJobManager')
        self.setup_pipeline(('DUR', 'sleep 5'))
        results = self.pipeline.run("pipe", output_dir=self.dir)
        result = results.programs.get()
        get_job_manager().run_all()
        for count in range(5):
            result.update_status()
            self.assertEqual(int(result.duration), count + 1)
            time.sleep(1)
