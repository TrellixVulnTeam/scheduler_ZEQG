import os
from job import Job


class Executor:
    def __init__(self):
        pass

    def exec(self, job):
        ssh = self.ssh_cmd(job.node)
        source = 'source activate tensorflow_p36'
        cd = 'cd /home/ubuntu/scheduler/base_jobs/1-11/official/keras_application_models'
        py = self.py_cmd(job)
        exec_cmd = self.combine_cmd(' ', self.gpu_cmd(job.gpus_loc[job.node]), py)
        combine = self.combine_cmd(';', source, cd, exec_cmd)
        final_cmd = ssh + ' "' + combine + '"'
        os.system(final_cmd)

    @staticmethod
    def gpu_cmd(gpu_list):
        gpus = ','.join(str(i) for i in gpu_list)
        cmd = 'env CUDA_VISIBLE_DEVICES='+gpus
        return cmd

    def py_cmd(self, job):
        base = 'python benchmark_main.py'
        model = '--model ' + job.model
        dist = '--dist_strat'
        num_gpus = '-ng ' + str(len(job.gpus_loc[job.node]))
        id = '--id ' + job.id
        port = '--port ' + job.address.split(':')[1]
        gpus_list = '--gpus_list ' + str(job.gpus_loc[job.node])
        node = '--node ' + job.node
        server_address = '--server_address ' + 'localhost:1080'
        other = '--num_train_images 50000 --train_epochs 10 --num_eval_images 10000'
        return self.combine_cmd(' ', base, model, dist, num_gpus, id, port, gpus_list, node, server_address, other)

    @staticmethod
    def combine_cmd(char, *cmds):
        cmd = char.join(_ for _ in cmds)
        return cmd

    @staticmethod
    def ssh_cmd(node):
        return 'ssh ' + node


if __name__ == '__main__':
    # example command for exec a benchmark job:
    # ssh localhost "
    # source activate tensorflow_p36;
    # cd xxx;
    # python benchmark_main.py --model resnet50 --dist_strat -ng 2
    # --id 1 --port 8888 --gpus_list [0,2,3,5] --node localhost --server_address localhost:1080
    # --num_train_images 50000 --train_epochs 10 --num_eval_images 10000
    # "
    construct_dict = {'id': 's1',
                      'model': 'inceptionv3',
                      'gpus_loc': {'localhost': [0, 2]},
                      'address': 'localhost:8888'
                      }
    job = Job()
    job.dict_store(construct_dict)
    from pprint import pprint
    pprint(vars(job))
    # E = Executor()
    # print(E.exec(job))