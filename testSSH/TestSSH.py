import paramiko

__version__ = '0.1'


class TestSSH:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def login_to_host(self, ip, port, username, password):
        try:
            self.client.connect(hostname=ip, port=port, username=username, password=password)
            return
        except paramiko.ssh_exception.NoValidConnectionsError:
            print("wrong ip or port entered")
            raise
        except paramiko.ssh_exception.AuthenticationException:
            print("wrong username or password entered")
            raise

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        err = stderr.readlines()
        if len(err) != 0:
            print("Wrong Command entered: ( " + "".join(err) + " )")
            raise TypeError
        return stdout.readlines()

    def get_hostname(self):
        hostname = TestSSH.execute_command(self, 'hostname')
        output = (hostname[0]).strip()
        return output

    def get_network_configurations(self):
        network = self.execute_command('ifconfig')
        return "".join(network)

    def create_directory(self, dir_name):
        exist = self.should_exist(dir_name)
        if exist == 1:
            sftp = self.client.open_sftp()
            sftp.rmdir(dir_name)
            sftp.close()
        sftp = self.client.open_sftp()
        sftp.mkdir(dir_name)
        sftp.close()
        return

    def should_exist(self, wanted_file):
        try:
            sftp = self.client.open_sftp()
            index = str(wanted_file).rfind("/")
            name = wanted_file
            print(index)
            if index == -1:
                list_of_dirs = sftp.listdir()
            else:
                path = wanted_file[:index + 1]
                name = wanted_file[index + 1:]
                list_of_dirs = sftp.listdir(path)
            sftp.close()
            if name in list_of_dirs:
                return 1
            else:
                raise FileNotFoundError('file or directory ' + wanted_file + 'not found')

        except FileNotFoundError:
            print("The directory ( " + wanted_file + ")  is not found, make sure the path is correct")
            raise

    def create_file(self, file_name, file_content, directory):
        self.execute_command('touch ' + str(directory).strip() + '/' + str(file_name))
        file = self.execute_command('echo ' + "\' " + str(file_content) + "\' >" + str(directory).strip() +
                                    '/' + str(file_name))
        return file

    def get_file(self, source, destination):
        try:
            sftp = self.client.open_sftp()
            sftp.get(source, destination)
            sftp.close()
            return
        except FileNotFoundError:
            print("The source file ( " + source + ") or the destination file ( " + destination + ") is not found, "
                                                                                                 "make sure the path "
                                                                                                 "is correct")
            raise

    def get_count_of_files(self, directory):
        try:
            sftp = self.client.open_sftp()
            count = sftp.listdir(directory)
            sftp.close()
            return len(count)
        except FileNotFoundError:
            print("The directory ( " + directory + ")  is not found, make sure the path is correct")
            raise

    def remove_file(self, file_name):
        try:
            sftp = self.client.open_sftp()
            sftp.remove(file_name)
            sftp.close()
            return
        except FileNotFoundError:
            print("The file ( " + file_name + ")  is not found, make sure the path is correct")
            raise

    def remove_files_in_directory(self, directory):
        try:
            directory = self.execute_command('rm ' + str(directory).strip() + '/*')
            return directory
        except TypeError:
            print("The Directory Name Is Not Correct")
            raise

    def put_file(self, source, destination):
        try:
            sftp = self.client.open_sftp()
            sftp.put(source, destination)
            sftp.close()
            return
        except FileNotFoundError:
            print("The source file ( " + source + ") or the destination file ( " + destination + ") is not found, "
                                                                                                 "make sure the path "
                                                                                                 "is correct")
            raise

    def logout_from_host(self):
        self.client.close()
        return
