import docker
import os

#@profile
def lambdo(filename):
    try:
        client = docker.from_env(version='auto')
    except Exception, e:
        print str(e) + ' Error while connecting Docker'
    try:
        response = client.containers.run('saravanan30/python2', 'python '+filename,
            remove=True, volumes={os.getcwd()+'/uploads':{'bind':'/usr/src/app', 'mode':'ro'}},
            name='test', working_dir='/usr/src/app')
        return response
    except Exception, e:
        if 'already in use' in str(e):
            container = client.containers.get(container_id='test')
            container.remove(v=True)
            response = client.containers.run('saravanan30/python2', 'python '+filename,
                remove=True, volumes={os.getcwd()+'/uploads':{'bind':'/usr/src/app', 'mode':'ro'}},
                name='test', working_dir='/usr/src/app')
            return response
        return str(e)

if __name__ == '__main__':
    print lamdocker('test.py')
