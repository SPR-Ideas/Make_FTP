"""
    Testing make_ftp
"""

from unittest.mock import Mock ,patch
from pyfakefs.fake_filesystem_unittest import TestCase
import make_ftp

FILES_SYSTEM= {
    "test_file_1.txt":"Hi from file",
    "home":"FOLDER",
    "test_folder" : "FOLDER",
    "test_folder/test_file2.txt" : "The file is in a folder",
    "home": "FOLDER",
    "test_file3.txt": "/home/test_file"
}

class TestFtp(TestCase):
    """TestClass for make_ftp"""

    def _setup_fakefs(self):
        self.setUpPyfakefs()
        for file_name , content in FILES_SYSTEM.items():

            if content == "FOLDER":
                self.fs.create_dir(file_name)
                continue

            self.fs.create_file(file_name, contents = content)

    def _patch_sys(self):
        sys_patcher = patch("make_ftp.sys")
        mock_sys = sys_patcher.start()
        self.addCleanup(sys_patcher.stop)

        return mock_sys

    def _patch_print(self):
        print_patcher = patch("make_ftp.print")
        mock_print = print_patcher.start()
        self.addCleanup(print_patcher.stop)
        return mock_print

    def _patch_os(self):
        os_patcher = patch("make_ftp.os.system")
        mock_os = os_patcher.start()
        # mock_os.getpid.return_value = 12233
        self.addCleanup(os_patcher.stop)
        return mock_os

    def _patch_uvicorn(self):
        uvicorn_patcher = patch("make_ftp.uvicorn")
        mock_uvicorn = uvicorn_patcher.start()
        self.addCleanup(uvicorn_patcher.stop)
        return mock_uvicorn

    def _patch_pyngrok(self):
        ngrok_patcher = patch("make_ftp.ngrok")
        mock_ngrok = ngrok_patcher.start()
        self.addCleanup(ngrok_patcher.stop)
        return mock_ngrok

    def _patch_file_response(self):
        file_response_patcher = patch("make_ftp.FileResponse")
        mock_file_response = file_response_patcher.start()
        self.addCleanup(file_response_patcher.stop)
        return mock_file_response

    def test_skeleton_of_generate_link(self):
        """
            Testing the skeleton of genarating_link().
        """
        self._setup_fakefs()
        self._patch_uvicorn()
        self._patch_os()
        mock_sys = self._patch_sys()
        mock_ngrok = self._patch_pyngrok()
        mock_print = self._patch_print()
        mock_file_response = self._patch_file_response()

        mock_sys.argv = ["","test_file_1.txt"]

        make_ftp.generate_link()
        make_ftp.give_file() # assuming that the client makes a requets.

        mock_print.assert_any_call(
            "\n\t/{} -> {}\n".format(
                    mock_sys.argv[1],
                    mock_ngrok.connect().public_url
            ))
        mock_file_response.assert_any_call(
            path = "/{}".format(mock_sys.argv[1]),
            filename = mock_sys.argv[1],
            media_type = 'text/all'
        )


    def test_skeleton_of_generate_link_for_a_folder(self):
        """
            Testing the generate_link() with a folder as
            sys argv.
        """
        self._setup_fakefs()
        self._patch_pyngrok()
        self._patch_uvicorn()
        mock_os = self._patch_os()
        mock_sys = self._patch_sys()
        mock_ngrok = self._patch_pyngrok()
        mock_print = self._patch_print()
        mock_file_response = self._patch_file_response()

        mock_os.side_effect = [
                     self.fs.create_file("/test_folder/test_folder.zip") ,
                     Mock()
                     ]
        mock_sys.argv = ["","test_folder"]

        make_ftp.generate_link()
        make_ftp.give_file()

        mock_print.assert_any_call(
            "\n\t{} -> {}\n".format(
                "/test_folder/test_folder.zip",
                mock_ngrok.connect().public_url
            ))
        mock_file_response.assert_any_call(
            path = "/test_folder/test_folder.zip",
            filename = "test_folder.zip",
            media_type = 'text/all'
        )

    def testing_generate_links_with_curent_files(self):
        """Testing generate link"""
        self._setup_fakefs()
        self._patch_pyngrok()
        self._patch_uvicorn()
        mock_os = self._patch_os()
        mock_sys = self._patch_sys()
        mock_ngrok = self._patch_pyngrok()
        mock_print = self._patch_print()
        mock_file_response = self._patch_file_response()

        mock_os.side_effect = [
                     self.fs.create_file("/home/home.zip") ,
                     Mock()
                     ]
        mock_sys.argv = ["","."]

        make_ftp.os.chdir("/home")
        make_ftp.generate_link()
        make_ftp.give_file()

        mock_print.assert_any_call(
            "\n\t{} -> {}\n".format("/home/home.zip",
            mock_ngrok.connect().public_url
            )
        )

    def test_generating_link_with_invalid_file(self):
        """Testing generate link() with invalid file."""
        self._setup_fakefs()
        self._patch_os()
        mock_sys = self._patch_sys()
        mock_print = self._patch_print()
        mock_sys.argv = ["","not avilable file.txt"]

        make_ftp.generate_link()
        mock_print.assert_any_call("File does not exist.")

    def test_help_option(self):
        """ Testing _help()"""
        mock_print = self._patch_print()
        make_ftp.help_()
        msg =  """
        make_ftp <usage> :
            usage:
            file_path : file_location can be absolute or relative
                        relative path.
    """
        mock_print.assert_any_call(msg)
