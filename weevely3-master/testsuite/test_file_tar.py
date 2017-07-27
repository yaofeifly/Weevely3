from testfixtures import log_capture
from testsuite.base_fs import BaseFilesystem
from testsuite import config
from core.sessions import SessionURL
from core import modules
import utils
from core import messages
import subprocess
import os

class FileTar(BaseFilesystem):

    def setUp(self):
        self.session = SessionURL(
                    self.url,
                    self.password,
                    volatile = True
                    )

        modules.load_modules(self.session)

        self.folders_abs = []
        self.folders_rel = []
        self.files_abs = []
        self.files_rel = []
        self.tars_abs = []
        self.tars_rel = []

        # Create the folder tree
        self.folders_abs, self.folders_rel =  self.populate_folders()
        self.files_abs, self.files_rel = self.populate_files(
                                    self.folders_abs,
                                    [ 'f1', 'f2', 'f3', 'f4' ]
                                )

        self.tars_rel.append('test_0.tar')
        self.tars_abs.append(os.path.join(config.script_folder, self.tars_rel[0]))

        self.check_call(config.cmd_env_cd_s_tar_s_s % (
            config.script_folder,
            self.tars_abs[0],
            self.folders_rel[0]
            )
        )

        # Other file for testing multiple file tarping
        self.other_file_rel = 'f5'
        self.other_file_abs = os.path.join(config.script_folder, self.other_file_rel)
        self.check_call(
            config.cmd_env_content_s_to_s % ('1', self.other_file_abs)
        )

        # Now remove the folder tree leaving the tar
        self._delete_tree()

        self.run_argv = modules.loaded['file_tar'].run_argv

        self.skip_deletion_teardown = False

    def _delete_tree(self):

        for file in self.files_abs:

            # Drrty fix due to the mod of the files are rwxr--r-- and can't
            # Be changed if also the folder has -x------. Changing both.
            modules.loaded['shell_php'].run_argv(['chmod(dirname("%s"), 0777);' % file])
            modules.loaded['shell_php'].run_argv(['chmod("%s", 0777);' % file])

            self.check_call(config.cmd_env_remove_s % (file))

        for folder in reversed(self.folders_abs):
            self.check_call(config.cmd_env_rmdir_s % (folder))

    def _delete_tars(self):
        for tarfile in self.tars_abs:
            self.check_call(config.cmd_env_remove_s % (tarfile))

    def tearDown(self):

        if self.skip_deletion_teardown: return

        self._delete_tree()
        self.check_call(config.cmd_env_remove_s % (self.other_file_abs))
        self._delete_tars()

    def test_compress_decompress(self):

        # Uncompress test.tar
        self.assertTrue(self.run_argv(["--decompress", 'test_0.tar', '.']));
        for fle in self.files_abs:
            self.assertEqual(self.check_output(config.cmd_env_print_repr_s % fle),'1')
        for folder in self.folders_abs:
            self.check_call(config.cmd_env_stat_permissions_s % folder)

        # Compress it again giving starting folder
        self.assertTrue(self.run_argv(['test_1.tar', self.folders_rel[0]]));
        self.tars_rel.append('test_1.tar')
        self.tars_abs.append(os.path.join(config.script_folder, self.tars_rel[-1]))

        # Uncompress the new archive and recheck
        self.assertTrue(self.run_argv(["--decompress", 'test_1.tar', '.']));
        for file in self.files_abs:
            self.assertEqual(self.check_output(config.cmd_env_print_repr_s % file),'1')
        for folder in self.folders_abs:
            self.check_call(config.cmd_env_stat_permissions_s % folder)

    def test_compress_multiple(self):

        # Uncompress test.tar
        self.assertTrue(self.run_argv(["--decompress", 'test_0.tar', '.']));
        for file in self.files_abs:
            self.assertEqual(self.check_output(config.cmd_env_print_repr_s % file),'1')
        for folder in self.folders_abs:
            self.check_call(config.cmd_env_stat_permissions_s % folder)

        # Create a new tar adding also other_file
        self.assertTrue(self.run_argv(['test_2.tar', self.folders_rel[0], self.other_file_rel]));
        self.tars_rel.append('test_2.tar')
        self.tars_abs.append(os.path.join(config.script_folder, self.tars_rel[-1]))

        # Uncompress the new archive and recheck
        self.assertTrue(self.run_argv(["--decompress", 'test_2.tar', '.']));
        for file in self.files_abs:
            self.assertEqual(self.check_output(config.cmd_env_print_repr_s % file),'1')
        for folder in self.folders_abs:
            self.check_call(config.cmd_env_stat_permissions_s % folder)

        self.check_call(config.cmd_env_stat_permissions_s % self.other_file_abs)

    @log_capture()
    def test_already_exists(self, log_captured):

        self.skip_deletion_teardown = True

        # Create a new tar with other_file, with the name test_0.tar
        self.assertIsNone(self.run_argv(['test_0.tar', self.other_file_rel]));
        self.assertEqual(log_captured.records[-1].msg,
                         "File 'test_0.tar' already exists, skipping compressing")

        self.check_call(config.cmd_env_remove_s % (self.other_file_abs))
        self._delete_tars()

    @log_capture()
    def test_unexistant_decompress(self, log_captured):
        self.skip_deletion_teardown = True

        self.assertIsNone(self.run_argv(["--decompress", 'bogus', '.']));
        self.assertEqual(log_captured.records[-1].msg,
                         "Skipping file 'bogus', check existance and permission")

        self.check_call(config.cmd_env_remove_s % (self.other_file_abs))
        self._delete_tars()

    @log_capture()
    def test_unexistant_compress(self, log_captured):
        self.skip_deletion_teardown = True

        self.assertIsNone(self.run_argv(['bogus.tar', 'bogus']));
        self.assertEqual(log_captured.records[-1].msg,
                         "File 'bogus.tar' not created, check existance and permission")

        self.check_call(config.cmd_env_remove_s % (self.other_file_abs))
        self._delete_tars()
